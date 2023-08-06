# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
Contains fsspec api implementation for aml uri
"""
from fsspec.asyn import (
    AsyncFileSystem,
    get_loop,
    sync,
    _run_coros_in_chunks
)
from fsspec.callbacks import _DEFAULT_CALLBACK
from fsspec.implementations.local import LocalFileSystem, make_path_posix
# from fsspec.utils import other_paths

import asyncio
import os
import pathlib
import re
import inspect
from glob import has_magic
import azureml.dataprep as _dprep
from azureml.dataprep.api._loggerfactory import track, _LoggerFactory
from azureml.dataprep.api._constants import ACTIVITY_INFO_KEY, ERROR_CODE_KEY, \
    COMPLIANT_MESSAGE_KEY, OUTER_ERROR_CODE_KEY
from azureml.dataprep.api.functions import get_stream_properties
from azureml.dataprep.rslex import StreamInfo, CachingOptions, BufferingOptions, Downloader, \
    Copier, PyIfDestinationExists, PyLocationInfo, PyDatastoreSource
from azureml.dataprep.api._rslex_executor import ensure_rslex_environment

_PUBLIC_API = 'PublicApi'
_APP_NAME = 'azureml-fsspec'
_logger = None
_DATASTORE_HANDLER = 'AmlDatastore'

# TODO change to new error code from rslex and throw customized user error
_USER_ERROR_MESSAGES = [
    "StreamError(NotFound)", "DataAccessError(NotFound)", "DataAccessError(PermissionDenied)", "OutputError(NotEmpty)"]

_STRING_TO_PYIFDESTINATIONEXISTS = {
    # if find conflict file in destination, wil leave the original file
    "APPEND": PyIfDestinationExists.APPEND,
    # if find conflict file in destination, will raise not empty error
    "FAIL_ON_FILE_CONFLICT": PyIfDestinationExists.FAIL_ON_FILE_CONFLICT,
    # if find conflict file in destination, will overwrite with new file"
    "MERGE_WITH_OVERWRITE": PyIfDestinationExists.MERGE_WITH_OVERWRITE,
}


def _to_py_if_destination_exists(overwrite):
    if not isinstance(overwrite, str):
        raise ValueError(
            'The overwrite kwargs should be a string')

    try:
        return _STRING_TO_PYIFDESTINATIONEXISTS[overwrite.upper()]
    except KeyError:
        raise ValueError(f"Given invalid overwrite kwargs {str(overwrite)}, supported "
                         "value are: 'APPEND', 'FAIL_ON_FILE_CONFLICT', "
                         "'MERGE_WITH_OVERWRITE'.")


def _get_logger():
    global _logger
    if _logger is None:
        _logger = _LoggerFactory.get_logger(__name__)
    return _logger


class AzureMachineLearningFileSystem(AsyncFileSystem):
    """
    Access Azure Machine Learning defined URI as if it were a file system.
    This exposes a filesystem-like API on top of Azure Machine Learning defined URI

    .. remarks::
        This will enable pandas/dask to load Azure Machine Learning defined URI.

        .. code-block:: python
            # list all the files from a folder
            datastore_uri_fs = AzureMachineLearningFileSystem(uri=
                'azureml://subscriptions/{sub_id}/resourcegroups/{rs_group}/'
                'workspaces/{ws}/datastores/{my_datastore}')
            datastore_uri_fs.ls('folder/')

            # load parquet file to pandas
            import pandas
            df = pandas.read_parquet('azureml://subscriptions/{sub_id}/resourcegroups/{rs_group}/workspaces/{ws}'
                                     '/datastores/workspaceblobstore/paths/myfolder/mydata.parquet')

            # load csv file to pandas
            import pandas
            df = pandas.read_csv('azureml://subscriptions/{sub_id}/resourcegroups/{rs_group}/workspaces/{ws}'
                                 '/datastores/workspaceblobstore/paths/myfolder/mydata.csv')

            # load parquet file to dask
            import dask.dataframe as dd
            df = dd.read_parquet('azureml://subscriptions/{sub_id}/resourcegroups/{rs_group}/workspaces/{ws}'
                                 '/datastores/workspaceblobstore/paths/myfolder/mydata.parquet')

            # load csv file to dask
            import dask.dataframe as dd
            df = dd.read_csv('azureml://subscriptions/{sub_id}/resourcegroups/{rs_group}/workspaces/{ws}'
                             '/datastores/workspaceblobstore/paths/myfolder/mydata.csv')

    :param uri: Azure Machine Learning defined URI
        Currently we support datastore uri, "azureml://subscriptions/([^\/]+)/resourcegroups/([^\/]+)/
        (?:Microsoft.MachineLearningServices/)?workspaces/([^\/]+)/datastores/([^\/]+)/paths/(.*)"
    :type uri: str
    """

    protocol = "azureml"

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def __init__(
            self,
            uri: str = None,
            **kwargs):
        """
        Initialize a new AzureMachineLearningFileSystem object

        :param uri: the uri to initialize AzureMachineLearningFileSystem.
        :type uri: str

        """
        super().__init__(
            asynchronous=False, loop=get_loop()
        )

        subscription_id, resource_group, workspace_name, datastore_name, _ = \
            AzureMachineLearningFileSystem._infer_storage_options(uri)
        self._path = uri
        datastore_source = {
            'subscription': subscription_id,
            'resourceGroup': resource_group,
            'workspaceName': workspace_name,
            'datastoreName': datastore_name
        }

        self._workspace_context = {
            'subscription': subscription_id,
            'resource_group': resource_group,
            'workspace_name': workspace_name,
            'datastore_name': datastore_name
        }
        self._datastore_source = datastore_source
        self._inspect_caller = ""
        try:
            callstack = inspect.stack()
            stack_count = 0
            for frame in callstack:
                cur_filename = frame.filename
                cur_filename = cur_filename.replace('\\', '/')
                if cur_filename.find('site-packages/pandas') != -1:
                    self._inspect_caller = 'pandas'
                elif cur_filename.find('site-packages/dask') != -1:
                    self._inspect_caller = 'dask'
                stack_count += 1
                if stack_count > 10:
                    break
        except Exception as e:
            _LoggerFactory.trace_warn(_get_logger(),
                                      f"__init__ get inspect caller have exceptions: {e}",
                                      self._workspace_context)

        _LoggerFactory.trace(_get_logger(), "__init__",
                             self._workspace_context)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    async def _info(self, path, refresh=True):
        """
        Info api

        :param path: the path to return info for.
        :type path: str
        :param refresh: whether to load it from dircache.
        :type refresh: bool
        :return: A dictionary of file details, returns FileNotFoundError if not exist
        :rtype: dict
        """
        normalized_path = self._strip_protocol(path, self._workspace_context)
        parent = self._parent(path)

        if not refresh:
            # try to get it from dir cache
            out = self._ls_from_cache(normalized_path.rstrip('/'))
            if not out:
                return {"name": path, "size": None, "type": "directory"}
            else:
                entries = [
                    f
                    for f in self.dircache[parent]
                    if f["name"] == normalized_path
                ]
                if len(entries) == 0:
                    # parent dir was listed but did not contain this path
                    raise FileNotFoundError(path)
                return entries[0]
        else:
            try:
                # try to list the parent path to return path info
                out = await self._ls(parent, detail=True, refresh=True)

                # the same path might have entry for both file and directory
                entries = [
                    f
                    for f in out
                    if f["name"] in [normalized_path, normalized_path + '/']
                ]

                if len(entries) == 0:
                    raise FileNotFoundError(path)
                return entries[0]
            except Exception as ex:
                raise FileNotFoundError(ex)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    async def _exists(self, path):
        """
        exists api

        :param path: the path to return info for.
        :type path: str
        :return: whether a path exists or not
        :rtype: bool
        """
        normalized_path = self._strip_protocol(path, self._workspace_context)
        parent = self._parent(path)

        # first check ls cache with key path and its parent path
        if self._ls_from_cache(normalized_path.rstrip('/')):
            return True

        out = self._ls_from_cache(parent)
        if out:
            files = [
                f
                for f in out
                if f["name"] == normalized_path
            ]
            if len(files) > 0:
                return True

        try:
            await self._info(path, refresh=True)
            return True
        except FileNotFoundError:
            return False

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def glob(self, path=None, **kwargs):
        """
        globbing result for the uri

        :param path: path to glob, it can be long form datastore uri or
                    just relative path in the format of {datastore}/{relative_path}
        :type path: str
        :return: A list of file paths
        :rtype: list[str]
        """
        return sync(self.loop, self._glob, path)

    async def _glob(self, path=None, **kwargs):
        """
        globbing result for the uri

        :param path: path to glob, default to be the uri from __init__
        :type path: str
        :return: A list of file paths
        :rtype: list[str]
        """
        custom_dimensions = {'app_name': _APP_NAME}
        custom_dimensions.update(self._workspace_context)

        with _LoggerFactory.track_activity(_get_logger(), 'glob', _PUBLIC_API,
                                           custom_dimensions) as activityLogger:
            try:
                if not path:
                    path = self._path
                path = self._strip_protocol(
                    path, self._workspace_context).rstrip("/")
                path = self._get_full_path_from_fs_root(path)
                dataflow = _dprep.Dataflow(
                    _dprep.api.engineapi.api.get_engine_api())
                dataflow = dataflow.add_step(
                    'Microsoft.DPrep.GetDatastoreFilesBlock',
                    {'datastores': [self._construct_datastore_source(path)]})
                stream_properties_expression = get_stream_properties(dataflow['Path'])
                dataflow = dataflow._add_columns_from_record(stream_properties_expression)
                records = dataflow._to_pyrecords()
                if len(records) < 1:
                    raise ValueError(f'No files found for {path}')
                else:
                    files = []
                    for r in records:
                        name = r['Path'].resource_identifier[len(self._datastore_source['datastoreName']) + 1:]
                        files.append(name)
                return files
            except Exception as e:
                if hasattr(activityLogger, ACTIVITY_INFO_KEY):
                    activityLogger.activity_info['error_code'] = getattr(
                        e, ERROR_CODE_KEY, '')
                    activityLogger.activity_info['message'] = getattr(
                        e, COMPLIANT_MESSAGE_KEY, str(e))
                    activityLogger.activity_info['outer_error_code'] = getattr(
                        e, OUTER_ERROR_CODE_KEY, '')

                AzureMachineLearningFileSystem._map_user_error(e)

    async def _ls(self, path=None, detail=False, refresh=True, **kwargs):
        """
        List uri, this will return the full list of files iteratively.

        :param path: path to list
        :type path: str
        :param detail: whether to return details other than path
        :type detail: bool
        :param refresh: whether to just list for dircache
        :type refresh: bool
        :return: A list of file paths if detail is False, else returns a list of dict
        :rtype: list[str] or list[dict]
        """
        custom_dimensions = {'app_name': _APP_NAME}
        custom_dimensions.update(self._workspace_context)

        with _LoggerFactory.track_activity(_get_logger(), 'ls', _PUBLIC_API,
                                           custom_dimensions) as activityLogger:
            try:
                ensure_rslex_environment()
                if not path:
                    path = self._path
                path = self._strip_protocol(
                    path, self._workspace_context).rstrip("/")
                path = self._get_full_path_from_fs_root(path)

                if not refresh:
                    try:
                        return self._ls_from_cache(path)
                    except KeyError:
                        raise FileNotFoundError

                ensure_rslex_environment()
                datastore_source = PyDatastoreSource(
                    self._datastore_source.get('subscription'),
                    self._datastore_source.get('resourceGroup'),
                    self._datastore_source.get('workspaceName'),
                    self._datastore_source.get('datastoreName'),
                    '',
                    '',
                    None
                )

                list_results = []
                # list result might have the same path for file and directory, but directory will have ending / in path
                entrys = datastore_source.list_directory(path)
                for entry in entrys:
                    list_results.append({
                        'name': entry.resource_identifier[len(self._datastore_source['datastoreName']) + 1:],
                        'type': entry.type_string,
                        'size': None if entry.type_string == 'directory' else entry.file_attributes.get_value('size')
                    })

                self.dircache[path] = list_results
                return self.dircache[path] if detail else sorted([o["name"] for o in self.dircache[path]])
            except Exception as e:
                if hasattr(activityLogger, ACTIVITY_INFO_KEY):
                    activityLogger.activity_info['error_code'] = getattr(
                        e, ERROR_CODE_KEY, '')
                    activityLogger.activity_info['message'] = getattr(
                        e, COMPLIANT_MESSAGE_KEY, str(e))
                    activityLogger.activity_info['outer_error_code'] = getattr(
                        e, OUTER_ERROR_CODE_KEY, '')

                AzureMachineLearningFileSystem._map_user_error(e)

    async def _open(
            self,
            path: str = None,
            mode: str = 'rb',
            **kwargs,
    ):
        """
        Open a file from a datastore uri

        :param path: the path to open, default to the first file
        :type path: str
        :param mode: mode to open the file, supported modes are ['r', 'rb'], both means read byte
        :type mode: str
        :return: OpenFile
        :rtype: OpenFile
        """

        """Open a file from a datastore uri

        Parameters
        ----------
        path: str
            Path to file to open, result returned from ls() or glob()
        """
        custom_dimensions = {'app_name': _APP_NAME, 'inspect_caller': self._inspect_caller}
        custom_dimensions.update(self._workspace_context)

        memory_cache_size = 2 * 1024 * 1024 * 1024
        read_threads = 64
        _FS_DOWNLOAD_MEMORY_CACHE_SIZE = '_FS_DOWNLOAD_MEMORY_CACHE_SIZE'
        if _FS_DOWNLOAD_MEMORY_CACHE_SIZE in os.environ:
            memory_cache_size = os.environ[_FS_DOWNLOAD_MEMORY_CACHE_SIZE]

        _FS_DOWNLOAD_READ_THREADS = '_FS_DOWNLOAD_READ_THREADS'
        if _FS_DOWNLOAD_READ_THREADS in os.environ:
            read_threads = os.environ[_FS_DOWNLOAD_READ_THREADS]

        with _LoggerFactory.track_activity(_get_logger(), 'open', _PUBLIC_API,
                                           custom_dimensions) as activityLogger:
            try:
                ensure_rslex_environment()

                if not path:
                    path = self._path
                path = self._strip_protocol(path, self._workspace_context)
                path = self._get_full_path_from_fs_root(path)
                self._validate_args_for_open(mode)

                dataflow = _dprep.Dataflow(
                    _dprep.api.engineapi.api.get_engine_api())

                # construct datastore source on top of the workspace context from __init__
                dataflow = dataflow.add_step(
                    'Microsoft.DPrep.GetDatastoreFilesBlock',
                    {'datastores': [self._construct_datastore_source(path)]})
                stream_properties_expression = get_stream_properties(
                    dataflow['Path'])
                dataflow = dataflow._add_columns_from_record(
                    stream_properties_expression)
                records = dataflow._to_pyrecords()
                if len(records) < 1:
                    raise ValueError("File not found for the path to open")
                if len(records) > 1:
                    raise ValueError("Path is not a single file path")

                r = records[0]
                si = StreamInfo(
                    r['Path'].handler, r['Path'].resource_identifier, r['Path'].arguments)
                downloader = Downloader(block_size=8 * 1024 * 1024, read_threads=read_threads,
                                        caching_options=CachingOptions(memory_cache_size=memory_cache_size))

                return si.open(buffering_options=BufferingOptions(64, downloader))
            except Exception as e:
                if hasattr(activityLogger, ACTIVITY_INFO_KEY):
                    activityLogger.activity_info['error_code'] = getattr(
                        e, ERROR_CODE_KEY, '')
                    activityLogger.activity_info['message'] = getattr(
                        e, COMPLIANT_MESSAGE_KEY, str(e))
                    activityLogger.activity_info['outer_error_code'] = getattr(
                        e, OUTER_ERROR_CODE_KEY, '')

                AzureMachineLearningFileSystem._map_user_error(e)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    async def _expand_path(self, path, recursive=False, maxdepth=None):
        if isinstance(path, str):
            out = await self._expand_path([path], recursive, maxdepth)
        else:
            # reduce depth on each recursion level unless None or 0
            maxdepth = maxdepth if not maxdepth else maxdepth - 1
            out = set()
            path = [self._strip_protocol(
                p, self._workspace_context) for p in path]
            for p in path:  # can gather here
                if has_magic(p):
                    bit = set(await self._glob(p))
                    out |= bit
                    continue
                elif recursive:
                    rec = set(await self._find(p, maxdepth=maxdepth, withdirs=False))
                    out |= rec
                if (not out or p not in out) and recursive is False:
                    # should only check once, for the root
                    out.add(p)
        if not out:
            raise FileNotFoundError(path)
        return list(sorted(out))

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def get(self, rpath, lpath, recursive=False, callback=_DEFAULT_CALLBACK, **kwargs):
        """Copy file(s) to local."""
        return sync(self.loop, self._get, rpath, lpath, recursive, callback, **kwargs)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    async def _get(
            self, rpath, lpath, recursive=False, callback=_DEFAULT_CALLBACK, **kwargs
    ):
        """Copy file(s) to local.

        Copies a specific file or tree of files (if recursive=True). If lpath
        ends with a "/", it will be assumed to be a directory, and target files
        will go within. Can submit a list of paths, which may be glob-patterns
        and will be expanded.

        The get_file method will be called concurrently on a batch of files. The
        batch_size option can configure the amount of futures that can be executed
        at the same time. If it is -1, then all the files will be uploaded concurrently.
        The default can be set for this instance by passing "batch_size" in the
        constructor, or for all instances by setting the "gather_batch_size" key
        in ``fsspec.config.conf``, falling back to 1/8th of the system limit .
        """
        rpath = self._strip_protocol(rpath, self._workspace_context)
        lpath = make_path_posix(lpath)
        if (await self._info(rpath))["type"] == "file" and recursive is True:
            raise ValueError("rpath type of single file should not use recursive download")
        rpaths = await self._expand_path(rpath, recursive=recursive)
        batch_size = kwargs.pop("batch_size", self.batch_size)
        rpath = self._get_full_path_from_fs_root(rpath)

        coros = []
        callback.set_size(len(rpaths))

        # needs to get parent folder if its download single file as base dir
        base_dir = rpath if len(
            rpaths) > 1 or recursive else self._parent(rpath)
        kwargs.update({'base_dir': base_dir})
        for remote_path in rpaths:
            remote_path = self._get_full_path_from_fs_root(remote_path)
            callback.branch(remote_path, lpath, kwargs)
            coros.append(self._get_file(remote_path, lpath, **kwargs))
        await _run_coros_in_chunks(coros, batch_size=batch_size, callback=callback)

    async def _get_file(self, rpath, lpath, overwrite="FAIL_ON_FILE_CONFLICT", callback=_DEFAULT_CALLBACK, **kwargs):
        """
        Copy single file remote to local
        :param lpath: Path to local file
        :param rpath: Path to remote file, rpath is in the format of {datastore_name}/{relative_path}
        :param overwrite: string. Suppurts values "APPEND", "FAIL_ON_FILE_CONFLICT", "MERGE_WITH_OVERWRITE".
        """
        custom_dimensions = {'app_name': _APP_NAME}
        custom_dimensions.update(self._workspace_context)

        with _LoggerFactory.track_activity(_get_logger(), 'get_file', _PUBLIC_API,
                                           custom_dimensions) as activityLogger:
            overwrite = _to_py_if_destination_exists(overwrite)

            try:
                ensure_rslex_environment()
                base_dir = kwargs.get('base_dir', None)

                copier = Copier(PyLocationInfo('Local', lpath, {}),
                                base_dir, overwrite)
                si = StreamInfo(_DATASTORE_HANDLER, rpath,
                                self._datastore_source)
                copier.copy_stream_info(si, '')
            except Exception as e:
                if hasattr(activityLogger, ACTIVITY_INFO_KEY):
                    activityLogger.activity_info['error_code'] = getattr(
                        e, ERROR_CODE_KEY, '')
                    activityLogger.activity_info['message'] = getattr(
                        e, COMPLIANT_MESSAGE_KEY, str(e))
                    activityLogger.activity_info['outer_error_code'] = getattr(
                        e, OUTER_ERROR_CODE_KEY, '')

                AzureMachineLearningFileSystem._map_user_error(e)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def put(self, lpath, rpath, recursive=False, callback=_DEFAULT_CALLBACK, **kwargs):
        """Copy file(s) to local."""
        return sync(self.loop, self._put, lpath, rpath, recursive, callback, **kwargs)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    async def _put(
            self,
            lpath,
            rpath,
            recursive=False,
            callback=_DEFAULT_CALLBACK,
            batch_size=None,
            **kwargs,
    ):
        """Copy file(s) from local.

        Copies a specific file or tree of files (if recursive=True). If rpath
        ends with a "/", it will be assumed to be a directory, and target files
        will go within.

        The put_file method will be called concurrently on a batch of files. The
        batch_size option can configure the amount of futures that can be executed
        at the same time. If it is -1, then all the files will be uploaded concurrently.
        The default can be set for this instance by passing "batch_size" in the
        constructor, or for all instances by setting the "gather_batch_size" key
        in ``fsspec.config.conf``, falling back to 1/8th of the system limit .
        """
        if not rpath:
            rpath = self._path
        # append ending / to indicate its a directory
        rpath = self._strip_protocol(rpath, self._workspace_context)
        rpath = self._get_full_path_from_fs_root(rpath)
        rpath = rpath.rstrip('/') + '/'
        if isinstance(lpath, str):
            lpath = make_path_posix(lpath)
        fs = LocalFileSystem()
        lpaths = fs.expand_path(lpath, recursive=recursive)
        rpaths = self._other_paths(lpaths, rpath)
        is_dir = {l_path: os.path.isdir(l_path) for l_path in lpaths}
        rdirs = [r_path for l_path, r_path in zip(lpaths, rpaths) if is_dir[l_path]]
        file_pairs = [(l_path, r_path) for l_path, r_path in zip(lpaths, rpaths) if not is_dir[l_path]]

        await asyncio.gather(*[self._makedirs(d, exist_ok=True) for d in rdirs])
        batch_size = batch_size or self.batch_size

        coros = []
        callback.set_size(len(file_pairs))
        for lfile, rfile in file_pairs:
            callback.branch(lfile, rfile, kwargs)
            coros.append(self._put_file(lfile, rfile, **kwargs))

        await _run_coros_in_chunks(
            coros, batch_size=batch_size, callback=callback
        )

    async def _put_file(
            self, lpath, rpath, overwrite="FAIL_ON_FILE_CONFLICT", callback=_DEFAULT_CALLBACK, **kwargs
    ):
        """
        Copy single file to remote
        :param lpath: Path to local file
        :param rpath: Path to remote file, rpath is in the format of {datastore_name}/{relative_path}
        :param overwrite: string. Suppurts values "APPEND", "FAIL_ON_FILE_CONFLICT", "MERGE_WITH_OVERWRITE".
        :param callback: callback function
        """
        custom_dimensions = {'app_name': _APP_NAME}
        custom_dimensions.update(self._workspace_context)
        with _LoggerFactory.track_activity(_get_logger(), 'put_file', _PUBLIC_API,
                                           custom_dimensions) as activityLogger:
            overwrite = _to_py_if_destination_exists(overwrite)

            try:
                # rpath has the remote file name, copy_stream_info expects folder
                rpath = self._parent(rpath)
                ensure_rslex_environment()
                destination_info = PyLocationInfo(
                    _DATASTORE_HANDLER,
                    rpath,
                    self._datastore_source)

                # get abspath and replace '\' to '/'
                lpath = os.path.abspath(lpath)
                lpath = lpath.replace('\\', '/')

                copier = Copier(destination_info, self._parent(lpath), overwrite)

                source_stream_info = StreamInfo('Local', lpath, {})
                copier.copy_stream_info(source_stream_info, '')
            except Exception as e:
                if hasattr(activityLogger, ACTIVITY_INFO_KEY):
                    activityLogger.activity_info['error_code'] = getattr(
                        e, ERROR_CODE_KEY, '')
                    activityLogger.activity_info['message'] = getattr(
                        e, COMPLIANT_MESSAGE_KEY, str(e))
                    activityLogger.activity_info['outer_error_code'] = getattr(
                        e, OUTER_ERROR_CODE_KEY, '')

                AzureMachineLearningFileSystem._map_user_error(e)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _validate_args_for_open(self, mode):
        supported_modes = ['r', 'rb']
        if mode not in supported_modes:
            raise ValueError(f'Invalid mode {mode}, supported modes are {supported_modes}, '
                             'both means read as byte array')

    def _parent(self, path):
        path = self._strip_protocol(path.rstrip("/"), self._workspace_context)
        if "/" in path:
            # path.rsplit("/", 1)[0].lstrip("/")
            return path.rsplit("/", 1)[0]
        # root path of datastore, eg: workspaceblobstore/
        else:
            return path

    def _get_full_path_from_fs_root(self, path):
        path = path.strip("/")
        path = os.path.normpath(path)
        path = path.replace('\\', '/')
        while path.startswith("../"):
            path = path[3:]
        if path.startswith(".."):
            path = path[2:]
        if path.startswith("."):
            path = path[1:]
        return f"{self._datastore_source['datastoreName']}/{path}"

    def _ls_from_cache(self, path):
        """Check cache for listing

        Returns listing, if found (may me empty list for a directly that exists
        but contains nothing), None if not in cache.

        Override the default implementation in fsspec because we need to append ending / to indicate its a directory
        """
        if path.rstrip("/") in self.dircache:
            return self.dircache[path.rstrip("/")]

    def _construct_datastore_source(self, path):
        # path in short form resource_identifier, eg workspace/myfolder/mydata.csv
        datastore_source = dict(self._datastore_source)
        segments = pathlib.Path(path)
        datastore_source.update({
            'datastoreName': str(segments.parts[0]),
            'path': str(pathlib.PurePosixPath(*segments.parts[1:]))
        })

        return datastore_source

    @staticmethod
    def _infer_storage_options(path):
        _data_path_uri_regex_pattern = re.compile(
            r'^azureml://subscriptions/([^\/]+)/resourcegroups/([^\/]+)/'
            r'(?:providers/Microsoft.MachineLearningServices/)?workspaces/([^\/]+)/datastores/([^\/]+)/paths/(.*)',
            re.IGNORECASE)

        _datastore_uri_regex_pattern = re.compile(
            r'^azureml://subscriptions/([^\/]+)/resourcegroups/([^\/]+)/'
            r'(?:providers/Microsoft.MachineLearningServices/)?workspaces/([^\/]+)/datastores/([^\/]+)', re.IGNORECASE)

        data_path_uri_match = _data_path_uri_regex_pattern.match(path)
        datastore_uri_match = _datastore_uri_regex_pattern.match(path)
        if data_path_uri_match:
            return data_path_uri_match[1], data_path_uri_match[2], data_path_uri_match[3], data_path_uri_match[4],\
                data_path_uri_match[5]
        elif datastore_uri_match:
            return datastore_uri_match[1], datastore_uri_match[2], datastore_uri_match[3], datastore_uri_match[4], '/'
        else:
            raise ValueError(f'{path} is not a valid datastore uri: '
                             f'azureml://subscriptions/([^\/]+)/resourcegroups/([^\/]+)/'
                             f'(?:Microsoft.MachineLearningServices/)?workspaces/([^\/]+)/'
                             f'datastores/([^\/]+)/paths/(.*)')

    @staticmethod
    def _get_kwargs_from_urls(path):
        """ Directly return the path """
        out = {}
        out["uri"] = path
        return out

    @staticmethod
    def _map_user_error(exception):
        for msg in _USER_ERROR_MESSAGES:
            if msg in exception.args[0]:
                raise ValueError(exception.args[0])

        raise exception

    @classmethod
    def _strip_protocol(cls, path, workspace_context=None):
        """
        Turn path from fully-qualified to file-system-specific
        return {datastore_name}/myfolder/mydata.parquet for
            'azureml://subscriptions/{sub_id}/resourcegroups/{rs_group}/workspaces/{ws}/'
            'datastores/{datastore_name}/paths/myfolder/mydata.parquet'
        """
        if path.startswith(cls.protocol + "://"):
            storage_options = AzureMachineLearningFileSystem._infer_storage_options(
                path)

            # Currently limit to the same workspace
            # So need to ensure workspace information is the same
            # with self._workspace_context from file system initializatoin
            if workspace_context and \
                    (storage_options[0] != workspace_context['subscription']
                     or storage_options[1] != workspace_context['resource_group']
                     or storage_options[2] != workspace_context['workspace_name']
                     or storage_options[3] != workspace_context['datastore_name']):
                raise ValueError(
                    'Please create new file system instance for different workspace or storage operations')

            return f'{storage_options[4]}'

        return path

    @staticmethod
    def _other_paths(paths, path2, is_dir=None, exists=False):
        def common_prefix(paths):
            """For a list of paths, find the shortest prefix common to all"""
            parts = [p.split("/") for p in paths]
            lmax = min(len(p) for p in parts)
            end = 0
            for i in range(lmax):
                end = all(p[i] == parts[0][i] for p in parts)
                if not end:
                    break
            i += end
            return "/".join(parts[0][:i])

        if isinstance(path2, str):
            is_dir = is_dir or path2.endswith("/")
            path2 = path2.rstrip("/")
            if len(paths) > 1:
                cp = common_prefix(paths)
                if exists:
                    cp = cp.rsplit("/", 1)[0]
                path2 = [p.replace(cp, path2, 1) for p in paths]
            else:
                if is_dir:
                    path2 = [path2.rstrip("/") + "/" + paths[0].rsplit("/")[-1]]
                else:
                    path2 = [path2]
        else:
            assert len(paths) == len(path2)
        return path2
