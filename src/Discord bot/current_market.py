import requests


class Universalis:
    BASE_URL = "https://universalis.app/api/v2/"

    def __init__(self, item_id=0, data_center="light"):
        """Initialize the Universalis object.
        Args: Item_id (Int) = The ID of the item. THe items would have an id only if the item is tradable.
        data_center (str) = is the world/server you want to check whatever item price.
        """

        self.item_id = item_id
        self.data_center = data_center

    def set_item_id(self, item_id):
        self.item_id = item_id

    def set_data_center(self, data_center):
        self.data_center = data_center

    def fetch_data(self):
        """Fetch the data from the API for the specified item id on the specified data center.
        Returns: Dict from the Market if it's successfully fetched, Otherwise it would return a str with an error.
        """

        if not self.item_id:
            return "Error: Item ID is required."

        url = f"{self.BASE_URL}{self.data_center}/{self.item_id}/"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return f"Error Fetching data from Universalis: {response.status_code}"

    def get_cheapest_price(self):
        """
        Get the cheapest price from the API for the specified item id on the specified data center.
        Returns:
            str: A formatted string with the cheapest price and world
        """
        market_data = self.fetch_data()

        if isinstance(market_data, dict) and "listings" in market_data:
            listings = market_data["listings"]

            if listings:
                cheapest_listing = listings[0]
                price = cheapest_listing["pricePerUnit"]
                world = cheapest_listing["worldName"]
                quantity = cheapest_listing["quantity"]
                return f"Cheapest price: {price}\nWorld: {world}\nQuantity: {quantity}"

            else:
                return "Error: Item ID is required."
        return market_data # Return an error


