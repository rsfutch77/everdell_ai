import matplotlib.pyplot as plt
import json
import numpy as np
import time

def plot_live(data_file, interval=1):
    plt.ion()  # Turn on interactive mode
    fig, axs = plt.subplots(3, 1, figsize=(10, 10))
    axs[0].set_title('TD Error Over Time')
    axs[0].set_xlabel('Episode')
    axs[0].set_ylabel('TD Error')
    axs[1].set_title('AI Scores Over Episodes')
    axs[1].set_xlabel('Episode')
    axs[1].set_ylabel('Score')
    axs[2].set_title('AI Win Rate Over Time')
    axs[2].set_xlabel('Episode')
    axs[2].set_ylabel('Win Rate')

    while True:
        try:
            with open(data_file, 'r') as f:
                content = f.read().strip()
                if not content:
                    print("Data file is empty. Skipping this iteration.")
                    time.sleep(interval)
                    continue
                try:
                    data = json.loads(content)
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                    time.sleep(interval)
                    continue
            for ax in axs:
                ax.clear()
            axs[0].set_title('TD Error Over Time')
            axs[1].set_title('AI Scores Over Episodes')
            axs[2].set_title('AI Win Rate Over Time')

            for agent_index, td_errors in enumerate(data['td_errors']):
                long_window_size = 200  # Increase the window size for a longer moving average
                if len(td_errors) >= long_window_size:
                    moving_avg = np.convolve(td_errors, np.ones(long_window_size)/long_window_size, mode='valid')
                    axs[0].plot(range(long_window_size - 1, len(td_errors)), moving_avg, label=f'AI {agent_index} Moving Avg')
            axs[0].legend()

            for agent_index, scores in enumerate(data['scores']):
                axs[1].plot(scores, label=f'AI {agent_index}')
            for agent_index, scores in enumerate(data['scores']):
                long_window_size = 20  # Increase the window size for a longer moving average
                if len(scores) >= long_window_size:
                    moving_avg = np.convolve(scores, np.ones(long_window_size)/long_window_size, mode='valid')
                    axs[1].plot(range(long_window_size - 1, len(scores)), moving_avg, linestyle='--', label=f'AI {agent_index} Moving Avg')
            axs[1].legend()

            for agent_index, win_rates in enumerate(data['win_rates']):
                axs[2].plot(win_rates, label=f'AI {agent_index}')
            axs[2].legend()

            plt.pause(interval)
        except Exception as e:
            print(f"Plotting error: {e}")
        time.sleep(interval)

    plt.ioff()  # Turn off interactive mode
    plt.show()
