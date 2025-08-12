def update_data(data):
    # Edit Below Here:
    course_title = "Learn TypeScript"
    chapter_title = "Types"

    # Don't touch below this
    for course_dict in data:
        if course_dict["course_title"] == course_title:
            for chapter_dict in course_dict["chapters"]:
                if chapter_dict["chapter_title"] == chapter_title:
                    for lesson_dict in chapter_dict["lessons"]:
                        lesson_dict["completed"] = True

    commit_message = f"Completed [Chapter: {chapter_title}] in [Course: {course_title}]"
    return data, commit_message