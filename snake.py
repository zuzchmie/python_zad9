import pygame
import random
import time

pygame.init()


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 30  
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 4  


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)
RED = (200, 0, 0)


GAME_DURATION = 60  
FRUIT_LIFESPAN = 5  


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Uproszczony Wąz")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)



def draw_element(position, color):
    x = position[0] * GRID_SIZE
    y = position[1] * GRID_SIZE
    rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, color, rect)

def move_snake(snake, direction):
    head_x, head_y = snake[0]
    dir_x, dir_y = direction
    
    new_head_x = (head_x + dir_x) % GRID_WIDTH
    new_head_y = (head_y + dir_y) % GRID_HEIGHT

    new_head = (new_head_x, new_head_y)
    snake.insert(0, new_head)
    
    return snake, new_head

def check_invalid_move(current_dir, new_dir):
    return current_dir[0] == -new_dir[0] and current_dir[1] == -new_dir[1]

def generate_fruit(snake_coords):
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake_coords:
            return pos



def game_loop():
    
    running = True
    game_over = False
    
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (1, 0)  
   
    fruit_pos = None
    fruit_spawn_time = 0
    score = 0
    should_grow = False
    
    start_time = time.time()
    
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if not game_over and event.type == pygame.KEYDOWN:
                new_direction = direction
                if event.key == pygame.K_UP:
                    new_direction = (0, -1)
                elif event.key == pygame.K_DOWN:
                    new_direction = (0, 1)
                elif event.key == pygame.K_LEFT:
                    new_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    new_direction = (1, 0)
                if new_direction != direction and check_invalid_move(direction, new_direction):
                    game_over = True
                else:
                    direction = new_direction

        if not game_over:
            elapsed_time = time.time() - start_time
            if elapsed_time >= GAME_DURATION:
                game_over = True
            if fruit_pos and time.time() - fruit_spawn_time > FRUIT_LIFESPAN:
                fruit_pos = None  
            if fruit_pos is None:
                fruit_pos = generate_fruit(snake)
                fruit_spawn_time = time.time()
            
            snake, new_head = move_snake(snake, direction)
            
            if new_head == fruit_pos:
                score += 1
                fruit_pos = None  
                should_grow = True  
            else:
                should_grow = False
            if not should_grow and len(snake) > 1:
                snake.pop()      
            if new_head in snake[1:]:
                 game_over = True
        screen.fill(BLACK)
        if fruit_pos:
            draw_element(fruit_pos, RED)
        for segment in snake:
            draw_element(segment, GREEN)

        
        time_left = max(0, GAME_DURATION - int(elapsed_time))
        score_text = font.render(f"Owoce: {score}", True, WHITE)
        time_text = font.render(f"Czas: {time_left}s", True, WHITE)
        
        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (SCREEN_WIDTH - time_text.get_width() - 10, 10))

        
        if game_over:
            end_message = "KONIEC GRY!"
            reason = "Upłynął czas." if elapsed_time >= GAME_DURATION else "Niedozwolony ruch."
            
            end_text1 = font.render(end_message, True, RED)
            end_text2 = font.render(f"Wynik: {score} owoców. {reason}", True, WHITE)
            
            rect1 = end_text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
            rect2 = end_text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
            
            screen.blit(end_text1, rect1)
            screen.blit(end_text2, rect2)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    game_loop()