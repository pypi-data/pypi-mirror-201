from .qb_errors import *
from .quickbase import QuickbaseClient
from typing import Any

class XmlQuickbaseClient(QuickbaseClient):
    apptoken: str | None = ...
    hours: int = ...
    ticket: str | None = ...
    def __init__(self, credentials: dict[str, str] | None = None, timeout: int = 90, database: str | None = None, authenticate: bool = True, 
                 apptoken: str | None = None, hours: int = 12, ticket: str | None = None, **kwargs: Any) -> None:
        """
        Client for Quickbase XML API
        :param credentials: (dict or None) A dictionary of credentials (default None) keys:
            username (required)
            password (required)
            realmhost (optional)
            base_url (required)
            user_token (optional)
        :param timeout: (int) The number of seconds to wait before timing out a request (default 90)
        :param database: (str or None) The Quickbase database ID (default None)
        :param authenticate: (bool) Whether to authenticate on instantiation (default True)
        :param apptoken: (str or None) The Quickbase application token (default None, required for some actions)
        :param hours: (int) The number of hours to extend the ticket (default 12)
        :param ticket: (str or None) The Quickbase ticket (default None)
        :param kwargs: (dict) Additional keyword arguments (used if credentials is None)
        """
        ...
    user_id: str = ...
    def authenticate(self) -> None:
        """
        Authenticate with Quickbase
        :return: None
        """
        ...
    def add_record(self, fields: dict[str, Any], database: str | None = None, ignore_error: bool = True, uploads: list[dict[str, str]] | None = None) -> int:
        """
        Add a record to a Quickbase database
        :param fields: (dict) A dictionary of field names and values
        :param database: (str or None) The Quickbase database ID (default None, will use self.database)
        :param ignore_error: (bool) Whether to ignore errors (default: False)
        :param uploads: (None or list of dict) List of dictionaries of file names and file contents and field IDs (default None)
        :return: (int) The record ID
        """
        ...
    def edit_record(self, rid: int, fields: dict[str, Any], database: str | None = None, uploads: list[dict[str, str]] | None = None) -> int: 
        """
        Edit a record in a Quickbase database
        :param rid: (int) The record ID
        :param fields: (dict) A dictionary of field names and values
        :param database: (str or None) The Quickbase database ID (default None, will use self.database)
        :param uploads: (None or list of dict) List of dictionaries of file names and file contents and field IDs (default None)
        :return: (int) The record ID
        """
        ...
    def delete_record(self, rid: int | None = None, key: int | None = None, database: str | None = None) -> dict[str, str]:
        """
        Delete a record from a Quickbase database
        :param rid: (int or None) The record ID (default None)
        :param key: (int or None) The record key (default None)
        :param database: (str or None) The Quickbase database ID (default None, will use self.database)
        :return: (dict) The response
        """
        ...
    def purge_records(self, rids: list[str | int] | None = None, query: str | None = None, qid: int | None = None, database: str | None = None) -> dict[str, Any]:
        """
        Purge records from a Quickbase database
        :param rids: (list of int or None) The record IDs (default None)
        :param query: (str or None) The query (default None)
        :param qid: (int or None) The query ID (default None)
        :param database: (str or None) The Quickbase database ID (default None, will use self.database)
        :return: (dict) The response
        """
        ...
    def do_query(self, query: str | None = None, qid: int | None = None, query_params: dict[str, str] | None = None, columns: list[str | int] | None = None,
                sort: list[str | int] | None = None, structured: bool = True, num: int | None = None, only_new: bool = False, skip: int | None = None,
                ascending: bool = True, include_rids: bool = False, return_metadata: bool = False, qid_custom_headers: bool = False, 
                database: str | None = None) -> list[dict[str, str]]:
        """
        Query a Quickbase database
        :param query: (str or None) The query (default None)
        :param qid: (int or None) The query ID (default None)
        :param query_params: (dict) A dictionary of query parameters (default {})
        :param columns: (list of str or None) The columns to return (default None)
        :param sort: (list of str or None) The columns to sort by (default None)
        :param structured: (bool) Whether to return structured results (default False)
        :param num: (int or None) The max number of records to return (default None)
        :param only_new: (bool) Whether to only return new or updated records (default False)
        :param skip: (int or None) The number of records to skip (default None)
        :param ascending: (bool) Whether to sort in ascending order (default True)
        :param include_rids: (bool) Whether to include record IDs (default False)
        :param return_metadata: (bool) Whether to return metadata (default False)
        :param qid_custom_headers: (bool) Whether to return custom headers (default False)
        :param database: (str or None) The Quickbase database ID (default None, will use self.database)
        :return: (list of dict) The results
        """
        ...
    def get_schema(self, database: str | None = None, required: list[str | int] | None = None, get_xml: bool = False) -> list[dict[str, Any]]:
        """
        Get the schema for a Quickbase database
        :param database: (str or None) The Quickbase database ID (default None, will use self.database)
        :param required: (list of str or None) The required fields (default None)
        :param get_xml: (bool) Whether to return the XML (default False)
        :return: (list of dict) The schema
        """
        ...
    def get_file(self, fname: str, folder: str, rid: str | int, fid: str | int, version: str | int = 0, database: str | None = None) -> bytes:
        """
        Get a file from a Quickbase database and write it to a file
        :param fname: (str) The file name
        :param folder: (str) The folder to write the file to (from the current working directory)
        :param rid: (str or int) The record ID
        :param fid: (str or int) The field ID
        :param version: (str or int) The version (default '')
        :param database: (str or None) The Quickbase database ID (default None, will use self.database)
        :return: (bytes) base64 encoded file contents
        """
        ...
    def upload_file(self, rid: str | int, upload: dict[str, str], database: str | None = None) -> dict[str, Any]:
        """
        Upload a file to a Quickbase database
        :param rid: (str or int) The record ID
        :param upload: (dict) A dictionary of the file name and file contents and field ID
        :param database: (str or None) The Quickbase database ID (default None, will use self.database)
        :return: (dict) The response
        """
        ...
    def import_from_csv(self, records_csv: str, clist: list[str | int], clist_output: list[str | int] | None = None, skipfirst: bool = False, 
                        database: str | None = None, required: list[str | int] | None = None, chunk: int | None = None) -> dict[str, Any]:
        """
        :param records_csv: (str) The records CSV string, comma separated with rows separated by newlines
        :param clist: (list of str) The column list
        :param clist_output: (list of str) The column list output (default None)
        :param skipfirst: (bool) Whether to skip the first row (default False)
        :param database: (str or None) The Quickbase database ID (default None, will use self.database)
        :param required: (list of str or None) The required fields to return (default None)
        :param chunk: (int or None) Amount to chunk the records (default None, will split into chunks of given number of records if not none or 0 - USES MULTPLE API CALLS)
        :return: (dict) The response
        """

        ...
    def get_user_info(self, email: str | None = None, rid: int | None = None) -> dict[str, str]:
        """
        Get user info for a Quickbase user
        :param email: (str or None) The user's email (default None)
        :param rid: (int or None) The user's record ID (default None)
        :return: (dict) The user info
        """
        ...
