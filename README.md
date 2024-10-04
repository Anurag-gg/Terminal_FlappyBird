# 🐦 Flappy Bird Terminal Edition

Welcome to **Flappy Bird: Terminal Edition**! This is a fun, minimalist version of the classic game built in Python using `curses` and ASCII art. Navigate your bird through the obstacles while trying to avoid hitting the pillars. Let's see how high you can score! 🎮

## How to Play 🚀

The controls are simple and intuitive:

- **Up Arrow** ⬆️: Move the bird upwards.
- **Down Arrow** ⬇️: Move the bird downwards.
- **Gravity** 🌍: The bird naturally falls down over time.

Your goal is to **dodge the pillars** and survive as long as you can. Each time you pass a pillar, your score increases by 1.

## Features 🎉

- **Old-School Graphics**: Enjoy the nostalgia of retro-style ASCII art and terminal graphics.
- **Simple Yet Addictive Gameplay**: The mechanics are easy, but the game is challenging!
- **Sound Effects**: Get a small beep sound when the game ends (because why not? 😄).
- **Responsive Controls**: Use the arrow keys to control the bird, and experience the game's smooth gravity system.

## Screenshots 🖼️

Here’s a sneak peek of what you can expect on your terminal:

```
    Score: 12
    -------------
    |           |
    |           |
    |    /\     |
    |   (o o)   |
    |   ( - )   |
    |    \/     |
    |           |
    |   @@@@@   |
    |           |
    |   @@@@@   |
    -------------
```

## Installation & Running the Game 🛠️

### 1. Prerequisites:
Make sure you have Python installed. You can check this by running:
```bash
python --version
```

### 2. Clone the Repository:
Clone this repo to get started:
```bash
git clone https://github.com/your-repo/flappy-bird-terminal.git
cd flappy-bird-terminal
```

### 3. Run the Game:
Fire up your terminal and run the game by executing:
```bash
python flappy.py
```

Make sure your terminal window is large enough (at least **30x120**).

## Code Overview 💻

This game is powered by Python’s `curses` module. Here's a brief rundown of the key parts of the code:

- **`main(stdscr)`**: The main game loop. It handles input, updates the game state, and refreshes the screen.
- **`getBird(...)`**: Manages the bird's position and handles gravity and user input.
- **`getPillar(...)`**: Generates the moving pillars.
- **`endScreen(stdscr)`**: Displays the game over screen along with your score.

## Contributing 🤝

We welcome contributions to improve this game! Feel free to fork the repo and submit pull requests. Whether it's fixing bugs, adding features, or polishing the graphics, we’d love to see what you come up with.

### To contribute:
1. Fork the repository.
2. Create a new branch for your feature/bug fix:
   ```bash
   git checkout -b my-new-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add some feature"
   ```
4. Push to the branch:
   ```bash
   git push origin my-new-feature
   ```
5. Submit a pull request.

Have fun playing, and may your bird fly high! 🐤✨
