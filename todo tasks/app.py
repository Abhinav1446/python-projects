import sys          # to read command-line arguments
import os           # to check if the JSON file exists
import json         # to read/write JSON data
from datetime import datetime  # to store created/updated timestamps

# Name of the JSON file used to store all tasks
task_list = 'tasklist.json'


class Tasklist:
    def __init__(self):
        # Load existing tasks from JSON (or start with an empty list)
        self.task = self.load_tasks()

    def load_tasks(self):
        """
        Load tasks from the JSON file.

        - If the file doesn't exist, create it with an empty list and return [].
        - If the file exists but is empty or invalid JSON, reset it to [].
        """
        if not os.path.exists(task_list):
            with open(task_list, 'w') as f:
                json.dump([], f, indent=4)
            return []

        try:
            with open(task_list, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            # File exists but is empty or corrupted → reset to an empty list
            with open(task_list, 'w') as f:
                json.dump([], f, indent=4)
            return []

    def save_tasks(self):
        """
        Save the in-memory task list (self.task) back into the JSON file.

        JSON cannot be updated "in-place", so we rewrite the whole file each time.
        """
        with open(task_list, 'w') as f:
            json.dump(self.task, f, indent=4)

    def get_id(self):
        """
        Generate the next task ID.

        - If there are no tasks, start IDs from 1.
        - Otherwise, return max(existing_ids) + 1.
        """
        if not self.task:
            return 1
        return max(task['id'] for task in self.task) + 1

    def add_task(self, task):
        """
        Add a new task with a unique ID, default status 'to-do',
        and timestamps for creation and last update.
        """
        new_id = self.get_id()
        now = datetime.now().isoformat()

        new_task = {
            'id': new_id,
            'name': task,
            'status': 'to-do',
            'created_on': now,
            'updated_on': now,
        }

        # Add the new task to the in-memory list
        self.task.append(new_task)

        # Persist updated list to the JSON file
        self.save_tasks()

        print(f"Task added successfully ID({new_id})")

    def delete_task(self, task_id):
        """
        Delete a task by its ID.
        """
        task_id = int(task_id)
        for task in self.task:
            if task['id'] == task_id:
                self.task.remove(task)
                self.save_tasks()
                print(f"Task deleted successfully ID({task_id})")
                return

        # If we reach here, no task matched the given ID
        print(f"No task found with ID({task_id})")

    def update_task(self, task_id, task_name):
        """
        Update the name of a task by its ID and refresh its 'updated_on' timestamp.
        """
        task_id = int(task_id)
        for task in self.task:
            if task['id'] == task_id:
                task['name'] = task_name
                task['updated_on'] = datetime.now().isoformat()
                self.save_tasks()
                print(f"Task updated successfully ID({task_id})")
                return

        print(f"No task found with ID({task_id})")

    def list_tasks(self):
        """
        List the names of all tasks.
        """
        if not self.task:
            print("No tasks found.")
            return

        for task in self.task:
            print(task['name'])

    def mark_in_progress(self, task_id):
        """
        Mark a task as 'in-progress' by its ID.
        """
        task_id = int(task_id)
        for task in self.task:
            if task['id'] == task_id:
                task['status'] = 'in-progress'
                task['updated_on'] = datetime.now().isoformat()
                self.save_tasks()
                print(f"Task is marked as in-progress ID({task_id})")
                return

        print(f"No task found with ID({task_id})")

    def mark_done(self, task_id):
        """
        Mark a task as 'done' by its ID.
        """
        task_id = int(task_id)
        for task in self.task:
            if task['id'] == task_id:
                task['status'] = 'done'
                task['updated_on'] = datetime.now().isoformat()
                self.save_tasks()
                print(f"Task is marked as done ID({task_id})")
                return

        print(f"No task found with ID({task_id})")

    def list_by_property(self, stat):
        """
        List tasks filtered by status:
        - 'to-do'
        - 'in-progress'
        - 'done'
        """
        if stat not in ('to-do', 'in-progress', 'done'):
            print("Usage: python app.py list <to-do|in-progress|done>")
            return

        found = False
        for task in self.task:
            if task['status'] == stat:
                print(task['name'])
                found = True

        if not found:
            print(f"No tasks found with status '{stat}'.")


def main():
    """
    Command-line interface handler.

    Supported commands:
      python app.py add <taskname>
      python app.py delete <taskid>
      python app.py update <taskid> <taskname>
      python app.py list
      python app.py list <to-do|in-progress|done>
      python app.py mark-in-progress <taskid>
      python app.py mark-done <taskid>
    """
    # Ensure at least one argument (the command) is provided
    if len(sys.argv) < 2:
        print("Usage: python app.py <command> [arguments]")
        sys.exit(1)

    tasks = Tasklist()
    command = sys.argv[1]

    if command == "add":
        # python app.py add <taskname>  → total args must be 3
        if len(sys.argv) == 3:
            tasks.add_task(sys.argv[2])
        else:
            print("Usage: python app.py add <taskname>")
            sys.exit(1)

    elif command == "delete":
        # python app.py delete <taskid>
        if len(sys.argv) == 3:
            tasks.delete_task(sys.argv[2])
        else:
            print("Usage: python app.py delete <taskid>")
            sys.exit(1)

    elif command == "update":
        # python app.py update <taskid> <taskname>
        if len(sys.argv) == 4:
            tasks.update_task(sys.argv[2], sys.argv[3])
        else:
            print("Usage: python app.py update <taskid> <taskname>")
            sys.exit(1)

    elif command == "list":
        # python app.py list
        if len(sys.argv) == 2:
            tasks.list_tasks()
        # python app.py list <status>
        elif len(sys.argv) == 3:
            pro = sys.argv[2]
            tasks.list_by_property(pro)
        else:
            print("Usage: python app.py list [to-do|in-progress|done]")
            sys.exit(1)

    elif command == "mark-in-progress":
        # python app.py mark-in-progress <taskid>
        if len(sys.argv) == 3:
            tasks.mark_in_progress(sys.argv[2])
        else:
            print("Usage: python app.py mark-in-progress <taskid>")
            sys.exit(1)

    elif command == "mark-done":
        # python app.py mark-done <taskid>
        if len(sys.argv) == 3:
            tasks.mark_done(sys.argv[2])
        else:
            print("Usage: python app.py mark-done <taskid>")
            sys.exit(1)

    else:
        print("Unknown command.")
        print("Usage: python app.py <command> [arguments]")
        sys.exit(1)


# This is called the "main guard":
# It ensures main() runs only when this file is executed directly,
# and NOT when it is imported as a module in another script.
if __name__ == '__main__':
    main()
