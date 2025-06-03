import copy
import random

class SimpleAI:
    DIRECTIONS = ['Up', 'Down', 'Left', 'Right']

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
            evaluations.append("{}: gain {}, empty {}".format(d, gained, empties))
            if value > best_value:
                best_value = value
                best_dir = d
        if best_dir is None:
            return None, "No valid moves left"
        explanation = " | ".join(evaluations) + " => choose {}".format(best_dir)
        return best_dir, explanation

