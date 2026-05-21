import os
from task2.analyzer import SentenceAnalyzer, WordAnalyzer, SmileyAnalyzer
from task2.validator_email import is_valid_email
from task2.archiver import archive_file, save_results_to_file
from utils.inputValidate import input_data

def display_menu():
    print("\nText Analyzer Menu:")
    print("1. Analyze sentences")
    print("2. Analyze words")
    print("3. Count smileys")
    print("4. Validate email")
    print("5. Archive result file")
    print("0. Exit\n")


def get_path_to_file(file: str):
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_file_dir, 'files', file)


def get_text():
    try:
        with open(get_path_to_file("file.txt"), "r") as file:
            return file.read()

    except FileNotFoundError:
        return None


def analyze_sentences():
    text = get_text()
    if text is None:
        print("Text file not found")
        return

    result = SentenceAnalyzer(text).process()
    for key, value in result.items():
        print(f"{key.replace('_', ' ').capitalize()}: {value}")


def analyze_words():  # g, h, i, j, k, l, m, n, o
    text = get_text()
    if text is None:
        print("Text file not found")
        return

    result = WordAnalyzer(text).process()

    print(f"Total words: {result['word_count']}")
    print(f"Average word length: {result['avg_word_length']}")
    print(f"Words in range [g-o]: {', '.join(result['words_in_range_g_to_o'])}")

    print(f"Longest word: {result['longest_word']}")
    print(f"Longest word index: {result['longest_word_index']}")

    print("Odd-indexed words: ", ', '.join(result['odd_words']))


def analyze_smileys():
    text = get_text()
    if text is None:
        print("Text file not found")
        return

    result = SmileyAnalyzer(text).process()
    print(f"Smiley count: {result['smiley_count']}")


def validate_email():
    email = input_data("Enter an email to validate: ", str)
    print("Valid email!" if is_valid_email(email) else "Invalid email.")


def archive_results():
    text = get_text()
    if text is None:
        print("Text file not found")
        return

    sentences_result = SentenceAnalyzer(text).process()
    words_result = WordAnalyzer(text).process()
    smileys_result = SmileyAnalyzer(text).process()

    results = [
        f"Sentence Analysis: {sentences_result}",
        f"Word Analysis: {words_result}",
        f"Smiley Analysis: {smileys_result}",
    ]

    filename = get_path_to_file("archive_result.txt")
    save_results_to_file(filename, results)

    try:
        info = archive_file(filename)
        print("File archived successfully.")
        print(f"Archived: {info['filename']} ({info['size']} bytes -> {info['compress_size']} compressed)")
    except FileNotFoundError:
        print("File not found")


def task2():
    while True:
        display_menu()
        choice = input_data("Choose an option: ", str)
        match choice:
            case "1": analyze_sentences()
            case "2": analyze_words()
            case "3": analyze_smileys()
            case "4": validate_email()
            case "5": archive_results()
            case "0": break
            case _: print("Invalid choice. Please try again.")
