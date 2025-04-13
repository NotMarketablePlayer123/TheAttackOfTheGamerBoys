Below is a comprehensive README.md example for your GitHub repository, updated with the correct game title:

---

# The Attack of the Gamer Boys

**The Attack of the Gamer Boys** is a fast-paced, arcade-style game built using [Pygame](https://www.pygame.org/). In this game, you play as a heroic gamer battling waves of enemies with your trusty controllers. Dodge incoming threats, collect power-ups, and rack up an impressive score to claim your place on the leaderboard!

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Gameplay](#gameplay)
- [Controls](#controls)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Dynamic Enemy Waves:** Enemies spawn continuously with increasing difficulty over time.
- **Diverse Enemies:** Face standard enemies and the formidable "Skells" enemy type, each with unique characteristics.
- **Power-Ups:** Collect different types of power-ups:
  - **PS5 Controller:** Increases shooting damage.
  - **Special Controller:** Allows you to throw multiple controllers at once.
  - **Nuke:** Clears all enemies from the screen.
- **Responsive Controls:** Move left and right to dodge enemies and aim your throws.
- **Floating Text Effects:** Visual feedback displays enemy hit points decreasing in real time.
- **Leaderboard:** Your score is recorded on a leaderboard that persists until the game is closed.
- **Restart & Exit Options:** End-of-game screen with options to restart or exit the game.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/the-attack-of-the-gamer-boys.git
   cd the-attack-of-the-gamer-boys
   ```

2. **Install Dependencies:**

   Ensure you have Python 3.x installed. Then install [Pygame](https://www.pygame.org/wiki/GettingStarted):
   ```bash
   pip install pygame
   ```

3. **Sprites:**

   The game expects the following sprite images to be present in a folder named `sprites` within the project directory:
   - `player.png`
   - `contoler.png`
   - `enemy.png`
   - `ps5_controller.png`
   - `special_controller.png`
   - `nuke.png`
   - `skells.png`

   Make sure these files are correctly named and placed in the folder for the game to load them.

## How to Run

From the repository's root directory, run the following command:
```bash
python game2.py
```

This command will launch the game window where you can start playing immediately.

## Gameplay

- **Objective:** Battle increasing waves of enemies by throwing controllers at them. Collect power-ups to enhance your attacks or clear the screen.
- **Scoring:** Points are awarded based on enemy type and kill method. Achieve a high score and aim for the top spot on the leaderboard.
- **Game Over:** The game ends if you suffer too many hits from the enemies. When game over occurs, you can choose to restart or exit.

## Controls

- **Left Arrow Key:** Move the player left.
- **Right Arrow Key:** Move the player right.
- **Space Bar:** Throw controllers (with power-up effects if active).
- **Additional Input:** Use the mouse or press "R" during the leaderboard screen to choose between restarting the game or exiting.

## Screenshots

*If you have screenshots available, add them here.*

```markdown
![Gameplay Screenshot](path/to/your/screenshot.png)
```

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/yourusername/the-attack-of-the-gamer-boys/issues) if you want to contribute.

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/YourFeature`.
3. Commit your changes: `git commit -m 'Add YourFeature'`.
4. Push to the branch: `git push origin feature/YourFeature`.
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Feel free to adjust the sections (such as screenshots or contributing guidelines) as you update your project, and replace `yourusername` in the repository URL with your actual GitHub username.

Enjoy developing and playing **The Attack of the Gamer Boys**!
