import pytest
from pyfbref.src.player import Player


class TestPlayer(object):
    @pytest.mark.parametrize(
        "player", ("Mason Mount", "Christian Pulisic", "Frank Lampard", "Eden Hazard")
    )
    def test_player_name(self, player):
        Player(player).name = player

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
            Player('Lebron James')

    def test_search_warning(self):
        with pytest.warns(UserWarning):
            Player('Jorginho')
