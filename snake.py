import tkinter as tk
import random
import webbrowser
import ctypes
import time

WIDTH, HEIGHT = 600, 600
CELL = 20
COLS = WIDTH // CELL
ROWS = HEIGHT // CELL
TICK = 90

BG = "black"
SNAKE = "#00ff00"
APPLE = "#ff0000"

VIDEO = "https://www.youtube.com/watch?v=tOzOD-82mW0"
LIMIT = 30
TARGET = 15

def max_volume():
    try:
        for _ in range(60):
            ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xAF, 0, 2, 0)
            time.sleep(0.008)
    except Exception:
        pass

def prank():
    max_volume()
    webbrowser.open(VIDEO)
    root.destroy()

snake = [(COLS // 2, ROWS // 2)]
direction = (1, 0)
pending_dir = direction
food = None
score = 0
start = time.time()
alive = True

def spawn_food():
    global food
    while True:
        pos = (random.randrange(COLS), random.randrange(ROWS))
        if pos not in snake:
            food = pos
            break

spawn_food()

root = tk.Tk()
root.title("")
root.resizable(False, False)
root.configure(bg=BG)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG, highlightthickness=0)
canvas.pack()

def draw():
    canvas.delete("all")
    for x, y in snake:
        canvas.create_rectangle(
            x * CELL, y * CELL,
            (x + 1) * CELL, (y + 1) * CELL,
            fill=SNAKE, outline=SNAKE
        )
    fx, fy = food
    canvas.create_rectangle(
        fx * CELL, fy * CELL,
        (fx + 1) * CELL, (fy + 1) * CELL,
        fill=APPLE, outline=APPLE
    )

def change_dir(new_dir):
    global pending_dir
    # don't allow reversing into yourself
    if (new_dir[0] * -1, new_dir[1] * -1) != direction:
        pending_dir = new_dir

def move():
    global direction, score, alive, pending_dir

    if not alive:
        return

    direction = pending_dir
    hx, hy = snake[0]
    nx, ny = hx + direction[0], hy + direction[1]
    new_head = (nx, ny)

    # hit wall or self
    if nx < 0 or nx >= COLS or ny < 0 or ny >= ROWS or new_head in snake:
        prank()
        return

    snake.insert(0, new_head)

    if new_head == food:
        score += 1
        spawn_food()
    else:
        snake.pop()

    # time bomb
    if time.time() - start >= LIMIT:
        if score < TARGET:
            prank()
        else:
            alive = False
            root.destroy()
        return

    draw()
    root.after(TICK, move)

root.bind("<Up>",    lambda e: change_dir((0, -1)))
root.bind("<Down>",  lambda e: change_dir((0, 1)))
root.bind("<Left>",  lambda e: change_dir((-1, 0)))
root.bind("<Right>", lambda e: change_dir((1, 0)))
root.bind("<Escape>", lambda e: root.destroy())

draw()
move()
root.mainloop()