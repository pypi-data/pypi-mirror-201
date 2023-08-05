"""
Define functionality to write to and read from manifest files.

See the Manifest class.
"""

from collections.abc import Sequence
import multiprocessing
import os
from typing import Dict
from typing import Generator
from typing import List
from typing import Optional

import hyperthought as ht
from hyperthought.metadata import MetadataItem

from . import database
from .database import MetadataApplicationFilter
from . import utils


MAX_PROCESSES = 60


class PathNotFoundException(Exception):
    pass


class JobDataNotFoundException(Exception):
    pass


def _compute_size_hash_and_end_bytes(file_: Dict) -> Dict:
    """
    Compute size, hash, and end bytes for a file.

    Parameters
    ----------
    file_ : dict
        Database record for the file of interest.

    Returns
    -------
    A dict with keys "id", "size", "hash", and "end_bytes".
    """
    path = file_["path"]
    size = os.path.getsize(path)
    file_hash = utils.get_hash(file_name=path)
    end_bytes = ",".join(str(i) for i in utils.get_end_bytes(path=path))
    return {
        "id": file_["id"],
        "size": size,
        "file_hash": file_hash,
        "end_bytes": end_bytes,
    }


class Manifest:
    """
    File transfer manifest.

    Maintains data on job, paths (files and folders to be transferred),
    parsers, and metadata.

    Parameters
    ----------
    manifest_file : str
        Path to manifest file, which will be a sqlite database.
    overwrite_manifest_file : bool
        If the manifest file already exists, this variable will determine
        whether the existing file will be used or if a new (blank) file
        will overwrite it.
    job_name : str or None
        Must be provided if a new database is created for the manifest.
        The name of the job.  Conventionally, [SOURCE_COMPUTER]_[DATETIME].
    username : str or None
        Must be provided if a new database is created for the manifest.
        The HyperThought username of the user making the upload request.
    workspace_alias : str
        Must be provided if a new database is created for the manifest.
        The alias of the workspace to which the files will be uploaded.
    ignore_path : str or None
        Must be provided if a new database is created for the manifest.
        The (beginning) part of each path that will not be duplicated in
        HyperThought.
    hyperthought_root : str
        Human-readable path to the root HyperThought folder.
        Ex:
            For a file `/a/b/c/d.txt`, ignore_path `/a/b`, and
            hyperthought_root `/x/y`, the path to the file after upload
            will be `/x/y/c/d.txt`.
    """

    def __init__(
        self,
        manifest_file: str,
        overwrite_manifest_file: bool = False,
        job_name: Optional[str] = None,
        username: Optional[str] = None,
        workspace_alias: Optional[str] = None,
        ignore_path: Optional[str] = None,
        hyperthought_root: str = "/",
    ) -> None:
        self._manifest_file = manifest_file
        self._job_name = job_name
        self._username = username
        self._workspace_alias = workspace_alias
        self._ignore_path = (
            utils.clean_path(ignore_path) if ignore_path else ignore_path
        )

        if (
            isinstance(self._ignore_path, str)
            and
            self._ignore_path.endswith(":")
        ):
            self._ignore_path += os.path.sep

        self._hyperthought_root = hyperthought_root.replace("\\", "/")
        self._hyperthought_root_id_path = ","
        self._database = None
        self._file_info_computed = False

        if os.path.exists(self._manifest_file):
            if not os.path.isfile(manifest_file):
                raise ValueError(f"{manifest_file} is not a file")

            if overwrite_manifest_file:
                self._create_database()
            else:
                self._set_database()
        else:
            self._create_database()

    def _create_database(self) -> None:
        """Create new database.  Load job information."""
        self._validate_job_data()
        connection = database.connect.get_connection(
            manifest_path=self._manifest_file,
            overwrite=True,
        )
        self._database = database.Database(connection=connection)
        self._database.create_job_data(
            job_name=self._job_name,
            username=self._username,
            workspace_alias=self._workspace_alias,
            ignore_path=self.ignore_path,
            hyperthought_root=self._hyperthought_root,
        )
        self._create_hyperthought_root()

    def _create_hyperthought_root(self) -> None:
        """Create File records for all hyperthought_root folders."""
        ht_id_path = ","
        stripped_root = self.hyperthought_root.strip("/")

        if not stripped_root:
            self._hyperthought_root_id_path = ht_id_path
            return

        root_folders = stripped_root.split("/")
        file_data = []

        for folder_name in root_folders:
            ht_id = utils.generate_id()
            file_data.append(
                {
                    "name": folder_name,
                    "hyperthought_id": ht_id,
                    "hyperthought_id_path": ht_id_path,
                    "is_folder": True,
                    "path": None,
                    "end_bytes": None,
                    "size": None,
                    "file_hash": None,
                }
            )
            ht_id_path = f"{ht_id_path}{ht_id},"

        self._database.bulk_load_files(file_data=file_data)
        self._hyperthought_root_id_path = ht_id_path

    def _set_database(self) -> None:
        """Connect to existing database."""
        connection = database.connect.get_connection(
            manifest_path=self._manifest_file,
            overwrite=False,
        )
        self._database = database.Database(connection=connection)
        job_data = self._database.get_job_data()

        if job_data is None:
            raise JobDataNotFoundException(
                f"No job data in {self._manifest_file}")

        self._job_name = job_data["job_name"]
        self._username = job_data["username"]
        self._workspace_alias = job_data["workspace_alias"]
        self._ignore_path = job_data["ignore_path"]
        self._hyperthought_root = job_data["hyperthought_root"]

        stripped_root = self._hyperthought_root.strip("/")

        if not stripped_root:
            return

        def get_hyperthought_id(name, hyperthought_id_path):
            """Get a hyperthought_id given name and hyperthought_id_path."""
            file_ = self.database.get_file(
                name=name,
                hyperthought_id_path=hyperthought_id_path,
            )

            if not file_:
                return None

            return file_["hyperthought_id"]

        root_folders = stripped_root.split("/")
        hyperthought_id_path = ","

        for folder_name in root_folders:
            hyperthought_id = get_hyperthought_id(
                name=folder_name,
                hyperthought_id_path=hyperthought_id_path,
            )

            if not hyperthought_id:
                hyperthought_id = utils.generate_id()
                self.database.create_file(
                    name=folder_name,
                    is_folder=True,
                    hyperthought_id=hyperthought_id,
                    hyperthought_id_path=hyperthought_id_path,
                )

            hyperthought_id_path += hyperthought_id + ","

        self._hyperthought_root_id_path = hyperthought_id_path

    def _validate_job_data(self) -> None:
        """
        Validate job data parameters (to constructor).

        Called from _create_database.
        """
        if not self._job_name or not isinstance(self._job_name, str):
            raise ValueError("job_name must be a non-empty string")

        if not self._username or not isinstance(self._username, str):
            raise ValueError("username must be a non-empty string")

        if (
            not self._workspace_alias
            or
            not isinstance(self._workspace_alias, str)
        ):
            raise ValueError("workspace_id must be a non-empty string")

        # TODO:  Make code below work properly when creating db from json.
        # if (
        #     self._ignore_path is not None
        #     and
        #     not os.path.isdir(self._ignore_path)
        # ):
        #     raise ValueError(
        #         "ignore_path_prefix must be a directory if provided")

        if (
            not self._hyperthought_root
            or
            not isinstance(self._hyperthought_root, str)
        ):
            raise ValueError("hyperthought_root must be a string")

        if not self._hyperthought_root.startswith("/"):
            raise ValueError("hyperthought_root must start with '/'")

    @property
    def database(self):
        return self._database

    @property
    def common_metadata(self) -> List[MetadataItem]:
        return ht.metadata.from_api_format(
            self.database.get_common_metadata())

    @common_metadata.setter
    def common_metadata(self, metadata: List[MetadataItem]) -> None:
        self._validate_metadata(metadata)
        self.database.create_or_update_common_metadata(metadata=metadata)

    @property
    def ignore_path(self) -> Optional[str]:
        return self._ignore_path

    @property
    def hyperthought_root(self) -> str:
        return self._hyperthought_root

    @property
    def hyperthought_root_id_path(self) -> str:
        return self._hyperthought_root_id_path

    @hyperthought_root_id_path.setter
    def hyperthought_root_id_path(self, value: str) -> None:
        self._hyperthought_root_id_path = value

    @property
    def file_info_computed(self) -> bool:
        return self._file_info_computed

    def _validate_metadata(self, metadata: List[MetadataItem]) -> None:
        """
        Make sure metadata is a list of MetadataItem objects.

        An exception will be raised if the metadata is not valid.
        """
        if not isinstance(metadata, Sequence) or isinstance(metadata, str):
            raise ValueError("metadata must be a non-string sequence")

        for item in metadata:
            if not isinstance(item, MetadataItem):
                raise ValueError(
                    "all elements of metadata must be instances of "
                    "hyperthought.metadata.MetadataItem"
                )

    def add_path(self, path: str) -> None:
        """
        Add a path to the manifest.

        Ancestor folders will be created as needed.
        """
        # TODO:  Consider removing this function and using add_paths instead.
        path = utils.clean_path(path)
        self._validate_path(path)

        # Exit early if the path has already been added.
        if self.has_path(path):
            return

        is_folder = os.path.isdir(path)

        if not is_folder:
            self._file_info_computed = False

        # Get a list of ancestor folders.
        len_ignorepath = (
            0
            if self._ignore_path is None
            else len(self._ignore_path)
        )

        ancestor_folders = (
            path[len_ignorepath:].strip(os.path.sep).split(os.path.sep)
        )[:-1]
        n_ancestors = len(ancestor_folders)
        ancestor_found = False

        # Determine how many ancestors need to be created.
        # Go backwards until an existing folder is found.
        # break_index will be one more than the index of the last folder that
        # already exists, or 1 if no folders exist.
        break_index = None

        for break_index in reversed(range(1, n_ancestors + 1)):
            ancestor_folders_to_join = ancestor_folders[0:break_index]
            ancestor_path = (
                os.path.join(self._ignore_path, *ancestor_folders_to_join)
                if self._ignore_path is not None
                else os.path.join(*ancestor_folders_to_join)
            )

            if self.has_path(ancestor_path):
                ancestor_found = True
                break

        # Get the hyperthought id path starting with an existing folder,
        # if present, or the root id path.
        if ancestor_found:
            # Maintain the invariant that break_index is the index of the
            # first folder that *doesn't* exist.
            break_index += 1
            ancestor_id = self.database.get_file_id(path=ancestor_path)
            ancestor = self.database.get_file(file_id=ancestor_id)
            ht_id_path = (
                f"{ancestor['hyperthought_id_path']}"
                f"{ancestor['hyperthought_id']},"
            )
        else:
            ht_id_path = self.hyperthought_root_id_path

        # Variable for bulk file record creation.
        file_data = []

        # Add folders that need to be created.
        if break_index is not None:
            for folder_index in range(break_index, n_ancestors + 1):
                ancestor_folders_to_join = ancestor_folders[:folder_index]
                folder_path = (
                    os.path.join(self._ignore_path, *ancestor_folders_to_join)
                    if self._ignore_path is not None
                    else os.path.join(*ancestor_folders_to_join)
                )
                ht_id = utils.generate_id()
                file_data.append(
                    {
                        "name": os.path.basename(folder_path),
                        "hyperthought_id": ht_id,
                        "hyperthought_id_path": ht_id_path,
                        "is_folder": True,
                        "path": folder_path,
                        "end_bytes": None,
                        "size": None,
                        "file_hash": None,
                    }
                )
                ht_id_path = f"{ht_id_path}{ht_id},"

        # Add the file/folder itself.
        file_data.append(
            {
                "name": os.path.basename(path),
                "hyperthought_id": utils.generate_id(),
                "hyperthought_id_path": ht_id_path,
                "is_folder": is_folder,
                "path": path,
                "end_bytes": None,
                "size": None,
                "file_hash": None,
            }
        )

        # Create all records.
        self.database.bulk_load_files(file_data=file_data)

    def add_paths(
        self,
        paths: List[str],
        parser_class_name: Optional[str] = None,
    ) -> None:
        """
        Add paths to the manifest.

        Ancestor folders will be created as needed.
        """
        # TODO:  Make paths type generic.  (Any sequence, not just lists.)
        paths = {utils.clean_path(path) for path in paths}

        for path in paths:
            self._validate_path(path)

        if parser_class_name is not None:
            self._validate_parser(parser_class_name=parser_class_name)

        len_ignorepath = (
            0
            if self._ignore_path is None
            else len(self._ignore_path)
        )

        def get_ancestor_paths(path):
            ancestor_tokens = (
                path[len_ignorepath:].strip(os.path.sep).split(os.path.sep)
            )[:-1]

            for index in range(1, len(ancestor_tokens) + 1):
                yield os.path.join(
                    self._ignore_path,
                    *ancestor_tokens[:index]
                )

        for path in list(paths):
            for ancestor_path in get_ancestor_paths(path):
                paths.add(ancestor_path)

        existing_paths = set()
        path_to_hyperthought_id = {}

        for file_ in self.database.get_files(paths=paths):
            existing_paths.add(file_["path"])
            path_to_hyperthought_id[file_["path"]] = file_["hyperthought_id"]

        for path in paths:
            if path not in existing_paths:
                path_to_hyperthought_id[path] = utils.generate_id()

        def get_hyperthought_id_path(path):
            hyperthought_id_path = self.hyperthought_root_id_path

            for ancestor_path in get_ancestor_paths(path):
                ancestor_hyperthought_id = (
                    path_to_hyperthought_id[ancestor_path])
                hyperthought_id_path += f"{ancestor_hyperthought_id},"

            return hyperthought_id_path

        paths_to_create = paths - existing_paths
        file_data = []

        for path in paths_to_create:
            file_data.append({
                "name": os.path.basename(path),
                "hyperthought_id": path_to_hyperthought_id[path],
                "hyperthought_id_path": get_hyperthought_id_path(path),
                "is_folder": os.path.isdir(path),
                "path": path,
                "end_bytes": None,
                "size": None,
                "file_hash": None,
            })

        # Create all file records.
        # NOTE:  file ids will be added in place by the bulk load method.
        self.database.bulk_load_files(file_data=file_data)

        if parser_class_name:
            parser_class = ht.parsers.get(parser_class_name)

            # There will be a 1:1 correspondence between the following lists.
            # Metadata records will be created first.
            # Then the ids for the metadata records, which will be added
            # to the list items in place by the bulk_load_metadata database
            # function, will be added to the entries in the other lists.
            metadata_data = []
            parser_data = []
            metadata_application_data = []

            for file_item in file_data:
                file_extension = (
                    os.path.splitext(file_item["path"])[-1].strip("."))

                if parser_class.is_valid_extension(file_extension):
                    metadata_data.append({
                        "metadata": None,
                    })
                    parser_data.append({
                        "file_id": file_item["id"],
                        "parser_class": parser_class_name,
                        "metadata_id": None
                    })
                    metadata_application_data.append({
                        "metadata_id": None,
                        "file_id": file_item["id"],
                    })

            self.database.bulk_load_metadata(metadata_data=metadata_data)

            for index in range(len(metadata_data)):
                metadata_item = metadata_data[index]

                if "id" not in metadata_item or metadata_item["id"] is None:
                    raise Exception(
                        "ids not added in place via call to "
                        "database.bulk_load_metadata"
                    )

                parser_data[index]["metadata_id"] = metadata_item["id"]
                metadata_application_data[index]["metadata_id"] = (
                    metadata_item["id"])

            self.database.bulk_load_parsers(parser_data=parser_data)
            self.database.bulk_load_metadata_application(
                metadata_application_data=metadata_application_data)

    def remove_path(self, path: str) -> None:
        """
        Remove a path from the manifest.

        Parameters
        ----------
        path : str
            The path to be removed.
        """
        ids_to_remove = [self.get_path_id(path)]

        if os.path.isdir(path):
            ids_to_remove.extend(
                file_["id"]
                for file_ in self.get_progeny(folder_path=path)
            )

        for id_ in ids_to_remove:
            self.database.delete_file(file_id=id_)

    def _validate_path(self, path: str) -> None:
        """
        Determine whether a path is valid.

        An exception will be raised if the path is not valid.
        """
        path = utils.clean_path(path)

        if self.ignore_path and not path.startswith(self.ignore_path):
            raise ValueError(
                f"path '{path}' does not begin with " f"'{self.ignore_path}'"
            )

        if (
            os.path.islink(path)
            or
            not (os.path.isfile(path) or os.path.isdir(path))
        ):
            raise ValueError(
                "path must be a file or directory (links not allowed)")

    def has_path(self, path: str) -> bool:
        """Determine whether a path has already been added."""
        # TODO:  Consider removing this function and always using has_paths.
        path = utils.clean_path(path)
        file_id = self.database.get_file_id(path=path)
        return file_id is not None

    def get_path_id(self, path: str) -> int:
        """Get internal id associated with a path."""
        path = utils.clean_path(path)
        path_id = self.database.get_file_id(path=path)

        if path_id is None:
            raise PathNotFoundException(
                f"path '{path}' has not been added to the manifest"
            )

        return path_id

    def get_progeny(self, folder_path: str) -> List[Dict]:
        """
        Get information on files under a given path in the manifest.

        This will search the manifest for such files, not the local file
        system.

        Parameters
        ----------
        folder_path : str
            The folder of interest.

        Returns
        -------
        A list of file records for paths under the given folder.
        """
        return self.database.get_progeny(folder_path=folder_path)

    def _validate_parser(self, parser_class_name: str) -> None:
        if parser_class_name not in ht.parsers.PARSERS:
            raise ValueError(f"parser '{parser_class_name}' not found")

    def add_parser(
        self,
        file_id: int,
        parser_class_name: str,
        apply_to_file_ids: List[int],
    ) -> None:
        """
        Add a parser application to the manifest.

        Parameters
        ----------
        file_id : int
            The id of the file to be parsed.
        parser_class_name : str
            The class name of the parser to be used.
        apply_to_file_ids : list of int
            Internal ids of files/folders to which the parsed metadata will
            be applied.
        """
        if not apply_to_file_ids:
            raise ValueError("apply_to_file_ids must not be empty")

        self._validate_parser(parser_class_name)
        metadata_id = self.database.create_metadata()
        metadata_application_data = [
            {
                "metadata_id": metadata_id,
                "file_id": file_id,
            }
            for file_id in apply_to_file_ids
        ]
        self.database.bulk_load_metadata_application(
            metadata_application_data=metadata_application_data
        )
        self.database.create_parser(
            file_id=file_id,
            parser_class=parser_class_name,
            metadata_id=metadata_id,
        )

    def add_metadata(
        self, metadata: List[MetadataItem], apply_to_file_ids: List[int]
    ) -> None:
        """
        Add file-specific metadata to the manifest.

        Parameters
        ----------
        metadata : list of MetadataItem
            The metadata of interest.
        apply_to_file_ids : list of str
            Internal ids of files/folders to which the metadata will be
            applied.
        """
        self._validate_metadata(metadata)
        metadata_id = self._database.create_metadata(metadata=metadata)
        metadata_application_data = [
            {"metadata_id": metadata_id, "file_id": file_id}
            for file_id in apply_to_file_ids
        ]
        self.database.bulk_load_metadata_application(
            metadata_application_data=metadata_application_data
        )

    def to_json(self, compute_file_info: bool = True) -> Dict:
        """Convert manifest database to JSON and return results."""
        if compute_file_info and not self.file_info_computed:
            self.compute_file_info()

        output = {}

        # Create the job section of the manifest.
        job_data = self.database.get_job_data()
        output["job"] = {
            "name": job_data["job_name"],
            "username": job_data["username"],
            "workspaceAlias": job_data["workspace_alias"],
            "hyperthoughtRootPath": job_data["hyperthought_root"],
            "ignorePathPrefix": job_data["ignore_path"],
        }

        # Create the files section.
        output_files = []
        folders = self.database.get_all_folders()

        for folder in folders:
            output_files.append({
                "id":  folder["hyperthought_id"],
                "path": folder["path"],
                "type": "folder",
                "size": None,
                "hash": None,
                "endBytes": None,
            })

        files = self.database.get_all_files()

        for file_ in files:
            end_bytes = [int(s) for s in file_["end_bytes"].split(",")]
            output_files.append({
                "id":  file_["hyperthought_id"],
                "path": file_["path"],
                "type": "file",
                "size": file_["size"],
                "hash": file_["file_hash"],
                "endBytes": end_bytes,
            })

        output["files"] = output_files

        # Create the metadata section.
        metadata_id_to_parsers = {}
        parsers = self.database.get_all_parsers()

        for parser in parsers:
            metadata_id = parser["metadata_id"]
            value = {
                "parserClass": parser["parser_class"],
                "parseFileId": parser["hyperthought_id"],
                "applyToFileIds": [],
            }
            metadata_id_to_parsers[metadata_id] = value

        # Map metadata id to file-specific metadata.
        metadata_id_to_specific = {}
        specified_metadata = self.database.get_all_metadata(file_specific=True)

        for metadata in specified_metadata:
            metadata_id = metadata["id"]
            value = {
                "metadata": metadata["metadata"],
                "applyToFileIds": [],
            }
            metadata_id_to_specific[metadata_id] = value

        metadata_applications = self.database.get_all_metadata_application()

        for metadata_application in metadata_applications:
            metadata_id = metadata_application["metadata_id"]
            file_id = metadata_application["hyperthought_id"]

            if metadata_id in metadata_id_to_parsers:
                metadata_id_to_parsers[metadata_id]["applyToFileIds"].append(
                    file_id)

            if metadata_id in metadata_id_to_specific:
                metadata_id_to_specific[metadata_id]["applyToFileIds"].append(
                    file_id)

        output["metadata"] = {
            "parsing": list(metadata_id_to_parsers.values()),
            "fileSpecific": list(metadata_id_to_specific.values()),
            "common": self.database.get_common_metadata(),
        }

        return output

    def get_file_page(self, start: int, length: int) -> List[Dict]:
        """
        Get a single page of file results.

        Parameters
        ----------
        start : int
            The start index for the page.
        length : int
            The page length.

        Returns
        -------
        List of dicts containing file information.
        """
        return self.database.get_file_page(start=start, length=length)

    def _compute_file_info_with_pool(
        self,
        n_processes: Optional[int] = None,
    ) -> None:
        """Compute file size, hash, and end bytes using a process pool."""
        if (
            n_processes is not None
            and
            not (isinstance(n_processes, int) and n_processes > 0)
        ):
            raise ValueError(
                "n_processes must be a positive integer if provided")

        if n_processes is None:
            n_processes = multiprocessing.cpu_count() * 2

        n_processes = min(n_processes, MAX_PROCESSES)
        files = self.database.get_all_files()
        pool = multiprocessing.Pool(processes=n_processes)
        all_updates = pool.map(_compute_size_hash_and_end_bytes, files)
        pool.close()
        pool.join()

        for updates in all_updates:
            id_ = updates.pop("id")
            self.database.update_file(id_=id_, updates=updates)

    def _compute_file_info_without_pool(self) -> None:
        """Compute file hashes and end bytes in the current process."""
        files = self.database.get_all_files()

        for file_ in files:
            updates = _compute_size_hash_and_end_bytes(file_=file_)
            id_ = updates.pop("id")
            self.database.update_file(id_=id_, updates=updates)

    def compute_file_info(
        self,
        use_pool: bool = True,
        n_processes: Optional[int] = None,
    ) -> None:
        """Compute hash and end_bytes for each file in the manifest."""
        if use_pool:
            self._compute_file_info_with_pool(n_processes=n_processes)
        else:
            self._compute_file_info_without_pool()

        self._file_info_computed = True

    def get_total_size(self) -> int:
        """Get the sum of file sizes for all files in the manifest."""
        return self.database.get_total_size()

    def get_metadata_application(
        self,
        metadata_id: int,
        filter_: MetadataApplicationFilter
    ) -> Generator[Dict, Optional[None], Optional[None]]:
        """
        Get ids for files to which metadata will be applied.

        Parameters
        ----------
        metadata_id : int
            Id of the Metadata record of interest.
        filter_ : MetadataApplicationFilter
            Enum instance used to specify filter for results.

        Yields
        ------
        Ids for files to which metadata will be applied.
        """
        generator = self.database.get_metadata_application(
            metadata_id=metadata_id,
            filter_=filter_,
        )

        for file_id in generator:
            yield file_id

    def close(self, compute_file_info: bool = True) -> None:
        """
        Close the manifest (database).

        Parameters
        ----------
        compute_file_info : bool
            If True, update file records to include sizes, hashes,
            and end bytes.
        """
        if compute_file_info and not self.file_info_computed:
            self.compute_file_info()

        self.database.connection.close()


def from_json(manifest_data: Dict, manifest_database_file: str) -> Manifest:
    """
    Create and return a manifest with the given (JSON) data.

    Convert JSON to SQLite and store in the specified database file.

    Parameters
    ----------
    manifest_data : dict
        In-memory JSON-formatted manifest data.
    manifest_database_file : str
        Path to the database file where the data will be stored.
        If the file already exists, it will be overwritten to contain the
        new data.

    Returns
    -------
    A Manifest object with a connection to the database file.
    The caller will be responsible for closing the connection via the `close`
    method.
    """
    # Create the Manifest object.
    manifest = Manifest(
        manifest_file=manifest_database_file,
        overwrite_manifest_file=True,
        job_name=manifest_data["job"]["name"],
        username=manifest_data["job"]["username"],
        workspace_alias=manifest_data["job"]["workspaceAlias"],
        ignore_path=manifest_data["job"]["ignorePathPrefix"],
        hyperthought_root=manifest_data["job"]["hyperthoughtRootPath"],
    )

    # Add files to the manifest.
    manifest_files = sorted(
        manifest_data["files"],
        key=lambda item: item["path"],
    )
    len_ignore_path = len(manifest.ignore_path) if manifest.ignore_path else 0
    path_to_hyperthought_id = {}
    manifest_id_to_hyperthought_id = {}
    file_data = []

    for manifest_file in manifest_files:
        path = utils.clean_path(manifest_file["path"])
        relative_path = path[len_ignore_path:].replace("\\", "/").strip("/")
        hyperthought_id = utils.generate_id()
        manifest_id_to_hyperthought_id[manifest_file["id"]] = hyperthought_id
        path_to_hyperthought_id[relative_path] = hyperthought_id
        is_folder = manifest_file["type"] == "folder"

        if not is_folder:
            end_bytes = ",".join(str(i) for i in manifest_file["endBytes"])
        else:
            end_bytes = None

        path_tokens = relative_path.split("/")
        hyperthought_id_path = manifest.hyperthought_root_id_path

        for index in range(0, len(path_tokens) - 1):
            parent_path = "/".join(path_tokens[:(index + 1)])

            if parent_path not in path_to_hyperthought_id:
                full_parent_path = f"{manifest.ignore_path}/{parent_path}"
                raise ValueError(f"missing parent path: {full_parent_path}")

            parent_id = path_to_hyperthought_id[parent_path]
            hyperthought_id_path = f"{hyperthought_id_path}{parent_id},"

        # TODO:  Add validation for manifest data:  size, hash.

        file_data.append({
            "name": os.path.basename(relative_path),
            "hyperthought_id": hyperthought_id,
            "hyperthought_id_path": hyperthought_id_path,
            "is_folder": is_folder,
            "path": path,
            "end_bytes": end_bytes,
            "size": manifest_file["size"],
            "file_hash": manifest_file["hash"],
        })

    manifest.database.bulk_load_files(file_data=file_data)
    ht_to_db_id = {
        item["hyperthought_id"]: item["id"]
        for item in file_data
    }
    manifest_id_to_database_id = {
        manifest_id: ht_to_db_id[manifest_id_to_hyperthought_id[manifest_id]]
        for manifest_id in manifest_id_to_hyperthought_id
    }

    # Add parsers to the manifest.
    for parser in manifest_data["metadata"]["parsing"]:
        file_id = manifest_id_to_database_id[parser["parseFileId"]]
        apply_to_file_ids = [
            manifest_id_to_database_id[id_] for id_ in parser["applyToFileIds"]
        ]
        manifest.add_parser(
            file_id=file_id,
            parser_class_name=parser["parserClass"],
            apply_to_file_ids=apply_to_file_ids,
        )

    # Add file-specific metadata.
    for metadata_item in manifest_data["metadata"]["fileSpecific"]:
        metadata = ht.metadata.from_api_format(
            metadata=metadata_item["metadata"])
        apply_to_file_ids = [
            manifest_id_to_database_id[id_]
            for id_ in metadata_item["applyToFileIds"]
        ]
        manifest.add_metadata(
            metadata=metadata,
            apply_to_file_ids=apply_to_file_ids,
        )

    # Add common metadata.
    manifest.common_metadata = ht.metadata.from_api_format(
        manifest_data["metadata"]["common"]
    )

    return manifest
