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
