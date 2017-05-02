## IMPORTS

from messages import SayText2


## ALL DECLARATIONS

__all__ = (
    'BattleRoyalGroup',
)


class BattleRoyalGroup:

    def __init__(self, owner, name):
        self._owner = owner
        self._name = name
        self._players = []
        self._players.append(owner)

    @property
    def owner(self):
        return self._owner

    @property
    def name(self):
        return self._name

    @property
    def players(self):
        return self._players

    def add_player(self, player):
        if player not in self._players:
            self._players.append(player)
            player.group = self
        else:
            SayText2('Already in group').send()

    def remove_player(self, player):
        if player in self._players:
            self._players.remove(player)
            player.group = None
        else:
            SayText2('Player is not in group').send()
       