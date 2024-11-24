import requests
from fuzzywuzzy import fuzz, process


class FFXIVSearch:
    UNIVERSAL_RATIO_CHECK = 80

    def __init__(self, base_url="https://ffxivcollect.com/api/"):
        self.base_url = base_url


    def get_base_url(self):
        return self.base_url

    def set_ase_url(self, url):
        if not url.startswith("https"):
            raise ValueError("Base URL muse start with \"http\"")
        self.base_url = url

    def fetch_data(self, endpoint: str):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return f"Error fetching {endpoint}"

    @staticmethod
    def _fuzzy_search(name, items, key="name"):
        names = [item[key].lower() for item in items]
        best_match, score = process.extractOne(name.lower(), names, scorer=fuzz.partial_ratio)
        return best_match, score

    def search_minions(self, name):
        minions = self.fetch_data("minions")

        if minions and isinstance(minions, dict):
            minions_list = minions.get("results", [])
            best_match, score = self._fuzzy_search(name, minions_list)

            if score > self.UNIVERSAL_RATIO_CHECK:
                for minion in minions_list:

                    if minion["name"].lower() in best_match:
                        """
                        Since there could be multiple sources I obtain them all
                        and join them together with a new line attached for it to be printed
                        In the proper place
                        """

                        source = "\n".join([f"Source: {obtain["type"]}\nText: {obtain["text"]}" for obtain in minion["sources"]])

                        image_url = minion["image"]
                        description = (f"Name: {minion["name"]}\n"
                                       f"ID: {minion["id"]}\n"
                                       f"Tradeable {minion["tradeable"]}\n"
                                       f"Item ID: {minion["item_id"]}\n"
                                       f"Behavior: {minion["behavior"]["name"]}\n"
                                       f"{source}\n"
                                       f"Owned: {minion["owned"]}\n"
                                       f"Race: {minion["race"]["name"]}\n")
                        return description, image_url
        return f"{name} not found", None

    def search_mount(self, name):
        mounts = self.fetch_data("mounts")

        if mounts and isinstance(mounts, dict):
            mounts_list = mounts.get("results", [])
            best_match, score = self._fuzzy_search(name, mounts_list)

            if score > self.UNIVERSAL_RATIO_CHECK:
                for mount in mounts_list:
                    if mount["name"].lower() in best_match:
                        source = "\n".join([f"Source: {obtain["type"]}\nText: {obtain["text"]}" for obtain in mount["sources"]])
                        image_url = mount["image"]

                        description = (f"Name: {mount["name"]}\n"
                                       f"ID: {mount["id"]}\n"
                                       f"Seats: {mount["seats"]}\n"
                                       f"Tradeable {mount["tradeable"]}\n"
                                       f"Item ID: {mount["item_id"]}\n"
                                       f"{source}\n"
                                       f"Owned: {mount["owned"]}\n"
                                       f"[Click her for the BGM]({mount["bgm"]})"
                                       )
                        return description, image_url
        return f"{name} not found", None

    def search_title(self, name):
        titles = self.fetch_data("titles")

        if titles and isinstance(titles, dict):
            titles_list = titles.get("results", [])

            best_match, score = self._fuzzy_search(name, titles_list)

            if score > self.UNIVERSAL_RATIO_CHECK:
                for title in titles_list:
                    if title["name"].lower() in best_match:
                        image_url = title["icon"]

                        if "achievement" in title:
                            achievement = title["achievement"]

                            achievement_info = (
                                f"Achievement Name: {achievement.get("name", "N/A")}\n"
                                f"Achievement Description: {achievement.get("description", "N/A")}\n"
                                f"Points: {achievement.get("points", "N/A")}\n"
                                f"Owned: {achievement.get("owned", "N/A")}"
                            )
                        else:
                            achievement_info = "N/A"

                        description = (
                            f"Name: {title["name"]}\n"
                            f"Female Name: {title["female_name"]}\n"
                            f"ID: {title["id"]}\n"
                            f"Owned: {title["owned"]}\n"
                            f"{achievement_info}\n"
                            f"Type: {title.get("type", {}).get("name", "N/A")}"
                        )

                        return description, image_url

            return f"{name} was not found", None


# def search_for_emote(name):
#     emotes = fetch_data("emotes")  # Changed endpoint to "emotes" for consistency
#
#     if emotes and isinstance(emotes, dict):
#         emote_list = emotes.get("results", [])
#
#         names = [name["name"] for name in emote_list]
#         best_match, score = process.extractOne(name.lower(), names, scorer=fuzz.partial_ratio)
#
#         if score > UNIVERSAL_RATIO_CHECK:
#             for emote in emote_list:
#                 if emote["name"].lower() in best_match.lower():
#                     icon_url = emote["icon"]
#                     sources = emote["sources"]
#
#                     # Get the type and description for the emote into format to be able to print it
#                     source_type = "\n".join([f"Type: {obtain["type"]}\nText: {obtain["text"]}" for obtain in sources])
#
#                     description = (f"Name: {emote['name']}\n"
#                                    f"ID: {emote['id']}\n"
#                                    f"Commands: {emote['command']}\n"
#                                    f"Tradeable: {emote['tradeable']}\n"
#                                    f"owned: {emote['owned']}\n"
#                                    f"{source_type}\n"
#                                    )
#
#                     return description, icon_url
#
#     return "Emote not found", None
#
#
# def search_for_achievement(name):
#     achievements = fetch_data("achievements")
#
#     if achievements and isinstance(achievements, dict):
#         achievement_list = achievements.get("results", [])
#
#         names = [name["name"] for name in achievement_list]
#         best_match, score = process.extractOne(name.lower(), names, scorer=fuzz.partial_ratio)
#
#         if score > UNIVERSAL_RATIO_CHECK:
#             for achievement in achievement_list:
#                 if achievement["name"].lower() in best_match.lower():
#                     icon_url = achievement["icon"]
#
#                     description = (
#                         f"Name: {achievement['name']}\n"
#                         f"ID: {achievement['id']}\n"
#                         f"Description: {achievement['description']}\n"
#                         f"Points: {achievement['points']}\n"
#                         f"Owned: {achievement['owned']}\n"
#                     )
#                     return description, icon_url
#     return "Achievement not found", None