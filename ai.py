import copy
import random


class SimpleAI:
    DIRECTIONS = ['Up', 'Down', 'Left', 'Right']

    CORNER_COORDS = {
        'top-left': (0, 0),
        'top-right': (0, 3),
        'bottom-left': (3, 0),
        'bottom-right': (3, 3),
    }

    def __init__(self, tips=None):
        self.preferred_corner = None
        if tips:
            self.update_preference(tips)

    def update_preference(self, tips):
        counts = {}
        for t in tips:
            if t.startswith('corner:'):
                corner = t.split(':')[1]
                counts[corner] = counts.get(corner, 0) + 1
        if counts:
            self.preferred_corner = max(counts, key=counts.get)

    def choose_move(self, game):
        evaluations = []
        best_value = -1
        best_dir = None
        for d in self.DIRECTIONS:
            temp = copy.deepcopy(game)
            changed, gained = temp.move(d)
            if not changed:
                evaluations.append("{}: invalid move".format(d))
                continue
            empties = sum(row.count(0) for row in temp.board)
            value = gained + empties * 2
            corner_score = 0
            if self.preferred_corner:
                r, c = self.CORNER_COORDS[self.preferred_corner]
                corner_score = temp.board[r][c]
                value += corner_score
            evaluations.append(
                "{}: gain {}, empty {}, corner {}".format(d, gained, empties, corner_score)
            )
            if value > best_value:
                best_value = value
                best_dir = d
        if best_dir is None:
            return None, "No valid moves left"
        explanation = " | ".join(evaluations) + " => choose {}".format(best_dir)
        return best_dir, explanation

