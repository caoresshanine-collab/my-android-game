import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Dynamic Fullscreen Mobile Setup for Pydroid 3
info = pygame.display.Info()
W, H = info.current_w, info.current_h
screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
pygame.display.set_caption("Flappy Bird Mobile with Menu")
clock = pygame.time.Clock()

# Responsive Font Scaling
font_title = pygame.font.SysFont("arial", int(H * 0.07), bold=True)
font_score = pygame.font.SysFont("arial", int(H * 0.06), bold=True)
font_msg = pygame.font.SysFont("arial", int(H * 0.035), bold=True)
font_btn = pygame.font.SysFont("arial", int(H * 0.03), bold=True)

# Theme Palette Colors
SKY_BLUE = (113, 197, 207)
BIRD_YELLOW = (250, 218, 94)
WING_COLOR = (240, 190, 40)
ORANGE_BEAK = (245, 130, 32)
PIPE_GREEN = (115, 191, 46)
WHITE = (255, 255, 255)
DARK_GRAY = (50, 50, 50)
BUTTON_COLOR = (230, 90, 40)
BUTTON_HOVER = (250, 110, 60)

# Scaled Mobile Game Parameters
GRAVITY = H * 0.0004
FLAP_STRENGTH = -H * 0.0105
PIPE_SPEED = W * 0.0065
PIPE_GAP = int(H * 0.23)       
PIPE_WIDTH = int(W * 0.15)

# Game States Constants
MENU, PLAYING, GAMEOVER = "menu", "playing", "gameover"
state = MENU

class MobileBird:
    def __init__(self):
        self.x = W * 0.25
        self.y = H // 2
        self.velocity = 0
        self.radius = int(H * 0.025)
        self.wing_angle = 0

    def update(self, is_playing=True):
        if is_playing:
            self.velocity += GRAVITY
            self.y += self.velocity
            # Animate wing oscillation directly mapped to velocity
            self.wing_angle += 0.2 + (abs(self.velocity) * 0.05)
        else:
            # Menu hover float effect
            self.wing_angle += 0.15

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def draw(self, time_tick=0):
        # 1. Draw Wing Profiles (Flaps dynamically up/down)
        if state == MENU:
            wing_sweep = math.sin(self.wing_angle) * (self.radius * 0.8)
        else:
            # Flapping tracking matches downward physics trajectory acceleration 
            wing_sweep = math.sin(self.wing_angle) * (self.radius * 0.8) if self.velocity < 0 else (self.radius * 0.4)
            
        # Draw Left/Back Wing Anchor Point
        pygame.draw.ellipse(screen, WING_COLOR, (int(self.x - self.radius * 0.8), int(self.y - wing_sweep), int(self.radius * 0.9), int(self.radius * 0.6)))

        # 2. Draw Main Rounded Bird Core Body
        pygame.draw.circle(screen, BIRD_YELLOW, (int(self.x), int(self.y)), self.radius)
        
        # 3. Draw Beak Element
        beak_pts = [
            (self.x + self.radius * 0.8, self.y - self.radius * 0.2),
            (self.x + self.radius * 1.4, self.y),
            (self.x + self.radius * 0.8, self.y + self.radius * 0.3)
        ]
        pygame.draw.polygon(screen, ORANGE_BEAK, beak_pts)

        # 4. Draw Face/Eye Accents
        eye_offset = int(self.radius * 0.4)
        eye_size = max(2, int(self.radius * 0.25))
        pupil_size = max(1, int(self.radius * 0.1))
        pygame.draw.circle(screen, WHITE, (int(self.x + eye_offset), int(self.y - eye_offset)), eye_size)
        pygame.draw.circle(screen, DARK_GRAY, (int(self.x + eye_offset + 1), int(self.y - eye_offset)), pupil_size)

class MobilePipe:
    def __init__(self, x):
        self.x = x
        self.width = PIPE_WIDTH
        self.top_height = random.randint(int(H * 0.1), H - PIPE_GAP - int(H * 0.15))
        self.bottom_y = self.top_height + PIPE_GAP
        self.bottom_height = H - self.bottom_y
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self):
        pygame.draw.rect(screen, PIPE_GREEN, (self.x, 0, self.width, self.top_height))
        pygame.draw.rect(screen, PIPE_GREEN, (self.x, self.bottom_y, self.width, self.bottom_height))

    def collide(self, bird):
        if bird.x + bird.radius > self.x and bird.x - bird.radius < self.x + self.width:
            if bird.y - bird.radius < self.top_height or bird.y + bird.radius > self.bottom_y:
                return True
        return False

class TouchButton:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        # Center checking relative to click position updates
        m_pos = pygame.mouse.get_pos()
        color = BUTTON_HOVER if self.rect.collidepoint(m_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, WHITE, self.rect, width=2, border_radius=12)
        
        txt_surface = font_btn.render(self.text, True, WHITE)
        screen.blit(txt_surface, txt_surface.get_rect(center=self.rect.center))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def reset_mobile_game():
    spawn_interval = int(W * 0.55)
    return MobileBird(), [MobilePipe(W + 50), MobilePipe(W + 50 + spawn_interval)], 0

# Instantiate layout entities
bird, pipes, score = reset_mobile_game()
menu_bird = MobileBird()
menu_bird.x = W // 2
menu_bird.y = H * 0.38

# Responsive Button sizing calculations
btn_w, btn_h = int(W * 0.5), int(H * 0.08)
play_btn = TouchButton((W - btn_w) // 2, int(H * 0.55), btn_w, btn_h, "PLAY")
retry_btn = TouchButton((W - btn_w) // 2, int(H * 0.58), btn_w, btn_h, "TRY AGAIN")
menu_btn = TouchButton((W - btn_w) // 2, int(H * 0.68), btn_w, btn_h, "MAIN MENU")

# --- MOBILE CORE RUNTIME LOOP ---
while True:
    dt = clock.tick(60)
    screen.fill(SKY_BLUE)
    
    # Process inputs natively from screen touch points
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.FINGERDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            # Handle touch coordinates capture securely across platforms
            pos = event.pos if hasattr(event, 'pos') else pygame.mouse.get_pos()
            
            if state == MENU:
                if play_btn.is_clicked(pos):
                    bird, pipes, score = reset_mobile_game()
                    state = PLAYING
                    bird.flap()
                    
            elif state == PLAYING:
                bird.flap()
                
            elif state == GAMEOVER:
                if retry_btn.is_clicked(pos):
                    bird, pipes, score = reset_mobile_game()
                    state = PLAYING
                    bird.flap()
                elif menu_btn.is_clicked(pos):
                    state = MENU

    # --- STATE MANAGEMENT CONTROLLERS ---
    if state == MENU:
        # Title design and floating preview display
        title_txt = font_title.render("FLAPPY BIRD", True, WHITE)
        screen.blit(title_txt, ((W - title_txt.get_width()) // 2, int(H * 0.15)))
        
        # Idle floating math sequence calculations for title screen bird asset
        menu_bird.y = (H * 0.35) + math.sin(pygame.time.get_ticks() * 0.005) * 15
        menu_bird.update(is_playing=False)
        menu_bird.draw()
        
        play_btn.draw()

    elif state == PLAYING:
        bird.update(is_playing=True)
        
        if bird.y + bird.radius >= H or bird.y - bird.radius <= 0:
            state = GAMEOVER

        for pipe in pipes:
            pipe.update()
            if pipe.collide(bird):
                state = GAMEOVER
                
            if not pipe.passed and pipe.x + pipe.width < bird.x:
                pipe.passed = True
                score += 1

        if pipes[0].x < -PIPE_WIDTH:
            pipes.pop(0)
            spawn_interval = int(W * 0.55)
            pipes.append(MobilePipe(pipes[-1].x + spawn_interval))

        # Render gameplay environment layout 
        for pipe in pipes:
            pipe.draw()
        bird.draw()

        # Center aligned running score text layout overlay
        score_txt = font_score.render(str(score), True, WHITE)
        screen.blit(score_txt, ((W - score_txt.get_width()) // 2, int(H * 0.05)))

    elif state == GAMEOVER:
        # Freeze and draw current scene layout backdrop layer elements
        for pipe in pipes:
            pipe.draw()
        bird.draw()

        # Display Game Over window configurations panels
        go_txt = font_title.render("GAME OVER", True, DARK_GRAY)
        screen.blit(go_txt, ((W - go_txt.get_width()) // 2, int(H * 0.2)))
        
        fs_txt = font_msg.render(f"Final Score: {score}", True, WHITE)
        screen.blit(fs_txt, ((W - fs_txt.get_width()) // 2, int(H * 0.32)))
        
        retry_btn.draw()
        menu_btn.draw()

    pygame.display.update()
