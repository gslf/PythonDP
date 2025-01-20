from dataclasses import dataclass
from enum import Enum
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class Position(Enum):
    """Wheel positions in a racing car."""
    FRONT_LEFT = "Front Left"
    FRONT_RIGHT = "Front Right"
    REAR_LEFT = "Rear Left"
    REAR_RIGHT = "Rear Right"

class MessageType(Enum):
    """Types of messages exchanged between actors."""
    CHANGE_TIRE = "change_tire"
    TIRE_CHANGED = "tire_changed"
    STOP = "stop"

@dataclass
class Message:
    """Message for actor communication."""
    msg_type: MessageType
    position: Position
    sender_mailbox: asyncio.Queue = None

class PitCrewMember:
    """Actor representing a pit crew member."""
    def __init__(self, position: Position):
        self.position = position
        self.mailbox = asyncio.Queue()

    async def run(self):
        """Process incoming messages."""
        while True:
            msg = await self.mailbox.get()
            if msg.msg_type == MessageType.STOP:
                break
                
            if msg.msg_type == MessageType.CHANGE_TIRE:
                logging.info(f"Starting tire change at {self.position.value}")
                await asyncio.sleep(1)  # Simulate work
                logging.info(f"Completed tire change at {self.position.value}")
                
                # Send completion message
                response = Message(MessageType.TIRE_CHANGED, self.position)
                await msg.sender_mailbox.put(response)

class RaceEngineer:
    """Supervisor actor coordinating the pit stop."""
    def __init__(self):
        self.mailbox = asyncio.Queue()
        self.crew_members = {
            pos: PitCrewMember(pos) for pos in Position
        }
        self.pending_changes = set(Position)

    async def run(self):
        """Process completion messages from crew members."""
        while self.pending_changes:
            msg = await self.mailbox.get()
            if msg.msg_type == MessageType.TIRE_CHANGED:
                self.pending_changes.remove(msg.position)
                if not self.pending_changes:
                    logging.info("All tire changes complete - Car clear to exit")

    async def coordinate_pit_stop(self):
        """Coordinate the entire pit stop process."""
        logging.info("Car entering pit lane")
        
        # Start crew member actors
        crew_tasks = [
            asyncio.create_task(member.run())
            for member in self.crew_members.values()
        ]
        
        # Send change tire messages to all crew members
        for position, member in self.crew_members.items():
            message = Message(
                MessageType.CHANGE_TIRE, 
                position,
                self.mailbox
            )
            await member.mailbox.put(message)

        # Wait for all changes to complete
        await self.run()
        
        # Stop all crew members
        for member in self.crew_members.values():
            await member.mailbox.put(Message(MessageType.STOP, None))
        
        # Wait for all tasks to complete
        await asyncio.gather(*crew_tasks)


async def main():
    """Simulate a complete pit stop."""
    engineer = RaceEngineer()
    await engineer.coordinate_pit_stop()
asyncio.run(main())