import tkinter as tk
from tkinter import messagebox
import ai_game
from main import cards, deck

def train_model(root):
    # Function to train the model
    num_episodes = 200  # Number of episodes to train the AI
    ai_player = ai_game.ReinforcementLearningAgent(alpha=0.1, gamma=0.9, epsilon=0.1)
    adversarial_ai_player = ai_game.ReinforcementLearningAgent(alpha=0.1, gamma=0.9, epsilon=0.1)
    local_deck = [ai_game.Card(name, points, cost) for name, points, cost in cards]
    game = ai_game.Game(local_deck, ai_player, adversarial_ai_player, turn_update_callback=update_turn_counter, ui_root=root, time_to_wait_entry=time_to_wait_entry)
    game.train(num_episodes)
    messagebox.showinfo("Training", "Model training complete!")

# ... rest of the ui.py file ...
def load_and_test_model():
    # Function to load and test the model
    ai_player = ai_game.ReinforcementLearningAgent()
    ai_player.load_model('ai_model.pkl')
    # Disable exploration to use the model for inference
    ai_player.epsilon = 0
    adversarial_ai_player = ai_game.ReinforcementLearningAgent(alpha=0.1, gamma=0.9, epsilon=0.1)
    local_deck = [ai_game.Card(name, points, cost) for name, points, cost in cards]
    game = ai_game.Game(local_deck, ai_player, adversarial_ai_player)
    num_episodes = 200  # Number of episodes for testing
    ai_wins = 0
    for episode in range(num_episodes):
        game.reset_game()
        while not game.is_game_over():
            game.play_turn()
        ai_score, adversarial_ai_score = game.calculate_score()
        if ai_score > adversarial_ai_score:
            ai_wins += 1
    win_rate = ai_wins / num_episodes
    messagebox.showinfo("Testing", f"Model tested for {num_episodes} episodes.\nAI Win Rate: {win_rate:.2%}")
    turn_counter_label = None

def update_turn_counter(turn):
    turn_counter_label.config(text=f"Turn: {turn + 1}")

def setup_ui():
    global turn_counter_label
def setup_ui():
    global turn_counter_label, time_to_wait_entry
    root = tk.Tk()
    root.title("Everdell AI")
    # Turn counter label
    turn_counter_label = tk.Label(root, text="Turn: 0")
    turn_counter_label.pack(anchor='ne', padx=10, pady=10)

    # Time to wait label and entry
    time_to_wait_frame = tk.Frame(root)
    time_to_wait_frame.pack(anchor='nw', padx=10, pady=10)
    time_to_wait_label = tk.Label(time_to_wait_frame, text="Time to Wait (seconds):")
    time_to_wait_label.pack(side=tk.LEFT)
    time_to_wait_entry = tk.Entry(time_to_wait_frame)
    time_to_wait_entry.pack(side=tk.LEFT)


    # Create a frame for the buttons
    frame = tk.Frame(root)
    frame.pack(pady=20)

    # Add a button to train the model
    train_button = tk.Button(frame, text="Train Model", command=lambda: train_model(root))
    train_button.pack(side=tk.LEFT, padx=10)

    # Add a button to load and test the model
    test_button = tk.Button(frame, text="Load and Test Model", command=load_and_test_model)
    test_button.pack(side=tk.LEFT, padx=10)

    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    setup_ui()
