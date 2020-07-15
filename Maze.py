import Person
from typing import List

class Maze:
    
    people_with_maze = []

    def __init__(self, length, width, people = [], end = []):
        self.length = length
        self.width = width

        for p in range(0 , len(people)):
            if isinstance(p, Person.Person):
                if p in self.people_with_maze:
                    raise f'{p.name} cannot be in more than one maze'
            else:
                raise 'Person object not specified'
        self.people = people

        if end and isinstance(end, List) and len(end) == 2 and 0 < end[0] < length and 0 < end[1] < width:
            self.end = end
        elif not end:
            self.end = [width, length]
        else:
            raise "incorrect end specified"

    def inMaze(self, point):
        test = 0 <= point[0] <= self.width and 0 <= point[1] <= self.length
        return test

    def addPerson(self, person):
        if not isinstance(person, Person.Person):
            raise 'Person object must be passed'
        elif person in self.people_with_maze:
            raise 'Person cannot be in more than one maze'
        self.people.append(person)

    def invokeMazePeople(self):
        for p in self.people:
            p.setMaze(self)
            p.start()
            p.join()

    def showPath(self, person):
        path = person.path
        border = '*' + ('*' * self.width) + '*'
        print(border)

        for l in range(0, self.length + 1):
            indexes = list(filter(lambda x : x[0] == l, person.path))
            line = '*'
            for w in range(0, self.width + 1):
                line += '*' if [l, w] in indexes else ' '
            line += '*'
            print(line)
        print(border)

