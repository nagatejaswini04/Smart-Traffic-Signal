import tkinter as tk
import random
import math

root = tk.Tk()
root.title("Smart Traffic Signal Monitoring System")
root.geometry("1250x900")
root.configure(bg="white")

canvas = tk.Canvas(root, width=1250, height=900, bg="white")
canvas.pack()

# =========================================================
# WINDOW / GEOMETRY
# =========================================================
W, H = 1250, 900
CX, CY = 625, 450
ROAD_W = 240
HALF = ROAD_W // 2

IX1, IY1 = CX - HALF, CY - HALF
IX2, IY2 = CX + HALF, CY + HALF

VEHICLE_LEN = 28
VEHICLE_WID = 16
GAP = 42
SPEED = 4

APPROACH_ORDER = ["north", "east", "south", "west"]
TURN_CHOICES = ["straight", "left", "right"]
TURN_WEIGHTS = [0.55, 0.25, 0.20]

# =========================================================
# ROAD DRAWING
# =========================================================
def draw_roads():
    canvas.create_rectangle(0, CY - HALF, W, CY + HALF, fill="gray35", outline="gray35")
    canvas.create_rectangle(CX - HALF, 0, CX + HALF, H, fill="gray35", outline="gray35")
    canvas.create_rectangle(IX1, IY1, IX2, IY2, fill="gray25", outline="white", width=2)

    for x in range(0, W, 60):
        canvas.create_line(x, CY, x + 30, CY, fill="white", width=3)

    for y in range(0, H, 60):
        canvas.create_line(CX, y, CX, y + 30, fill="white", width=3)

    # stop lines
    canvas.create_line(IX1, IY1 - 25, IX2, IY1 - 25, fill="white", width=4)
    canvas.create_line(IX1, IY2 + 25, IX2, IY2 + 25, fill="white", width=4)
    canvas.create_line(IX1 - 25, IY1, IX1 - 25, IY2, fill="white", width=4)
    canvas.create_line(IX2 + 25, IY1, IX2 + 25, IY2, fill="white", width=4)

    # zebra crossing
    for i in range(8):
        canvas.create_rectangle(IX1 + i * 28, IY1 - 20, IX1 + i * 28 + 16, IY1 - 8, fill="white", outline="white")
        canvas.create_rectangle(IX1 + i * 28, IY2 + 8, IX1 + i * 28 + 16, IY2 + 20, fill="white", outline="white")
        canvas.create_rectangle(IX1 - 20, IY1 + i * 28, IX1 - 8, IY1 + i * 28 + 16, fill="white", outline="white")
        canvas.create_rectangle(IX2 + 8, IY1 + i * 28, IX2 + 20, IY1 + i * 28 + 16, fill="white", outline="white")

    canvas.create_text(CX, 35, text="NORTH", font=("Arial", 16, "bold"), fill="black")
    canvas.create_text(CX, H - 30, text="SOUTH", font=("Arial", 16, "bold"), fill="black")
    canvas.create_text(80, CY, text="WEST", font=("Arial", 16, "bold"), fill="black")
    canvas.create_text(W - 80, CY, text="EAST", font=("Arial", 16, "bold"), fill="black")

draw_roads()

# =========================================================
# TITLES
# =========================================================
title_label = tk.Label(
    root,
    text="Smart Traffic Signal Monitoring System",
    font=("Arial", 22, "bold"),
    bg="white"
)
title_label.place(x=320, y=12)

info_label = tk.Label(
    root,
    text="",
    font=("Arial", 15, "bold"),
    bg="white",
    fg="blue"
)
info_label.place(x=180, y=50)

timer_label = tk.Label(
    root,
    text="Timer: 0s",
    font=("Arial", 16, "bold"),
    bg="white",
    fg="darkgreen"
)
timer_label.place(x=585, y=84)

# =========================================================
# SIGNALS
# =========================================================
signals = {}

def create_signal(name, x, y):
    canvas.create_rectangle(x, y, x + 36, y + 100, fill="black", outline="white")
    red = canvas.create_oval(x + 8, y + 8, x + 28, y + 28, fill="grey")
    yellow = canvas.create_oval(x + 8, y + 40, x + 28, y + 60, fill="grey")
    green = canvas.create_oval(x + 8, y + 72, x + 28, y + 92, fill="grey")
    signals[name] = {"red": red, "yellow": yellow, "green": green}

def set_signal(direction, color):
    for c in ("red", "yellow", "green"):
        canvas.itemconfig(signals[direction][c], fill="grey")
    canvas.itemconfig(signals[direction][color], fill=color)

def all_red():
    for d in signals:
        set_signal(d, "red")

create_signal("north", IX2 + 35, IY1 - 90)
create_signal("south", IX1 - 70, IY2 + 10)
create_signal("west", IX1 - 90, IY1 + 20)
create_signal("east", IX2 + 55, IY2 - 120)

# =========================================================
# PANEL
# =========================================================
count_text_ids = {}
time_text_ids = {}

def draw_side_panel():
    canvas.create_text(1010, 180, text="Vehicle Count", font=("Arial", 15, "bold"), fill="black")
    canvas.create_text(1150, 180, text="Green Time", font=("Arial", 15, "bold"), fill="black")

    ys = {"north": 220, "south": 255, "east": 290, "west": 325}
    for d in ys:
        count_text_ids[d] = canvas.create_text(
            1010, ys[d], text=f"{d.capitalize()}: 0",
            font=("Arial", 14, "bold"), fill="black"
        )
        time_text_ids[d] = canvas.create_text(
            1150, ys[d], text="0 s",
            font=("Arial", 14, "bold"), fill="darkgreen"
        )

draw_side_panel()

# =========================================================
# LANE MAPPING
# =========================================================
LANE = {
    # incoming lanes
    "north_in": (CX - 35, None),   # top to down
    "south_in": (CX + 35, None),   # bottom to up
    "west_in": (None, CY - 35),    # left to right, upper half
    "east_in": (None, CY - 75),    # right to left, moved to empty upper lane

    # outgoing lanes
    "north_out": (CX + 35, -100),
    "south_out": (CX - 35, H + 100),
    "west_out": (-100, CY - 75),   # matches east incoming lane
    "east_out": (W + 100, CY - 35)
}

STOP_LINE = {
    "north": IY1 - 25,
    "south": IY2 + 25,
    "west": IX1 - 25,
    "east": IX2 + 25
}

vehicle_colors = {
    "north": "#e74c3c",
    "south": "#3498db",
    "east": "#f1c40f",
    "west": "#2ecc71"
}

def dist(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

def move_towards(x, y, tx, ty, step):
    d = dist(x, y, tx, ty)
    if d == 0 or d <= step:
        return tx, ty, True
    r = step / d
    return x + (tx - x) * r, y + (ty - y) * r, False

# =========================================================
# TURN PATHS
# =========================================================
TARGETS = {
    ("north", "straight"): LANE["south_out"],
    ("north", "left"):     LANE["east_out"],
    ("north", "right"):    LANE["west_out"],

    ("south", "straight"): LANE["north_out"],
    ("south", "left"):     LANE["west_out"],
    ("south", "right"):    LANE["east_out"],

    ("west", "straight"):  LANE["east_out"],
    ("west", "left"):      LANE["north_out"],
    ("west", "right"):     LANE["south_out"],

    ("east", "straight"):  LANE["west_out"],
    ("east", "left"):      LANE["south_out"],
    ("east", "right"):     LANE["north_out"],
}

TURN_MID = {
    ("north", "left"):   (CX - 35, CY - 35),
    ("north", "right"):  (CX - 90, CY + 35),

    ("south", "left"):   (CX + 35, CY + 35),
    ("south", "right"):  (CX + 90, CY - 35),

    ("west", "left"):    (CX - 35, CY - 35),
    ("west", "right"):   (CX + 35, CY - 90),

    ("east", "left"):    (CX + 35, CY - 75),
    ("east", "right"):   (CX - 35, CY - 75),
}

# =========================================================
# VEHICLE CLASS
# =========================================================
class Vehicle:
    def __init__(self, approach, movement, x, y):
        self.approach = approach
        self.movement = movement
        self.x = x
        self.y = y
        self.crossed = False
        self.turn_started = False
        self.turn_mid_done = False
        self.finished = False
        self.id = canvas.create_rectangle(0, 0, 0, 0, fill=vehicle_colors[approach], outline="black")
        self.update_shape()

    def update_shape(self):
        if self.approach in ("north", "south") and not self.turn_started and self.movement == "straight":
            canvas.coords(
                self.id,
                self.x - VEHICLE_WID / 2, self.y - VEHICLE_LEN / 2,
                self.x + VEHICLE_WID / 2, self.y + VEHICLE_LEN / 2
            )
        elif self.approach in ("west", "east") and not self.turn_started and self.movement == "straight":
            canvas.coords(
                self.id,
                self.x - VEHICLE_LEN / 2, self.y - VEHICLE_WID / 2,
                self.x + VEHICLE_LEN / 2, self.y + VEHICLE_WID / 2
            )
        else:
            canvas.coords(self.id, self.x - 12, self.y - 12, self.x + 12, self.y + 12)

    def update_crossed(self):
        if self.crossed:
            return

        if self.approach == "north" and self.y + VEHICLE_LEN / 2 > STOP_LINE["north"]:
            self.crossed = True
        elif self.approach == "south" and self.y - VEHICLE_LEN / 2 < STOP_LINE["south"]:
            self.crossed = True
        elif self.approach == "west" and self.x + VEHICLE_LEN / 2 > STOP_LINE["west"]:
            self.crossed = True
        elif self.approach == "east" and self.x - VEHICLE_LEN / 2 < STOP_LINE["east"]:
            self.crossed = True

    def leader_ok(self, leader):
        if leader is None:
            return True

        if self.approach == "north":
            return self.y + SPEED < leader.y - GAP
        if self.approach == "south":
            return self.y - SPEED > leader.y + GAP
        if self.approach == "west":
            return self.x + SPEED < leader.x - GAP
        if self.approach == "east":
            return self.x - SPEED > leader.x + GAP
        return True

    def move_on_approach(self):
        if self.approach == "north":
            self.y += SPEED
        elif self.approach == "south":
            self.y -= SPEED
        elif self.approach == "west":
            self.x += SPEED
        elif self.approach == "east":
            self.x -= SPEED

    def move_after_cross(self):
        if self.movement == "straight":
            tx, ty = TARGETS[(self.approach, "straight")]
            self.x, self.y, done = move_towards(self.x, self.y, tx, ty, SPEED)
            if done:
                self.finished = True
            return

        mid = TURN_MID[(self.approach, self.movement)]
        end = TARGETS[(self.approach, self.movement)]

        if not self.turn_started:
            self.turn_started = True

        if not self.turn_mid_done:
            self.x, self.y, done = move_towards(self.x, self.y, mid[0], mid[1], SPEED)
            if done:
                self.turn_mid_done = True
        else:
            self.x, self.y, done = move_towards(self.x, self.y, end[0], end[1], SPEED)
            if done:
                self.finished = True

    def step(self, leader, current_green):
        self.update_crossed()

        can_go = False
        if self.crossed:
            can_go = True
        elif self.approach == current_green and self.leader_ok(leader):
            can_go = True

        if can_go:
            if self.crossed:
                self.move_after_cross()
            else:
                self.move_on_approach()
                self.update_crossed()

        self.update_shape()

# =========================================================
# VEHICLE STORAGE
# =========================================================
vehicles = {"north": [], "south": [], "east": [], "west": []}

def clear_vehicles():
    for d in vehicles:
        for v in vehicles[d]:
            canvas.delete(v.id)
        vehicles[d].clear()

def build_cycle_vehicles(counts):
    clear_vehicles()

    for approach in APPROACH_ORDER:
        count = counts[approach]
        for i in range(count):
            movement = random.choices(TURN_CHOICES, weights=TURN_WEIGHTS, k=1)[0]

            if approach == "north":
                x = LANE["north_in"][0]
                y = STOP_LINE["north"] - 30 - i * GAP
            elif approach == "south":
                x = LANE["south_in"][0]
                y = STOP_LINE["south"] + 30 + i * GAP
            elif approach == "west":
                x = STOP_LINE["west"] - 30 - i * GAP
                y = LANE["west_in"][1]
            else:
                x = STOP_LINE["east"] + 30 + i * GAP
                y = LANE["east_in"][1]

            vehicles[approach].append(Vehicle(approach, movement, x, y))

def update_count_labels():
    for d in vehicles:
        canvas.itemconfig(count_text_ids[d], text=f"{d.capitalize()}: {len(vehicles[d])}")

def update_time_labels(times):
    for d in times:
        canvas.itemconfig(time_text_ids[d], text=f"{times[d]} s")

# =========================================================
# TRAFFIC LOGIC
# =========================================================
def generate_traffic():
    return {
        "north": random.randint(5, 12),
        "south": random.randint(5, 12),
        "east": random.randint(5, 12),
        "west": random.randint(5, 12),
    }

def calculate_green_time(count):
    return min(12, max(4, 3 + count // 2))

def calculate_all_green_times(counts):
    return {d: calculate_green_time(counts[d]) for d in counts}

current_index = 0
current_green = None
signal_state = "red"
green_times = {}

def start_full_cycle():
    global current_index, green_times
    counts = generate_traffic()
    green_times = calculate_all_green_times(counts)
    build_cycle_vehicles(counts)
    update_count_labels()
    update_time_labels(green_times)
    current_index = 0
    run_next_direction()

def run_next_direction():
    global current_index, current_green, signal_state

    if current_index >= len(APPROACH_ORDER):
        info_label.config(text="Cycle complete. Updating traffic density...")
        timer_label.config(text="Timer: 0s")
        root.after(1500, start_full_cycle)
        return

    current_green = APPROACH_ORDER[current_index]
    signal_state = "green"
    gtime = green_times[current_green]

    all_red()
    set_signal(current_green, "green")

    info_label.config(
        text=f"{current_green.upper()} road GREEN | Vehicles: {len(vehicles[current_green])} | Green Time: {gtime}s"
    )

    countdown_green(gtime)

def countdown_green(time_left):
    global signal_state
    if time_left > 0:
        timer_label.config(text=f"Timer: {time_left}s")
        root.after(1000, countdown_green, time_left - 1)
    else:
        signal_state = "yellow"
        set_signal(current_green, "yellow")
        info_label.config(text=f"{current_green.upper()} road YELLOW")
        timer_label.config(text="Timer: 2s")
        root.after(2000, end_current_direction)

def end_current_direction():
    global signal_state, current_index
    signal_state = "red"
    all_red()
    current_index += 1
    run_next_direction()

# =========================================================
# ANIMATION
# =========================================================
def animate():
    for approach in APPROACH_ORDER:
        lane = vehicles[approach]
        leader = None
        kept = []

        for v in lane:
            v.step(leader, current_green)

            if not v.crossed:
                leader = v

            if not v.finished:
                kept.append(v)
            else:
                canvas.delete(v.id)

        vehicles[approach] = kept

    update_count_labels()
    root.after(40, animate)

# =========================================================
# START
# =========================================================
all_red()
animate()
start_full_cycle()

root.mainloop()