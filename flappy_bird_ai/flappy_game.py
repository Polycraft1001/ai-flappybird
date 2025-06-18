
import pygame
import random

# Constants
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
GRAVITY = 0.25
BIRD_JUMP = -6
PIPE_GAP = 100
PIPE_SPEED = 2

class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 0))  # Yellow bird
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def jump(self):
        self.velocity = BIRD_JUMP

    def move(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.center = (self.x, int(self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Pipe:
    def __init__(self, x, height):
        self.x = x
        self.height = height
        self.top_rect = pygame.Rect(x, 0, 52, height)
        self.bottom_rect = pygame.Rect(x, height + PIPE_GAP, 52, SCREEN_HEIGHT - height - PIPE_GAP)
        self.passed = False

    def move(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.top_rect)  # Green pipes
        pygame.draw.rect(screen, (0, 255, 0), self.bottom_rect)

class Ground:
    def __init__(self):
        self.height = 100
        self.rect = pygame.Rect(0, SCREEN_HEIGHT - self.height, SCREEN_WIDTH, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, (139, 69, 19), self.rect)  # Brown ground

class FlappyGame:
    def __init__(self, headless=False):
        pygame.init()
        self.headless = headless
        if not headless:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Flappy Bird AI")
        self.clock = pygame.time.Clock()
        self.reset_game()
        self.last_score_check = 0 # Initialize here

    def reset_game(self):
        self.bird = Bird()
        self.pipes = []
        self.ground = Ground()
        self.score = 0
        self.game_over = False
        self.spawn_pipe()

    def spawn_pipe(self):
        pipe_height = random.randint(50, SCREEN_HEIGHT - self.ground.height - PIPE_GAP - 50)
        self.pipes.append(Pipe(SCREEN_WIDTH, pipe_height))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def update(self):
        if self.game_over:
            return

        self.bird.move()

        # Move and remove pipes
        for pipe in self.pipes:
            pipe.move()
            if pipe.x < -52:
                self.pipes.remove(pipe)

            # Check if pipe passed
            if not pipe.passed and pipe.x < self.bird.x:
                pipe.passed = True
                self.score += 1
                if not self.headless:
                    print(f"Score: {self.score}")

        # Spawn new pipes
        if len(self.pipes) == 0 or self.pipes[-1].x < SCREEN_WIDTH - 150:
            self.spawn_pipe()

        # Collision detection
        if self.bird.rect.colliderect(self.ground.rect) or self.bird.y < 0:
            self.game_over = True
        for pipe in self.pipes:
            if self.bird.rect.colliderect(pipe.top_rect) or self.bird.rect.colliderect(pipe.bottom_rect):
                self.game_over = True

    def draw(self):
        if not self.headless:
            self.screen.fill((135, 206, 235))  # Sky blue background
            self.bird.draw(self.screen)
            for pipe in self.pipes:
                pipe.draw(self.screen)
            self.ground.draw(self.screen)
            pygame.display.update()

    def get_state(self):
        # Find the next pipe
        next_pipe = None
        for pipe in self.pipes:
            if pipe.x + 52 > self.bird.x:
                next_pipe = pipe
                break

        if next_pipe:
            vertical_distance = self.bird.y - (next_pipe.top_rect.height + PIPE_GAP / 2)
            horizontal_distance = next_pipe.x - self.bird.x
        else:
            vertical_distance = 0  # No pipe in sight
            horizontal_distance = SCREEN_WIDTH # No pipe in sight

        return (int(vertical_distance), int(horizontal_distance), int(self.bird.velocity))

    def run_frame(self, action=None):
        if action == 1: # Jump
            self.bird.jump()

        self.update()
        if not self.headless:
            self.draw()
            self.clock.tick(60)

        reward = 1  # Reward for staying alive
        if self.game_over:
            reward = -100
        elif self.score > self.last_score_check:
            reward = 5
            self.last_score_check = self.score

        return self.get_state(), reward, self.game_over, self.score

    def run(self):
        self.last_score_check = 0
        while True:
            self.handle_input()
            state, reward, done, score = self.run_frame()
            if done:
                self.reset_game()

if __name__ == '__main__':
    game = FlappyGame()
    game.run()


