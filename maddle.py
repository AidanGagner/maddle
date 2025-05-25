import sys
from maddle_functions import game
from pathlib import Path


def create_dir(stories_dir):
    """Prompts user to create a maddle_stories directory if it doesn't exist."""
    print("\nNo maddle_stories folder found. Create one?")
    creation = input("Enter y or n: ").lower()
    if creation == "y":
        try:
            stories_dir.mkdir(parents=True)
            print("\nSuccess!")
        except PermissionError:
            print("\nYou do not have permission to create a folder.\n")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        print("\nThen we've no business here.\n")
        sys.exit(0)


def is_it_empty(path):
    """Returns True if the maddle_stories directory exists but is empty."""
    return path.is_dir() and not any(path.iterdir())


def main():
    base_dir = Path.home() / "maddle"
    stories_dir = base_dir / "maddle_stories"

    if not stories_dir.exists():
        create_dir(stories_dir)

    while True:
        print("\n* * * MADDLE * * *")
        print(
            """[c] Choose a Story
[i] Instructions
[q] Exit"""
        )
        choice = input("> ").strip().lower()
        if choice == "q":
            sys.exit(0)
        elif choice == "c":
            if is_it_empty(stories_dir):
                print(
                    "\nThere are no stories to choose from!\nAdd some .txt files to the maddle_stories folder!"
                )
            else:
                print()
                game(stories_dir)
        elif choice == "i":
            print(
                """\nWRITE YOUR OWN STORIES!

Just put 'em in .txt files and save them to the maddle_stories folder.

Whenever you want the player to input their own words, use brackets like this:
    [noun], [verb], [adjective], [or any prompt you want technically]

Just make sure you don't use square brackets for anything else.

If you discover any bugs, call an exterminator?\n"""
            )
            input(">>")
        else:
            print("Invalid input. Please try again.")


if __name__ == "__main__":
    main()
