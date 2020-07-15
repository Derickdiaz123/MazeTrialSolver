import Person
from typing import List
from concurrent.futures import *

class Maze:
    ''' Represent a Maze people can traverse from a starting point to ending point
    
    Acts as the main controller for multiple people (threads)
    threads will attempt to move within the boundaries until the endpoint is reached. If the person fails, the person will try again until it succeeds.
    
    '''

    def __init__(self, width:int, height:int, people:list = [], end:int = [], threads:int = 3) -> object:
        ''' Initializes Maze

        Attributes:
            
            height:
                Integer representing the size of the maze from top to bottom
            width:
                Integer representing the size of the maze from left to right
            people:
                List of people attempting to solve the maze. Each person must be unique and assigned to only one maze.
            end:
                Array with two values defining the point the person must hit to solve the maze. By default it will be [width, height]
        '''

        # Maze size attributes
        self.height = height
        self.width = width

        self.threads = threads

        # Verifies that the people array only contains Person Object and that the person is only assigned to one maze
        for p in people:
            if isinstance(p, Person.Person):
                if p.maze:
                    raise f'{p.name} cannot be in more than one maze'
                elif not self.point_in_maze([p.x, p.y]):
                    raise f'{p.name} starting point is not within the maze'
            else:
                raise 'Person object not specified'

        # If no error is raised, the person array is added
        self.people = people

        # Verifies that the end point is a list that contains only two values and the values are within the maze
        # If no endpoint is specified, set the endpoint to the bottom right corner of the maze
        if end and isinstance(end, list) and len(end) == 2 and self.point_in_maze(end):
            self.end = end
        elif not end:
            self.end = [width, height]
        else:
            raise "incorrect end point specified"


    def point_in_maze(self, point:list) -> bool:
        ''' Check if the point is within the maze

        Args:

            point:
                A list with two values denoting an x and y value

        '''

        return 0 <= point[0] <= self.width and 0 <= point[1] <= self.height


    def add_person(self, person:Person) -> None:
        ''' Adds a person to the maze

        Args:

            person:
                Person that will be added
        
        '''

        # Checks if the parameter is a Person Object and person does not have a maze added
        if not isinstance(person, Person.Person):
            raise 'Person object must be passed'
        elif person.maze:
            raise 'Person cannot be in more than one maze'
        self.people.append(person)


    def invoke_people(self):
        ''' Invoke each person to start attempting to solve the maze'''
        with ThreadPoolExecutor(self.threads) as executor:
            for p in self.people:
                p.set_maze(self)
                executor.submit(p.start)

    def get_maze_path(self, person):
        ''' Prints out the resulting path within the maze for the person
        Args:
            person:
                Person object that traversed the maze

        '''
        
        # Generates the top border of the maze  
        border = '*' + ('*' * self.width) + '*'
        maze = border + '\n'

        # Generates the inside of the maze
        # If the person has steps on a specific point it will print a * otherwise print a blank space
        # TODO: Can be replaced with a list comprehension that's converted to a string and printed
        for l in range(0, self.height + 1):
            indexes = list(filter(lambda x : x[0] == l, person.path))
            line = '*'
            for w in range(0, self.width + 1):
                line += '*' if [l, w] in indexes else ' '
            line += '*'
            maze += line + '\n'
        maze += border
        return maze

