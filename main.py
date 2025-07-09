import json
import os
from auto_git_push import auto_git_push

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Agent:
    def __init__(self):
        self.data = self.load_data()
        self.running = True

    def json_to_markdown(self, data, title_padding=25, max_per_row=10):
        output = []
        prefix_str = "⏳In Progress || ✅Complete || ➖Not Started"
        output.append(prefix_str)

        for course in data:
            output.append('<details>')
            output.append(f"<summary><strong>{self.course_status(course)} {course['course_title']}</strong></summary>\n")
            output.append('```')
            for chapter in course['chapters']:
                title = chapter['chapter_title'].ljust(title_padding)
                checkboxes = ["[✔️]" if l["completed"] else "[ ]" for l in chapter["lessons"]]
                
                # Split checkboxes into chunks of max_per_row
                rows = [checkboxes[i:i+max_per_row] for i in range(0, len(checkboxes), max_per_row)]
                
                for i, row in enumerate(rows):
                    prefix = title if i == 0 else " " * title_padding
                    output.append(f"{prefix}{' '.join(row)}")
            output.append('```')
            output.append('</details>')

            output.append("\n")
        return "\n".join(output)

    # helper function for json_to_markdown: add symbol for complete, incomplete, in progress
    def course_status(self, course):
        incomplete = 0
        complete = 0
        for chapter_dict in course["chapters"]:
            for lesson_dict in chapter_dict["lessons"]:
                if lesson_dict["completed"]:
                    complete += 1
                else:
                    incomplete += 1
        if complete == 0:
            return "➖"
        if incomplete == 0:
            return "✅"
        return "⏳"

    def load_data(self):
        with open('bootdev_ts.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self):
        # update bootdev_ts.json
        with open("bootdev_ts.json", "w") as f:
            json.dump(self.data, f, indent=2)

    def update_readme(self):
        # Generate markdown
        md_output = self.json_to_markdown(self.data)

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
        for course_dict in self.data:
            if course_dict["course_title"] == "Learn Memory Management in C":
                for chapter_dict in course_dict["chapters"]:
                    if chapter_dict["chapter_title"] == "C Basics":
                        for lesson_dict in chapter_dict["lessons"]:
                            lesson_dict["completed"] = True


    def auto_commit(self):
        auto_git_push()
        self.running = False

    def parse_command(self, choice):
        match choice:
            case 'v':
                self.view_data()
            case 'm':
                pass
            case 's':
                self.update_readme()
                self.save_data()
            case 'a':
                self.auto_commit()
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
            print("a. Auto Add-Commit-Push to GitHub")
            print("q. Exit")
            print("t. Run Temporary Function")
            print()

            choice = input("Select an option: ")
            clear_screen()

            self.parse_command(choice)
            

if __name__ == '__main__':
    Agent().run()