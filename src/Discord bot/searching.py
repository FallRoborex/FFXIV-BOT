import requests
from fuzzywuzzy import fuzz, process
from current_market import Universalis


class FFXIVSearch:
    UNIVERSAL_RATIO_CHECK = 80

    def __init__(self, base_url="https://ffxivcollect.com/api/"):
        self.base_url = base_url
        self.item_id = 0
        self.universalis = Universalis()

    def set_item_id(self, item_id):
        self.item_id = item_id
        self.universalis.set_item_id(item_id)

    def get_cheapest_price(self):
        return self.universalis.get_cheapest_price()

    def get_base_url(self):
        return self.base_url

    def set_base_url(self, url):
        if not url.startswith("https"):
            raise ValueError("Base URL muse start with \"http\"")
        self.base_url = url

    def fetch_data(self, endpoint: str):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url)

        # Check to see if the connection was successful to the api
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error fetching {endpoint}"

    # Method that would help the user if they misspelled a word and still get a result. UNIVERSAL RATIO CHECK would change the percentage
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
                        item_id = minion["item_id"]

                        if minion["tradeable"]:
                            self.set_item_id(item_id)

                        image_url = minion["image"]
                        description = (f"Name: {minion["name"]}\n"
                                       f"ID: {minion["id"]}\n"
                                       f"Tradeable {minion["tradeable"]}\n"
                                       f"Item ID: {item_id}\n"
                                       f"Behavior: {minion["behavior"]["name"]}\n"
                                       f"{source}\n"
                                       f"Owned: {minion["owned"]}\n"
                                       f"Race: {minion["race"]["name"]}\n"
                                       f"{self.universalis.get_cheapest_price()}\n")
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
                        tradeable = mount["tradeable"]

                        if tradeable:
                            self.set_item_id(mount["item_id"])


                        description = (f"Name: {mount["name"]}\n"
                                       f"ID: {mount["id"]}\n"
                                       f"Seats: {mount["seats"]}\n"
                                       f"Tradeable {tradeable}\n"
                                       f"Item ID: {mount["item_id"]}\n"
                                       f"{source}\n"
                                       f"Owned: {mount["owned"]}\n"
                                       f"{self.universalis.get_cheapest_price()}\n"
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

    def search_emote(self, name):
        emotes = self.fetch_data("emotes")  # Get the data for emotes

        if emotes and isinstance(emotes, dict):
            emotes_list = emotes["results"]

            best_match, score = self._fuzzy_search(name, emotes_list)

            if score > self.UNIVERSAL_RATIO_CHECK:
                for emote in emotes_list:
                    if emote["name"].lower() in best_match:
                        icon_url = emote["icon"]

                        # Get the type and description for the emotes into format to be able to print it
                        source_type = "\n".join([f"Type: {obtain["type"]}\nText: {obtain["text"]}" for obtain in emote["sources"]])
                        tradeable = emote["tradeable"]

                        if tradeable:
                            self.set_item_id(emote["item_id"])

                        description = (f"Name: {emote['name']}\n"
                                       f"ID: {emote['id']}\n"
                                       f"Commands: {emote['command']}\n"
                                       f"Tradeable: {tradeable}\n"
                                       f"owned: {emote['owned']}\n"
                                       f"{source_type}\n"
                                       f"{self.universalis.get_cheapest_price()}\n"
                                       )

                        return description, icon_url
            return f"{name} was not found.", None

    def search_achievement(self, name):
        achievement = self.fetch_data("achievements")

        if achievement and isinstance(achievement, dict):
            achievements_list = achievement["results"]

            best_match, score = self._fuzzy_search(name, achievements_list)

            if score > self.UNIVERSAL_RATIO_CHECK:
                for achievement in achievements_list:
                    if achievement["name"].lower() in best_match:
                        icon_url = achievement["icon"]

                        description = (
                            f"Name: {achievement['name']}\n"
                            f"ID: {achievement['id']}\n"
                            f"Description: {achievement['description']}\n"
                            f"Points: {achievement['points']}\n"
                            f"Owned: {achievement['owned']}\n"
                        )

                        return description, icon_url

            return f"{name} was not found", None
