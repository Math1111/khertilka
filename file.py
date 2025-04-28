import pygame
import math

pygame.init()
size = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Piccoaamee mumin")
BACKGROUND = (0, 0, 0)
POINT_RADIUS = 5
HIGHLIGHT_COLOR = (255, 255, 0)
POINTS_FILE_NAME = "points.txt"
LINE_COLOR = (255, 255, 255)
PRIVIDA_COLOR = (192, 192, 192)
points = []


def get_closest_point(mouse_pos):
    closest_point = None
    closest_distance = float("inf")
    for point in points:
        distance = (point[0] - mouse_pos[0]) ** 2 + (point[1] - mouse_pos[1]) ** 2
        if distance <= POINT_RADIUS ** 2 and distance < closest_distance:
            closest_point = point
            closest_distance = distance
    return closest_point


def save_points():
    with open(POINTS_FILE_NAME, "w") as f:
        for point in points:
            f.write(f"{point[0]} {point[1]}\n")


def load_points():
    points.clear()
    try:
        with open(POINTS_FILE_NAME, "r") as f:
            for line in f:
                x, y = map(int, line.split())
                points.append((x, y))
    except FileNotFoundError:
        pass


load_points()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            closest_point = get_closest_point(event.pos)
            if closest_point is not None:
                if event.button == 1:  # Left click - select existing point
                    pass  # Already handled by closest_point check
                elif event.button == 3:  # Right click - remove point
                    points.remove(closest_point)
            elif event.button == 1:  # Left click - add new point
                points.append(event.pos)

    screen.fill(BACKGROUND)

    # Draw lines between points
    if len(points) >= 2:
        for i in range(len(points) - 1):
            start_point = points[i]
            end_point = points[i + 1]
            pygame.draw.line(screen, LINE_COLOR, start_point, end_point, 3)

    # Draw preview line from last point to mouse
    if len(points) >= 1:
        last_point = points[-1]
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, PRIVIDA_COLOR, last_point, mouse_pos, 3)

    # Highlight closest point
    closest_point = get_closest_point(pygame.mouse.get_pos())
    if closest_point is not None:
        pygame.draw.circle(screen, HIGHLIGHT_COLOR, closest_point, POINT_RADIUS, 1)

    # Draw all points
    for point in points:
        pygame.draw.circle(screen, LINE_COLOR, point, POINT_RADIUS)

    pygame.display.flip()

save_points()
pygame.quit()