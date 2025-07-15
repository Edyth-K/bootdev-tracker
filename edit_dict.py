def update_data(data):
    for course_dict in data:
        if course_dict["course_title"] == "Learn JavaScript":
            for chapter_dict in course_dict["chapters"]:
                if chapter_dict["chapter_title"] == "Comparisons":
                    for lesson_dict in chapter_dict["lessons"]:
                        lesson_dict["completed"] = True

    commit_message = "Completed [Comparisons] in [Learn JavaScript]" # Edit This 
    return data, commit_message