
# 🤖 Bittle Robotics Programming Curriculum

This curriculum provides a progressive robotics programming guide for Grades 1–12. Activities are grouped by learning level—Foundation, Logic, and Mastery—and include setup, student instructions, code examples (block-based and Python), and learning outcomes based on Bloom’s Taxonomy.

---

## 📘 Grades 1–4: Foundation Level

### 🐾 Activity 1: Robot Pet Show (Week 2)

**Setup**:  
- Students in pairs  
- One Bittle robot per pair  
- Tablets with block-based interface  

**What Students Do**:  
Create a sequence of tricks for their robot pet using drag-and-drop blocks.

**Code Example (Block-Based)**:
```

\[When Green Flag Clicked]
\[Motion] Stand Up
\[Control] Wait (1) seconds
\[Sound] Play Sound "Bark"
\[Motion] Walk Forward (2) steps
\[Motion] Turn Left (90) degrees
\[Motion] Wave Paw
\[Control] Wait (2) seconds
\[Motion] Sit Down
\[Sound] Play Sound "Happy Bark"

```

**Student Instructions**:
- Drag blocks from palette to workspace
- Connect blocks top to bottom
- Test with green flag
- Adjust timing to match music
- Debug if robot doesn't follow sequence

**Bloom’s Level**: *Applying*

---

### 🚧 Activity 2: Obstacle Race Challenge (Week 3)

**Setup**:  
- Identical maze layouts  
- One robot per pair  
- Timer  

**What Students Do**:  
Program robot to navigate a maze using only movement commands.

**Code Example (Block-Based)**:
```

\[When Green Flag Clicked]
\[Motion] Walk Forward (3) steps
\[Motion] Turn Right (90) degrees
\[Motion] Walk Forward (2) steps
\[Motion] Turn Left (90) degrees
\[Motion] Walk Forward (4) steps
\[Motion] Turn Right (90) degrees
\[Motion] Walk Forward (1) step
\[Sound] Play Sound "Victory"

```

**Bloom’s Level**: *Analyzing*

---

### 📖 Activity 3: Bittle Storytime Adventure (Week 4)

**Setup**:  
- Story template worksheets  
- Props (trees, houses)  
- Robots with speakers  

**What Students Do**:  
Write a story and program robot to act out each scene.

**Code Example (Block-Based)**:
```

// Scene 1
\[Motion] Walk Forward (3) steps
\[Sound] Play Sound "Walking"
// Scene 2
\[Motion] Turn Left (45) degrees
\[Motion] Wave Paw
\[Sound] Play Sound "Hello"
// Scene 3
\[Motion] Spin Right (360) degrees
\[Motion] Jump
\[Sound] Play Sound "Laugh"
// Scene 4
\[Motion] Walk Backward (3) steps
\[Motion] Sit Down
\[Sound] Play Sound "Home"

```

**Bloom’s Level**: *Creating*

---

## 🧠 Grades 5–8: Logic Level

### 🧱 Activity 4: Sensor-Based Navigation (Week 2)

**Setup**:  
- Obstacle course  
- Robots with ultrasonic sensors  

**Code Example (Block-Based)**:
```

\[When Green Flag Clicked]
Set \[speed] to (50)
Forever
Set \[distance] to \[Ultrasonic Sensor]
If \[distance] < (15)
Stop Moving
Walk Backward (1) step at speed (30)
Turn Right (90)
Wait (0.5)
Else
Walk Forward at speed \[speed]

```

**Bloom’s Level**: *Applying*

---

### 🕵️ Activity 5: Debug Detective Challenge (Week 4)

**Setup**:  
- Tablets with buggy code  
- Robots for testing  

**Buggy Code**:
```

Repeat (4)
Walk Forward (2) steps
Turn Right (45 degrees)

```

**Fixed Code**:
```

Repeat (4)
Walk Forward (2) steps
Turn Right (90 degrees)

```

**Bloom’s Level**: *Evaluating*

---

### 🧩 Activity 6: Logic Maze Solver (Week 5)

**Setup**:  
- Complex maze  
- Robots with side sensors  

**Code Example (Block-Based)**:
```

Forever
Set front\_distance = Ultrasonic
Set right\_distance = Right Sensor
If right\_distance > 20
Turn Right
Move Forward
Else if front\_distance > 15
Move Forward
Else
Turn Left
Wait (0.2)

````

**Bloom’s Level**: *Analyzing*

---

## 🚀 Grades 9–12: Mastery Level

### 🕷️ Activity 7: Custom Gait Development (Week 6)

**Setup**:  
- Python environment  
- Bittle robots  

**Code Snippet (Python)**:
```python
class CustomGait:
    def spider_walk(self):
        for t in range(0, 100, 5):
            progress = t / 100.0
            height = self.step_height * math.sin(math.pi * progress)
            self.robot.set_servo_angle('front_left_shoulder', 45 + height)
````

**Bloom’s Level**: *Creating*

---

### 🧠 Activity 8: AI-Enhanced Navigation (Week 10)

**Setup**:

* Camera and ML environment
* Python + OpenCV + Scikit-learn

**Code Snippet (Python)**:

```python
def analyze_environment(self):
    _, frame = self.camera.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    red_mask = cv2.inRange(hsv, (0, 50, 50), (10, 255, 255))
    green_mask = cv2.inRange(hsv, (40, 50, 50), (80, 255, 255))
```

**Bloom’s Level**: *Evaluating → Creating*

---


## 🧾 Assessment Rubrics

### Grades 1–4: Block Programming

| Level          | Description                            |
| -------------- | -------------------------------------- |
| 1 – Novice     | Can place blocks but needs help        |
| 2 – Developing | Creates sequences with guidance        |
| 3 – Proficient | Independently creates working programs |
| 4 – Advanced   | Creates complex code and helps others  |

### Grades 5–8: Logic Programming

| Level          | Description                            |
| -------------- | -------------------------------------- |
| 1 – Novice     | Uses basic conditionals with help      |
| 2 – Developing | Combines sensors and logic with errors |
| 3 – Proficient | Builds autonomous logic flows          |
| 4 – Advanced   | Optimizes and innovates                |

### Grades 9–12: Advanced Programming

| Level          | Description                       |
| -------------- | --------------------------------- |
| 1 – Novice     | Writes Python with guidance       |
| 2 – Developing | Implements functional algorithms  |
| 3 – Proficient | Efficient, original code          |
| 4 – Advanced   | Innovates across multiple systems |

---

## ✨ Contributing

To suggest improvements or add new activities:

* Fork the repo
* Open a pull request
* Or start a discussion in the Issues tab

---

`````


