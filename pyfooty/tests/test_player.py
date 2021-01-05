import pytest
from pyfooty.src.player import Player


class TestPlayer(object):
    @pytest.mark.parametrize(
        "player", ("Mason Mount", "Christian Pulisic", "Frank Lampard", "Eden Hazard")
    )
    def test_player_name(self, player):
        assert Player(player).name == player

    @pytest.mark.parametrize(
        "player", ("Mason Mount", "Christian Pulisic", "Eden Hazard")
    )
    def test_player_tables(self, player):
        player_obj = Player(player)
        player_obj.get_tables()

        assert len(player_obj.tables) == 10

    def test_player_float(self):
        with pytest.raises(TypeError):
            Player(43)

    def test_invalid_player(self):
        with pytest.raises(ValueError):
            Player("Lebron James")

    def test_search_warning(self):
        with pytest.warns(UserWarning):
            Player("Jorginho")

    @pytest.mark.parametrize(
        "table_type",
        (
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
        ),
    )
    def test_player_table(self, table_type):
        player_obj = Player("Mason Mount")
        player_obj.get_table(table_type)

    def test_table_not_found(self):
        with pytest.raises(ValueError):
            player_obj = Player("Frank Lampard")
            player_obj.get_table("Possession")

    def test_invalid_table(self):
        with pytest.raises(ValueError):
            player_obj = Player("Eden Hazard")
            player_obj.get_table("Real Madrid")

    def test_valid_tables(self):
        assert len(Player("Frank Lampard").valid_tables) == 5

    def test_repr(self):
        print(Player("Cristiano Ronaldo"))
