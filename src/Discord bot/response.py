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


def search_for_mount(name):
    mounts = fetch_mount()

    if mounts and isinstance(mounts, dict):

        mounts_list = mounts.get('results', [])
        for mount in mounts_list:
            if name.lower() in mount['name'].lower():
                return f"Name: {mount['name']}\nID: {mount['id']}\nSource: {mount['sources']}"
    return "Mount not found"


def get_response(user_input: str) -> str:
    lowered = str(user_input.lower()).split()
    command = lowered.pop(0)
    item = " ".join(lowered)

    if "mount" in command:
        return search_for_mount(item)

    else:
        return choice(["I don't understand what the hell you are talking about."])
