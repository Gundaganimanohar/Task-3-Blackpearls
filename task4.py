import json
from datetime import datetime

class Task:
    def __init__(self, description, priority='Medium', category='General', due_date=None):
        self.description = description
        self.priority = priority
        self.completed = False
        self.category = category
        self.due_date = due_date

    def to_dict(self):
        return {
            'description': self.description,
            'priority': self.priority,
            'completed': self.completed,
            'category': self.category,
            'due_date': self.due_date
        }

    @staticmethod
    def from_dict(data):
        task = Task(data['description'], data['priority'], data['category'], data['due_date'])
        task.completed = data['completed']
        return task

def load_tasks(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return [Task.from_dict(task) for task in data]
    except FileNotFoundError:
        return []

def save_tasks(tasks, filename):
    with open(filename, 'w') as file:
        json.dump([task.to_dict() for task in tasks], file, indent=4)

def add_task(tasks):
    description = input("Enter task description: ")
    priority = input("Enter task priority (Low, Medium, High): ")
    category = input("Enter task category: ")
    due_date = input("Enter due date (YYYY-MM-DD) or leave blank: ")
    if due_date:
        due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
    task = Task(description, priority, category, due_date)
    tasks.append(task)

def delete_task(tasks):
    view_tasks(tasks)
    index = int(input("Enter task number to delete: ")) - 1
    if 0 <= index < len(tasks):
        tasks.pop(index)

def update_task(tasks):
    view_tasks(tasks)
    index = int(input("Enter task number to update: ")) - 1
    if 0 <= index < len(tasks):
        task = tasks[index]
        task.description = input(f"Enter new description (current: {task.description}): ") or task.description
        task.priority = input(f"Enter new priority (current: {task.priority}): ") or task.priority
        task.category = input(f"Enter new category (current: {task.category}): ") or task.category
        due_date = input(f"Enter new due date (current: {task.due_date}) (YYYY-MM-DD) or leave blank: ")
        if due_date:
            task.due_date = datetime.strptime(due_date, '%Y-%m-%d').date()

def mark_task_completed(tasks):
    view_tasks(tasks)
    index = int(input("Enter task number to mark as complete: ")) - 1
    if 0 <= index < len(tasks):
        tasks[index].completed = True

def view_tasks(tasks, filter_by=None):
    for i, task in enumerate(tasks):
        if filter_by and not filter_by(task):
            continue
        status = "Done" if task.completed else "Not Done"
        due_date = task.due_date if task.due_date else "No due date"
        print(f"{i+1}. [{status}] {task.description} - Priority: {task.priority}, Category: {task.category}, Due: {due_date}")

def filter_tasks(tasks):
    filter_type = input("Filter by (priority, category, due_date, completed): ")
    if filter_type == "priority":
        priority = input("Enter priority (Low, Medium, High): ")
        view_tasks(tasks, filter_by=lambda task: task.priority == priority)
    elif filter_type == "category":
        category = input("Enter category: ")
        view_tasks(tasks, filter_by=lambda task: task.category == category)
    elif filter_type == "due_date":
        due_date = input("Enter due date (YYYY-MM-DD): ")
        if due_date:
            due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
            view_tasks(tasks, filter_by=lambda task: task.due_date == due_date)
    elif filter_type == "completed":
        status = input("Enter status (done, not done): ")
        view_tasks(tasks, filter_by=lambda task: task.completed == (status == "done"))

def main():
    filename = 'tasks.json'
    tasks = load_tasks(filename)

    while True:
        print("\nTo-Do List Application")
        print("1. View tasks")
        print("2. Add task")
        print("3. Delete task")
        print("4. Update task")
        print("5. Mark task as complete")
        print("6. Filter tasks")
        print("7. Save and exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            view_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            delete_task(tasks)
        elif choice == '4':
            update_task(tasks)
        elif choice == '5':
            mark_task_completed(tasks)
        elif choice == '6':
            filter_tasks(tasks)
        elif choice == '7':
            save_tasks(tasks, filename)
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
