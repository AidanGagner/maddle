import re
import sys
import time
from pathlib import Path


def scroll(text, delay=0.01):
    """Prints text one character at a time."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def sequential_replace(text, replacements):
    """Replaces each [placeholder] with the player-provided text."""

    def replacement_generator():
        for word in replacements:
            yield word

    gen = replacement_generator()
    return re.sub(r"\[[^\[\]]+?\]", lambda _: next(gen), text)


def read_with_punc_pauses(text):
    """Pauses the story display at the end of each sentence."""
    scroll("\n* * * STORYTIME * * *\n")
    input()
    segments = re.split(r'([.!?]"?)', text)
    for i in range(0, len(segments) - 1, 2):
        scroll(segments[i] + segments[i + 1])
        input()
    if len(segments) % 2 != 0:
        scroll(segments[-1])


def game(stories_dir: Path):
    """Runs the maddles game using selected story files."""
    print("* CHOOSE A STORY *")
    maddle_files = [
        f for f in stories_dir.iterdir() if f.is_file() and f.suffix == ".txt"
    ]

    if not maddle_files:
        print("No stories found!")
        return

    for index, file in enumerate(maddle_files, start=1):
        print(f"[{index}] {file.stem}")

    story_choice = input("> ").strip()

    try:
        choice_index = int(story_choice) - 1
        if 0 <= choice_index < len(maddle_files):
            file_path = maddle_files[choice_index]
            text = file_path.read_text(encoding="utf-8")
        else:
            print("Invalid input.")
            return
    except ValueError:
        print("Input must be a number.")
        return

    # Finds all to-be-replaced text in brackets, like [noun] and [verb.]
    player_words = re.findall(r"\[[^\[\]]+?\]", text)

    print()
    user_inputs = []
    for i, player_word in enumerate(player_words, 1):
        prompt = player_word[1:-1]
        user_input = input(f"{prompt}:\n  > ")
        user_inputs.append(user_input)

    final_text = sequential_replace(text, user_inputs)

    print("\n")
    read_with_punc_pauses(final_text)
