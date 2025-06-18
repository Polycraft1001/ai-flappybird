import pygame
import pickle
import random
from flappy_game import FlappyGame, SCREEN_WIDTH, SCREEN_HEIGHT
from train_ai import discretize_state, VERTICAL_DISTANCE_BINS, HORIZONTAL_DISTANCE_BINS, VELOCITY_BINS

class AIPlayer:
    def __init__(self, q_table_path='q_table.pkl', actions=[0, 1]):
        self.q_table = self.load_q_table(q_table_path)
        self.actions = actions

    def load_q_table(self, path):
        try:
            with open(path, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            print(f"Q-table file not found at {path}. Starting with an empty Q-table.")
            return {}
        except Exception as e:
            print(f"Error loading Q-table: {e}. Starting with an empty Q-table.")
            return {}

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def choose_action(self, state_raw):
        state = discretize_state(state_raw)
        
        # If state is not in Q-table, default to jump (action 1)
        if not any((state, action) in self.q_table for action in self.actions):
            return 1 # Default to jump

        q_values = [self.get_q_value(state, action) for action in self.actions]
        max_q = max(q_values)
        
        # Choose action with highest Q-value. If multiple, pick randomly.
        best_actions = [self.actions[i] for i, q in enumerate(q_values) if q == max_q]
        return random.choice(best_actions)

def play_game_with_ai():
    game = FlappyGame(headless=False)
    ai_player = AIPlayer()

    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        state_raw = game.get_state()
        action = ai_player.choose_action(state_raw)

        _, _, done, score = game.run_frame(action)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        game.screen.blit(score_text, (10, 10))
        pygame.display.update()

        if done:
            game.reset_game()

if __name__ == '__main__':
    play_game_with_ai()


