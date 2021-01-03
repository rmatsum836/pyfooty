import requests
import re
from bs4 import BeautifulSoup

def get_soup(fbref_url, name=None):
    """ Get soup of FBRef URL

    Parameters
    ----------
    fbref_url : str
        Url of FBRef. Can either be the search url or an exact match url
    name : str
        Name to search for, must be used with the search url.
    """
    if name:
        fbref_url += "=" + name
    response = requests.get(fbref_url)
    comm = re.compile("<!--|-->")
    soup = BeautifulSoup(comm.sub("", response.text), "lxml")

    return soup

def get_available_tables(url, name=None):
    """ Get available tables for specific player"""
    soup = get_soup(url, name)
    all_divs = soup.findAll("div", {"class": "table_wrapper"})
    div = tuple([x.find("span")["data-label"] for x in all_divs])
    return div

def get_matchlog_str(table_type):
    """ Get valid strings to get matchlog data"""
    matchlog_dict = {
            "Scores & Fixtures": "schedule",
            "Shooting": "shooting",
            "Goalkeeping": "keeper",
            "Passing": "passing",
            "Pass Types": "passing_types",
            "Goal and Shot Creation": "gca",
            "Defensive Actions": "defense",
            "Possession": "possession",
            "Miscellaneous Stats": "misc",
            }

    return matchlog_dict[table_type]
