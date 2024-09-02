import json
from typing import List, Dict, Any
from bson import ObjectId

DATA_FILE = "data.json"

def read_data() -> Dict[str, Any]:
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            print(f"Read data from {DATA_FILE}: {data}")  # Debugging
            return data
    except FileNotFoundError:
        return {"items": []}
    except json.JSONDecodeError:
        return {"items": []}

def write_data(data: Dict[str, Any]) -> None:
    try:
        with open(DATA_FILE, "w") as file:
            print(f"Writing data to {DATA_FILE}: {data}")  # Debugging
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error writing data to file: {e}")

def get_items() -> List[Dict[str, Any]]:
    data = read_data()
    return data.get("items", [])

def add_item(item: Dict[str, Any]) -> None:
    data = read_data()
    items = data.get("items", [])
    items.append(item)
    data["items"] = items
    write_data(data)

def find_item(item_id: str) -> Dict[str, Any]:
    data = read_data()
    items = data.get("items", [])
    for item in items:
        if item.get("id") == item_id:
            return item
    return {}

def update_item(item_id: str, item_update: Dict[str, Any]) -> Dict[str, Any]:
    data = read_data()
    items = data.get("items", [])
    for index, item in enumerate(items):
        if item.get("id") == item_id:
            items[index].update(item_update)
            data["items"] = items
            write_data(data)
            return items[index]
    return {}

def delete_item(item_id: str) -> Dict[str, Any]:
    data = read_data()
    items = data.get("items", [])
    for index, item in enumerate(items):
        if item.get("id") == item_id:
            deleted_item = items.pop(index)
            data["items"] = items
            write_data(data)
            return deleted_item
    return {}
