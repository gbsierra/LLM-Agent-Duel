from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage
import re
import random

class NimAgent:
    """
    Initialize the Nim agent with a name and a language model.

    Attributes:
        name (str): The name of the agent.
        model (str): The name of the LLM model to use.
        illegal_moves (int): Count of illegal moves proposed.
        fallbacks_used (int): Count of times fallback was triggered.
    """
    def __init__(self, name, model="llama3.2:latest"):
        self.name = name
        self.llm = ChatOllama(model=model)
        self.illegal_moves = 0
        self.fallbacks_used = 0

    """
    Extract a move from the LLM's raw text response.

    Args:
        text (str): The raw response from the LLM.

    Returns:
        tuple: A move in the form (heap_index, num_removed).

    Raises:
        ValueError: If the move format is invalid.
    """
    @staticmethod
    def extract_move(text):
        # Normalize and strip quotes/extra parentheses
        text = text.strip().strip("'\"")
        text = re.sub(r"^\(+|\)+$", "", text)
        match = re.search(r"(\d+),\s*(\d+)", text)
        if match:
            return int(match.group(1)), int(match.group(2))
        raise ValueError(f"Invalid move format: {text}")

    """
    Propose a move based on the current Nim state and shared memory.

    Args:
        state (NimState): The current state of the Nim game.
        memory (list): A list of recent moves.
        output (bool): Whether to print debug output.
        prompt (str): The type of prompt to use

    Returns:
        tuple or None: A legal move (heap_index, num_removed), or None if invalid.
    """
    def propose_move(self, state, memory, output=False, prompt="baseline"):
        legal_moves = state.get_legal_moves()
        if not legal_moves:
            return None

        match prompt:
            case "baseline":
                prompt = f"""
                You are playing the game of Nim.
                Current heaps: {state}
                Recent moves: {memory}
                Legal moves: {legal_moves}

                Choose the best next move from the list of legal moves.
                Only respond with a Python tuple from the list above, like (heap_index, num_removed).
                Do not invent new moves. Do not explain.
                """

            case "game_theorist":
                prompt = f"""
                You are a world-class game theorist specializing in combinatorial games like Nim.

                Current heaps: {state}
                Recent moves: {memory}
                Legal moves: {legal_moves}

                Use your deep understanding of game theory to choose the best next move from the list of legal moves.
                Only respond with a Python tuple from the list above, like (heap_index, num_removed). Do not explain.
                """

            case "math_genius":
                prompt = f"""
                You are a mathematical genius specializing in combinatorial games like Nim.

                Current heaps: {state}
                Recent moves: {memory}
                Legal moves: {legal_moves}

                Use your mathematical insight to choose the best next move from the list of legal moves.
                Only respond with a Python tuple from the list above, like (heap_index, num_removed). Do not explain.
                """

            case "XOR_strat":
                prompt = f"""
                You are playing the game of Nim.

                Your objective is to win by removing objects from the heaps so that your opponent is left in a losing position.

                Follow this rule-based strategy:
                - Compute the Nim sum (bitwise XOR of all heap sizes).
                - If the Nim sum is 0, you are in a losing position. Choose any legal move.
                - If the Nim sum is not 0, choose a move that changes one heap so that the new Nim sum becomes 0.

                Current heaps: {state}
                Recent moves: {memory}
                Legal moves: {legal_moves}

                Choose the next move that follows this rule-based strategy. Only respond with a Python tuple from the list above, like (heap_index, num_removed).
                Do not invent new moves. Do not explain.
                """
   
        response = self.llm.invoke([HumanMessage(content=prompt)])
        raw = response.content.strip()

        try:
            move = NimAgent.extract_move(raw)
            if move in legal_moves:
                return move
            else:
                if output:
                    print(f"⚠️ {self.name} proposed an illegal move: {move}")
                self.illegal_moves += 1
        except ValueError:
            if output:
                print(f"❌ {self.name} gave an invalid response.")
            self.illegal_moves += 1

        # Fallback to a random legal move
        if output:
            print(f"🔁 {self.name} falling back to random legal move.")
        self.fallbacks_used += 1
        return random.choice(legal_moves)