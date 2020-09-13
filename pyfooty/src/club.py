import requests
import re
import pandas as pd
import warnings
from bs4 import BeautifulSoup
from pyfooty.src.baseclass import AbstractFooty
from pyfooty.src.utils import get_soup, get_available_tables
from datetime import date

class Club(AbstractFooty):
    """A Club object.
    The Club object represents a soccer club with available data from FBRef.com.
    Parameters
    ----------
    club_name : str
        Name of team to search on FBRef
    year : int, default=None
    Attributes
    ---------
    name : str
        Name of team to search on FBRef
    valid_tables : tuple
        Tuple of valid tables
    """
    fbref_url = "https://fbref.com/search/search.fcgi?search"

    def __init__(self, club_name, year=None):
        if year:
            self._year = _validate_year(year)
        else:
            self._year = _validate_year(date.today().year)
        self._name, self._club_url = _validate_name(Club.fbref_url, club_name, self.year)
        self._valid_tables = get_available_tables(self.club_url)

    @property
    def name(self):
        return self._name

    @property
    def valid_tables(self):
        return self._valid_tables

    @property
    def club_url(self):
        return self._club_url

    @property
    def year(self):
        return self._year

    def __repr__(self):
        desc = "<club: {}, year: {}, id: {}>".format(self.name, self.year, id(self))
        return desc

    def get_table(self, table_type="Standard Stats"):
        """
        Grab a single table from a club's page

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
        if table_type not in self.valid_tables:
            raise ValueError(f"Invalid table type requested: {table_type}")
        soup = get_soup(self.club_url)
        all_divs = soup.findAll("div", {"class": "table_wrapper"})
        div = [x for x in all_divs if x.find("span")["data-label"] == table_type]
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
        soup = get_soup(self.club_url)
        all_tables = soup.findAll("tbody")
        all_headers = soup.findAll("div", {"class": "section_heading"})
        head_labels = [
            i.span["data-label"]
            for i in all_headers
            if i.span["data-label"] in self.valid_tables
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

def _validate_name(url, name, year=None):
    if not isinstance(name, str):
        raise TypeError("Search name must be a string")
    soup = get_soup(url, name)
    strong_str = [i.next_element for i in soup.findAll("strong")]
    title = soup.find("title")
    if "0 hits" in strong_str:
        raise ValueError(f"`{name}` not found in FBRef")
    if "Search Results" in title.next_element:
        # Grab first search result for Clubs
        search = soup.find("div", {"id": "clubs"})
        search_name = search.find("div", {"search-item-alt-names"}).contents[0]
        year_url = f"{year}-{year+1}"
        search_url = "https://fbref.com" + search.find("div", {"search-item-url"}).contents[0].contents[0]
        actual_url = get_soup(search_url).find("meta", {"property": "og:url"})['content']
        url_list = actual_url.split('/')
        url_list.insert(-1, year_url)
        final_url = '/'.join([i for i in url_list])
        msg = f"Exact match for {name} not found.  Setting `name` to first search result: {search_name}"
        warnings.warn(msg)
    return search_name, final_url

def _validate_year(year):
    """ Validate year is given as an int"""
    if not isinstance(year, int):
        raise TypeError("Year must give of type `int`.")
    if year <= 1900:
        raise ValueError("Please enter a year after 1990.")

    return year

if __name__ == "__main__":
    club = Club("Chelsea", 2019)
    #standard = club.get_table("Standard Stats")
