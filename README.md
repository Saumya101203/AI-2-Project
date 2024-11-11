## Spaceship Battle Game with AI
This is a simple spaceship battle game where a player controls a spaceship and attempts to hit an AI-controlled spaceship with lasers. The game uses fuzzy logic for the AI's decision-making, allowing the AI to dodge the player's lasers and shoot back. The game ends when one spaceship hits the other with a laser. Players can restart the game after a round.

## Table of Contents
Game Features
Installation
How to Play
Game Controls
AI Behavior
Credits

### Game Features
Player-controlled spaceship that moves left or right and shoots lasers.
AI-controlled spaceship that uses fuzzy logic to dodge lasers and shoot back.
Laser mechanics where both the player and the AI can shoot lasers at each other.
Game Over screen when one spaceship hits the other with a laser.
Restart option using the Enter key after the game ends.
Installation
Clone or download this repository to your local machine.

Make sure you have Python 3.x installed on your system.

#### Install the required libraries:

```
pip install pygame numpy scikit-fuzzy
```
Run the game with the following command:
```
python game.py
```
### How to Play
**Start the game**: When you run the game, the player’s spaceship will be positioned at the bottom of the screen, and the AI’s spaceship will be at the top.
**Move the player’s spaceship**: Use the Left and Right arrow keys to move the player’s spaceship horizontally.
**Shoot lasers**: Press the Spacebar to shoot lasers from the player's spaceship.
**AI behavior**: The AI will dodge incoming lasers and shoot back at regular intervals. The AI's movements and decisions are based on fuzzy logic that takes into account the player's spaceship position.
**Game Over**: The game ends when either the player hits the AI's spaceship with a laser or the AI hits the player's spaceship with a laser. A "Game Over" screen will appear with an option to restart.
**Restart the game**: Press Enter after the game ends to restart the game.
#### Game Controls
**Left Arrow**: Move player’s spaceship left.
**Right Arrow**: Move player’s spaceship right.
**Spacebar**: Fire laser from player’s spaceship.
**Enter**: Restart the game after a game-over screen.
#### AI Behavior
The AI spaceship uses fuzzy logic to decide how to move and dodge lasers:
The AI calculates the distance between itself and the player.
Based on this distance, the AI decides whether to move left, right, or stay still.
The AI also dodges the player's lasers by predicting their trajectory and reacting accordingly.
The AI fires lasers at the player at regular intervals, but this firing rate is adjustable for difficulty.
The AI's behavior becomes progressively more difficult as it is optimized to avoid laser strikes.
### Credits
Game Engine: Built with Python and Pygame for the graphical interface and game mechanics.
Fuzzy Logic: Implemented using the scikit-fuzzy library to control the AI's behavior.
Graphics: Basic geometric shapes (spaceships and lasers) for simplicity.
