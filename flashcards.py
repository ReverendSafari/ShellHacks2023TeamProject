class FlashSet:
    def __init__(self, name):
        self.name = name
        self.flashcards = {}  # Use a dictionary to store flashcards

    def add_flashcard(self, term, translation):
        flashcard = FlashCard(term, translation)
        self.flashcards[term] = flashcard  # Use term as the key and FlashCard object as the value

    def display_flashcards(self):
        print(f"Flashcards in '{self.name}':")
        for term, flashcard in self.flashcards.items():
            print(f"Term: {term}, Translation: {flashcard.translation}")

class FlashCard:
    def __init__(self, term, translation):
        self.term = term
        self.translation = translation

def create_new_set():
    set_name = input("Enter the name of the new flashcard set: ")
    new_set = FlashSet(set_name)
    return new_set

def add_flashcards_to_set(flashset):
    while True:
        term = input("Enter the term (or type 'done' to finish adding flashcards): ")
        if term.lower() == 'done':
            break
        translation = input("Enter the translation: ")
        flashset.add_flashcard(term, translation)
        print("Flashcard added successfully.")

def practice_flashcards(flashset):
    print(f"Practice '{flashset.name}' Flashcards:")

    for term, flashcard in flashset.flashcards.items():
        expected_translation = flashcard.translation

        user_translation = input(f"What is the translation of '{term}'? (Type 'exit' to quit): ")

        if user_translation.lower() == 'exit':
            print("Exiting flashcard practice.")
            break

        if user_translation.strip().lower() == expected_translation.lower():
            print("Correct! Moving to the next flashcard.")
        else:
            print(f"Wrong. The correct translation is '{expected_translation}'.")
            print("Type the correct word to continue:")

            while True:
                user_input = input().strip().lower()
                if user_input == expected_translation.lower():
                    print("Correct! Moving to the next flashcard.")
                    break
                else:
                    print("Wrong. Try again.")

def main():
    flashcard_sets = {}  # Use a dictionary to store flashcard sets

    while True:
        print("\nFlashcard Program Menu:")
        print("1. Create a new flashcard set")
        print("2. Add flashcards to a set")
        print("3. Display flashcards in a set")
        print("4. Practice flashcard set")
        print("5. Exit")

        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == "1":
            new_set = create_new_set()
            flashcard_sets[new_set.name] = new_set  # Use the set name as the dictionary key
            print(f"Flashcard set '{new_set.name}' created.")
        elif choice == "2":
            set_name = input("Enter the name of the set to add flashcards to: ")
            flashset = flashcard_sets.get(set_name)
            if flashset is None:
                print(f"Set '{set_name}' not found. Please create the set first.")
            else:
                add_flashcards_to_set(flashset)
        elif choice == "3":
            set_name = input("Enter the name of the set to display: ")
            flashset = flashcard_sets.get(set_name)
            if flashset is None:
                print(f"Set '{set_name}' not found.")
            else:
                flashset.display_flashcards()
        elif choice == "4":
            set_name = input("Enter the name of the set to practice: ")
            flashset = flashcard_sets.get(set_name)
            if flashset is None:
                print(f"Set '{set_name}' not found.")
            else:
                practice_flashcards(flashset)
        elif choice == "5":
            print("Exiting the flashcard program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
