import random

class VacuumEnvironment:
    def __init__(self, room_status, vacuum_position=0):
        """
        Initialize the vacuum environment.
        :param room_status: list of int (0=dirty, 1=clean) for 100 locations
        :param vacuum_position: int, current vacuum position (0-99)
        """
        self.room = room_status
        self.vacuum_pos = vacuum_position

    def is_clean(self):
        """Return True if all locations are clean."""
        return all(status == 1 for status in self.room)

    def clean_current(self):
        """Clean current location if dirty."""
        if self.room[self.vacuum_pos] == 0:
            self.room[self.vacuum_pos] = 1
            print(f"Cleaned location {self.vacuum_pos}")

    def move_to(self, position):
        """Move vacuum to a new location."""
        print(f"Moving from {self.vacuum_pos} to {position}")
        self.vacuum_pos = position

    def display(self):
        """Display the 10x10 room with vacuum position marked as *."""
        display_room = []
        for i, status in enumerate(self.room):
            if i == self.vacuum_pos:
                display_room.append(f"*{status}")
            else:
                display_room.append(f" {status}")
        for row in range(10):
            print(' '.join(display_room[row*10:(row+1)*10]))
        print()


class GoalBasedAgent:
    def __init__(self, environment):
        self.env = environment

    def run(self):
        """
        Goal-based agent logic:
        - While room not clean:
          - Clean current location if dirty.
          - Else move to the next dirty location (lowest index).
        """
        print("Goal-Based Agent started.\n")
        while not self.env.is_clean():
            self.env.display()
            if self.env.room[self.env.vacuum_pos] == 0:
                self.env.clean_current()
            else:
                dirty_positions = [i for i, status in enumerate(self.env.room) if status == 0]
                if dirty_positions:
                    new_pos = dirty_positions[0]
                    self.env.move_to(new_pos)
        self.env.display()
        print("Goal achieved: Room is clean.\n")


class UtilityBasedAgent:
    def __init__(self, environment):
        self.env = environment
        self.utility = 0

    def run(self):
        """
        Utility-based agent logic:
        - Clean current location if dirty (+10 utility).
        - Else move to next dirty location (-1 utility per move).
        - Stop when all clean.
        """
        print("Utility-Based Agent started.\n")
        while True:
            self.env.display()
            if self.env.room[self.env.vacuum_pos] == 0:
                self.env.clean_current()
                self.utility += 10
            else:
                dirty_positions = [i for i, status in enumerate(self.env.room) if status == 0]
                if dirty_positions:
                    new_pos = dirty_positions[0]
                    self.env.move_to(new_pos)
                    self.utility -= 1
                else:
                    break
        self.env.display()
        print(f"Cleaning complete with utility score: {self.utility}\n")


if __name__ == "__main__":
    # Seed random for reproducibility
    random.seed(42)

    # Create a 10x10 room with random dirt (0) and clean (1)
    room_size = 100
    initial_room = [random.choice([0, 1]) for _ in range(room_size)]

    print("Initial room state (first 20 locations):")
    print(initial_room[:20], "\n")

    # Initialize environment and agents
    env_goal = VacuumEnvironment(room_status=initial_room.copy(), vacuum_position=0)
    env_utility = VacuumEnvironment(room_status=initial_room.copy(), vacuum_position=0)

    goal_agent = GoalBasedAgent(env_goal)
    utility_agent = UtilityBasedAgent(env_utility)

    # Run Goal-Based Agent and show cleaning process
    goal_agent.run()

    # Run Utility-Based Agent and show cleaning process
    utility_agent.run()
