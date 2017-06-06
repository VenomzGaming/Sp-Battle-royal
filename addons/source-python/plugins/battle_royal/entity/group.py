## IMPORTS

from messages import SayText2


## ALL DECLARATIONS

__all__ = (
    'BattleRoyalGroup',
)


class BattleRoyalGroup:
    '''
        BattleRoyalGroup manage all players group.
        :param BattleRoyalPlayer owner:
            The owner of the group.
        :param str name:
            Name of the group (for the moment string without spaces)

    '''
    
    limit_player = 2

    def __init__(self, owner, name):
        self._owner = owner
        self.name = name
        self._players = []
        self.add_player(owner)

    @property
    def owner(self):
        'Return :class BattleRoyalPlayer'
        return self._owner

    @property
    def players(self):
        'Return a list of all grouped players.'
        return self._players

    def is_in_group(self, player):
        'Check if the player is in group.'
        return player in self._players

    def add_player(self, player):
        'Add player in group if it is not full.'
        if len(self._players) < self.limit_player:
            if player not in self._players:
                self._players.append(player)
                player.group = self
            else:
                SayText2('Already in a group').send()
        else:
            SayText2('Limit player exceed').send()

    def remove_player(self, player):
        'Remove player from the group.'
        if player in self._players:
            self._players.remove(player)
            player.group = None
        else:
            SayText2('Player is not in group').send()
       