import pytest
from pyfbref.src.player import Player

class TestPlayer(object):
    @pytest.mark.parametrize("player", ("Mason Mount", "Christian
    Pulisic", "Frank Lampard", "Eden Hazard"))
    def test_player_name(self, player):
        Player(player).name = player
