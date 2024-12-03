# The Command Design Pattern in Python

The Command Design Pattern is a behavioral design pattern that turns a request into a stand-alone object containing all information about the request. This transformation allows you to parameterize methods with different requests, delay or queue a request's execution, and support undoable operations. The Command Pattern embodies the principle of encapsulation, not just of data but of operations themselves. 

The Command Pattern works like a restaurant: a client places an order (the Command) with a waiter (the Invoker). The order is an entity that contains all the necessary information about the desired dish. The waiter takes the order and passes it to the chef in the kitchen (the Receiver), who knows how to prepare the dish. The waiter doesn't need to know how to cook; their job is to ensure the order reaches the chef. Additionally, the order can be modified or canceled before it's prepared, much like commands can be queued, executed, or undone in the pattern.

![Command Design Pattern Representation](/Command/res/command_visualization.png)


Command pattern components:
- **Invoker:** The object that sends the command. It knows how to execute a command but doesn't know anything about the command's implementation.
- **Command:** The baton that encapsulates the action and its parameters.
- **Receiver:** The object that performs the action when the command is executed.

This pattern decouples the object that invokes the operation from the one that knows how to perform it. By encapsulating a request as an object, you can parameterize clients with queues, requests, and operations.

## Implementation
 ```python
 from abc import ABC, abstractmethod

# Command Interface
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

# Receiver
class TextEditor:
    def __init__(self):
        self.text = ""

    def write(self, content):
        self.text += content

    def delete(self, num_chars):
        self.text = self.text[:-num_chars]

    def __str__(self):
        return self.text

# Concrete Commands
class WriteCommand(Command):
    def __init__(self, editor, content):
        self.editor = editor
        self.content = content

    def execute(self):
        self.editor.write(self.content)

    def undo(self):
        self.editor.delete(len(self.content))

class DeleteCommand(Command):
    def __init__(self, editor, num_chars):
        self.editor = editor
        self.num_chars = num_chars
        self.deleted_text = ""

    def execute(self):
        self.deleted_text = self.editor.text[-self.num_chars:]
        self.editor.delete(self.num_chars)

    def undo(self):
        self.editor.write(self.deleted_text)

# Invoker
class EditorInvoker:
    def __init__(self):
        self.history = []

    def execute_command(self, command):
        command.execute()
        # Save the command to history for undo functionality
        self.history.append(command)

    def undo(self):
        if self.history:
            command = self.history.pop()
            command.undo()
        else:
            print("Nothing to undo.")

# Client Code
if __name__ == "__main__":
    editor = TextEditor()
    invoker = EditorInvoker()

    print("Initial Text:", editor)

    # Write "Hello "
    command = WriteCommand(editor, "Hello ")
    invoker.execute_command(command)
    print("After WriteCommand('Hello '):", editor)

    # Write "World!"
    command = WriteCommand(editor, "World!")
    invoker.execute_command(command)
    print("After WriteCommand('World!'):", editor)

    # Delete last 6 characters
    command = DeleteCommand(editor, 6)
    invoker.execute_command(command)
    print("After DeleteCommand(6):", editor)

    # Undo Delete
    invoker.undo()
    print("After Undo DeleteCommand:", editor)

    # Undo Write "World!"
    invoker.undo()
    print("After Undo WriteCommand('World!'):", editor)
 ```
