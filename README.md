# Othello Game with AI

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [AI Algorithm](#ai-algorithm)
  - [Minimax Algorithm](#minimax-algorithm)
  - [Alpha-Beta Pruning](#alpha-beta-pruning)
- [How It Works](#how-it-works)

## Overview

This project implements the classic board game Othello (also known as Reversi) with an AI opponent using the minimax algorithm with alpha-beta pruning. The game is built with Python and Tkinter for the graphical user interface (GUI).

## Features

- **Game Modes**: 
  - Player vs Player (PvP)
  - Player vs Computer (PvC)
- **AI Difficulty Levels**: 
  - Easy
  - Medium
  - Hard
- **Optimal AI Moves**: Uses the minimax algorithm with alpha-beta pruning for intelligent decision-making.

## AI Algorithm

### Minimax Algorithm

The minimax algorithm is a decision-making algorithm used in game theory for minimizing the possible loss for a worst-case scenario. When dealing with perfect play in games like Othello, the minimax algorithm explores all possible moves and their outcomes to choose the optimal move.

### Alpha-Beta Pruning

Alpha-beta pruning is an optimization technique for the minimax algorithm that reduces the number of nodes evaluated in the search tree. It keeps track of two values, alpha and beta:
- **Alpha**: The best value that the maximizer currently can guarantee.
- **Beta**: The best value that the minimizer currently can guarantee.

By pruning branches that cannot influence the final decision, alpha-beta pruning significantly speeds up the minimax algorithm.

## How It Works

1. **Game Initialization**:
   - The game board is set up with the initial four disks placed in the center.

2. **Player Moves**:
   - Players (human or AI) make moves on the board. Valid moves are highlighted.

3. **AI Turn**:
   - When it's the AI's turn, the AI uses the minimax algorithm with alpha-beta pruning to determine the optimal move.
   - The algorithm recursively evaluates possible moves up to a specified depth, considering the best and worst-case scenarios for each move.

4. **Minimax Algorithm**:
   - **Maximizing Player**: The AI tries to maximize its score by choosing the move with the highest utility value.
   - **Minimizing Player**: The AI also simulates the opponent's moves to minimize the opponent's score, ensuring a strategic advantage.

5. **Alpha-Beta Pruning**:
   - During the recursive search, branches that are less favorable than previously explored branches are pruned to reduce computation time.

## Screenshot

![Othello Game Screenshot](https://github.com/Salma-Mamdoh/Ai_Project/blob/master/Othello%20Game%20Screenshot.png)
