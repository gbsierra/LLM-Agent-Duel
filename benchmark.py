import os
import csv
from datetime import datetime
from main import run_game
from main import prompt_types_hanoi, prompt_types_nim

# game config
game_input = ""
NUM_GAMES = 10
results = []

# Ensure benchmarks directory exists
os.makedirs("benchmarks", exist_ok=True)

# get input for game type
game_input = input("Select Towers of Hanoi or Nim Game (H/N):").strip().lower()
if game_input == "h":
    game_input = "hanoi"
elif game_input == "n":
    game_input = "nim"
else:
    print("Invalid selection! Defaulting to Nim.")
    game_input = "nim"

# print possible prompt types and get inputs
if game_input == "hanoi":
    print("Available prompt types for Towers of Hanoi:")
    for i, prompt in enumerate(prompt_types_hanoi, start=1):
        print(f"{i}. {prompt}")
    selected_prompts = input("Select prompt types by number (comma-separated, e.g. 1,2): ").strip()
    selected_prompts = [prompt_types_hanoi[int(i) - 1] for i in selected_prompts.split(",") if i.isdigit()]

elif game_input == "nim":
    print("Available prompt types for Nim:")
    for i, prompt in enumerate(prompt_types_nim, start=1):
        print(f"{i}. {prompt}")
    selected_prompts = input("Select prompt types by number (comma-separated, e.g. 1,2): ").strip()
    selected_prompts = [prompt_types_nim[int(i) - 1] for i in selected_prompts.split(",") if i.isdigit()]



# for all selected prompts,
for prompt in selected_prompts:
    
    print(f"\nRunning benchmark for {game_input} with prompt type: {prompt}")
    results = []  # reset results for each prompt

    # run games, appending results
    for i in range(NUM_GAMES):
        result = run_game(selected_game=game_input, output=False, prompt=prompt)
        result["game_number"] = i + 1
        results.append(result)
        print(f"Game {i+1}: Winner = {result['winner']}, Turns = {result['turns']}")

    # create timestamped filename in benchmarks dir
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join("benchmarks", f"{game_input}_benchmark_{prompt}_{timestamp}.csv")

    # Save results to CSV
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "game_number", "winner", "turns", "solved",
            "illegal_moves_agent_a", "illegal_moves_agent_b",
            "fallbacks_agent_a", "fallbacks_agent_b"
        ])
        writer.writeheader()
        writer.writerows(results)

print(f"\n✅ Benchmarking completed. Results have been saved to benchmarks directory.\n")