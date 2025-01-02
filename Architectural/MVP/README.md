# Model-View-Presenter (MVP) pattern

The Model-View-Presenter (MVP) pattern is an architectural design pattern derived from MVC (Model-View-Controller). MVP's core philosophy is based on thi components:

Model: Manages data and business logic
View: Handles UI elements and user interaction
Presenter: Acts as a mediator between Model and View
 
The key distinction between MVC and MVP lies in how the View and Controller/Presenter handle user interactions and UI logic. MVP takes a stricter approach to separation of concerns. In MVP, the View is completely passive (often called a "dumb view") and has no knowledge of the Model at all. All user interactions and UI logic are delegated to the Presenter. The View's sole responsibilities are:

1. Displaying what it's told to display
2. Forwarding user interactions to the Presenter
3. Providing an interface for the Presenter to manipulate the UI

The Presenter in MVP serves as a middle-man that completely mediates between View and Model, handling UI logic and state, reaction to user inputs, model updates and view updates.

The trade-off is that the Presenter can become quite large as it handles all the UI logic that would be split between View and Controller in MVC. 

![Modal View Presenter Visual Representation](/Architectural/MVP/res/mvp_visualization.png)

### Pattern Comparison

| Pattern | Data Management | UI Handling | User Input | Complexity | Learning Curve |
|---------|-----------------|--------------|------------|------------|----------------|
| MVC | Model component | View component | Controller component | Medium | Moderate |
| MVP | Presenter handles model | Passive view | View delegates to presenter | Medium-High | Steep |
| MVVM | ViewModel | View | Two-way data binding | High | Steep |
| Clean Architecture | Use cases & entities | Interface adapters | Controllers | Very High | Very Steep |


## Implementation
Let's consider a task management application to understand MVP in action. We need a model that manages task data (creation, storage, update) and a view that displays the task list. The presenter coordinates operations between the view and the model.

```python
from dataclasses import dataclass
from typing import List, Protocol
from datetime import datetime

# Model
@dataclass
class Task:
    id: int
    title: str
    completed: bool
    created_at: datetime

class TaskRepository:
    def __init__(self) -> None:
        self._tasks: List[Task] = []
    
    def add_task(self, title: str) -> Task:
        task = Task(
            id=len(self._tasks) + 1,
            title=title,
            completed=False,
            created_at=datetime.now()
        )
        self._tasks.append(task)
        return task
    
    def get_all_tasks(self) -> List[Task]:
        return self._tasks.copy()
    
    def mark_completed(self, task_id: int) -> None:
        task = next((t for t in self._tasks if t.id == task_id), None)
        if task:
            task.completed = True

# View Protocol
class TaskView(Protocol):
    def display_tasks(self, tasks: List[Task]) -> None: ...
    def get_new_task_input(self) -> str: ...
    def show_task_added_message(self, task: Task) -> None: ...
    def show_error_message(self, message: str) -> None: ...

# Concrete View Implementation
class ConsoleTaskView:
    def display_tasks(self, tasks: List[Task]) -> None:
        print("\n=== Task List ===")
        for task in tasks:
            status = "✓" if task.completed else " "
            print(f"[{status}] {task.id}. {task.title}")
    
    def get_new_task_input(self) -> str:
        return input("Enter new task title: ")
    
    def show_task_added_message(self, task: Task) -> None:
        print(f"Task added: {task.title}")
    
    def show_error_message(self, message: str) -> None:
        print(f"Error: {message}")

# Presenter
class TaskPresenter:
    def __init__(self, view: TaskView, repository: TaskRepository):
        self._view = view
        self._repository = repository
    
    def add_new_task(self) -> None:
        title = self._view.get_new_task_input()
        if not title:
            self._view.show_error_message("Task title cannot be empty")
            return
            
        task = self._repository.add_task(title)
        self._view.show_task_added_message(task)
        self.refresh_task_list()
    
    def refresh_task_list(self) -> None:
        tasks = self._repository.get_all_tasks()
        self._view.display_tasks(tasks)
    
    def mark_task_completed(self, task_id: int) -> None:
        self._repository.mark_completed(task_id)
        self.refresh_task_list()

# Usage Example
def main() -> None:
    repository = TaskRepository()
    view = ConsoleTaskView()
    presenter = TaskPresenter(view, repository)
    
    # Add some tasks
    presenter.add_new_task()  # User inputs task
    presenter.add_new_task()  # User inputs task
    presenter.mark_task_completed(1)  # Mark first task as completed

if __name__ == "__main__":
    main()
```