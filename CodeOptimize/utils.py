import json
import re
from typing import Optional

def get_method_fqn(response: str) -> list[str]:
    """
    Extracts the strings enclosed within triple backticks from the provided response string.

    :param response: The string to extract the FQNs from.
    :return: A list of strings containing the extracted FQNs.
    """

    fqns = re.findall(r"```(.*?)```", response, re.DOTALL)
    return fqns

def load_KG(kg_json: str) -> list[dict]:
    """
    Loads the Knowledge Graph (KG) from the specified JSON file.

    :param kg_json: The path to the JSON file containing the KG.
    :return: The KG loaded as a list of dictionaries.
    """
    with open(kg_json, "r") as j:
        kg = json.loads(j.read())
    return kg

def check_valid(fqn: str, KG: list[dict]) -> Optional[dict]:
    """
    Checks if the given FQN (fully-qualified name) exists in the provided Knowledge Graph (KG).

    :param fqn: The FQN to check.
    :param KG: The Knowledge Graph as a list of dictionaries, where each dictionary represents an API entry.
    :return: The API dictionary if the FQN exists in the KG, None otherwise.
    """

    for api_dict in KG:
        if api_dict["api_fqn"].lower() == fqn.lower():
            return api_dict
    return None

def check_deprecated(api_dict: dict) -> bool:
    """
    Checks if the given API entry is marked as deprecated.

    :param api_dict: The dictionary representing an API entry.
    :return: True if the API entry is marked as deprecated, False otherwise.
    """
    return api_dict["deprecated"]

def get_exceptions_to_handle(fqn: str, KG: list[dict]) -> Optional[dict]:
    """
    Retrieves the exceptions to be handled for a given fully qualified name (FQN) from the knowledge graph.

    :param fqn: The fully qualified name of the API.
    :param KG: The knowledge graph containing API information.
    :return: A dictionary representing the exceptions to handle, or None if no exceptions are found for the given FQN.
    """
    for api_dict in KG:
        if api_dict["api_fqn"].lower() == fqn.lower():
            return api_dict["exceptions"]
    return None

