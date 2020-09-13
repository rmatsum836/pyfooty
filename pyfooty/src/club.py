from pyfooty.src.baseclass import FBref
from pyfooty.src.utils import get_soup, get_available_tables
import warnings

class Club(FBref):
    """A Club object.

    The Club object represents a soccer club with available data from FBRef.com.

    Parameters
    ----------
    club_name : str
        Name of team to search on FBRef

    Attributes
    ---------
    name : str
        Name of team to search on FBRef
    valid_tables : tuple
        Tuple of valid tables
    """
    def __init__(self, club_name):
        self._name = _validate_name(FBref.fbref_url, club_name)
        self._valid_tables = get_available_tables(
            FBref.fbref_url, self.name,
        )

    def __repr__(self):
        desc = "<club: {}, id: {}>".format(self.name, id(self))
        return desc

def _validate_name(url, name):
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
        msg = f"Exact match for {name} not found.  Setting `name` to first search result: {search_name}"
        warnings.warn(msg)
        name = search_name
    return name

if __name__ == "__main__":
    puli = Club("Chelsea")
    standard = puli.get_table("Standard Stats")
