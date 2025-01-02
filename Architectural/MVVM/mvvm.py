from dataclasses import dataclass
from typing import List, Optional, Callable
from enum import Enum
from datetime import datetime

# MODEL
@dataclass
class TodoItem:
    """Represents a single todo item in the system"""
    id: int
    text: str
    completed: bool
    created_at: datetime

class TodoModel:
    """Model class that manages the todo data and business logic"""
    def __init__(self):
        self._todos: List[TodoItem] = []
        
    def add_todo(self, text: str) -> TodoItem:
        """Adds a new todo item and returns it"""
        todo = TodoItem(
            id=len(self._todos) + 1,
            text=text,
            completed=False,
            created_at=datetime.now()
        )
        self._todos.append(todo)
        return todo
        
    def toggle_todo(self, todo_id: int) -> None:
        """Toggles the completed state of a todo"""
        for todo in self._todos:
            if todo.id == todo_id:
                todo.completed = not todo.completed
                break
                
    def get_todos(self) -> List[TodoItem]:
        """Returns all todos"""
        return self._todos.copy()

class FilterState(Enum):
    ALL = "all"
    ACTIVE = "active"
    COMPLETED = "completed"

# VIEW MODEL
class TodoViewModel:
    """
    ViewModel that manages the presentation logic and state
    Acts as a bridge between the View and Model
    """
    def __init__(self, model: TodoModel):
        self._model = model
        self._filter_state: FilterState = FilterState.ALL
        self._on_data_changed: Optional[Callable[[], None]] = None

    def set_data_changed_callback(self, callback: Callable[[], None]) -> None:
        """Sets the callback to be called when data changes"""
        self._on_data_changed = callback

    def notify_data_changed(self) -> None:
        """Notifies the View that data has changed"""
        if self._on_data_changed:
            self._on_data_changed()

    def add_todo(self, text: str) -> None:
        """Adds a new todo item"""
        self._model.add_todo(text)
        self.notify_data_changed()

    def toggle_todo(self, todo_id: int) -> None:
        """Toggles the completed state of a todo"""
        self._model.toggle_todo(todo_id)
        self.notify_data_changed()

    def set_filter(self, filter_state: FilterState) -> None:
        """Sets the current filter state"""
        self._filter_state = filter_state
        self.notify_data_changed()

    @property
    def filtered_todos(self) -> List[TodoItem]:
        """Returns filtered todos based on current filter state"""
        todos = self._model.get_todos()
        if self._filter_state == FilterState.ALL:
            return todos
        elif self._filter_state == FilterState.ACTIVE:
            return [todo for todo in todos if not todo.completed]
        else:  # COMPLETED
            return [todo for todo in todos if todo.completed]

# VIEW (simplified example)
class TodoView:
    """
    View class that handles the UI representation
    In a real application, this might be a GUI framework class
    """
    def __init__(self, view_model: TodoViewModel):
        self.view_model = view_model
        self.view_model.set_data_changed_callback(self.render)

    def render(self) -> None:
        """Renders the current state of the todo list"""
        print("\n=== Todo List ===")
        for todo in self.view_model.filtered_todos:
            status = "✓" if todo.completed else "☐"
            print(f"{todo.id}. [{status}] {todo.text}")
        print("================")

# Usage example
model = TodoModel()
view_model = TodoViewModel(model)
view = TodoView(view_model)

# Simulate user interactions
view_model.add_todo("Buy groceries")
view_model.add_todo("Walk the dog")
view_model.toggle_todo(2)
view_model.set_filter(FilterState.ACTIVE)