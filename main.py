import json
import os
from json_to_readme import json_to_markdown

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Agent:
    def __init__(self):
        self.data = self.load_data()
        self.running = True

    def load_data(self):
        with open('bootdev_ts.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self):
        # update bootdev_ts.json
        with open("bootdev_ts.json", "w") as f:
            json.dump(self.data, f, indent=2)

    def update_readme(self):
        # Generate markdown
        md_output = json_to_markdown(self.data)

        # Save to README.md
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(md_output)
        print("Markdown progress saved to PROGRESS.md")

    def view_data(self):
        index = 0
        for course_dict in self.data:
            if index != 0:
                break
            print(course_dict)
            index += 1

    def temp(self):
        index = 0
        for course_dict in self.data:
            if index != 0:
                break
            for chapter_dict in course_dict["chapters"]:
                for lesson_dict in chapter_dict["lessons"]:
                    lesson_dict["completed"] = True
            index += 1

    def parse_command(self, choice):
        match choice:
            case 'v':
                self.view_data()
            case 'm':
                pass
            case 's':
                self.update_readme()
                self.save_data()
            case 'q':
                self.running = False
            case 't':
                self.temp()

    def run(self):
        while self.running:
            
            print("\n=== Main Menu ===")
            print("v. View Data")
            print("m. Mark Lesson Complete")
            print("s. Save Progress")
            print("q. Exit")
            print()
            print("t. Run Temporary Function")

            choice = input("Select an option: ")
            clear_screen()

            self.parse_command(choice)
            

if __name__ == '__main__':
    Agent().run()