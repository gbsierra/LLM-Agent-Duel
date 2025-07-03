from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage
import re
import random

class NimAgent:

    """
    Initialize the Nim with a name and a language model.

    Attributes:
        name (str): The name of the agent.
        model (str): The name of the LLM model to use.
    """
    def __init__(self, name, model="llama3.2:latest"):
        self.name = name
        self.llm = ChatOllama(model=model)

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

    Returns:
        tuple or None: A legal move (heap_index, num_removed), or None if invalid.
    """
    def propose_move(self, state, memory):
        legal_moves = state.get_legal_moves()
        if not legal_moves:
            return None

        prompt = f"""
                You are playing the game of Nim.
                Current heaps: {state}
                Recent moves: {memory}
                Legal moves: {legal_moves}

                Choose the best next move from the list of legal moves.
                Only respond with a Python tuple from the list above, like (heap_index, num_removed).
                Do not invent new moves. Do not explain.
                """

        response = self.llm.invoke([HumanMessage(content=prompt)])
        raw = response.content.strip()
        #print(f"Raw response from {self.name}: {raw}")

        try:
            move = NimAgent.extract_move(raw)
            if move in legal_moves:
                return move
            else:
                print(f"⚠️ {self.name} proposed an illegal move: {move}")
        except ValueError:
            print(f"❌ {self.name} gave an invalid response.")

        # Fallback to a random legal move
        print(f"🔁 {self.name} falling back to random legal move.")
        return random.choice(legal_moves)