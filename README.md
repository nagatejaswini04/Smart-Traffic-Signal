#  Smart Traffic Signal Monitoring System
#PES2UG24AM095
#PES2UG25AM808
#PES2UG24AM113
##  Overview
This project is a simulation of a **Smart Traffic Signal System** built using Python and Tkinter.  
It dynamically controls traffic signals based on vehicle density at a four-way intersection.

Unlike traditional traffic lights with fixed timers, this system **adapts signal timing intelligently**, improving traffic flow and reducing congestion.

---

##  Objectives
- Simulate a real-world traffic intersection
- Reduce waiting time using dynamic signal control
- Visualize vehicle movement and signal changes
- Demonstrate basic traffic optimization concepts

---

##  Features
-  Real-time vehicle simulation
-  Dynamic signal timing based on traffic density
- Four-directional traffic control (North, South, East, West)
-  Automatic timer adjustment for each signal
- Graphical interface using Tkinter
-  Continuous traffic cycle simulation

---

##  Technologies Used
- Python
- Tkinter (GUI)
- Random module (traffic generation)
- Math module (movement calculations)

---

##  How It Works
1. Vehicles are randomly generated in all four directions.
2. The system counts the number of vehicles in each lane.
3. Based on vehicle density, **green signal time is calculated dynamically**.
4. Signals switch in a cycle: North → East → South → West.
5. Vehicles move according to signal status:
   - Green → Move
   - Red → Stop
6. Turning movements (left, right, straight) are also simulated.
7. The process repeats continuously.

---


---

## ▶️ How to Run

1. Install Python (if not already installed)
2. Download the project
3. Open terminal/command prompt
4. Run:

```bash
python traffic.py
```

Output:

A graphical window opens showing:

Roads and intersection
Moving vehicles
Traffic signals
Timer and vehicle count
