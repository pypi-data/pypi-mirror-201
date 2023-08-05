"""
Database functionality for a file transfer manifest.

An object of class Database is available via the `database` property of a
manifest object.
"""

from enum import Enum
from enum import IntEnum
import os
import sqlite3
from typing import Dict
from typing import Generator
from typing import List
from typing import Optional

import hyperthought as ht
from hyperthought.metadata import MetadataItem

from . import connect, template  # noqa: F401


class FileStatus(IntEnum):
    """Enum corresponding to status in FileStatus table."""

    PENDING = 1
    READY = 2
    HASH_MATCHES = 3
    MALWARE_FREE = 4
    UPLOADED = 5
    CREATED = 6
    NOT_READY = 7
    HASH_MISMATCH = 8
    MALWARE_DETECTED = 9
    UPLOAD_ERROR = 10
    CREATION_ERROR = 11
    UNKNOWN_ERROR = 12
    METADATA_UPDATE_ERROR = 13


class ParserStatus(IntEnum):
    """Enum corresponding to status in ParserStatus table."""

    PENDING = 1
    PARSED = 2
    PARSER_ERROR = 3


class MetadataApplicationFilter(Enum):
    """
    Enum used to filter results when getting metadata application records.
    """

    FILES_ONLY = 1
    FOLDERS_ONLY = 2
    FILES_AND_FOLDERS = 3


class Database:
    """
    Manager class an upload job embedded database.

    Parameters
    ----------
    connection : sqlite3.Connection
        A connection to the database of interest.

    Exceptions
    ----------
    A ValueError will be thrown if the db_connection parameter cannot be
    validated.
    """

    def __init__(self, connection: sqlite3.Connection) -> None:
        if not isinstance(connection, sqlite3.Connection):
            raise ValueError("db_connection must be a sqlite3 connection")

        self._connection = connection

    @property
    def connection(self):
        return self._connection

    def create_job_data(
        self,
        job_name: str,
        username: str,
        workspace_alias: str,
        ignore_path: Optional[str] = None,
        hyperthought_root: str = "/",
        commit: bool = True,
    ) -> None:
        """
        Create a record in the JobData table.

        By assumption, there should only be one such record.
        """
        sql = """
        INSERT INTO JobData (
            job_name,
            username,
            workspace_alias,
            ignore_path,
            hyperthought_root
        ) VALUES (
            :job_name,
            :username,
            :workspace_alias,
            :ignore_path,
            :hyperthought_root
        )
        """
        cursor = self.connection.cursor()
        cursor.execute(
            sql,
            {
                "job_name": job_name,
                "username": username,
                "workspace_alias": workspace_alias,
                "ignore_path": ignore_path,
                "hyperthought_root": hyperthought_root,
            },
        )

        if commit:
            self.connection.commit()

    def create_file(
        self,
        name: str,
        is_folder: bool,
        hyperthought_id: str,
        hyperthought_id_path: str,
        path: Optional[str] = None,
        end_bytes: Optional[List[int]] = None,
        size: Optional[int] = None,
        file_hash: Optional[str] = None,
        commit: bool = True,
    ) -> Optional[int]:
        """
        Create a file record in the database.

        Parameters
        ----------
        name : str
            Name of file or folder.
        is_folder : bool
            True iff the record in question is for a folder, not a file.
        hyperthought_id : str
            The id of the file/folder in HyperThought.  Specified prior to
            document creation.
        hyperthought_id_path : str
            Comma-separated list of parent folder ids in HyperThought.
            Corresponds to content.path in NoSQL database documents.
        path : str or None
            Local path to a file.  Not used for folders.
        end_bytes : list of int
            Comma-separated ints representing bytes found at the end of a file.
        size : int or None
            The expected size of the file.  Required of files, not folders.
        file_hash : str or None
            The hash for the file.  Required of files, not folders.
        commit : bool
            Determines whether changes will be committed to the database.
            This may be false if the changes are part of a transaction.

        Returns
        -------
        The id for the file.

        Exceptions
        ----------
        -   ValueErrors will be thrown if the parameters cannot be validated.
        -   An IntegrityError will be thrown if the insert query violates
            integrity constraints.  (This may happen if a record already exists
            for the path, due to a uniqueness constraint.)
        """
        if not is_folder and (not isinstance(size, int) or size < 0):
            raise ValueError("size for a file must be a non-negative integer")

        if end_bytes is not None and not isinstance(end_bytes, str):
            raise ValueError("end_bytes must be a string if provided")

        if end_bytes is not None:
            valid_chars = set("0123456789,")
            invalid_chars = set(end_bytes) - valid_chars

            if invalid_chars:
                raise ValueError(
                    f"Invalid chars in end_bytes: {invalid_chars}")

        # Define and execute the relevant SQL statement.
        sql = """
        INSERT INTO File (
            name,
            hyperthought_id,
            hyperthought_id_path,
            is_folder,
            path,
            end_bytes,
            size,
            file_hash
        )
        VALUES (
            :name,
            :hyperthought_id,
            :hyperthought_id_path,
            :is_folder,
            :path,
            :end_bytes,
            :size,
            :file_hash
        )
        """
        cursor = self.connection.cursor()

        cursor.execute(
            sql,
            {
                "name": name,
                "hyperthought_id": hyperthought_id,
                "hyperthought_id_path": hyperthought_id_path,
                "is_folder": is_folder,
                "path": path,
                "end_bytes": end_bytes,
                "size": size,
                "file_hash": file_hash,
            },
        )
        file_id = cursor.lastrowid

        if commit:
            self.connection.commit()

        return file_id

    def delete_file(self, file_id: int, commit: bool = True) -> None:
        """
        Remove a file record from the database.

        Parameters
        ----------
        file_id : int
            The id of the file to be deleted.
        commit : bool
            Determines whether changes will be committed to the database.
            This may be false if the changes are part of a transaction.
        """
        cursor = self.connection.cursor()
        sql = "DELETE FROM File WHERE id = :id"
        cursor.execute(sql, {"id": file_id})

        if commit:
            self.connection.commit()

    def get_total_size(self) -> int:
        """Get the sum of file sizes for all files in the manifest."""
        sql = """
        SELECT SUM(size) AS total_bytes
        FROM File
        WHERE size IS NOT NULL
        """
        cursor = self.connection.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        return row["total_bytes"]

    def create_parser(
        self,
        file_id: int,
        parser_class: str,
        metadata_id: int,
        commit: bool = True,
    ) -> Optional[int]:
        """
        Create a Parser record.

        A Parser record associates a parser class (class name) with a file
        to be parsed.

        Parameters
        ----------
        file_id : int
            The id of the file to be parsed.
        parser_class : str
            The name of a parser class, as defined in the hyperthought package.
        metadata_id : int
            id of the Metadata record that will store the parsed metadata.
        commit : bool
            Determines whether changes will be committed to the database.
            This may be false if the changes are part of a transaction.

        Returns
        -------
        The id for the parser.

        Exceptions
        ----------
        -   ValueErrors will be thrown if the parameters cannot be validated.
        -   An IntegrityError will be thrown if the insert query violates
            integrity constraints.  (This may happen if a record already exists
            for a parser/file combination, due to a uniqueness constraint.)
        """
        if parser_class not in ht.parsers.PARSERS:
            raise ValueError(f"'{parser_class}' is not a valid parser class")

        sql = """
        INSERT INTO Parser (file_id, parser_class, metadata_id)
        VALUES (:file_id, :parser_class, :metadata_id)
        """
        cursor = self.connection.cursor()
        cursor.execute(
            sql,
            {
                "file_id": file_id,
                "parser_class": parser_class,
                "metadata_id": metadata_id,
            },
        )
        parser_id = cursor.lastrowid

        if commit:
            self.connection.commit()

        return parser_id

    def create_metadata(
        self,
        metadata: Optional[List[MetadataItem]] = None,
        commit: bool = True,
    ) -> Optional[int]:
        """
        Create a Metadata record.

        Store metadata, whether specified directly or parsed from a file,
        in a Metadata table record.

        Parameters
        ----------
        metadata : list of hyperthought.metadata.MetadataItem or None
            A list of metadata items, in hyperthought package object format.
            The metadata will be converted to the API format before being
            stored in the table, since the METADATA type added to the database
            uses JSON serialization.
            If None, the metadata will be added later when a file is parsed.
        commit : bool
            Determines whether changes will be committed to the database.
            This may be false if the changes are part of a transaction.

        Returns
        -------
        The id of the Metadata record created.

        Exceptions
        ----------
        -   A ValueError will be thrown if the metadata is not valid.
        """
        if metadata is None:
            api_metadata = None
        else:
            if not isinstance(metadata, list):
                raise ValueError("metadata must be a list if not None")

            for item in metadata:
                if not isinstance(item, ht.metadata.MetadataItem):
                    raise ValueError(
                        "all metadata items must be instances of MetadataItem"
                    )

            api_metadata = ht.metadata.to_api_format(metadata=metadata)

        sql = "INSERT INTO Metadata (metadata) VALUES (:metadata)"
        cursor = self.connection.cursor()
        cursor.execute(sql, {"metadata": api_metadata})
        metadata_id = cursor.lastrowid

        if commit:
            self.connection.commit()

        return metadata_id

    def create_or_update_common_metadata(
        self,
        metadata: List[MetadataItem],
        commit: bool = True,
    ) -> None:
        """
        Add a row to the common metadata table.

        Parameters
        ----------
        metadata : list of hyperthought.metadata.MetadataItem
            Metadata to be added as common metadata.
        """
        if not metadata:
            return

        if not isinstance(metadata, list):
            raise ValueError("metadata must be a list if not None")

        for item in metadata:
            if not isinstance(item, ht.metadata.MetadataItem):
                raise ValueError(
                    "all metadata items must be instances of MetadataItem")

        api_metadata = ht.metadata.to_api_format(metadata=metadata)
        cursor = self.connection.cursor()

        # Remove previously created common metadata, if any.
        sql = "DELETE FROM CommonMetadata"
        cursor.execute(sql)

        # Add common metadata.
        sql = "INSERT INTO CommonMetadata (metadata) VALUES (:metadata)"
        cursor.execute(sql, {"metadata": api_metadata})

        if commit:
            self.connection.commit()

    def create_metadata_application(
        self,
        metadata_id: int,
        file_id: int,
        commit: bool = True,
    ) -> Optional[int]:
        """
        Create a MetadataApplication record to associate metadata with a file.

        Parameters
        ----------
        metadata_id : int
            The id of a record in the Metadata table.
        file_id : int
            The id of a file to which the metadata should be added.
        commit : bool
            Determines whether changes will be committed to the database.
            This may be false if the changes are part of a transaction.

        Returns
        -------
        The id of the MetadataApplication record.

        Exceptions
        ----------
        -   An IntegrityError will be thrown if the insert query violates
            integrity constraints.  (This may happen if a record already exists
            for the metadata/file combination, due to a uniqueness constraint.)
        """
        sql = """
        INSERT INTO MetadataApplication (metadata_id, file_id)
        VALUES (:metadata_id, :file_id)
        """
        cursor = self.connection.cursor()
        cursor.execute(
            sql,
            {
                "metadata_id": metadata_id,
                "file_id": file_id,
            },
        )
        metadata_application_id = cursor.lastrowid

        if commit:
            self.connection.commit()

        return metadata_application_id

    def get_job_data(self) -> Optional[Dict]:
        """Get job data from the JobData table."""
        cursor = self.connection.cursor()
        sql = "SELECT * FROM JobData"
        cursor.execute(sql)
        row = cursor.fetchone()

        if row is None:
            return None

        return {key: row[key] for key in row.keys()}

    def get_common_metadata(self) -> List[Dict]:
        """Get common metadata."""
        cursor = self.connection.cursor()
        sql = "SELECT metadata FROM CommonMetadata"
        cursor.execute(sql)
        row = cursor.fetchone()

        if row is None:
            return []

        return row["metadata"]

    def get_parser_count(self) -> int:
        """
        Count the number of Parser records.

        This is also the number of parsing operations.
        """
        cursor = self.connection.cursor()
        sql = "SELECT COUNT(*) AS parser_count FROM Parser"
        cursor.execute(sql)
        return cursor.fetchone()["parser_count"]

    def get_parsers_for_file(self, file_id: int) -> List[Dict]:
        """
        Get all parsers to be applied to a specified file.

        Parameters
        ----------
        file_id : int
            The id of the file of interest.

        Returns
        -------
        A list of dicts containing data from the Parser table.
        """
        cursor = self.connection.cursor()
        sql = "SELECT * FROM Parser WHERE file_id = :file_id"
        cursor.execute(sql, {"file_id": file_id})
        return [
            {
                key: row[key]
                for key in row.keys()
            }
            for row in cursor.fetchall()
        ]

    def get_all_folders(self) -> List[Dict]:
        """
        Get all folders in the job.

        Returns
        -------
        A list of dicts containing information on all folders in the job.
        """
        # TODO:  Use generator.
        cursor = self.connection.cursor()
        sql = "SELECT * FROM File WHERE is_folder"
        cursor.execute(sql)
        return [
            {
                key: row[key]
                for key in row.keys()
            }
            for row in cursor.fetchall()
        ]

    def get_all_files(self) -> List[Dict]:
        """
        Get all files in the job.

        Returns
        -------
        A list of dicts containing information on all files in the job.
        """
        # TODO:  Use generator.
        cursor = self.connection.cursor()
        sql = "SELECT * FROM File WHERE NOT is_folder"
        cursor.execute(sql)
        return [
            {
                key: row[key]
                for key in row.keys()
            }
            for row in cursor.fetchall()
        ]

    def get_file_id(self, path: str) -> Optional[int]:
        """Get an id for a File record given a path."""
        cursor = self.connection.cursor()
        sql = """
        SELECT id
        FROM File
        WHERE path = :path
        """
        cursor.execute(sql, {"path": path})
        row = cursor.fetchone()

        if row is None:
            return None

        return row["id"]

    def get_all_file_metadata(self, file_id: int) -> List[Dict]:
        """
        Get all metadata to be added to a file in HyperThought.

        Get all metadata using MetadataApplication records as a lookup for
        Metadata records.

        Parameters
        ----------
        file_id : int
            The database id for the file of interest.

        Returns
        -------
        Aggregated API-formatted metadata from all sources.
        """
        all_metadata = []
        sql = """
            SELECT metadata FROM CommonMetadata
            UNION
            SELECT metadata
            FROM MetadataApplication INNER JOIN Metadata
                ON MetadataApplication.metadata_id = Metadata.id
            WHERE MetadataApplication.file_id = :file_id
            """
        cursor = self.connection.cursor()
        cursor.execute(sql, {"file_id": file_id})

        for row in cursor.fetchall():
            metadata = row["metadata"]

            if metadata:
                all_metadata.extend(row["metadata"])

        return all_metadata

    def get_file(
        self,
        file_id: Optional[int] = None,
        name: Optional[str] = None,
        hyperthought_id_path: Optional[str] = None,
    ) -> Optional[Dict]:
        """
        Get a file/folder record given identifying information.

        Parameters
        ----------
        file_id : int or None
            The database id for the file/folder.
        name: str or None
            The name of the file/folder.
        hyperthought_id_path: str or None
            Comma-separated parent folder ids, e.g. ",uuid,uuid,uuid,".

        Either file_id or name and hyperthought_id must be provided.
        """
        if file_id is None and (name is None or hyperthought_id_path) is None:
            raise ValueError(
                "file_id or name and hyperthought_id_path must be provided")

        cursor = self.connection.cursor()

        if file_id:
            sql = "SELECT * FROM File WHERE id = :file_id"
            cursor.execute(sql, {"file_id": file_id})
        else:
            sql = """
            SELECT *
            FROM File
            WHERE
                name = :name
                AND
                hyperthought_id_path = :hyperthought_id_path
            """
            cursor.execute(sql, {
                "name": name,
                "hyperthought_id_path": hyperthought_id_path,
            })

        row = cursor.fetchone()

        if not row:
            return None

        return {key: row[key] for key in row.keys()}

    def get_files(
        self,
        file_ids: Optional[List[int]] = None,
        paths: Optional[List[str]] = None
    ) -> Generator[Dict, Optional[None], Optional[None]]:
        """
        Get all file records corresponding a list of ids or paths.

        Parameters
        ----------
        file_ids : list of int
            Database ids for the files of interest.
        paths : list of str
            Paths for files of interest.
            Must be provided if file_ids is not.

        Returns
        -------
        A list of dicts containing file record data.
        """
        if not file_ids and not paths:
            raise ValueError("file_ids or paths must be provided")

        if file_ids:
            sql = "SELECT * FROM File WHERE id IN ("
            items = file_ids
        else:
            sql = "SELECT * FROM File WHERE path IN ("
            items = paths

        params = {}
        key_index = 0

        for item in items:
            key = f"item_{key_index}"
            key_index += 1
            sql += f":{key}, "
            params[key] = item

        sql = sql[:-2] + ")"  # Remove trailing ", " and close parenthesis.
        cursor = self.connection.cursor()
        cursor.execute(sql, params)

        for row in cursor.fetchall():
            yield {
                key: row[key]
                for key in row.keys()
            }

        cursor.close()

    def get_all_metadata_application(self) -> Generator[Dict, Optional[None], Optional[None]]:  # noqa: E501
        """Get all MetadataApplication records."""
        cursor = self.connection.cursor()
        sql = """
        SELECT
            MetadataApplication.*,
            File.hyperthought_id
        FROM
            MetadataApplication INNER JOIN File
                ON MetadataApplication.file_id = File.id
        """
        cursor.execute(sql)

        for row in cursor.fetchall():
            yield {
                key: row[key]
                for key in row.keys()
            }

    def get_all_parsers(self) -> Generator[Dict, Optional[None], Optional[None]]:  # noqa: 501
        """Get all Parser records."""
        cursor = self.connection.cursor()
        sql = """
        SELECT
            Parser.*,
            File.hyperthought_id
        FROM
            Parser INNER JOIN File
                ON Parser.file_id = File.id
        """
        cursor.execute(sql)

        for row in cursor.fetchall():
            yield {
                key: row[key]
                for key in row.keys()
            }

    def get_all_metadata(self, file_specific: bool = True) -> Generator[Dict, Optional[None], Optional[None]]:  # noqa: 501
        """
        Get all Metadata records.

        Parameters
        ----------
        file_specific : bool
            If true, filter results to include only those records with
            no corresponding Parser record.
        """
        cursor = self.connection.cursor()

        if file_specific:
            sql = """
            SELECT Metadata.*
            FROM Metadata LEFT JOIN Parser
                ON Metadata.id = Parser.metadata_id
            WHERE Parser.id IS NULL
            """
        else:
            sql = "SELECT * FROM Metadata"

        cursor.execute(sql)

        for row in cursor.fetchall():
            yield {
                key: row[key]
                for key in row.keys()
            }

    def _update(
        self,
        table: str,
        id_: int,
        updates: Dict,
        commit: bool = True,
    ) -> None:
        """
        Convenience function used to update a record.

        The caller will be responsible for ensuring that keys in the updates
        dict correspond to attributes in the table.
        """
        valid_tables = (
            "File",
            "Parser",
            "Metadata",
        )

        if table not in valid_tables:
            raise ValueError(f"Invalid table: {table}")

        sql = f"UPDATE {table} "

        set_statements = []
        params = {}

        for key in updates:
            set_statements.append(f"{key} = :{key}")
            params[key] = updates[key]

        sql += "SET " + ",".join(set_statements) + " WHERE id = :id"
        params["id"] = id_

        cursor = self.connection.cursor()
        cursor.execute(sql, params)

        if commit:
            self.connection.commit()

    def update_file(
        self,
        id_: int,
        updates: Dict,
        commit: bool = True,
    ) -> None:
        """
        Update a file record.

        Parameters
        ----------
        id_ : int
            id of the file to be updated.
        updates : dict
            Updates to be committed to the database.
            Keys must correspond to File table attributes.
        commit : bool
            Determines whether changes will be committed to the database.
            This may be false if the changes are part of a transaction.
        """
        self._update(table="File", id_=id_, updates=updates, commit=commit)

    def reset_file_statuses(
        self,
        existing_statuses: List[FileStatus],
        new_status: FileStatus,
        commit: bool = True,
    ) -> None:
        """
        Reset file statuses to a new value.

        All file records having one of the specified existing statuses
        will have their status changed to the new status.

        Parameters
        ----------
        existing_statuses : list of FileStatus
            The file statuses to be changed.
        new_status : FileStatus
            The status to which all file records with one of the existing
            statuses will be changed.
        commit : bool
            Determines whether changes will be committed to the database.
            This may be false if the changes are part of a transaction.
        """
        status_map = {
            f"status{i:02}": existing_statuses[i].value
            for i in range(len(existing_statuses))
        }

        sql = """
            UPDATE File
            SET file_status_id = :new_status_id
            WHERE
                file_status_id IN (
            """

        for key in status_map:
            sql += f":{key}, "

        # Remove comma + space and add closing parenthesis.
        sql = sql[:-2] + ")"

        status_map["new_status_id"] = new_status.value
        cursor = self.connection.cursor()
        cursor.execute(sql, status_map)

        if commit:
            self.connection.commit()

    def get_parser(self, parser_id: int) -> Optional[Dict]:
        """Get a parser record data given a parser id."""
        sql = "SELECT * FROM Parser WHERE id = :parser_id"
        cursor = self.connection.cursor()
        cursor.execute(sql, {"parser_id": parser_id})
        row = cursor.fetchone()

        if not row:
            return None

        return {key: row[key] for key in row.keys()}

    def get_progeny(self, folder_path: str) -> List[Dict]:
        """Get all children of a given folder that are in the manifest."""
        cursor = self.connection.cursor()
        sql = "SELECT * FROM File WHERE path LIKE :path_pattern"
        path_pattern = f"{folder_path.rstrip(os.path.sep)}{os.path.sep}%"
        cursor.execute(sql, {"path_pattern": path_pattern})
        return [
            {
                key: row[key]
                for key in row.keys()
            }
            for row in cursor.fetchall()
        ]

    def update_parser(
        self,
        id_: int,
        updates: Dict,
        commit: bool = True,
    ) -> None:
        """
        Update a parser record.

        Parameters
        ----------
        id_ : int
            id of the parser to be updated.
        updates : dict
            Updates to be committed to the database.
            Keys must correspond to Parser table attributes.
        commit : bool
            Determines whether changes will be committed to the database.
            This may be false if the changes are part of a transaction.
        """
        self._update(table="Parser", id_=id_, updates=updates, commit=commit)

    def get_metadata(self, metadata_id: int) -> Optional[Dict]:
        """Get a metadata record from a metadata id."""
        sql = "SELECT * FROM Metadata WHERE id = :metadata_id"
        cursor = self.connection.cursor()
        cursor.execute(sql, {"metadata_id": metadata_id})
        row = cursor.fetchone()

        if not row:
            return None

        return {key: row[key] for key in row.keys()}

    def update_metadata(
        self,
        id_: int,
        updates: Dict,
        commit: bool = True,
    ) -> None:
        """
        Update a metadata record.

        Parameters
        ----------
        id_ : int
            id of the metadata record to be updated.
        updates : dict
            Updates to be committed to the database.
            Keys must correspond to Metadata table attributes.
        commit : bool
            Determines whether changes will be committed to the database.
            This may be false if the changes are part of a transaction.
        """
        self._update(table="Metadata", id_=id_, updates=updates, commit=commit)

    def bulk_load_files(
        self,
        file_data: List[Dict],
        commit: bool = True,
    ) -> None:
        """
        Bulk load files in the database.

        Parameters
        ----------
        file_data : list of dicts
            Data on the files to be loaded.
            Keys in each dict must include the following:
                name : str
                    The name of the file or folder.
                hyperthought_id : str
                    The id of the file/folder in HyperThought.
                    (Specified prior to document creation.)
                hyperthought_id_path : str
                    Comma-separated list of parent folder ids in HyperThought.
                    Corresponds to content.path in NoSQL database documents.
                is_folder : bool
                    True iff the record in question is for a folder,
                    not a file.
                path : str
                    Local path to the file or folder.
                    Can be None (for folders that don't exist locally).
                end_bytes : str or None
                    Comma-separated ints representing bytes found at the end
                    of a file.
                size : int or None
                    The expected size of the file.
                    Required of files, not folders.
                file_hash : str or None
                    The hash for the file.  Required of files, not folders.
        commit : bool
            Determines whether changes will be committed to the database.
            This may be false if the changes are part of a transaction.
        """
        cursor = self.connection.cursor()
        next_id = self.get_last_id(table="File") + 1
        required_keys = {
            "name",
            "hyperthought_id",
            "hyperthought_id_path",
            "is_folder",
            "path",
            "end_bytes",
            "size",
            "file_hash",
        }

        for item in file_data:
            if not isinstance(item, dict):
                raise ValueError("All elements of file_data must be dicts.")

            keys = set(item.keys())
            missing_keys = required_keys - keys

            if missing_keys:
                raise ValueError(
                    f"Element in file_data missing keys: {missing_keys}")

            item["id"] = next_id
            next_id += 1

        sql = """
            INSERT INTO File (
                name,
                hyperthought_id,
                hyperthought_id_path,
                is_folder,
                path,
                end_bytes,
                size,
                file_hash
            ) VALUES (
                :name,
                :hyperthought_id,
                :hyperthought_id_path,
                :is_folder,
                :path,
                :end_bytes,
                :size,
                :file_hash
            )
            """
        cursor.executemany(sql, file_data)

        if commit:
            self.connection.commit()

    def bulk_load_parsers(
        self,
        parser_data: List[Dict],
        commit: bool = True,
    ) -> None:
        """
        Bulk load parsers into the database. Will add a database_id in place to
        parser_data entries.

        ids for the parsers will be added to parser_data in place.

        Parameters
        ----------
        parser_data : list of dict
            Consists of metadata parsers for files to be uploaded. Each parser
            entry should contain the following keys:
                file_id : int
                    Foreign key id of the file the parser is associated with.
                parser_class : string
                    Class of the parser.
                metadata_id : int
                    Foreign key id of the metadata associated with the parser.
        commit : bool
            Determines whether changes will be committed to the database.
            This may be false if the changes are part of a transaction.
        """
        cursor = self.connection.cursor()
        next_id = self.get_last_id(table="Parser") + 1
        required_keys = {
            "file_id",
            "parser_class",
            "metadata_id",
        }

        for item in parser_data:
            if not isinstance(item, dict):
                raise ValueError("All elements of parser_data must be dicts.")

            keys = set(item.keys())
            missing_keys = required_keys - keys

            if missing_keys:
                raise ValueError(
                    f"Element in parser_data missing keys: {missing_keys}")

            item["id"] = next_id
            next_id += 1

        sql = """
            INSERT INTO Parser (
                id,
                file_id,
                parser_class,
                metadata_id
            ) VALUES (
                :id,
                :file_id,
                :parser_class,
                :metadata_id
            )
        """
        cursor.executemany(sql, parser_data)

        if commit:
            self.connection.commit()

    def bulk_load_metadata(
        self,
        metadata_data: List[Dict],
        commit: bool = True,
    ) -> None:
        """
        Bulk load metadata into the database. Will add a database_id in place
        to metadata_data entries.

        ids for the new records will be added to metadata_data in place.

        Parameters
        ----------
        metadata_data : list of dict
            contains metadata entries with the following keys to be committed
            to the database:
                metadata : list of dicts or None
                    API-formatted metadata
        commit : bool
            Determines whether changes will be committed to the database.
            This may be false if the changes are part of a transaction.
        """
        cursor = self.connection.cursor()
        next_id = self.get_last_id(table="Metadata") + 1
        required_keys = {
            "metadata",
        }

        for item in metadata_data:
            if not isinstance(item, dict):
                raise ValueError(
                    "All elements of metadata_data must be dicts.")

            keys = set(item.keys())
            missing_keys = required_keys - keys

            if missing_keys:
                raise ValueError(
                    f"Element in metadata_data missing keys: {missing_keys}"
                )

            item["id"] = next_id
            next_id += 1

        sql = """
            INSERT INTO Metadata (
                id,
                metadata
            ) VALUES (
                :id,
                :metadata
            )
            """
        cursor.executemany(sql, metadata_data)

        if commit:
            self.connection.commit()

    def bulk_load_metadata_application(
        self,
        metadata_application_data: List[Dict],
        commit: bool = True,
    ) -> None:
        """
        Bulk load MetadataApplication data into the database.
        metadata_application_data entries will have a database_id added to them
        in place.

        ids for the new records will be added to metadata_application_data
        in place.

        Parameters
        ----------
        metadata_application_data : list
            contains MetadataApplication entries with the following keys to be
            committed to the database:
                metadata_id : int
                    id of record in Metadata table.
                file_id : int
                    id of record in File table.
        commit : bool
            Determines whether changes will be committed to the database.
            This may be false if the changes are part of a transaction.
        """
        cursor = self.connection.cursor()
        next_id = self.get_last_id(table="MetadataApplication") + 1
        required_keys = {
            "metadata_id",
            "file_id",
        }

        for item in metadata_application_data:
            if not isinstance(item, dict):
                raise ValueError(
                    "All elements of metadata_application_data must be dicts."
                )

            keys = set(item.keys())
            missing_keys = required_keys - keys

            if missing_keys:
                raise ValueError(
                    "Element in metadata_application_data missing keys: "
                    f"{missing_keys}"
                )

            item["id"] = next_id
            next_id += 1

        sql = """
            INSERT INTO MetadataApplication (
                id,
                metadata_id,
                file_id
            ) VALUES (
                :id,
                :metadata_id,
                :file_id
            )
        """
        cursor.executemany(sql, metadata_application_data)

        if commit:
            self.connection.commit()

    def get_last_id(self, table: str) -> int:
        """Get the last id in a table."""
        valid_tables = {"Parser", "Metadata", "MetadataApplication", "File"}

        if table not in valid_tables:
            raise ValueError(f"Invalid table: {table}")

        sql = f"SELECT MAX(id) AS last_id FROM {table}"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        last_id = result["last_id"]

        if last_id is None:
            last_id = 0

        return last_id

    def get_file_count(self, include_root_folders: bool = False) -> int:
        """Get number of files in the database."""
        cursor = self.connection.cursor()

        if include_root_folders:
            sql = "SELECT COUNT(*) AS file_count FROM File"
        else:
            # As of 2/15/2023, a File record corresponds to a HyperThought
            # root folder iff its path is null.
            sql = """
            SELECT COUNT(*) AS file_count
            FROM File
            WHERE path IS NOT NULL
            """

        cursor.execute(sql)
        result = cursor.fetchone()
        return result["file_count"]

    def update_folder_hyperthought_id(
        self,
        old_id: str,
        new_id: str,
        commit: bool = True,
    ) -> None:
        """
        Update database when an existing folder is found in HyperThought.

        Change the id of the folder record, as well as id paths for all
        progeny.

        Parameters
        ----------
        old_id : str
            The id of the folder according to the database.
        new_id : str
            The id of the folder in HyperThought.
        commit : bool
            Determines whether changes will be committed to the database.
            This may be false if the changes are part of a transaction.
        """
        cursor = self.connection.cursor()

        # Get the folder record.
        sql = "SELECT * FROM File WHERE hyperthought_id = :old_id"
        cursor.execute(sql, {"old_id": old_id})
        folder = cursor.fetchone()

        if not folder:
            return

        # Reset id for folder record.
        updates = {"hyperthought_id": new_id}
        self.update_file(id_=folder["id"], updates=updates, commit=commit)

        # Reset id paths for progeny.
        parent_path = folder["hyperthought_id_path"]
        old_id_path = f"{parent_path}{old_id},"
        new_id_path = f"{parent_path}{new_id},"
        sql = """
        UPDATE File
        SET hyperthought_id_path = REPLACE(
            hyperthought_id_path, :old_id_path, :new_id_path)
        WHERE hyperthought_id_path LIKE :pattern
        """
        cursor.execute(sql, {
            "old_id_path": old_id_path,
            "new_id_path": new_id_path,
            "pattern": f"{old_id_path}%"
        })

        if commit:
            self.connection.commit()

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
            Specify filter for results.

        Yields
        ------
        Ids for files to which metadata will be applied.
        """
        if filter_ == MetadataApplicationFilter.FILES_ONLY:
            sql = """
            SELECT
                MetadataApplication.file_id
            FROM
                Metadata
                INNER JOIN MetadataApplication
                    ON Metadata.id = MetadataApplication.metadata_id
                INNER JOIN File
                    ON MetadataApplication.file_id = File.id
            WHERE
                Metadata.id = :metadata_id
                AND
                NOT File.is_folder
            """
        elif filter_ == MetadataApplicationFilter.FOLDERS_ONLY:
            sql = """
            SELECT
                MetadataApplication.file_id
            FROM
                Metadata
                INNER JOIN MetadataApplication
                    ON Metadata.id = MetadataApplication.metadata_id
                INNER JOIN File
                    ON MetadataApplication.file_id = File.id
            WHERE
                Metadata.id = :metadata_id
                AND
                File.is_folder
            """
        else:
            sql = """
            SELECT
                MetadataApplication.file_id
            FROM
                Metadata
                INNER JOIN MetadataApplication
                    ON Metadata.id = MetadataApplication.metadata_id
            WHERE
                Metadata.id = :metadata_id
            """

        cursor = self._connection.cursor()
        cursor.execute(sql, {"metadata_id": metadata_id})

        for row in cursor.fetchall():
            yield row["file_id"]

        cursor.close()

    def has_connectivity_errors(self) -> bool:
        """Determine whether connectivity errors occurred."""
        sql = """
        SELECT COUNT(*) AS error_count
        FROM File
        WHERE file_status_id IN (
            :upload_error_status_id,
            :creation_error_status_id,
            :metadata_update_error_status_id
        )
        """
        cursor = self.connection.cursor()
        cursor.execute(
            sql,
            {
                "upload_error_status_id": FileStatus.UPLOAD_ERROR.value,
                "creation_error_status_id": FileStatus.CREATION_ERROR.value,
                "metadata_update_error_status_id": (
                    FileStatus.METADATA_UPDATE_ERROR.value),
            },
        )
        row = cursor.fetchone()
        return bool(row["error_count"])

    def has_other_errors(self) -> bool:
        """Determine whether any non-connectivity errors occurred."""
        sql = """
        SELECT COUNT(*) AS error_count
        FROM File
        WHERE file_status_id IN (
            :hash_mismatch_status_id,
            :malware_detected_status_id,
            :other_error_status_id
        )
        """
        cursor = self.connection.cursor()
        cursor.execute(
            sql,
            {
                "hash_mismatch_status_id": FileStatus.HASH_MISMATCH.value,
                "malware_detected_status_id": (
                    FileStatus.MALWARE_DETECTED.value),
                "other_error_status_id": FileStatus.UNKNOWN_ERROR.value,
            },
        )
        row = cursor.fetchone()
        return bool(row["error_count"])

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
        # Start by getting results of interest from the database.
        sql = """
        SELECT
            File.id,
            File.path,
            File.size,
            FileStatus.status,
            File.is_folder
        FROM
            File
            INNER JOIN FileStatus ON File.file_status_id = FileStatus.id
        WHERE
            File.path IS NOT NULL
        LIMIT
            :start, :length
        """
        cursor = self.connection.cursor()
        cursor.execute(sql, {
            "start": start,
            "length":length,
        })
        file_records = [
            {
                key: row[key]
                for key in row.keys()
            }
            for row in cursor.fetchall()
        ]
        cursor.close()

        # Next, transform the records so they contain data needed for the files
        # list view.
        job_data = self.get_job_data()
        ignore_path = job_data["ignore_path"]
        len_ignore_path = len(ignore_path)
        hyperthought_root = job_data["hyperthought_root"].rstrip("/")

        def get_hyperthought_path(file_record):
            relative_path = (
                file_record["path"][len_ignore_path:]
                .replace("\\", "/")
                .lstrip("/")
            )
            return f"{hyperthought_root}/{relative_path}"

        def get_type(file_record):
            if file_record["is_folder"]:
                return "Folder"

            extension = os.path.splitext(file_record["path"])[-1].strip(".")
            return extension

        def transform_record(file_record):
            return {
                "id": file_record["id"],
                "local_path": file_record["path"],
                "hyperthought_path": get_hyperthought_path(file_record),
                "type": get_type(file_record),
                "status": file_record["status"],
            }

        file_page = [
            transform_record(file_record)
            for file_record in file_records
        ]


        # Return the result.
        return file_page
