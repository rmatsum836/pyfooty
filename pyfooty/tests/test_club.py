import pytest
from pyfooty.src.club import Club

class TestClub(object):
    @pytest.mark.parametrize(
        "club_name", ("Chelsea", "Real Madrid", "Barcelona")
    )
    def test_club_name(self, club_name):
        assert club_name in Club(club_name).name

    def test_club_year(self):
        chelsea = Club("Chelsea FC", 2019)
        assert chelsea.year == 2019

    def test_club_tables(self):
        club_obj = Club("Chelsea FC", 2019)

        assert len(club_obj.valid_tables) == 13

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
