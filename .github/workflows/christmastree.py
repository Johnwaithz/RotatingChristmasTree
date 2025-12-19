import pygame
import math
import random

# --- INITIALIZATION ---
pygame.init()
pygame.mixer.init()

# Initial Window Size
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Happy Holidays!! from Eng Ngugi")
clock = pygame.time.Clock()
FPS = 60

# --- STYLING & ASSETS ---
BG_COLOR = (5, 5, 20)
MUSIC_FILE = "jinglebells.mp3"
pygame.font.init()


def get_font(width):
    # Dynamic font size based on current window width
    return pygame.font.SysFont("georgia", int(width // 20), bold=True)


font = get_font(WIDTH)

try:
    pygame.mixer.music.load(MUSIC_FILE)
    pygame.mixer.music.play(-1)
except:
    print("Music file not found.")


# --- GENERATE TREE POINTS ---
def generate_tree_points(num_points=1200):
    points = []
    for _ in range(num_points):
        h = random.random()
        angle = random.uniform(0, 2 * math.pi)

        # We use relative coordinates (-1 to 1) so they can scale with the window
        radius = (1 - h)
        x = radius * math.cos(angle)
        z = radius * math.sin(angle)
        y = -h  # Vertical normalized

        color = random.choice([(255, 0, 0), (255, 215, 0), (255, 255, 255), (0, 255, 0)])
        points.append({'pos': [x, y, z], 'color': color})
    return points


tree_points = generate_tree_points()
angle_y = 0

# --- MAIN LOOP ---
running = True
while running:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Handle Window Resizing
        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            font = get_font(WIDTH)  # Update font size for new width

    angle_y += 0.02
    projected_points = []

    # Dynamic scaling factors based on current window size
    tree_width_scale = WIDTH * 0.18
    tree_height_scale = HEIGHT * 0.45
    fov = WIDTH * 0.6
    dist = WIDTH * 0.8

    # 1. Project 3D points
    for p in tree_points:
        nx, ny, nz = p['pos']

        # Scale normalized points to window size
        x = nx * tree_width_scale
        y = ny * tree_height_scale + (HEIGHT * 0.25)
        z = nz * tree_width_scale

        # Rotation
        rx = x * math.cos(angle_y) + z * math.sin(angle_y)
        rz = -x * math.sin(angle_y) + z * math.cos(angle_y)

        factor = fov / (dist + rz)
        sx = rx * factor + WIDTH // 2
        sy = y * factor + HEIGHT // 2

        projected_points.append((rz, sx, sy, p['color'], factor))

    # 2. Sort by depth
    projected_points.sort(key=lambda x: x[0], reverse=True)

    # 3. Draw solid lights
    for z, sx, sy, color, f in projected_points:
        size = max(1, int((WIDTH * 0.0035) * f))
        pygame.draw.circle(screen, color, (int(sx), int(sy)), size)

    # 4. Top Star
    star_y_rel = -1.0  # Top of normalized tree
    star_y_scaled = star_y_rel * tree_height_scale + (HEIGHT * 0.25)
    star_sy = star_y_scaled * (fov / dist) + HEIGHT // 2
    pygame.draw.circle(screen, (255, 255, 0), (WIDTH // 2, int(star_sy)), int(WIDTH * 0.008))

    # 5. Dazzling Message
    t_val = pygame.time.get_ticks() * 0.004
    text_color = (
        int(127 + 127 * math.sin(t_val)),
        int(127 + 127 * math.sin(t_val + 2)),
        int(127 + 127 * math.sin(t_val + 4))
    )

    text_surf = font.render("Merry Christmas & a Prosperous 2026", True, text_color)
    text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT - (HEIGHT * 0.12)))
    screen.blit(text_surf, text_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()