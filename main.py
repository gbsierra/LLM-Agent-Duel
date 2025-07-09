from memory.shared_memory import SharedMemory
import os # to clear console


# prompt types
prompt_types_hanoi = ["baseline", "recursive_genius", "math_genius", "recursive_strat"]
prompt_types_nim = [ "baseline", "game_theorist", "math_genius", "XOR_strat" ]

# Game selection: "hanoi" or "nim"
def run_game(selected_game="nim", output=True, prompt="baseline"):
    # Importing necessary modules based on selected game
    if selected_game == "hanoi":
        from agents.hanoi_agent import HanoiAgent
        from puzzles.hanoi import HanoiState

        agent1 = HanoiAgent("Llama3.2 Agent", model="llama3.2:latest")
        agent2 = HanoiAgent("Gemma3 Agent", model="gemma3:latest")
        state = HanoiState(num_disks=3)

        def is_done():
            return state.is_solved()

    elif selected_game == "nim":
        from agents.nim_agent import NimAgent
        from puzzles.nim import NimState

        agent1 = NimAgent("Llama3.2 Agent", model="llama3.2:latest")
        agent2 = NimAgent("Gemma3 Agent", model="gemma3:latest")
        state = NimState([3, 4, 5])

        def is_done():
            return state.is_game_over()

    else:
        raise ValueError("Unsupported game selected.")

    # Shared memory for agents to use
    memory = SharedMemory()
    agents = [agent1, agent2]
    turn = 0

    # Main game loop
    while not is_done() and turn < 20:
        agent = agents[turn % 2]
        move = agent.propose_move(state, memory.get_recent(), output=output, prompt=prompt)

        if output:
            print(f"{agent.name} proposes move: {move}")

        if move is None:
            if output:
                print("⚠️ No valid move proposed. Skipping turn.")
        elif state.move(*move):
            memory.update(move, state)
        else:
            if output:
                print("Illegal move. Skipping.")

        if output:
            state.display()

        turn += 1

    # Game result
    winner = agents[(turn - 1) % 2].name if is_done() else None

    if output:
        if winner:
            print(f"🎉 {winner} wins!")
        else:
            print(f"❌ Game ended without a solution in {turn} turns.")

    # Return result for logging or analysis
    return {
        "winner": winner,
        "turns": turn,
        "solved": is_done(),
        "illegal_moves_agent_a": agent1.illegal_moves,
        "illegal_moves_agent_b": agent2.illegal_moves,
        "fallbacks_agent_a": agent1.fallbacks_used,
        "fallbacks_agent_b": agent2.fallbacks_used
    }

if __name__ == "__main__":
    # select game
    game_input = input("Select Towers of Hanoi or Nim Game (H/N):").strip().lower()

    if game_input in ["H", "h"]:
        game_input = "hanoi"

        # print available prompt types
        print("Available prompt types for Towers of Hanoi:")
        for i, prompt in enumerate(prompt_types_hanoi, start=1):
            print(f"{i}. {prompt}")
    elif game_input in ["N", "n"]:
        game_input = "nim"

        # print available prompt types
        print("Available prompt types for Nim:")
        for i, prompt in enumerate(prompt_types_nim, start=1):
            print(f"{i}. {prompt}")
    else:
        print("Invalid selection! Defaulting to Nim.")
        game_input = "nim"

        # print available prompt types
        print("Available prompt types for Nim:")
        for i, prompt in enumerate(prompt_types_nim, start=1):
            print(f"{i}. {prompt}")

    # select prompt type
    prompt_type = int(input("Select a prompt type (enter the number): ")) - 1
    if game_input == "hanoi":
        prompt_type = prompt_types_hanoi[prompt_type]
    elif game_input == "nim":
        prompt_type = prompt_types_nim[prompt_type]

    # ask to clear screen
    clear_screen = input("Would you like the console cleared? (Y/N): ").strip().lower()
    if clear_screen in ["Y", "y"]:
        os.system('cls' if os.name == 'nt' else 'clear')
    
    # add title
    print(f"\nRunning: {game_input}\n Prompt type: {prompt_type}\n")

    # run game 
    run_game(selected_game=game_input, output=True, prompt=prompt_type)