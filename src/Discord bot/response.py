from typing import Tuple, Any

import requests


def fetch_data(endpoint: str):
    base_url = "https://ffxivcollect.com/api/"
    url = f"{base_url}{endpoint}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error fetching {endpoint}"


def search_for_minions(name):
    minions = fetch_data("minions")

    if minions and isinstance(minions, dict):
        minions_list = minions.get("results", [])

        for minion in minions_list:
            if name.lower() in minion["name"].lower():
                for source in minion["sources"]:
                    image_url = minion["image"]
                    description = (f"Name: {minion["name"]}\n"
                                   f"ID: {minion["id"]}\n"
                                   f"Tradeable {minion["tradeable"]}\n"
                                   f"Behavior: {minion["behavior"]["name"]}\n"
                                   f"Type: {source["type"]}\n"
                                   f"Text: {source["text"]}\n"
                                   f"Owned: {minion["owned"]}\n"
                                   f"Race: {minion["race"]["name"]}\n")
                    return description, image_url

    return "Minion not found"


def search_for_mount(name):
    mounts = fetch_data("mounts")

    if mounts and isinstance(mounts, dict):
        mounts_list = mounts.get('results', [])

        for mount in mounts_list:
            # Checks if the mount is in the API Database
            if name.lower() in mount['name'].lower():
                # Allow you to split the sources so that I can display it better
                for source in mount["sources"]:
                    image_url = mount["image"]
                    # Return the str and image URL
                    description = (f"Name: {mount['name']}\n"
                                   f"ID: {mount['id']}\n"
                                   f"Seats: {mount['seats']}\n"
                                   f"Type: {source['type']}\n"
                                   f"Text: {source['text']}\n"
                                   f"Related Type: {source['related_type']}\n"
                                   f"Owned: {mount['owned']}\n")
                    return description, image_url

    return "Mount not found"
