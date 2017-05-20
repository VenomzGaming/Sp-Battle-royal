from random import choice
from time import time

from engines.server import global_vars
from engines.sound import Sound



## ALL DECLARATION

__all__ = (
    'Sprint',
    'SPRINT_START_SOUND',
    'LOW_STAMINA_SOUND',
)

## GLOBALS

SPRINT_START_SOUND = Sound('player/suit_sprint.wav')

LOW_STAMINA_SOUND = Sound('player/suit_denydevice.wav')

STEP_SOUNDS = [
    'npc/combine_soldier/gear1.wav',
    'npc/combine_soldier/gear2.wav',
    'npc/combine_soldier/gear3.wav',
    'npc/combine_soldier/gear4.wav',
    'npc/combine_soldier/gear5.wav',
    'npc/combine_soldier/gear6.wav',
]

STEP_SOUND_INTERVAL = 0.3
DEFAULT_PLAYER_SPEED = 1
SPRINTING_PLAYER_SPEED = 1.2
AIRBORNE_PLAYER_SPEED = 1

## CLASS

class Sprint:
    def __init__(self, player):
        self.player = player
        self.sprinting = False
        self.key_pressed = False
        self.speed = 0
        self.last_step = 0

        self._step_sounds = []
        for sound_path in STEP_SOUNDS:
            self._step_sounds.append(Sound(sound_path, player.index))

    def ensure_speed(self, speed):
        if self.speed != speed:
            self.speed = speed
            self.player.speed = speed

    def step(self):
        cur_step = time()
        if cur_step - self.last_step >= STEP_SOUND_INTERVAL:
            choice(self._step_sounds).play()
            self.last_step = cur_step


# @OnTick
# def listener_on_tick():
#     for sprinting_player in player_manager.values():
#         if sprinting_player.player.ground_entity == -1:
#             sprinting_player.ensure_speed(AIRBORNE_PLAYER_SPEED)
#         else:
#             if sprinting_player.sprinting:
#                 sprinting_player.ensure_speed(SPRINTING_PLAYER_SPEED)
#             else:
#                 sprinting_player.ensure_speed(DEFAULT_PLAYER_SPEED)

#         if sprinting_player.sprinting:
#             inthandle = sprinting_player.player.active_weapon
#             if inthandle == INVALID_ENTITY_INTHANDLE:
#                 continue

#             entity = Entity(index_from_inthandle(inthandle))
#             entity.next_attack = global_vars.current_time + 1
#             entity.next_secondary_fire_attack = global_vars.current_time + 1