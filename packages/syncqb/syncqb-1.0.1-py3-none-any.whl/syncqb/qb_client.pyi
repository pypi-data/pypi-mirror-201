from json_quickbase import JsonQuickbaseClient
from xml_quickbase import XmlQuickbaseClient

def get_client(json_sdk: bool = False, creds: dict[str, str] | None = ...) ->JsonQuickbaseClient | XmlQuickbaseClient:
    """
    Get a QuickbaseClient instance
    (Use get_json_client or get_xml_client for type hints and docstrings)
    :param json_sdk: (bool) Use the JSON SDK instead of the XML SDK (default: False)
    :param creds: (dict or None) A dictionary of credentials. If omitted, will look for credentials in a .env file
    :return: (JsonQuickbaseClient or XmlQuickbaseClient) A QuickbaseClient instance
    """
    ...
def get_json_client(creds: dict[str, str] | None = ...) -> JsonQuickbaseClient:
    """
    Get a JsonQuickbaseClient instance
    :param creds: (dict or None) A dictionary of credentials. If omitted, will look for credentials in a .env file
    :return: (JsonQuickbaseClient) A JsonQuickbaseClient instance
    """
    ...
def get_xml_client(creds: dict[str, str] | None = ...) -> XmlQuickbaseClient:
    """
    Get a XmlQuickbaseClient instance
    :param creds: (dict or None) A dictionary of credentials. If omitted, will look for credentials in a .env file
    :return: (XmlQuickbaseClient) An XmlQuickbaseClient instance
    """
    ...
def set_qb_info() -> None:
    """
    Set Quickbase credentials in a .env file
    :return: None
    """
    ...
