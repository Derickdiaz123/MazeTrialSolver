
from Person import Person
from Maze import Maze



maze = Maze(100, 100)

test_case_1 = Person('Test', 0, 0)
test_case_2 = Person('Test1', 0, 0)

maze.addPerson(test_case_1)
maze.addPerson(test_case_2)

maze.invokeMazePeople()

# maze.showPath(test_case_1)