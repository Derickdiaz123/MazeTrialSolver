
from Person import Person
from Maze import Maze



maze = Maze(10, 10, end=[5,5])

test_case_1 = Person('Test', 0, 0)
test_case_2 = Person('Test1', 4, 3)

maze.addPerson(test_case_1)
maze.addPerson(test_case_2)

maze.invokeMazePeople()