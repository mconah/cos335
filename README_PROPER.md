# Word Ladder Visualization Project

## Overview
This project implements the Word Ladder problem with multiple visualization approaches, including real-time BFS exploration.

## Files

### Core Algorithm
- **word_ladder.py** - Contains 20 functions (one per team member) that solve the Word Ladder II problem using BFS + DFS to find ALL shortest transformation sequences.

### Visualization Options

#### 1. Real-Time Visualizer (RECOMMENDED) ⭐
- **word_ladder_realtime.py** - Interactive real-time visualization showing BFS exploration step-by-step
- Uses matplotlib interactive mode (`plt.ion()`)
- Features:
  - Live updates as algorithm explores words
  - Color-coded nodes (current, visited, path, start, end)
  - 10 diverse test cases (successful and failing)
  - Final results showing all shortest paths
  - DAG visualization of parent relationships

**Run it:**
```bash
python word_ladder_realtime.py
```

#### 2. Static Image Generator (LEGACY)
- **word_ladder_visualizer.py** - Generates static PNG images saved to disk
- Uses non-interactive backend (`matplotlib.use('Agg')`)
- Creates output directory with BFS frames and path visualizations

**Run it:**
```bash
python word_ladder_visualizer.py
```

### Documentation
- **REALTIME_VISUALIZATION_GUIDE.md** - Comprehensive guide on implementing real-time visualization
  - Explains 5 different approaches (Interactive mode, FuncAnimation, Tkinter, PyQt, Browser-based)
  - Troubleshooting tips
  - Extension ideas
  - Comparison table of static vs real-time

## Quick Start

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Run real-time visualization with 10 test cases
python word_ladder_realtime.py
```

## Test Cases Included

The real-time visualizer includes 10 test cases:

| Case | Start | End | Expected | Description |
|------|-------|-----|----------|-------------|
| 1 | hit | cog | ✅ Success | Classic example with 2 paths |
| 2 | cat | dog | ✅ Success | Short path |
| 3 | hit | cog | ❌ Fail | Missing end word |
| 4 | start | end | ✅ Success | Multiple paths |
| 5 | cat | bat | ✅ Success | One-step transformation |
| 6 | aaa | bbb | ❌ Fail | Disconnected components |
| 7 | cold | warm | ✅ Success | Long chain required |
| 8 | lead | gold | ❌ Fail | End word not in dictionary |
| 9 | five | four | ✅ Success | Complex with multiple solutions |
| 10 | test | test | ✅ Success | Edge case: same start/end |

## Requirements

```
networkx>=2.6
matplotlib>=3.4
```

All dependencies are in `requirements.txt`.

## How Real-Time Visualization Works

The key is using matplotlib's interactive mode:

```python
import matplotlib.pyplot as plt

# Enable interactive mode
plt.ion()
plt.show()

# In the BFS loop:
while queue:
    current = queue.popleft()
    
    # Update visualization
    ax.clear()
    draw_graph(current_state)
    
    # Pause to create animation effect
    plt.pause(0.3)  # This is the magic!
    plt.gcf().canvas.draw()
    plt.gcf().canvas.flush_events()

# Turn off when done
plt.ioff()
plt.show()
```

See **REALTIME_VISUALIZATION_GUIDE.md** for complete implementation details.

## Project Structure

```
/workspace/
├── word_ladder.py                    # Core algorithm (20 functions)
├── word_ladder_realtime.py           # Real-time visualizer (NEW)
├── word_ladder_visualizer.py         # Static image generator
├── REALTIME_VISUALIZATION_GUIDE.md   # Documentation
├── README_PROPER.md                  # This file
├── requirements.txt                  # Dependencies
├── venv/                             # Virtual environment
└── output/                           # Generated images (from static visualizer)
```

## License
Educational project for Word Ladder II visualization.
