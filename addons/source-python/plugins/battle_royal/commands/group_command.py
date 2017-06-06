## IMPORTS

import re
from commands import CommandReturn
from commands.typed import TypedSayCommand
from messages import SayText2
from players.entity import Player

from .filter import Filter
from ..entity.battleroyal import _battle_royal
from ..entity.group import BattleRoyalGroup
from ..menus.group import group_menu


## CLASS COMMAND GROUP

class CommandGroup:
    '''
        CommandGroup manage all group command
        executed by a player.
        :param Object command_info:
            TypedSayCommand info
        :param str use_filter (default=False)
            Use filter to get player.
    '''

    def __init__(self, command_info, use_filter=False):
        self.caller = _battle_royal.get_player(Player(command_info.index)) if command_info.index is not None else None

        if len(command_info.command) >= 2:
            self.type, self.filter, self.args = self._parse_command(command_info)
            
            if not use_filter:
                self.args = self.filter
                self.filter = None
            else:
                self.target = self._get_player()

    @staticmethod
    def _parse_command(command_info):
        '''Method used to parse the command info.'''
        command = list(command_info.command)
        command_name = re.sub(r'(!|/)', '', command[0])
        command_filter = command[1]
        args = ','.join(command[2:])
        return (command_name, command_filter, args)


    def _get_player(self):
        '''Get filter player'''
        find = None
        players = [user for user in Filter(self.filter, self.caller)]

        if len(players) == 0:
            if self.caller is not None:
                SayText2('Not Found').send(self.caller.index)
            else:
                print('Player not found.')
        else:
            find = players
        return find

    def _check_group(self):
        '''Check if owner have already a group'''
        if self.caller.group == None:
            SayText2('You have any group').send()
            return False
        return True

    def _check_owner(self):
        '''Check if player is group's owner.'''
        if self.caller.group.owner.userid != self.caller.userid:
            SayText2('You must be the owner to manage the group').send()
            return False
        return True

    def create(self):
        '''Create a group.'''
        if self._check_group():
            SayText2('You have already a group.').send()
            return

        if self.args not in _battle_royal.teams:
            group = BattleRoyalGroup(self.caller, self.args)
            _battle_royal.add_team(group)
            SayText2('Group ' + group.name + ' created').send()
        else:
            SayText2('Group already exist').send()

    def delete(self):
        '''Delete a group.'''
        if not self._check_owner():
            return

        if self.caller.group.name in _battle_royal.teams:
            team = self.caller.group
            _battle_royal.remove_team(team)
            for player in team:
                player.group = None
            SayText2('Group deleted').send()
        else:
            SayText2('Group does not exist').send()

    def leave(self):
        '''Leave a group.'''
        if not self._check_group:
            return False

        group = self.caller.group    
        group.remove_player(self.caller)
        if len(group.players) == 0 and group.name in _battle_royal.teams:
            _battle_royal.remove_team(group)
            del group

    def add_player(self):
        '''Add player to group.'''
        if not self._check_group and not self._check_owner:
            return False

        if not isinstance(self.target, list):
            SayText2('More thant one player').send()
        else:
            if self.target is not None:
                group_menu.sender = self.caller
                group_menu.send(self.target.index)
            else:
                SayText2('Player with ' + self.filter + ' is not found').send()

    def remove_player(self):
        '''Remove player from group'''
        if not self._check_group and not self._check_owner:
            return False

        if not isinstance(self.target, list):
            SayText2('More thant one player').send()
        else:
            br_player = _battle_royal.get_player(self.target)
            self.caller.group.remove_player(br_player)
            SayText2('Removed ' + br_player.name + ' from the group').send()


## GROUP COMMANDS

@TypedSayCommand('/create')
@TypedSayCommand('!create')
def _create_group(command_info, group_name:str):
    command = CommandGroup(command_info)
    command.create()
    return CommandReturn.BLOCK


@TypedSayCommand('/delete')
@TypedSayCommand('!delete')
def _create_group(command_info):
    command = CommandGroup(command_info)
    command.delete()
    return CommandReturn.BLOCK


@TypedSayCommand('/invit')
@TypedSayCommand('!invit')
@TypedSayCommand('/group')
@TypedSayCommand('!group')
def _invit_to_group(command_info, filter_value:str):
    command = CommandGroup(command_info, True)
    command.add_player()
    return CommandReturn.BLOCK


@TypedSayCommand('/leave')
@TypedSayCommand('!leave')
def _invit_to_group(command_info):
    command = CommandGroup(command_info)
    command.leave()
    return CommandReturn.BLOCK


@TypedSayCommand('/remove')
@TypedSayCommand('!remove')
def _remove_to_group(command_info, filter_value:str):
    command = CommandGroup(command_info, True)
    command.remove_player()
    return CommandReturn.BLOCK