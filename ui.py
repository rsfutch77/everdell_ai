import tkinter as tk
from tkinter import messagebox
import ai_game
from main import cards, deck

def train_model():
    # Function to train the model
    num_episodes = 1000  # Number of episodes to train the AI
    ai_player = ai_game.ReinforcementLearningAgent()
    adversarial_ai_player = ai_game.AdversarialAIPlayer()
    local_deck = [ai_game.Card(name, points) for name, points in cards]
    game = ai_game.Game(local_deck, ai_player, adversarial_ai_player)
    game.train(num_episodes)
    messagebox.showinfo("Training", "Model training complete!")

def load_and_test_model():
    # Function to load and test the model
    ai_player.load_model('ai_model.pkl')
    messagebox.showinfo("Testing", "Model loaded and ready for testing!")

def setup_ui():
    root = tk.Tk()
    root.title("Everdell AI")

    # Create a frame for the buttons
    frame = tk.Frame(root)
    frame.pack(pady=20)

    # Add a button to train the model
    train_button = tk.Button(frame, text="Train Model", command=train_model)
    train_button.pack(side=tk.LEFT, padx=10)

    # Add a button to load and test the model
    test_button = tk.Button(frame, text="Load and Test Model", command=load_and_test_model)
    test_button.pack(side=tk.LEFT, padx=10)

    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    setup_ui()