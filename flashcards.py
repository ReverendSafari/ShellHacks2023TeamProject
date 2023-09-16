class FlashSet:
    def __init__(self, name):
        self.name = name
        self.flashcards = []

    def add_flashcard(self, term, translation):
        flashcard = FlashCard(term, translation)
        self.flashcards.append(flashcard)

    def display_flashcards(self):
        print(f"Flashcards in '{self.name}':")
        for index, flashcard in enumerate(self.flashcards, start=1):
            print(f"{index}. Term: {flashcard.term}, Translation: {flashcard.translation}")

class FlashCard:
    def __init__(self, term, translation):
        self.term = term
        self.translation = translation

def create_new_set():
    set_name = input("Enter the name of the new flashcard set: ")
    new_set = FlashSet(set_name)
    return new_set

def main():
    flashcard_sets = []

    while True:
        print("\nFlashcard Program Menu:")
        print("1. Create a new flashcard set")
        print("2. Add a flashcard to a set")
        print("3. Display flashcards in a set")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "1":
            new_set = create_new_set()
            flashcard_sets.append(new_set)
            print(f"Flashcard set '{new_set.name}' created.")
        elif choice == "2":
            if not flashcard_sets:
                print("No flashcard sets available. Create a new set first.")
            else:
                print("Choose a flashcard set to add a flashcard to:")
                for index, flashcard_set in enumerate(flashcard_sets, start=1):
                    print(f"{index}. {flashcard_set.name}")
                set_choice = int(input("Enter the number of the set: ")) - 1

                term = input("Enter the term: ")
                translation = input("Enter the translation: ")

                flashcard_sets[set_choice].add_flashcard(term, translation)
                print("Flashcard added successfully.")
        elif choice == "3":
            if not flashcard_sets:
                print("No flashcard sets available. Create a new set first.")
            else:
                print("Choose a flashcard set to display:")
                for index, flashcard_set in enumerate(flashcard_sets, start=1):
                    print(f"{index}. {flashcard_set.name}")
                set_choice = int(input("Enter the number of the set: ")) - 1

                flashcard_sets[set_choice].display_flashcards()
        elif choice == "4":
            print("Exiting the flashcard program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()