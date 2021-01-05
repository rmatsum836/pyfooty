import pytest
from pyfooty.src.club import Club


class TestClub(object):
    @pytest.mark.parametrize("club_name", ("Chelsea", "Real Madrid", "Barcelona"))
    def test_club_name(self, club_name):
        assert club_name in Club(club_name).name

    def test_club_year(self):
        chelsea = Club("Chelsea FC", 2019)
        assert chelsea.year == 2019

    def test_club_tables(self):
        club_obj = Club("Chelsea FC", 2019)

        assert len(club_obj.valid_tables) == 13

    @pytest.mark.parametrize(
        "table_type",
        (
            "Shooting",
            "Scores & Fixtures",
            "Goalkeeping",
            "Passing",
            "Pass Types",
            "Goal and Shot Creation",
            "Defensive Actions",
            "Possession",
            "Miscellaneous Stats",
        ),
    )
    def test_club_matchlog(self, table_type):
        club_obj = Club("Chelsea FC", 2019)
        club_obj.get_matchlog(table_type)

    def test_club_float(self):
        with pytest.raises(TypeError):
            Club(43)

    def test_club_invalid_year(self):
        with pytest.raises(TypeError):
            Club("Chelsea FC", 2000.0)
        with pytest.raises(ValueError):
            Club("Chelsea FC", 1900)

    def test_get_club_table(self):
        chelsea = Club("Chelsea FC", 2019)
        chelsea.get_table("Standard Stats")

    def test_get_all_tables(self):
        manu = Club("Manchester United", 1999)
        manu.get_tables()

    def test_invalid_club(self):
        with pytest.raises(ValueError):
            Club("Charlotte Hornets")

    def test_invalid_table(self):
        juventus = Club("Juventus", 2008)
        with pytest.raises(ValueError):
            juventus.get_table("Free throws")
