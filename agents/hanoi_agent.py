from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage
import re

class HanoiAgent:

    """
    Initialize the HanoiAgent with a name and a language model.

    Args:
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
        tuple: A move in the form (from_peg, to_peg).

    Raises:
        ValueError: If the move format is invalid.
    """
    @staticmethod
    def extract_move(text):
        match = re.search(r"\((\d+),\s*(\d+)\)", text)
        if match:
            return int(match.group(1)), int(match.group(2))
        raise ValueError(f"Invalid move format: {text}")

    """
    Propose the next move in the Tower of Hanoi puzzle using the language model.

    Args:
        state: The current state of the puzzle. Must implement get_legal_moves().
        memory (list): A list of recent moves to avoid repetition.

    Returns:
        tuple or None: A legal move (from_peg, to_peg), or None if the response is invalid or illegal.
    """
    def propose_move(self, state, memory):
        legal_moves = state.get_legal_moves()
        prompt = f"""
                You are solving the Tower of Hanoi puzzle.

                Your goal is to move all disks from peg 0 to peg 2, following these rules:
                - Only one disk can be moved at a time.
                - A larger disk may never be placed on top of a smaller disk.

                Current state: {state}
                Recent moves: {memory}
                Legal moves: {legal_moves}

                Choose the best next move from the list of legal moves that brings you closer to solving the puzzle.
                Avoid repeating previous states or undoing recent moves.
                Only respond with a Python tuple like (from_peg, to_peg). Do not explain.
                """
        response = self.llm.invoke([HumanMessage(content=prompt)])
        raw = response.content.strip()
        # print(f"Raw response from {self.name}: {raw}")
        try:
            move = HanoiAgent.extract_move(raw)
            if move in legal_moves:
                return move
            else:
                print(f"⚠️ {self.name} proposed an illegal move: {move}")
        except ValueError:
            print(f"❌ {self.name} gave an invalid response.")
        return None