import pygame
import random
import sys

# تهيئة pygame
pygame.init()

# إعدادات الشاشة
WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20

# الألوان
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# إنشاء الشاشة
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('لعبة الدودة - Snake Game')
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (BLOCK_SIZE, 0)
        
    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        self.body.insert(0, new_head)
        self.body.pop()
        
    def grow(self):
        tail = self.body[-1]
        self.body.append(tail)
        
    def check_collision(self):
        head = self.body[0]
        # التحقق من الاصطدام بالحواف
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return True
        # التحقق من الاصطدام بالجسم
        if head in self.body[1:]:
            return True
        return False
        
    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

class Apple:
    def __init__(self):
        self.position = self.random_position()
        
    def random_position(self):
        x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        return (x, y)
        
    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

def main():
    snake = Snake()
    apple = Apple()
    score = 0
    font = pygame.font.Font(None, 36)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # التحكم بالاتجاهات
                if event.key == pygame.K_UP and snake.direction != (0, BLOCK_SIZE):
                    snake.direction = (0, -BLOCK_SIZE)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -BLOCK_SIZE):
                    snake.direction = (0, BLOCK_SIZE)
                elif event.key == pygame.K_LEFT and snake.direction != (BLOCK_SIZE, 0):
                    snake.direction = (-BLOCK_SIZE, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-BLOCK_SIZE, 0):
                    snake.direction = (BLOCK_SIZE, 0)
        
        snake.move()
        
        # التحقق من أكل التفاحة
        if snake.body[0] == apple.position:
            snake.grow()
            apple.position = apple.random_position()
            score += 1
        
        # التحقق من الاصطدام
        if snake.check_collision():
            print(f'Game Over! النقاط النهائية: {score}')
            running = False
        
        # رسم كل شيء
        screen.fill(BLACK)
        snake.draw(screen)
        apple.draw(screen)
        
        # عرض النقاط
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(10)  # سرعة اللعبة
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
