from random import choice, randint
import requests


def fetch_mount():
    url = "https://ffxivcollect.com/api/mounts"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return "Error fetching mounts data"


def search_for_mount(name) -> str:
    mounts = fetch_mount()

    if mounts and isinstance(mounts, dict):
        mounts_list = mounts.get('results', [])
        for mount in mounts_list:
            # Checks if the mount is in the API Database
            if name.lower() in mount['name'].lower():
                # Allow to Split the sources so that I can display it better
                for source in mount["sources"]:
                    # Return the str
                    return (f"Name: {mount['name']}\n"
                            f"ID: {mount['id']}\nSeats: {mount["seats"]}\n"
                            f"Type: {source["type"]}\nText: {source["text"]}\nRelated Type: {source["related_type"]}\n" 
                            f"{mount["image"]}")

    return "Mount not found"


def get_response(user_input: str) -> str:
    lowered = str(user_input.lower()).split()
    command = lowered.pop(0)
    item = " ".join(lowered)

    if "mount" in command:
        return search_for_mount(item)

    else:
        return choice(["I don't understand what the hell you are talking about."])