class Solution:
    def convert_to_uppercase(self, text: str) -> str:
        return text.upper()

    def convert_to_lowercase(self, text: str) -> str:
        return text.lower()

    def capitalize_sentence(self, text: str) -> str:
        return text.capitalize()

    def count_word_occurrences(self, text: str, target: str) -> int:
        return text.count(target)

    def replace_word(self, text: str, old_word: str, new_word: str) -> str:
        return text.replace(old_word, new_word)

    def split_sentence(self, text: str) -> list:
        return text.split()
