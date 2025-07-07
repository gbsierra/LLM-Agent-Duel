import os
import csv
from datetime import datetime
from main import run_game

# game config
selected_game = "hanoi"
NUM_GAMES = 10
results = []

# Ensure benchmarks directory exists
os.makedirs("benchmarks", exist_ok=True)

# run games, appending results
for i in range(NUM_GAMES):
    result = run_game(selected_game=selected_game, output=False)
    result["game_number"] = i + 1
    results.append(result)
    print(f"Game {i+1}: Winner = {result['winner']}, Turns = {result['turns']}")

# create timestamped filename in benchmarks dir
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = os.path.join("benchmarks", f"{selected_game}_benchmark_{timestamp}.csv")

# Save results to CSV
with open(filename, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "game_number", "winner", "turns", "solved",
        "illegal_moves_agent_a", "illegal_moves_agent_b",
        "fallbacks_agent_a", "fallbacks_agent_b"
    ])
    writer.writeheader()
    writer.writerows(results)

print(f"✅ Benchmark completed. Results have been saved to {filename}")