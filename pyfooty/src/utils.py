import requests
import re
from bs4 import BeautifulSoup

def get_soup(fbref_url, name=None):
    if name:
        fbref_url += "=" + name
    response = requests.get(fbref_url)
    comm = re.compile("<!--|-->")
    soup = BeautifulSoup(comm.sub("", response.text), "lxml")

    return soup

def get_available_tables(url, name=None):
    """ Get available tables for specific player or team"""
    soup = get_soup(url, name)
    all_divs = soup.findAll("div", {"class": "table_wrapper"})
    div = tuple([x.find("span")["data-label"] for x in all_divs])
    return div
