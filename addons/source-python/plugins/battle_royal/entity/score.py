## IMPORTS

from ..config import _configs


## ALL DECLARATION

__all__ = (
    'ScoreAmount',
    'Score',
)


## CLASS

class ScoreAmount:
    HEADSHOT = _configs['score_headshot'].get_int()
    KILL = _configs['score_kill'].get_int()
    ASSIST = _configs['score_assist'].get_int()


class Score:
    '''
        Score manage all players score of the Battle royal game.
        :param BattleRoyalPlayer player:
            A player
    '''

    additional_score = 0

    def __init__(self, player):
        self._player = player

    def update_additional_score(self, score):
        'Update additional score.'
        self.additional_score = score

    def set_score(self, headshot=False, assist=False):
        'Set player score.'
        score_amount = self.additional_score
        if not assist:
            score_amount += ScoreAmount.KILL + (ScoreAmount.HEADSHOT if headshot else 0)
        else:
            score_amount += ScoreAmount.ASSIST

        self._player.score += score_amount

    def get_score(self, score):
        # 'Get player score.'
        return self._player.score



    

