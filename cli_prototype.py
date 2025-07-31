#!/usr/bin/env python3
"""
CLI Prototype for Boot.dev Progress Tracker

This is a basic prototype demonstrating how to create a vim-like CLI interface
using Python's curses library. This prototype shows the fundamental concepts
you'll need to build your interactive progress tracker.

Key concepts demonstrated:
1. Basic curses setup and cleanup
2. Drawing text to the terminal
3. Handling keyboard input
4. Managing cursor navigation
5. Simple state management

Run this with: python3 cli_prototype.py
"""

import curses
import json

# Sample data structure - simplified version of your bootdev_ts.json
# This mimics the structure you already have but with fewer items for testing
SAMPLE_DATA = [
    {
        "course_title": "Learn Python",
        "chapters": [
            {
                "chapter_title": "Introduction",
                "lessons": [
                    {"lesson_number": 1, "completed": True},
                    {"lesson_number": 2, "completed": True},
                    {"lesson_number": 3, "completed": False},
                    {"lesson_number": 4, "completed": False}
                ]
            },
            {
                "chapter_title": "Variables", 
                "lessons": [
                    {"lesson_number": 1, "completed": True},
                    {"lesson_number": 2, "completed": False},
                    {"lesson_number": 3, "completed": False}
                ]
            },
            {
                "chapter_title": "Functions",
                "lessons": [
                    {"lesson_number": 1, "completed": False},
                    {"lesson_number": 2, "completed": False}
                ]
            }
        ]
    },
    {
        "course_title": "Learn JavaScript",
        "chapters": [
            {
                "chapter_title": "Basics",
                "lessons": [
                    {"lesson_number": 1, "completed": True},
                    {"lesson_number": 2, "completed": False}
                ]
            }
        ]
    }
]

with open('bootdev_ts.json', 'r', encoding='utf-8') as f:
    SAMPLE_DATA = json.load(f)

class ProgressCLI:
    """
    Main class for the CLI interface.
    
    This class manages:
    - The data structure (courses/chapters/lessons)
    - The current cursor position
    - Which courses are expanded (showing chapters)
    - Drawing the interface
    - Handling keyboard input
    """
    
    def __init__(self, data):
        # Store the course data
        self.data = data
        
        # Navigation state
        self.cursor_position = 0  # Which line the cursor is on (0-based)
        self.expanded_courses = set()  # Which courses are expanded (showing chapters)
        
        # This will hold a flat list of displayable items for easy navigation
        # Each item will be a dictionary with info about what it represents
        self.navigation_items = []
        
        # Build the initial navigation list
        self.rebuild_navigation_items()
    
    def rebuild_navigation_items(self):
        """
        Build a flat list of navigation items from the nested course data.
        
        This converts our nested structure (courses -> chapters -> lessons)
        into a flat list that's easy to navigate with up/down arrows.
        
        Each item in the list contains:
        - type: "course" or "chapter"  
        - display_text: what to show on screen
        - course_index: which course this relates to
        - chapter_index: which chapter (if applicable)
        """
        self.navigation_items = []
        
        # Loop through each course in our data
        for course_index, course in enumerate(self.data):
            # Always add the course to navigation
            self.navigation_items.append({
                "type": "course",
                "display_text": course["course_title"],
                "course_index": course_index,
                "chapter_index": None  # Courses don't have a chapter index
            })
            
            # Only add chapters if this course is expanded
            if course_index in self.expanded_courses:
                for chapter_index, chapter in enumerate(course["chapters"]):
                    # Create progress display for this chapter
                    progress_display = self.create_progress_display(chapter["lessons"])
                    
                    self.navigation_items.append({
                        "type": "chapter",
                        "display_text": f"  {chapter['chapter_title']} {progress_display}",
                        "course_index": course_index,
                        "chapter_index": chapter_index
                    })
    
    def create_progress_display(self, lessons):
        """
        Create a visual representation of lesson progress.
        
        Takes a list of lessons and returns a string like "[✔] [✔] [ ] [ ]"
        where ✔ means completed and empty brackets mean not completed.
        """
        progress_boxes = []
        for lesson in lessons:
            if lesson["completed"]:
                progress_boxes.append("[✔]")
            else:
                progress_boxes.append("[ ]")
        
        return " ".join(progress_boxes)
    
    def draw_interface(self, stdscr):
        """
        Draw the entire interface to the screen.
        
        stdscr is the main screen object provided by curses.
        It's like a canvas where we can draw text at specific positions.
        
        The coordinate system:
        - (0, 0) is top-left corner
        - (y, x) where y is row, x is column
        - y increases going down, x increases going right
        """
        
        # Clear the screen first
        # This removes any previous content
        stdscr.clear()
        
        # Get screen dimensions
        height, width = stdscr.getmaxyx()
        
        # Draw a title at the top
        title = "Boot.dev Progress Tracker - CLI Prototype"
        # Center the title by calculating the x position
        title_x = (width - len(title)) // 2
        stdscr.addstr(0, title_x, title)
        
        # Draw a separator line
        separator = "=" * min(50, width - 2)
        separator_x = (width - len(separator)) // 2
        stdscr.addstr(1, separator_x, separator)
        
        # Draw instructions
        instructions = [
            "Controls:",
            "  ↑/↓ : Navigate up/down",
            "  →   : Expand course / Mark next lesson complete",
            "  ←   : Collapse course / Mark last lesson incomplete", 
            "  q   : Quit"
        ]
        
        for i, instruction in enumerate(instructions):
            stdscr.addstr(3 + i, 2, instruction)
        
        # Start drawing the navigation items below the instructions
        start_y = 3 + len(instructions) + 2
        
        # Draw each navigation item
        for i, item in enumerate(self.navigation_items):
            y_pos = start_y + i
            
            # Don't draw beyond the screen
            if y_pos >= height - 1:
                break
                
            # Determine if this item is selected (has the cursor)
            is_selected = (i == self.cursor_position)
            
            # Create the display string
            if is_selected:
                # Show cursor with ">" for selected item
                display_line = f"> {item['display_text']}"
            else:
                # Show space instead of cursor for non-selected items
                display_line = f"  {item['display_text']}"
            
            # Draw the line
            # If it's selected, we could add highlighting here (covered later)
            stdscr.addstr(y_pos, 2, display_line)
        
        # Draw current status at the bottom
        status_y = height - 2
        current_item = self.navigation_items[self.cursor_position] if self.navigation_items else None
        if current_item:
            status = f"Selected: {current_item['type']} - {current_item['display_text'].strip()}"
            # Truncate if too long
            if len(status) > width - 4:
                status = status[:width - 7] + "..."
            stdscr.addstr(status_y, 2, status)
        
        # Actually display everything we've drawn
        # Nothing appears on screen until we call refresh()
        stdscr.refresh()
    
    def handle_keypress(self, key):
        """
        Handle keyboard input and update the application state.
        
        Returns True if the program should continue, False if it should quit.
        """
        
        # Handle up arrow - move cursor up
        if key == curses.KEY_UP:
            if self.cursor_position > 0:
                self.cursor_position -= 1
        
        # Handle down arrow - move cursor down
        elif key == curses.KEY_DOWN:
            if self.cursor_position < len(self.navigation_items) - 1:
                self.cursor_position += 1
        
        # Handle right arrow - expand/progress
        elif key == curses.KEY_RIGHT:
            if self.navigation_items:
                current_item = self.navigation_items[self.cursor_position]
                
                if current_item["type"] == "course":
                    # Expand the course (show its chapters)
                    course_index = current_item["course_index"]
                    self.expanded_courses.add(course_index)
                    # Rebuild navigation to include the newly visible chapters
                    self.rebuild_navigation_items()
                
                elif current_item["type"] == "chapter":
                    # Mark next lesson as complete
                    self.mark_next_lesson_complete(current_item)
                    # Rebuild to update the progress display
                    self.rebuild_navigation_items()
        
        # Handle left arrow - collapse/regress
        elif key == curses.KEY_LEFT:
            if self.navigation_items:
                current_item = self.navigation_items[self.cursor_position]
                
                if current_item["type"] == "course":
                    # Collapse the course (hide its chapters)
                    course_index = current_item["course_index"]
                    if course_index in self.expanded_courses:
                        self.expanded_courses.remove(course_index)
                        # Rebuild navigation to hide the chapters
                        self.rebuild_navigation_items()
                        # Make sure cursor is still valid after rebuilding
                        if self.cursor_position >= len(self.navigation_items):
                            self.cursor_position = len(self.navigation_items) - 1
                
                elif current_item["type"] == "chapter":
                    # Mark last completed lesson as incomplete
                    self.mark_last_lesson_incomplete(current_item)
                    # Rebuild to update the progress display
                    self.rebuild_navigation_items()
        
        # Handle quit
        elif key == ord('q') or key == ord('Q'):
            return False  # Signal to quit
        
        return True  # Continue running
    
    def mark_next_lesson_complete(self, chapter_item):
        """
        Find the first incomplete lesson in a chapter and mark it complete.
        """
        course = self.data[chapter_item["course_index"]]
        chapter = course["chapters"][chapter_item["chapter_index"]]
        
        # Find first incomplete lesson
        for lesson in chapter["lessons"]:
            if not lesson["completed"]:
                lesson["completed"] = True
                break  # Only mark one lesson at a time
    
    def mark_last_lesson_incomplete(self, chapter_item):
        """
        Find the last completed lesson in a chapter and mark it incomplete.
        """
        course = self.data[chapter_item["course_index"]]
        chapter = course["chapters"][chapter_item["chapter_index"]]
        
        # Find last completed lesson (search backwards)
        for lesson in reversed(chapter["lessons"]):
            if lesson["completed"]:
                lesson["completed"] = False
                break  # Only mark one lesson at a time
    
    def run(self, stdscr):
        """
        Main program loop.
        
        This function is called by curses.wrapper() and receives the main screen object.
        It sets up the curses environment and runs the main interaction loop.
        """
        
        # Configure curses settings
        # Don't display pressed keys on screen
        curses.noecho()
        
        # React to keys immediately (don't wait for Enter)
        curses.cbreak()
        
        # Enable special keys (arrow keys, function keys, etc.)
        stdscr.keypad(True)
        
        # Try to use colors if the terminal supports them
        if curses.has_colors():
            curses.start_color()
            # You can define color pairs here for highlighting
            # curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        
        # Main program loop
        while True:
            # Draw the current state of the interface
            self.draw_interface(stdscr)
            
            # Wait for user input
            # This blocks until the user presses a key
            key = stdscr.getch()
            
            # Handle the keypress and check if we should continue
            should_continue = self.handle_keypress(key)
            
            if not should_continue:
                break  # Exit the main loop

def main():
    """
    Entry point for the program.
    
    curses.wrapper() is a helper function that:
    1. Initializes curses
    2. Calls our function (cli.run)
    3. Automatically cleans up curses when done
    4. Restores the terminal to normal state
    5. Handles exceptions properly
    
    This is the recommended way to use curses because it ensures
    the terminal is always restored properly, even if an error occurs.
    """
    
    # Create our CLI object with the sample data
    cli = ProgressCLI(SAMPLE_DATA)
    
    # Run the interface using curses.wrapper
    # This handles all the setup and cleanup for us
    try:
        curses.wrapper(cli.run)
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nProgram interrupted by user")
    except Exception as e:
        # Handle any other errors
        print(f"An error occurred: {e}")
        print("Make sure your terminal supports curses (most do)")

if __name__ == "__main__":
    main()