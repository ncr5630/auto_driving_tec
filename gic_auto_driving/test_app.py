import unittest
from unittest.mock import patch
from io import StringIO
from gic_auto_driving.app import App, ConsoleInputOutput, InteractionChain, DrivingSupervisor, Car, initialize_cars, initialize_field


class TestCar(unittest.TestCase):
    def test_car_creation(self):
        car = Car("Car1", 0, 0, "N")
        self.assertEqual(car.name, "Car1")
        self.assertEqual(car.x, 0)
        self.assertEqual(car.y, 0)
        self.assertEqual(car.direction, "N")


class TestConsoleInputOutput(unittest.TestCase):
    @patch('builtins.input', return_value='test_input')
    def test_get_input(self, mock_input):
        io_handler = ConsoleInputOutput()
        result = io_handler.get_input("Prompt: ")
        self.assertEqual(result, "test_input")

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_output(self, mock_stdout):
        io_handler = ConsoleInputOutput()
        io_handler.print_output("Test Output")
        self.assertEqual(mock_stdout.getvalue(), "Test Output\n")


class TestDrivingSupervisor(unittest.TestCase):
    def setUp(self):
        self.io_handler = ConsoleInputOutput()

    def test_initialize(self):
        supervisor = DrivingSupervisor(self.io_handler)
        supervisor.initialize('3x4', ['Car1 1 2 S', 'Car2 0 0 N'])
        self.assertIsNotNone(supervisor.field)
        self.assertIsNotNone(supervisor.cars)
        self.assertEqual(len(supervisor.cars), 2)

    def test_is_valid_position(self):
        supervisor = DrivingSupervisor(self.io_handler)
        supervisor.field = [[' ' for _ in range(3)] for _ in range(4)]
        self.assertTrue(supervisor.is_valid_position(1, 2))
        self.assertFalse(supervisor.is_valid_position(5, 2))
        self.assertFalse(supervisor.is_valid_position(1, -1))

    def test_is_collision(self):
        supervisor = DrivingSupervisor(self.io_handler)
        supervisor.cars = {'Car1': Car('Car1', 1, 2, 'N'), 'Car2': Car('Car2', 3, 4, 'S')}
        self.assertTrue(supervisor.is_collision(1, 2))
        self.assertFalse(supervisor.is_collision(0, 0))
        self.assertTrue(supervisor.is_collision(3, 4))

    def test_run_simulation(self):
        supervisor = DrivingSupervisor(self.io_handler)
        supervisor.initialize('3x3', ['Car1 1 1 N', 'Car2 0 0 S'])
        supervisor.run_simulation()
        report = supervisor.get_driving_report()
        self.assertEqual(report, [('Car1', 1, 2), ('Car2', 0, -1)])


class TestInteractionChain(unittest.TestCase):
    def setUp(self):
        self.io_handler = ConsoleInputOutput()

    @patch('builtins.input', return_value='Invalid Command')
    @patch('sys.stdout', new_callable=StringIO)
    def test_prompt_invalid_command(self, mock_stdout, mock_input):
        chain = InteractionChain(self.io_handler)
        chain.prompt()
        expected_output = "Invalid command.\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)


class TestApp(unittest.TestCase):
    def setUp(self):
        self.io_handler = ConsoleInputOutput()

    @patch('builtins.input', side_effect=['Run simulation', '3x3', 'Car1 1 1 N', 'Car2 0 0 S', 'done'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_simulation(self, mock_stdout, mock_input):
        app = App()
        app.run_simulation('3x3', ['Car1 1 1 N', 'Car2 0 0 S'])
        expected_output = "Field: 3x3\nCars: ['Car1 1 1 N', 'Car2 0 0 S']\nDriving Report: [('Car1', 1, 2), ('Car2', 0, -1)]\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)


class TestInitializationFunctions(unittest.TestCase):
    def test_initialize_field(self):
        field = initialize_field('3x4')
        self.assertEqual(len(field), 4)
        self.assertEqual(len(field[0]), 3)

    def test_initialize_cars(self):
        input_cars = ['Car1 1 2 S', 'Car2 0 0 N']
        cars = initialize_cars(input_cars)
        self.assertEqual(len(cars), 2)
        self.assertTrue('Car1' in cars)
        self.assertTrue('Car2' in cars)
        self.assertEqual(cars['Car1'].x, 1)
        self.assertEqual(cars['Car2'].direction, 'N')


if __name__ == '__main__':
    unittest.main()
