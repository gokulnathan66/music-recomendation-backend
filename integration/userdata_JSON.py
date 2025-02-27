import json
import os
import uuid
from typing import Optional

file_path = 'user_data.json'

def read_user_data(user_id: str) -> Optional[list]:
    """
    Reads and retrieves user-specific data from a JSON file.
    
    Parameters:
        user_id (str): The unique identifier of the user whose data needs to be fetched.
    
    Returns:
        Optional[list]: A list of stored strings associated with the user_id if found,
                        otherwise None if the user does not exist.
    """
    if not os.path.exists(file_path):
        return None  # File does not exist
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    return data.get(user_id, None)  # Return data for the user_id or None if not found

def write_user_data(user_id: str, new_data: str) -> None:
    """
    Writes or appends user-specific data to a JSON file.
    
    If the user_id already exists, the new data string is appended to their list.
    Otherwise, a new entry is created for the user.
    
    Parameters:
        user_id (str): The unique identifier of the user.
        new_data (str): The new string to be added to the user's stored data.
    
    Returns:
        None
    """
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = {}  # Create a new dictionary if file does not exist
    
    if user_id in data:
        data[user_id].append(new_data)  # Append new string for existing user
    else:
        data[user_id] = [new_data]  # Create a new list for the new user
    
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)  # Write updated data back to the file

def generate_user_id() -> str:
    """
    Generates a unique user identifier using UUID.
    
    Returns:
        str: A randomly generated unique identifier.
    """
    return str(uuid.uuid4())
