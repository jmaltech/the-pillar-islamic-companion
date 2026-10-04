import json
from pathlib import Path


class FlashcardManager:
    def __init__(self):
        data_path = Path(__file__).resolve().parents[1] / "data" / "flashcards.json"
        with data_path.open("r", encoding="utf-8") as file:
            self.flashcards = json.load(file)

        self.current_index = 0
        self.list_length = len(self.flashcards)
        self.is_flipped = False

    def next_card(self):
        self.current_index = (self.current_index + 1) % self.list_length
        self.is_flipped = False

    def prev_card(self):
        self.current_index = (self.current_index - 1) % self.list_length
        self.is_flipped = False

    def flip_card(self):
        self.is_flipped = not self.is_flipped

    def get_current_text(self):
        if self.is_flipped:
            return self.flashcards[self.current_index]["answer"]
        return self.flashcards[self.current_index]["question"]

    def get_current_number(self):
        return f"{self.current_index + 1} / {self.list_length}"


if __name__ == "__main__":
    islamic_questions = FlashcardManager()
    print(islamic_questions.get_current_text())
