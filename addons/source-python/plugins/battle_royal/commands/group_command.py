## IMPORTS

import re
from commands.typed import TypedSayCommand, CommandReturn
from messages import SayText2
from players.entity import Player

from . import Filter
from .manager import command_manager


## CLASS COMMAND GROUP

class CommandGroup:

    def __init__(self, command_info):
        self.type, self.filter, self.args = self._parse_command(command_info)
        self.caller = _battle_royal.get_player(Player(command_info.index)) if command_info.index is not None else None
        self.target = self._get_player()


    @staticmethod
    def _parse_command(command_info):
        command = list(command_info.command)
        command_name = re.sub(r'(!|/)', '', command[0])
        command_filter = command[1]
        args = ','.join(command[2:])
        return (command_name, command_filter, args)


    def _get_player(self):
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
        if self.caller.group == None:
            SayText2('You have any group').send()
            return False

        if self.caller.group.owner.userid != self.caller.userid:
            SayText2('You must be the owner to manage the group').send()
            return True

    def _check_group(self):
        if self.caller.group == None:
            SayText2('You have any group').send()
            return False
        return True

    def _check_owner(self):
        if self.caller.group.owner.userid != self.caller.userid:
            SayText2('You must be the owner to manage the group').send()
            return False
        return True

    def create(self):
        if group_name not in _battle_royal.teams:
            group = BattleRoyalGroup(self.caller, group_name)
            _battle_royal.add_team(group)
            SayText2('Group ' + group.name + ' created').send()
        else:
            SayText2('Group already exist').send()

    def delete(self):
        if self.caller.group.name in _battle_royal.teams:
            team = _battle_royal.get_team(self.caller.group.name)
            _battle_royal.remove_team(team)
            for player in team:
                player.group = None
            SayText2('Group deleted').send()
        else:
            SayText2('Group does not exist').send()

    def leave(self):
        if not self._check_group:
            return False
        group = self.caller.group    
        group.remove_player(self.caller)
        if len(group.players) == 0 and group.name in _battle_royal.teams:
            _battle_royal.remove_team(group)
            del group


    def add_player(self):
        if not self._check_group and not self._check_owner:
            return False

        if not isinstance(self.target, list):
            SayText2('More thant one player').send()
        else:
            if self.target is not None:
                br_player = _battle_royal.get_player(self.target)
                self.caller.group.add_player(br_player)
                SayText2('Added ' + br_player.name + ' to group').send()
            else:
                SayText2('Player with ' + self.filter + ' is not found').send()

    def remove_player(self):
        if not self._check_group and not self._check_owner:
            return False

        if not isinstance(self.target, list):
            SayText2('More thant one player').send()
        else:
            br_player = _battle_royal.get_player(self.target)
            self.caller.group.remove_player(br_player)
            SayText2('Removed ' + br_player.name + ' from the group').send()


## GROUP COMMANDS

@TypedSayCommand(['!create', '/create'])
def _create_group(command_info, group_name:str):
    command = CommandGroup(command_info)
    command.create()
    return CommandReturn.BLOCK


@TypedSayCommand(['!delete', '/delete'])
def _create_group(command_info):
    command = CommandGroup(command_info)
    command.delete()
    return CommandReturn.BLOCK


@TypedSayCommand(['!invit', '/invit', '!group', '/group'])
def _invit_to_group(command_info, filter_value:str):
    command = CommandGroup(command_info)
    command.add_player()
    return CommandReturn.BLOCK


@TypedSayCommand(['!leave', '/leave'])
def _invit_to_group(command_info, filter_value:str):
    command = CommandGroup(command_info)
    command.leave()
    return CommandReturn.BLOCK


@TypedSayCommand(['!remove', '/remove'])
def _remove_to_group(command_info, filter_value:str):
    command = CommandGroup(command_info)
    command.remove_player()
    return CommandReturn.BLOCK