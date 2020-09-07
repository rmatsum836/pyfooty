import requests
import re
import pandas as pd
from bs4 import BeautifulSoup


class Player(object): 
    search_url = "https://fbref.com/search/search.fcgi?search"

    def __init__(self, player_name):
        if not isinstance(player_name, str):
            raise TypeError("Player name must be a string")
        self.name = player_name

    def __repr__(self):
        desc = "<player: {}, id: {}>".format(self.name, id(self))
        return desc

    def get_tables(self):
        search = player.search_url + "=" + self.name
        response = requests.get(search)
        comm = re.compile("<!--|-->")
        soup = BeautifulSoup(comm.sub("", response.text), "lxml")
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
            rows = table.find_all('tr')
            for row in rows:
                if row.find('th', {'scope': 'row'}) != None:
                    cells = row.find_all('td')
                    for cell in cells:
                        cell_text = cell.text.encode()
                        text = cell_text.decode("utf-8")
                        try:
                            text = float(text)
                        except ValueError:
                            pass
                        if cell['data-stat'] in pre_df_dict.keys():
                            pre_df_dict[cell['data-stat']].append(text)
                        else:
                            pre_df_dict[cell['data-stat']] = [text]

            df = pd.DataFrame.from_dict(pre_df_dict)
            df_dict[f'{label}'] = df

        return df_dict

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


if __name__ == "__main__":
    puli = Player("Christian pulisic")
    #puli.get_table()
    print(puli)
