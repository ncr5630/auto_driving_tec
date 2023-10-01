class Car:
    def __init__(self, name, x, y, direction):
        self.name = name
        self.x = x
        self.y = y
        self.direction = direction


class ConsoleInputOutput:
    @staticmethod
    def get_input(prompt):
        return input(prompt)

    @staticmethod
    def print_output(output):
        print(output)


class DrivingSupervisor:
    def __init__(self, io_handler):
        self.field = None
        self.cars = None
        self.driving_report = None
        self.io_handler = io_handler

    def initialize(self, input_field, input_cars):
        self.field = initialize_field(input_field)
        self.cars = initialize_cars(input_cars)

    def is_valid_position(self, x, y):
        return 0 <= x < len(self.field[0]) and 0 <= y < len(self.field)

    def is_collision(self, new_x, new_y):
        cars_val = self.cars.values()
        new_x = new_x
        new_y = new_y
        data = any(car.x == new_x and car.y == new_y for car in cars_val)
        return data

    def run_simulation(self):
        driving_report = []

        for car in self.cars.values():
            if not self.is_valid_position(car.x, car.y) or not self.is_collision(car.x, car.y):
                self.io_handler.print_output(f"Skipping simulation for car {car.name}.")
            else:
                self.move_car(car)
                driving_report.append((car.name, car.x, car.y))

        self.driving_report = driving_report

    def move_car(self, car):
        # Placeholder simulation logic
        # Move each car one step in its current direction
        if car.direction == "N":
            car.y += 1
        elif car.direction == "S":
            car.y -= 1
        elif car.direction == "E":
            car.x += 1
        elif car.direction == "W":
            car.x -= 1

    def get_driving_report(self):
        return self.driving_report


def initialize_field(input_field):
    dimensions = input_field.strip().split('x')
    if len(dimensions) != 2:
        raise ValueError("Invalid field dimensions format. Please use 'widthxheight'.")

    width, height = map(int, dimensions)

    field = [[' ' for _ in range(width)] for _ in range(height)]

    return field


def initialize_cars(input_cars):
    cars = {}
    for single in input_cars:
        for line in single.splitlines():
            # Ignore empty lines
            if not line.strip():
                continue

            # Split the line into parts and handle the case where there are fewer than 4 values
            parts = line.split()
            name, x, y, direction = parts[0], int(parts[1]) if len(parts) > 1 else 0, int(parts[2]) if len(
                parts) > 2 else 0, parts[3] if len(parts) > 3 else "N"

            cars[name] = Car(name, x, y, direction)

    return cars


class InteractionChain:

    def __init__(self, io_handler):
        self.io_handler = io_handler
        self.on_run_simulation = None

    def prompt(self):
        command = self.io_handler.get_input("Enter a command: ")
        if command == "Run simulation" and self.on_run_simulation:
            input_field = self.io_handler.get_input("Enter field details: ")
            input_cars = []
            car = 1
            while True:
                input_car = self.io_handler.get_input("Enter car details: ")

                if input_car.lower() == 'done':
                    break
                car += 1
                input_cars.append(input_car)
            self.on_run_simulation(input_field, input_cars)
        else:
            self.io_handler.print_output("Invalid command.")


class App:

    def __init__(self):
        self.io_handler = ConsoleInputOutput()
        self.interaction_chain = InteractionChain(self.io_handler)
        self.driving_supervisor = DrivingSupervisor(self.io_handler)

        # Add on_run_simulation event
        self.interaction_chain.on_run_simulation = self.run_simulation

    def run_simulation(self, input_field, input_cars):
        self.io_handler.print_output(f"Field: {input_field}")
        self.io_handler.print_output(f"Cars: {input_cars}")

        self.driving_supervisor.initialize(input_field, input_cars)
        self.driving_supervisor.run_simulation()

        report = self.driving_supervisor.get_driving_report()
        self.io_handler.print_output(f"Driving Report: {report}")


# Example usage
if __name__ == "__main__":
    app = App()
    app.interaction_chain.prompt()
