from abc import ABC, abstractmethod

# Engine Interface - The abstract product
class Engine(ABC):
    @abstractmethod
    def assemble(self) -> str:
        pass

# Specific engines - Concrete Products
class Formula1Engine(Engine):
    def assemble(self) -> str:
        return "Assembling a high-performance Formula 1 engine!"

class RallyEngine(Engine):
    def assemble(self) -> str:
        return "Assembling a rugged Rally engine built for endurance!"

# Engine Factory
class EngineFactory:
    @staticmethod
    def create_engine(motorsport: str) -> Engine:
        if motorsport == "Formula 1":
            return Formula1Engine()
        elif motorsport == "Rally":
            return RallyEngine()
        else:
            raise ValueError(f"Unknown motorsport type: {motorsport}")

# Test Factory behavior
if __name__ == "__main__":

    # The client code doesn't need to know which 
    # specific engine class it is working with.
    first_engine = EngineFactory.create_engine("Formula 1")
    print(first_engine.assemble())

    second_engine = EngineFactory.create_engine("Rally")
    print(second_engine.assemble())                                                                           