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
                    return (f"Name: {minion["name"]}\nID: {minion["id"]}\nTradeable {minion["tradeable"]}\n"
                            f"Behavior: {minion["behavior"]["name"]}\nType: {source["type"]}\nText: {source["text"]}\nOwned: {minion["owned"]}\n"
                            f"Race: {minion["race"]["name"]}\n"
                            f"{minion["image"]}")

    return "Minion not found"


def search_for_mount(name) -> str:
    mounts = fetch_data("mounts")

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
                            f"Type: {source["type"]}\nText: {source["text"]}\nRelated Type: {source["related_type"]}\nOwned: {mount["owned"]}\n"
                            f"{mount["image"]}")

    return "Mount not found"
