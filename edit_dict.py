def update_data(data):
    for course_dict in data:
        if course_dict["course_title"] == "Learn JavaScript":
            for chapter_dict in course_dict["chapters"]:
                if chapter_dict["chapter_title"] == "Variables":
                    for lesson_dict in chapter_dict["lessons"]:
                        lesson_dict["completed"] = True

    # enabled = False
    # total_chapters = 0
    # total_courses = 0
    # for course_dict in self.data:
        
    #     if course_dict["course_title"] == "Learn Memory Management in C":
    #         enabled = True
    #     if course_dict["course_title"] == "Capstone Project":
    #         enabled = False
    #     if enabled:
    #         total_courses += 1
    #         print(f"Course Title: {course_dict["course_title"]}")
    #         num_chapters = 0
    #         for chapter_dict in course_dict["chapters"]:
    #             num_chapters += 1
    #             total_chapters += 1
    #         print(f"Chapters: {num_chapters}")
    # print(f"Total Courses: {total_courses}")
    # print(f"Total Chapters: {total_chapters-1}")

    return data