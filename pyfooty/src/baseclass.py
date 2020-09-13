import pandas as pd
import warnings
from abc import ABCMeta, abstractmethod
from pyfooty.src.utils import get_soup, get_available_tables

class AbstractFooty(metaclass = ABCMeta): 
    """ Abstract class for PyRef data. Should be inherited for all other
    classes

    """

    @property
    @abstractmethod
    def name(self):
        pass

    @name.setter
    @abstractmethod
    def name(self, value):
        pass

    @property
    @abstractmethod
    def valid_tables(self, fbref_url, name):
        pass

    @abstractmethod
    def get_table(self, table_type):
        pass

    @abstractmethod
    def get_tables(self):
        pass

class FBref(AbstractFooty):
    """ Generic fbref object
    """
    fbref_url = "https://fbref.com/search/search.fcgi?search"

    def __init__(self, name):
        self._name = _validate_name(FBref.fbref_url, name)
        self._valid_tables = get_available_tables(
            FBref.fbref_url, self.name,
        )

    @property
    def name(self):
        return self._name

    @property
    def valid_tables(self):
        return self._valid_tables

    def get_table(self, table_type="Standard Stats"):
        """
        Grab a single table from a player's page

        Parameters
        ------------
        table_type : str, default="Standard Stats"
            Table type to grab from fbref.

        Returns
        -------
        df : Pandas.DataFrame
            DataFrame of `table_type`
        """
        if table_type not in self.valid_tables:
            raise ValueError(f"Invalid table type requested: {table_type}")
        soup = get_soup(FBref.fbref_url, self.name)
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
        Grab all available tables from a FBref page

        Returns
        -------
        df_dict : dict
            Dictionary of DataFrame objects
        """
        soup = get_soup(FBref.fbref_url, self.name)
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


def _validate_name(url, name):
    if not isinstance(name, str):
        raise TypeError("Search name must be a string")
    soup = get_soup(url, name)
    strong_str = [i.next_element for i in soup.findAll("strong")]
    title = soup.find("title")
    if "0 hits" in strong_str:
        raise ValueError(f"`{name}` not found in FBRef")
    if "Search Results" in title.next_element:
        # Grab first search result
        search = soup.findAll("div", {"class": "search-item-alt-names"})[0]
        search_name = search.contents[0]
        msg = f"Exact match for {name} not found.  Setting `name` to first search result: {search_name}"
        warnings.warn(msg)
        name = search_name
    return name
