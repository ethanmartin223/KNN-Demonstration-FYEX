# ---------------------------- Imports ------------------------------- #
import math, random
import time
import tkinter as tk

# ---------------------------- Settings ------------------------------- #
actual_window_width: int = 800
actual_window_height: int = 800

visualization_grid_height: int = 13
visualization_grid_width: int = 13

timer_speed: int = 500  # ms
classification_wait_time: int = 500  # ms

K_value = 6
num_of_colors = 8
show_lines = 1
dot_size = 8  # (visualization_grid_width + visualization_grid_height) / 2

# ---------------------------- points ------------------------------- #
group_colors = ['red', 'green', 'blue', 'orange', 'yellow', 'purple', 'brown', 'tan']
# point_set: dict[int:tuple[int]] = {0: [(1, 12), (2, 5), (3, 6), (3, 10), (3.5, 8),
#                                        (2, 11), (2, 9), (1, 7), (4,8), (5,7.2), (8,9), (7,10)],
#                                    1: [(5, 3), (3, 2), (1.5, 9), (7, 2), (6, 1), (3.8, 1), (5.6, 4), (4, 2), (2, 5)],
#                                    2: []}

point_set = {}
for i in range(num_of_colors):
    point_set[i] = [(random.uniform(1, visualization_grid_width), random.uniform(1, visualization_grid_height)) for _ in
                    range(25)]

# ---------------------------- Window Init ------------------------------- #
window = tk.Tk()
window.geometry(f"{actual_window_width}x{actual_window_height}")

canvas = tk.Canvas(height=visualization_grid_height, width=visualization_grid_width, bg='black')
canvas.pack(fill='both', expand=True)


# ---------------------------- Functions ------------------------------- #
def draw_points(points):
    for i in points:
        for j in points[i]:
            x = ((j[0] * actual_window_width) / visualization_grid_width)
            y = ((j[1] * actual_window_height) / visualization_grid_height)
            canvas.create_rectangle(x - dot_size / 2, y - dot_size / 2, x + dot_size / 2, y + dot_size / 2,
                                    fill=group_colors[i], outline=group_colors[i])


def add_random_point(points):
    x = random.uniform(1, visualization_grid_width)
    y = random.uniform(1, visualization_grid_height)

    fx = ((x * actual_window_width) / visualization_grid_width)
    fy = ((y * actual_window_height) / visualization_grid_height)
    if show_lines:
        canvas.create_oval(fx - dot_size / 2, fy - dot_size / 2, fx + dot_size / 2, fy + dot_size / 2,
                           fill='white', tags='temp', outline='white')
        canvas.update()
        window.update()
        time.sleep(classification_wait_time / 1000)
    classification = classify_point(points, (x, y), K_value)
    canvas.create_rectangle(fx - dot_size / 2, fy - dot_size / 2, fx + dot_size / 2, fy + dot_size / 2,
                            fill=group_colors[classification], outline=group_colors[classification])
    if show_lines:
        canvas.update()
        window.update()
        time.sleep(classification_wait_time / 1000)
        canvas.delete('temp')

    points[classification].append((x, y))


def classify_point(points, p, k=3):
    distance = []
    for group in points:
        for feature in points[group]:
            euclidean_distance = math.sqrt((feature[0] - p[0]) ** 2 + (feature[1] - p[1]) ** 2)
            distance.append((euclidean_distance, group, feature))
    distance = sorted(distance)[:k + 1]

    freqs = [0 for i in range(num_of_colors)]
    for d in distance:
        if show_lines:
            dx = ((d[2][0] * actual_window_width) / visualization_grid_width)
            dy = ((d[2][1] * actual_window_height) / visualization_grid_height)
            px = ((p[0] * actual_window_width) / visualization_grid_width)
            py = ((p[1] * actual_window_height) / visualization_grid_height)

            canvas.create_line(dx, dy, px, py, fill=group_colors[d[1]], tags='temp')
        freqs[d[1]] += 1
    max_location = 0
    max_value = -1
    for i, v in enumerate(freqs):
        if v > max_value:
            max_location = i
            max_value = v
    return max_location


def loop(points):
    add_random_point(points)
    window.after(timer_speed, lambda: loop(points))


def up(e):
    global timer_speed, classification_wait_time, K_value
    timer_speed += 100
    classification_wait_time += 100


def down(e):
    global timer_speed, classification_wait_time, K_value
    if timer_speed > 0:
        timer_speed -= 100
        classification_wait_time -= 100
    if timer_speed < 0:
        timer_speed = 0
        classification_wait_time = 0


def right(e):
    global K_value
    K_value += 1


def left(e):
    global K_value
    K_value -= 1


def reset(e):
    global point_set
    point_set.clear()
    for i in range(num_of_colors):
        point_set[i] = [(random.uniform(1, visualization_grid_width), random.uniform(1, visualization_grid_height)) for
                        _ in range(25)]
    canvas.delete('all')
    draw_points(point_set)


def toggle(e):
    global show_lines
    show_lines = not show_lines


# ---------------------------- Mainloop ------------------------------- #
draw_points(point_set)
window.after(timer_speed, lambda: loop(point_set))
window.bind('<Up>', up)
window.bind('<Down>', down)
window.bind('<Right>', right)
window.bind('<Left>', left)
window.bind('<r>', reset)
window.bind('<space>', toggle)
window.mainloop()
