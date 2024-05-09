import tkinter as tk
from tkinter import messagebox
import ai_game
from main import cards, agents

def train_model(root, num_agents_entry):
    # Function to train the model
    num_episodes = 200  # Number of episodes to train the AI
    # agents are already defined in main.py, no need to redefine them here
    deck = [ai_game.Card(name, points, cost) for name, points, cost in cards]
    try:
        # Read the value from the num_agents_entry and convert it to an integer
        number_of_agents = int(num_agents_entry.get())
    except ValueError:
        # If the value is not a valid integer, default to 2 agents
        number_of_agents = 2
    agents = [ai_game.ReinforcementLearningAgent(alpha=0.1, gamma=0.9, epsilon=0.1) for _ in range(number_of_agents)]
    game = ai_game.Game(deck, agents, turn_update_callback=update_turn_counter, ui_root=root, time_to_wait_entry=time_to_wait_entry)
    game.train(num_episodes)
    messagebox.showinfo("Training", "Model training complete!")

def load_and_test_model():
    # Function to load and test the model
    agents[0] = ai_game.ReinforcementLearningAgent()
    agents[0].load_model('ai_model.pkl')
    # Disable exploration to use the model for inference
    agents[0].epsilon = 0
    agents[1] = ai_game.ReinforcementLearningAgent(alpha=0.1, gamma=0.9, epsilon=0.1)
    local_deck = [ai_game.Card(name, points, cost) for name, points, cost in cards]
    game = ai_game.Game(local_deck, agents[0], agents[1])
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
def setup_ui():
    global turn_counter_label, time_to_wait_entry, num_agents_entry
    root = tk.Tk()
    root.title("Everdell AI")
    # Turn counter label
    turn_counter_label = tk.Label(root, text="Turn: 0")
    turn_counter_label.pack(anchor='ne', padx=10, pady=10)

    # Number of agents label and entry
    num_agents_frame = tk.Frame(root)
    num_agents_frame.pack(anchor='nw', padx=10, pady=10)
    num_agents_label = tk.Label(num_agents_frame, text="Number of Agents:")
    num_agents_label.pack(side=tk.LEFT)
    num_agents_entry = tk.Entry(num_agents_frame, textvariable=tk.StringVar(value="2"))
    num_agents_entry.pack(side=tk.LEFT)

    # Time to wait label and entry
    time_to_wait_frame = tk.Frame(root)
    time_to_wait_frame.pack(anchor='nw', padx=10, pady=10)
    time_to_wait_label = tk.Label(time_to_wait_frame, text="Time to Wait (seconds):")
    time_to_wait_label.pack(side=tk.LEFT)
    time_to_wait_entry = tk.Entry(time_to_wait_frame, textvariable=tk.StringVar(value="0.001"))
    time_to_wait_entry.pack(side=tk.LEFT)


    # Create a frame for the buttons
    frame = tk.Frame(root)
    frame.pack(pady=20)

    # Add a button to train the model
    train_button = tk.Button(frame, text="Train Model", command=lambda: train_model(root, num_agents_entry))
    train_button.pack(side=tk.LEFT, padx=10)

    # Add a button to load and test the model
    test_button = tk.Button(frame, text="Load and Test Model", command=load_and_test_model)
    test_button.pack(side=tk.LEFT, padx=10)

    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    setup_ui()
