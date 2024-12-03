from abc import ABC, abstractmethod

class Subject:
    """
    Represents the subject that maintains a list of observers
    and notifies them of any state changes.
    """

    def __init__(self):
        # Initialize an empty list of observers
        self._observers = []
        # Internal state of the subject
        self._state = None

    def attach(self, observer):
        """
        Attach an observer to the subject.
        """
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"Attached an observer: {observer}")

    def detach(self, observer):
        """
        Detach an observer from the subject.
        """
        try:
            self._observers.remove(observer)
            print(f"Detached an observer: {observer}")
        except ValueError:
            print("Observer not found among attached observers.")

    def notify(self):
        """
        Notify all observers about a state change.
        """
        print("Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    @property
    def state(self):
        """
        Get the state of the subject.
        """
        return self._state

    @state.setter
    def state(self, value):
        """
        Set the state of the subject and notify observers.
        """
        self._state = value
        print(f"Subject state changed to: {self._state}")
        self.notify()


class Observer(ABC):
    """
    Abstract base class for observers.
    """

    @abstractmethod
    def update(self, subject):
        """
        Receive update from subject.
        """
        pass


class ConcreteObserverA(Observer):
    """
    A concrete observer that reacts to updates from the subject.
    """

    def update(self, subject):
        if subject.state < 3:
            print(f"ConcreteObserverA: Reacted to state change to {subject.state}")


class ConcreteObserverB(Observer):
    """
    Another concrete observer with a different reaction.
    """

    def update(self, subject):
        if subject.state == 0 or subject.state >= 2:
            print(f"ConcreteObserverB: Reacted to state change to {subject.state}")


# Usage example
if __name__ == "__main__":
    # Create a subject instance
    subject = Subject()

    # Create observer instances
    observer_a = ConcreteObserverA()
    observer_b = ConcreteObserverB()

    # Attach observers to the subject
    subject.attach(observer_a)
    subject.attach(observer_b)

    # Change the state of the subject
    print("\nFirst state change:")
    subject.state = 2  # Both observers may react

    print("\nSecond state change:")
    subject.state = 3  # Only ConcreteObserverB reacts

    # Detach an observer
    subject.detach(observer_a)

    print("\nThird state change:")
    subject.state = 0  # Only ConcreteObserverB reacts
