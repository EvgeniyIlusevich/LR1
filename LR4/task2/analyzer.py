import re

class BaseAnalyzer:
    """Base class for all processors."""
    def __init__(self, text):
        self.text = text

    def process(self):
        raise NotImplementedError("Must be overridden in subclass")


class SentenceAnalyzer(BaseAnalyzer):
    """Processes sentence statistics from text."""
    def process(self):
        sentences = re.findall(r'[^.!?]+[.!?]', self.text)
        declarative = len(re.findall(r'[^.!?]+\.', self.text))
        interrogative = len(re.findall(r'[^.!?]+\?', self.text))
        imperative = len(re.findall(r'[^.!?]+!', self.text))
        avg_sentence_len = sum(len(re.findall(r'\b\w+\b', sentence)) for sentence in sentences) / len(sentences) if sentences else 0

        return {
            "total": len(sentences),
            "declarative": declarative,
            "interrogative": interrogative,
            "imperative": imperative,
            "avg_sentence_length": round(avg_sentence_len, 2)
        }


class WordAnalyzer(BaseAnalyzer):
    """Processes word statistics from text."""
    def process(self):
        words = re.findall(r'\b\w+\b', self.text)

        # 1. Calculate the average word length
        avg_word_len = sum(len(word) for word in words) / len(words) if words else 0

        # 2. Find words within the range g-o (inclusive)
        in_range = [word for word in words if re.search(r'[g-o]', word, re.IGNORECASE)]

        # 3. Find the longest word and its position
        longest_word = max(words, key=len)
        longest_word_index = words.index(longest_word) + 1

        # 4. Extract odd-indexed words (1st, 3rd, 5th, etc.)
        odd_words = words[::2]

        return {
            "word_count": len(words),
            "avg_word_length": round(avg_word_len, 2),
            "words_in_range_g_to_o": in_range,
            "longest_word": longest_word,
            "longest_word_index": longest_word_index,
            "odd_words": odd_words
        }


class SmileyAnalyzer(BaseAnalyzer):
    """Finds all valid smileys in the text."""
    def process(self):
        smileys = re.findall(r'[:;]-*([\(\)\[\]])\1+', self.text)
        return {"smiley_count": len(smileys)}