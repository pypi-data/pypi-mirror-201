from qb_errors import *
from quickbase import QuickbaseClient
from typing import Any

class JsonQuickbaseClient(QuickbaseClient):
    headers: dict[str, str] | None = ...

    def __init__(self, credentials: dict[str, str] | None = None, timeout: int | None = None, **kwargs: Any) -> None: 
        """
        Client for Quickbase JSON API
        :param credentials: (dict or None) a dictionary of credentials (default: None) 
            username (optional)
            password (optional)
            realmhost (optional)
            base_url (required)
            user_token (required)
        :param timeout: The number of seconds to wait before timing out a request
        :param kwargs: Additional keyword arguments (used if credentials is None)
        """
        ...
    def nest(self, data_list: list[dict[str, Any]]) ->  list[dict[str, Any]]:
        """
        Takes a list of dictionaries and nests the values in a dictionary with a 'value' key.
        This is necessary for Quickbase to accept the data.
        :param data_list: (list of dict) your list of record data
        :return: (list of dict) your list of record data
        """
        ...
    def denest(self, data_list: list[dict[str, Any]]) ->  list[dict[str, Any]]: 
        """
        Takes a list of dictionaries and removes the 'value' key from the values.
        :param data_list: (list of dict) your list of record data
        :return: (list of dict) your list of record data
        """
        ...
    def none_to_0(self, data_list: list[dict[str, Any]]) ->  list[dict[str, Any]]: 
        """
        Takes a list of dictionaries and replaces None values with 0.
        :param data_list: (list of dict) your list of record data
        :return: (list of dict) your list of record data
        """
        ...
    def round_ints(self, data_list: list[dict[str, Any]]) ->  list[dict[str, Any]]: 
        """
        Takes a list of dictionaries and rounds all float values that are actually integers.
        :param data_list: (list of dict) your list of record data
        :return: (list of dict) your list of record data
        """
        ...
    def get_schema(self, database: str | None = None, include_permissions: bool = False) -> list[dict[str, Any]]: 
        """
        Get the schema of a Quickbase table.
        :param database: (str or None) Quickbase Table ID (default None, uses self.database)
        :param include_permissions: (bool) Whether to include permissions in the schema (default False)
        :return: (list of dict) your list of record data
        """
        ...
    def get_primary_key(self, database: str | None = None) -> str: 
        """
        Get the primary key of a Quickbase table.
        :param database: (str or None) Quickbase Table ID (default None, uses self.database)
        :return: (str) the primary key field ID
        """
        ...
    def do_query(self, query: str | None = None, qid: int | None = None, columns: list[str | int] | None = None, sort: list[str | int] | None = None, 
                 num: int | None = None, skip: int | None = None, ascending: bool = True, database: str | None = None, round_ints: bool = True, 
                 require_all: bool = False) -> list[dict[str, Any]]: 
        """
        Query a Quickbase table.
        :param query: (str or None) Quickbase query string (default None)
        :param qid: (int or None) Quickbase report ID (default None)
        :param columns: (None or list of str or int) List of column IDs to return (default None)
        :param sort: (None or list of str or int) List of column IDs to sort by (default None)
        :param num: (int or None) Max number of records to return (default None)
        :param skip: (int or None) Number of records to skip (default None)
        :param ascending: (bool) Whether to sort ascending (default True)
        :param database: (str or None) Quickbase Table ID (default None, uses self.database)
        :param round_ints: (bool) Whether to round integers (default True)
        :param require_all: (bool) Whether to require all records be returned (default False, risk of performance issues if True - USES MULTPLE API CALLS)
        :return: (list of dict) your list of record data
        """
        ...
    def add_record(self, fields: dict[str, Any], database: str | None = None, uploads: list[dict[str, str | bytes]] | None = None, 
                   safemode: bool = False, return_fields: list[str | int] | None = None) -> int | dict[str, Any]: 
        """
        Add a record to a Quickbase table.
        :param fields: (dict) Dictionary of field IDs and values
        :param database: (str or None) Quickbase Table ID (default None, uses self.database)
        :param uploads: (None or list of dict) List of dictionaries of file names and file contents and field IDs (default None)
        :param safemode: (bool) Whether to raise an error if you might edit a record (default False)
        :param return_fields: (None or list of str or int) List of fields to return (default None)
        :return: (int or dict) The record ID or record data
        """
        ...
    def edit_record(self, rid: int | None = None, key: int | None = None, fields: dict[str, Any] | None = None, database: str | None = None, 
                    uploads: list[dict[str, str | bytes]] | None = None, return_fields: list[str | int] | None = None) -> int | dict[str, Any]:
        """
        Edit a record in a Quickbase table.
        :param rid: (int or None) Quickbase record ID (default None)
        :param key: (int or None) Quickbase key (default None)
        :param fields: (dict or None) Dictionary of field IDs and values (default None)
        :param database: (str or None) Quickbase Table ID (default None, uses self.database)
        :param uploads: (None or list of dict) List of dictionaries of file names and file contents and field IDs (default None)
        :param return_fields: (None or list of str or int) List of fields to return (default None)
        :return: (int or dict) The record ID or record data
        """
        ...
    def delete_record(self, rid: str | int, database: str | None = None) -> dict[str, int]:
        """
        Delete a record from a Quickbase table.
        :param rid: (str or int) Quickbase record ID
        :param database: (str or None) Quickbase Table ID (default None, uses self.database)
        :return: (dict) The response
        """
        ...
    def add_multiple_records(self, data: list[dict[str, Any]], database: str | None = None, return_fields: list[str | int] | None = None, 
                             round_ints: bool = False, safemode: bool = False) -> dict[str, Any]:
        """
        Add multiple records to a Quickbase table.
        :param data: (list of dict) List of dictionaries of field IDs and values
        :param database: (str or None) Quickbase Table ID (default None, uses self.database)
        :param return_fields: (None or list of str or int) List of fields to return (default None)
        :param round_ints: (bool) Whether to round integers (default False)
        :param safemode: (bool) Whether to raise an error if you might edit a record (default False)
        :return: (dict) The response
        """
        ...
    def edit_multiple_records(self, data: list[dict[str, Any]], database: str | None = None, 
                              return_fields: list[str | int] | None = None, round_ints: bool = False) -> dict[str, Any]:
        """
        Edit multiple records in a Quickbase table.
        :param data: (list of dict) List of dictionaries of field IDs and values
        :param database: (str or None) Quickbase Table ID (default None, uses self.database)
        :param return_fields: (None or list of str or int) List of fields to return (default None)
        :param round_ints: (bool) Whether to round integers (default False)
        :return: (dict) The response
        """
        ...
    def purge_records(self, database: str | None = None, rids: list[str | int] | None = None, query: str | None = None) -> dict[str, int]:
        """
        Purge records from a Quickbase table.
        :param database: (str or None) Quickbase Table ID (default None, uses self.database)
        :param rids: (None or list of str or int) List of record IDs to purge (default None)
        :param query: (str or None) Quickbase query string (default None)
        :return: (dict) The response
        """
        ...
    def upload_file(self, rid: str | int, upload: dict[str, str | bytes], database: str | None = None) -> dict[str, Any]:
        """
        Upload a file to a Quickbase record.
        :param rid: (str or int) Quickbase record ID
        :param upload: (dict) Dictionary of file name and file contents and field ID
        :param database: (str or None) Quickbase Table ID (default None, uses self.database)
        :return: (dict) The response
        """
        ...
    def get_file(self, url: str | None = None, database: str | None = None, 
                 record: str | int | None = None, field: str | int | None = None, version: int = 1) -> tuple[dict[str, Any], bytes]:
        """
        Download a file from a Quickbase record.
        :param url: (str or None) Quickbase file URL (default None)
        :param database: (str or None) Quickbase Table ID (default None, uses self.database)
        :param record: (str or int or None) Quickbase record ID (default None)
        :param field: (str or int or None) Quickbase field ID (default None)
        :param version: (int) Quickbase file version (default 1)
        :return: (tuple) The response and file contents
        """
        ...
    def import_from_csv(self, records_csv: str, clist: list[str | int], database: str | None = None) -> dict[str, Any] | bool:
        """
        Import records from a CSV string into a Quickbase table.
        :param records_csv: (str) CSV string
        :param clist: (list of str or int) List of field IDs
        :param database: (str or None) Quickbase Table ID (default None, uses self.database)
        :return: (dict or bool) The response or False if unsuccessful
        """
        ...
    def change_record_owner(self, rid: int, database: str, new_owner: str) -> str:
        """
        Change the owner of a record in a Quickbase table.
        :param rid: (int) Quickbase record ID
        :param database: (str) Quickbase Table ID
        :param new_owner: (str) New owner email
        :return: (str) The response
        """
        ...
