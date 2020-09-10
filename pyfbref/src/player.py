import requests
import re
import pandas as pd
import warnings
from bs4 import BeautifulSoup


class Player(object):
    fbref_url = "https://fbref.com/search/search.fcgi?search"

    def __init__(self, player_name):
        if not isinstance(player_name, str):
            raise TypeError("Player name must be a string")
        self.name, self.search_str = _validate_name(Player.fbref_url, player_name)

    def __repr__(self):
        desc = "<player: {}, id: {}>".format(self.name, id(self))
        return desc

    def get_table(self, table_type="Standard Stats"):
        """
        Grab a single table from a player's page

        Parameters
        ------------
        table_type : str, default="Standard Stats"
            Table type to grab from fbref. Valid args include: 
            "Standard Stats",
            "Shooting",
            "Passing",
            "Pass Types",
            "Goal and Shot Creation",
            "Defensive Actions",
            "Possession",
            "Playing Time",
            "Miscellaneous Stats",
            "Player Club Summary"

        Returns
        -------
        df : Pandas.DataFrame
            DataFrame of `table_type`
        """
        if table_type not in valid_headers():
            raise ValueError(f"Invalid table type requested: {table_type}")
        soup = _get_soup(Player.fbref_url, self.name, self.search_str)
        all_divs = soup.findAll("div", {"class": "table_wrapper"})
        div = [x for x in all_divs if x.find("span")['data-label'] == table_type]
        if len(div) == 0:
            raise ValueError(f"Table type '{table_type}' not found for {self.name}")
        div = div[0]
        table = div.find("tbody")
        rows = table.find_all("tr")
        pre_df_dict = dict()
        for row in rows:
            if row.find("th", {"scope": "row"}) != None:
                cells = row.find_all("td")
                for cell in cells:
                    cell_text = cell.text.encode()
                    text = cell_text.decode("utf-8")
                    try:
                        text = float(text)
                    except ValueError:
                        pass
                    if cell["data-stat"] in pre_df_dict.keys():
                        pre_df_dict[cell["data-stat"]].append(text)
                    else:
                        pre_df_dict[cell["data-stat"]] = [text]

        df = pd.DataFrame.from_dict(pre_df_dict)

        return df


    def get_tables(self):
        """
        Grab all available tables from a player's page

        Returns
        -------
        df_dict : dict
            Dictionary of DataFrame objects
        """
        soup = _get_soup(Player.fbref_url, self.name, self.search_str)
        all_tables = soup.findAll("tbody")
        all_headers = soup.findAll("div", {"class": "section_heading"})
        head_labels = [
            i.span["data-label"]
            for i in all_headers
            if i.span["data-label"] in valid_headers()
        ]

        df_dict = dict()
        for table, label in zip(all_tables, head_labels):
            pre_df_dict = dict()
            rows = table.find_all("tr")
            for row in rows:
                if row.find("th", {"scope": "row"}) != None:
                    cells = row.find_all("td")
                    for cell in cells:
                        cell_text = cell.text.encode()
                        text = cell_text.decode("utf-8")
                        try:
                            text = float(text)
                        except ValueError:
                            pass
                        if cell["data-stat"] in pre_df_dict.keys():
                            pre_df_dict[cell["data-stat"]].append(text)
                        else:
                            pre_df_dict[cell["data-stat"]] = [text]

            df = pd.DataFrame.from_dict(pre_df_dict)
            df_dict[f"{label}"] = df

        self.tables = df_dict


def valid_headers():
    valid = [
        "Standard Stats",
        "Shooting",
        "Passing",
        "Pass Types",
        "Goal and Shot Creation",
        "Defensive Actions",
        "Possession",
        "Playing Time",
        "Miscellaneous Stats",
        "Player Club Summary",
    ]

    return valid


def _get_soup(fbref_url, name, search_str=None):
    if search_str is None:
        search_str = fbref_url + "=" + name
    response = requests.get(search_str)
    comm = re.compile("<!--|-->")
    soup = BeautifulSoup(comm.sub("", response.text), "lxml")

    return soup


def _validate_name(url, name):
    search_str = None
    soup = _get_soup(url, name)
    strong_str = [i.next_element for i in soup.findAll("strong")]
    title = soup.find("title")
    if "0 hits" in strong_str:
        raise ValueError(f"`{name}` not found in FBRef")
    if "Search Results" in title.next_element:
        # Grab first search result
        search = soup.findAll("div", {"class": "search-item-name"})[0]
        search_name = search.next_element.next_element.next_element
        search_str = "https://fbref.com/" + search.a["href"]
        msg = f"Exact match for {name} not found.  Setting `player_name` to first search result: {search_name}"
        warnings.warn(msg)
        name = search_name
    return name, search_str


if __name__ == "__main__":
    puli = Player("Christian Pulisic")
    standard = puli.get_table()
