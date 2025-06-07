import random
from game import Game

ACTIONS = ['Up', 'Down', 'Left', 'Right']

def rotate_board(board):
    return [list(row) for row in zip(*board[::-1])]

def normalize_state(state):
    board = [list(state[i*4:(i+1)*4]) for i in range(4)]
    boards = []
    b = board
    for _ in range(4):
        boards.append(tuple(tile for row in b for tile in row))
        b = rotate_board(b)
    return max(boards)

def choose_action(q_table, state, epsilon):
    if random.random() < epsilon:
        return random.choice(ACTIONS)
    values = [q_table.get((state, a), 0.0) for a in ACTIONS]
    max_v = max(values)
    best = [a for a, v in zip(ACTIONS, values) if v == max_v]
    return random.choice(best)

def update_q(q_table, state, action, reward, next_state, alpha, gamma):
    max_next = max(q_table.get((next_state, a), 0.0) for a in ACTIONS)
    old = q_table.get((state, action), 0.0)
    q_table[(state, action)] = old + alpha * (reward + gamma * max_next - old)

def play_episode(q_table, epsilon, alpha, gamma):
    game = Game()
    state = normalize_state(game.get_state())
    total = 0
    done = False
    max_tile = game.max_tile()
    while not done:
        action = choose_action(q_table, state, epsilon)
        reward, done = game.step(action)
        total += reward
        max_tile = max(max_tile, game.max_tile())
        next_state = normalize_state(game.get_state())
        update_q(q_table, state, action, reward, next_state, alpha, gamma)
        state = next_state
    return total, max_tile

def train(episodes=1000, epsilon=0.1, alpha=0.1, gamma=0.9):
    q_table = {}
    results = []
    for ep in range(1, episodes + 1):
        score, m_tile = play_episode(q_table, epsilon, alpha, gamma)
        results.append((score, m_tile))
        print("Episode {}: score {} max_tile {}".format(ep, score, m_tile))
    return q_table, results

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--episodes', type=int, default=1000)
    parser.add_argument('--epsilon', type=float, default=0.1)
    parser.add_argument('--alpha', type=float, default=0.1)
    parser.add_argument('--gamma', type=float, default=0.9)
    args = parser.parse_args()
    train(args.episodes, args.epsilon, args.alpha, args.gamma)
