
from Person import Person
from Maze import Maze

Maze(
    10, 
    10,
    people = [
        Person('Test', 0, 0),
        Person('Test1', 0, 0),
    ],
).invoke_people()