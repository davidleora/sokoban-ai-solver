#!/usr/bin/env python3
"""
Manual Sokoban Game Player
Play Sokoban manually to test game logic and understand the puzzles.

Usage:
    python manual_play.py

Controls:
    U or u - Move Up
    D or d - Move Down
    L or l - Move Left
    R or r - Move Right
    Q or q - Quit
    H or h - Show help
    S or s - Show current state
"""

from pathlib import Path
from src.sokoban import game_environment
import os


class ManualPlayer:
    def __init__(self, map_file):
        self.game = game_environment.SokobanGame(map_file)
        self.move_history = []
        self.step_count = 0
        
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def display_map(self):
        """Display the current map state."""
        map_str = self.game.serialize_map()
        print("\n" + "="*50)
        print(map_str)
        print("="*50)
        
    def display_legend(self):
        """Display the legend for map symbols."""
        print("\n📋 Legend:")
        print("  @ = Player")
        print("  $ = Box")
        print("  . = Goal (target)")
        print("  * = Box on goal")
        print("  + = Player on goal")
        print("  # = Wall")
        print("    = Empty space")
        
    def display_status(self):
        """Display current game status."""
        player_pos = self.game.gameStateObj['player']
        boxes = self.game.gameStateObj['boxes']
        goals = self.game.levelObj['goals']
        
        print(f"\n📊 Status:")
        print(f"  Steps taken: {self.step_count}")
        print(f"  Player position: {player_pos}")
        print(f"  Boxes: {len(boxes)} | Goals: {len(goals)}")
        print(f"  Boxes on goals: {sum(1 for box in boxes if box in goals)}/{len(goals)}")
        
        if self.move_history:
            recent_moves = ''.join(self.move_history[-10:])
            print(f"  Recent moves: {recent_moves}")
    
    def display_help(self):
        """Display help menu."""
        print("\n❓ Help:")
        print("  U or u - Move Up ⬆️")
        print("  D or d - Move Down ⬇️")
        print("  L or l - Move Left ⬅️")
        print("  R or r - Move Right ➡️")
        print("  Q or q - Quit game")
        print("  H or h - Show this help")
        print("  S or s - Show current state")
        print("  Z or z - Undo last move (not implemented yet)")
    
    def make_move(self, direction):
        """
        Make a move and return whether it was successful.
        
        Args:
            direction: 'U', 'D', 'L', or 'R'
            
        Returns:
            tuple: (success: bool, message: str)
        """
        direction = direction.upper()
        
        if direction not in ['U', 'D', 'L', 'R']:
            return False, "❌ Invalid direction! Use U, D, L, or R"
        
        # Try to make the move
        if self.game.makeMove(direction):
            self.move_history.append(direction)
            self.step_count += 1
            
            # Check if game is won
            if self.game.isLevelFinished():
                return True, "🎉 Congratulations! You solved the puzzle!"
            
            return True, "✅ Move successful!"
        else:
            return False, "❌ Invalid move! (wall, box blocked, or out of bounds)"
    
    def play(self):
        """Main game loop."""
        self.clear_screen()
        print("🎮 Welcome to Manual Sokoban Player! 🎮")
        self.display_legend()
        self.display_help()
        
        self.display_map()
        self.display_status()
        
        print("\n▶️  Game started! Enter your moves:")
        
        while True:
            try:
                # Get user input
                move = input("\n➤ Your move (U/D/L/R, H for help, Q to quit): ").strip()
                
                if not move:
                    continue
                
                move_upper = move.upper()
                
                # Handle special commands
                if move_upper == 'Q':
                    print("\n👋 Thanks for playing! Goodbye!")
                    break
                
                elif move_upper == 'H':
                    self.display_help()
                    continue
                
                elif move_upper == 'S':
                    self.clear_screen()
                    self.display_map()
                    self.display_status()
                    continue
                
                # Try to make the move
                success, message = self.make_move(move_upper)
                
                # Clear screen and display updated state
                self.clear_screen()
                self.display_map()
                self.display_status()
                print(f"\n{message}")
                
                # Check if won
                if self.game.isLevelFinished():
                    print(f"\n🏆 PUZZLE SOLVED! 🏆")
                    print(f"📝 Solution: {''.join(self.move_history)}")
                    print(f"📊 Total steps: {self.step_count}")
                    
                    replay = input("\n🔄 Play again? (y/n): ").strip().lower()
                    if replay == 'y':
                        # Reload the game
                        self.game = game_environment.SokobanGame(self.game.DATA_FILE)
                        self.move_history = []
                        self.step_count = 0
                        self.clear_screen()
                        self.display_map()
                        self.display_status()
                    else:
                        print("👋 Thanks for playing!")
                        break
                        
            except KeyboardInterrupt:
                print("\n\n👋 Game interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n⚠️  Error: {e}")


def main():
    """Main entry point."""
    print("🎮 Manual Sokoban Player 🎮\n")
    
    # Default map
    default_map = Path.cwd() / "dataset/human_demos/4_1.txt"
    
    # Show available maps
    print("📁 Available maps in dataset/human_demos/:")
    demo_dir = Path.cwd() / "dataset/human_demos"
    if demo_dir.exists():
        maps = sorted([f.name for f in demo_dir.glob("*.txt")])
        for i, map_name in enumerate(maps[:10], 1):  # Show first 10
            print(f"  {i}. {map_name}")
        if len(maps) > 10:
            print(f"  ... and {len(maps) - 10} more")
    
    print(f"\n📍 Default map: {default_map.name}")
    
    # Ask user for map selection
    choice = input(f"\nEnter map filename (or press Enter for default): ").strip()
    
    if choice:
        map_file = Path.cwd() / "dataset/human_demos" / choice
        if not map_file.exists():
            # Try adding .txt extension
            map_file = Path.cwd() / "dataset/human_demos" / f"{choice}.txt"
            if not map_file.exists():
                print(f"⚠️  Map not found! Using default: {default_map.name}")
                map_file = default_map
    else:
        map_file = default_map
    
    print(f"\n✅ Loading map: {map_file.name}\n")
    
    try:
        player = ManualPlayer(map_file)
        player.play()
    except FileNotFoundError:
        print(f"❌ Error: Map file not found: {map_file}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()

