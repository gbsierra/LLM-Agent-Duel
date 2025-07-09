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
        self.illegal_moves = 0  # Track number of illegal moves
        self.fallbacks_used = 0  # Track number of fallbacks used (not used in this agent)

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
        state: The current state of the Hanoi puzzle.
        memory (list): A list of recent moves to avoid repetition.
        output (bool): Whether to print debug information.
        prompt (str): The type of prompt to use

    Returns:
        tuple or None: A legal move (from_peg, to_peg), or None if the response is invalid or illegal.
    """
    def propose_move(self, state, memory, output=False, prompt="baseline"):
        legal_moves = state.get_legal_moves()

        match prompt:
            case "baseline":
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

            case "recursive_genius":
                prompt = f"""
                You are a recursive problem-solving expert, known for solving Tower of Hanoi puzzles with perfect efficiency.

                Your goal is to move all disks from peg 0 to peg 2, following these rules:
                - Only one disk can be moved at a time.
                - A larger disk may never be placed on top of a smaller disk.

                Current state: {state}
                Recent moves: {memory}
                Legal moves: {legal_moves}

                Use your recursive reasoning to choose the best next move from the list of legal moves.
                Only respond with a Python tuple like (from_peg, to_peg). Do not explain.
                """

            case "math_genius":
                prompt = f"""
                You are a mathematical genius, known for solving Tower of Hanoi puzzles with perfect efficiency.

                Your goal is to move all disks from peg 0 to peg 2, following these rules:
                - Only one disk can be moved at a time.
                - A larger disk may never be placed on top of a smaller disk.

                Current state: {state}
                Recent moves: {memory}
                Legal moves: {legal_moves}

                Use your mathematical insight to choose the best next move from the list of legal moves.
                Only respond with a Python tuple like (from_peg, to_peg). Do not explain.
                """

            case "recursive_strat":
                prompt = f"""
                You are solving the Tower of Hanoi puzzle with 3 disks.

                Your objective is to move all disks from peg 0 to peg 2 using peg 1 as auxiliary.
                Follow the classic recursive strategy:
                - Move the top n-1 disks to the auxiliary peg.
                - Move the largest disk to the target peg.
                - Move the n-1 disks from the auxiliary peg to the target peg.

                Current state: {state}
                Recent moves: {memory}
                Legal moves: {legal_moves}

                Choose the next move that follows this recursive plan. Only respond with a Python tuple like (from_peg, to_peg).
                """

        response = self.llm.invoke([HumanMessage(content=prompt)])
        raw = response.content.strip()

        if output:
            print(f"Raw response from {self.name}: {raw}")

        try:
            move = HanoiAgent.extract_move(raw)
            if move in legal_moves:
                return move
            else:
                self.illegal_moves += 1
                if output:
                    print(f"⚠️ {self.name} proposed an illegal move: {move}")
        except ValueError:
            self.illegal_moves += 1
            if output:
                print(f"❌ {self.name} gave an invalid response.")
        return None