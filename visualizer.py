import matplotlib.pyplot as plt
import threading
import time

class Visualizer:
    def __init__(self):
        self.q_values_over_time = {action: [] for action in range(3)}
        self.running = True

    def update(self, q_values):
        """Append new Q-values for visualization."""
        for action, value in q_values.items():
            self.q_values_over_time[action].append(value)

    def start(self):
        """Start the visualization in a separate thread."""
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        """Plot Q-values dynamically."""
        plt.ion()
        fig, ax = plt.subplots()
        while self.running:
            ax.clear()
            for action, values in self.q_values_over_time.items():
                ax.plot(range(len(values)), values, label=f"Action {action}")
            ax.set_title("Q-values Over Time")
            ax.set_xlabel("Time")
            ax.set_ylabel("Q-values")
            ax.legend()
            plt.pause(0.1)
            time.sleep(0.1)
        plt.ioff()

    def stop(self):
        """Stop the visualization."""
        self.running = False
