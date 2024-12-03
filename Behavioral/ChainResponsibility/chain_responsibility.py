class Handler:
    """
    Base handler class for the chain of responsibility.
    """
    def __init__(self, successor=None):
        self.successor = successor

    def handle(self, issue):
        if self.successor:
            return self.successor.handle(issue)
        return f"Issue '{issue}' could not be resolved."

class Mechanic(Handler):
    """
    Handles mechanical issues.
    """
    def handle(self, issue):
        if issue == "mechanical":
            return "Mechanic: Fixed the mechanical issue."
        return super().handle(issue)

class Electrician(Handler):
    """
    Handles electrical issues.
    """
    def handle(self, issue):
        if issue == "electrical":
            return "Electrician: Fixed the electrical issue."
        return super().handle(issue)

class PitCrew(Handler):
    """
    Handles pit stop related issues (e.g., tire change).
    """
    def handle(self, issue):
        if issue == "pit stop":
            return "PitCrew: Handled the pit stop."
        return super().handle(issue)


if __name__ == "__main__":
    # Setting up the chain of responsibility
    pit_crew = PitCrew()
    electrician = Electrician(successor=pit_crew)
    mechanic = Mechanic(successor=electrician)

    # Handling different issues
    issues = ["mechanical", "electrical", "pit stop", "aero"]
    
    for issue in issues:
        result = mechanic.handle(issue)
        print(f"{issue.capitalize()} Issue: {result}")