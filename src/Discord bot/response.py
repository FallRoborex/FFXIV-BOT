import requests
from fuzzywuzzy import fuzz, process

UNIVERSAL_RATIO_CHECK = 80


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
        names = [minion["name"] for minion in minions_list]
        best_match, score = process.extractOne(name.lower(), names, scorer=fuzz.partial_ratio)

        if score > UNIVERSAL_RATIO_CHECK:
            for minion in minions_list:
                if minion["name"].lower() in best_match.lower():
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

    return "Minion not found", None


def search_for_mount(name):
    mounts = fetch_data("mounts")

    if mounts and isinstance(mounts, dict):
        mounts_list = mounts.get('results', [])

        names = [mount["name"].lower() for mount in mounts_list]
        best_match, score = process.extractOne(name.lower(), names, scorer=fuzz.partial_ratio)

        if score > UNIVERSAL_RATIO_CHECK:
            for mount in mounts_list:
                # Checks if the mount is in the API Database
                if mount["name"].lower() == best_match.lower():
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
                                       f"Owned: {mount['owned']}\n"
                                       f"Tradeable: {mount["tradeable"]}\n")
                        return description, image_url

    return "Mount not found", None


def search_for_title(name):
    titles = fetch_data("titles")  # Changed endpoint to "titles" for consistency
    if titles and isinstance(titles, dict):
        title_list = titles.get("results", [])

        names = [title["name"] for title in title_list]
        best_match, score = process.extractOne(name.lower(), names, scorer=fuzz.partial_ratio)

        if score > UNIVERSAL_RATIO_CHECK:
            for title in title_list:
                if title["name"].lower() in best_match.lower():
                    image_url = title.get("icon")

                    category_type = "\n".join([f"name: {category['name']}" for category in title.get("categories", [])])

                    achievement_info = ""
                    if "achievement" in title:
                        achievement = title["achievement"]
                        achievement_info = (
                            f"Achievement Name: {achievement.get('name', 'N/A')}\n"
                            f"Achievement Description: {achievement.get('description', 'N/A')}\n"
                            f"Points: {achievement.get('points', 'N/A')}\n"
                            f"Owned: {achievement.get('owned', 'N/A')}\n"
                        )

                    description = (
                        f"Name: {title['name']}\n"
                        f"ID: {title['id']}\n"
                        f"{category_type}\n"
                        f"{achievement_info}\n"
                        f"Type: {title.get('type', {}).get('name', 'N/A')}"
                    )
                    return description, image_url

    return "Title not found", None


def search_for_emote(name):
    pass


def search_for_achievement(name):
    pass
