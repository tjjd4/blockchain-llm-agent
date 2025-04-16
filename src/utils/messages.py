import os
import json
from typing import Dict

SCHEMA_DIR = os.path.join("app", "schemas")

def get_classify_system_messages() -> Dict[str, str]:
    classify_system_message = {
        "role": "system",
        "content":
            "Determine if the following transaction text is for a token swap or a transfer. "
            "Use the appropriate schema to assist your understanding, but identifying the transaction type is the priority. "
            "Do not rely solely on whether the schema can be fully populated. "
            "Return '1' for transfer, '2' for swap, and '0' for neither. "
            "Do not output anything besides this number. "
            "If one number is classified for the output, make sure to omit the other two in your generated response."
    }

    return classify_system_message

def get_convert_system_messages() -> Dict[str, str]:
    convert_system_message = {
        "role": "system",
        "content":
            "Please analyze the following transaction text and fill out the properties in JSON schema based on the provided details."
            "All prices are assumed to be in USD."
    }

    return convert_system_message

def get_transfer_schema_message() -> Dict[str, str]:
    schema_path = os.path.join(SCHEMA_DIR, "transfer.json")
    with open(schema_path, "r", encoding="utf-8") as f:
        transfer_schema = json.load(f)
        transfer_schema_message = {
            "role": "system",
            "content": "[Transfer Schema] Token Transfer Schema:\n" + json.dumps(transfer_schema, indent=2)
        }

        return transfer_schema_message

def get_swap_system_message() -> Dict[str, str]:
    swap_system_message = {
        "role": "system",
        "content":
            "Please analyze the following transaction text and fill out the JSON schema based on the provided details."
            "All prices are assumed to be in USD."
    }

    return swap_system_message

def get_swap_schema_message() -> Dict[str, str]:
    schema_path = os.path.join(SCHEMA_DIR, "swap.json")
    with open(schema_path, "r", encoding="utf-8") as f:
        swap_schema = json.load(f)
        swap_schema_message = {
            "role": "system",
            "content": "[Transfer Schema] Token Transfer Schema:\n" + json.dumps(swap_schema, indent=2)
        }

        return swap_schema_message

def get_instruction_message() -> Dict[str, str]:
    instruction_message = {
        "role": "system",
        "content":
            "The outputted JSON should be an instance of the schema."
            "Never output the schema itself, but instead fill out its values."
            "It is not necessary to include the parameters/contraints that are not directly related to the data provided."
            "If no chain is specified to excecute the transaction on, default to 'mainnet'",
    }

    return instruction_message


def get_mcp_system_message() -> Dict[str, str]:
    mcp_system_message = {
        "role": "system",
        "content":
            """You are an intelligent assistant with access to both Resources and Tools through the MCP (Model Context Protocol) interface:

            Resources (for accessing content):
            - Use read_resource for accessing file contents via URIs (e.g., "storage://local/config.txt")
            - Resources represent actual data and content you can read
            - Resource URIs follow the pattern: storage://local/{/path}

            Tools (for performing operations):
            - Discover available tools using list_tools
            - Each tool has:
            * A unique name (e.g., "write_file")
            * A description of its purpose
            * A schema defining its required arguments
            - To use a tool:
            1. First call list_tools to discover available tools and their parameters
            2. Then call_tool with:
                * name: The tool's name (e.g., "write_file")
                * args: An object matching the tool's parameter schema

            Best Practices:
            1. Always discover tools first - don't assume which tools are available
            2. Use the exact parameter structure defined in each tool's schema
            3. Tools are server-specific - different servers may provide different capabilities
            4. Use Resources for reading content, Tools for actions and modifications

            Example workflow:
            1. List available tools to discover capabilities
            2. Match tool parameters exactly to their schemas
            3. Use tools and resources appropriately for your task
            """
    }
    return mcp_system_message