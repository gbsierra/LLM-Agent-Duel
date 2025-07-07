from memory.shared_memory import SharedMemory

# Game selection: "hanoi" or "nim"
def run_game(selected_game="nim", output=True):
    # Importing necessary modules based on selected game
    if selected_game == "hanoi":
        from agents.hanoi_agent import HanoiAgent
        from puzzles.hanoi import HanoiState

        agent1 = HanoiAgent("Agent A")
        agent2 = HanoiAgent("Agent B")
        state = HanoiState(num_disks=3)

        def is_done():
            return state.is_solved()

    elif selected_game == "nim":
        from agents.nim_agent import NimAgent
        from puzzles.nim import NimState

        agent1 = NimAgent("Agent A")
        agent2 = NimAgent("Agent B")
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
        move = agent.propose_move(state, memory.get_recent(), output=output)

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
    run_game(selected_game="hanoi", output=True)