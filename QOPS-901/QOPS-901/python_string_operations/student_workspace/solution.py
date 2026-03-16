class Solution:
    def convert_to_uppercase(self, text: str) -> str:
        text = "python programming language"
        result = text.upper()
        print(f"Uppercase: {result}")

    def convert_to_lowercase(self, text: str) -> str:
        text = "WELCOME TO PYTHON"
        result = text.lower()
        print(f"Lowercase: {result}")

    def capitalize_sentence(self, text: str) -> str:
        text = "python is easy to learn"
        result = text.capitalize()
        print(f"Capitalized: {result}")

    def count_word_occurrences(self, text: str, target: str) -> int:
        text = "data science is fun because data drives decisions"
        count = text.count("data")
        print(f"Count of 'data': {count}")

    def replace_word(self, text: str, old_word: str, new_word: str) -> str:
        text = "Python is a powerful language"
        result = text.replace("Python", "Java")
        print(f"Replaced: {result}")

    def split_sentence(self, text: str) -> list:
        text = "Python makes data analysis easier"
        words = text.split()
        print(f"Split Words: {words}")
