# Kalaha
**Board Game** assignment for the Introduction to AI (02180) course at DTU. \
This project implements the board game **Kalaha (or Mancala)** with AI players using **Minimax** and **Alpha-Beta pruning**. It also includes benchmarking tools and plotting utilities to compare performance.

---
## Project Structure
```
├── main.py              # Entry point for playing the game
├── game.py              # Game loop and rules execution
├── board.py             # Board representation and mechanics
├── player.py            # Abstract Player + HumanPlayer
├── ai_player.py         # AI logic (Minimax + Alpha-Beta)
├── benchmark.py         # Runs benchmark experiments (text output)
├── plot_benchmark.py    # Runs experiments + generates plots
├── img/                 # Output directory for generated images
```

---
## How to Run
### 1. Play the game
```bash
python3 main.py
```

You’ll be prompted to choose:
- 1) Human vs Human
- 2) Human vs AI
- 3) AI vs AI

---
### 2. Run benchmarks (console output)
```bash
python3 benchmark.py
```
The output produces a full benchmark on the console output, showing three experiments:
- Experiment 1: **Alpha-Beta vs Alpha-Beta**, with different dephts
- Experiment 2: **Alpha-Beta vs Minimax (Equal Depth)**, swapping the players after the first run
- Experiment 3: **Speed - average time per move**, comparing time per move across different dephts

---
### 3. Generate plots (recommended)
```bash
python3 plot_benchmark.py
```
Produces 3 graphs under `img/`:
- `winrate_comparison.png`: **win rate comparison** between Alpha-Beta and Minimax across different depths. 
- `time_comparison.png`: **average time per move** as a function of search depth for Minimax and Alpha-Beta pruning
- `node_comparison.png`: **number of nodes explored** by Minimax and Alpha-Beta pruning as a function of search depth

---
## Requirements
- Python 3.x
- matplotlib

### Install dependencies:
```
pip install matplotlib
```