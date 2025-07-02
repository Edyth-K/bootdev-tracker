import json

def json_to_markdown(data, title_padding=25, max_per_row=10):
    output = []
    for course in data:
        output.append(f"# {course['course_title']}\n")
        output.append('```')
        for chapter in course['chapters']:
            title = chapter['chapter_title'].ljust(title_padding)
            checkboxes = ["[x]" if l["completed"] else "[ ]" for l in chapter["lessons"]]
            
            # Split checkboxes into chunks of max_per_row
            rows = [checkboxes[i:i+max_per_row] for i in range(0, len(checkboxes), max_per_row)]
            
            for i, row in enumerate(rows):
                prefix = title if i == 0 else " " * title_padding
                output.append(f"{prefix}{' '.join(row)}")
        output.append('```')

        output.append("\n---\n")
    return "\n".join(output)

def main():
    # Load JSON progress data
    with open("bootdev_ts.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Generate markdown
    md_output = json_to_markdown(data)
    
    # Save to markdown file
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(md_output)
    print("Markdown progress saved to PROGRESS.md")

if __name__ == "__main__":
    main()
