import enum
import threading
from random import randrange
import Maze



class Person(threading.Thread):
    ''' Person Class'''
    
    semaphore = threading.Semaphore(1)  # Limits thread from printing at the same time and keep treads waiting for the next ticket

    def __init__(self, name, x, y):
        ''' Initializes a Person Object with the following attributes

        Attributes:

            name:
                Person's name
            x:
                Person's x value in starting postiion
            y:
                Person's y value in starting poitions

        Unspecified Attributes:

            direction_queue:
                Keeps track of all possible direction the person can take in a two dimentional plane : Left (L), Right (R), Up (U), Down (D)
            path:
                Keeps track of all point the person has gone
            trials:
                Keep track of how many times the person had to start over because there were no moves left
            maze:
                Current maze the person is attempting to solve

        Description:
            Each person is an instance of a thread. This allows for multiple people to solve a maze at the same time.
        
        '''

        threading.Thread.__init__(self)

        self.direction_queue = ['R', 'L', 'U', 'D']
        self.name = name
        
        # Checks points 
        if isinstance(x, int) and isinstance(y, int):
            self.maze = None
            self.x = x
            self.y = y
            self.path = [[x, y]]
            self.trials = 1
        else:
            raise "An integer value must be specified for both x and y"


    def move(self, direction):
        ''' Moves the person in the specified direction

        Args:
            direction:
                Direction the person is moving. Valid values are L, R, U, D
        '''
        if direction == 'L':
            self.x = self.x - 1
        elif direction == 'R':
            self.x = self.x + 1
        elif direction == 'U':
            self.y = self.y + 1
        elif direction == 'D':
            self.y = self.y - 1
        else:
            raise "Valid direction not specified"

    
    def random_direction(self):
        ''' Chooses a random direction based on the values that are left in the direction queue'''

        return self.direction_queue[randrange(0, len(self.direction_queue))]


    def attempt_maze(self, maze):
        '''Persons attempts to solve the maze by picking a random direction. This will continue until person reaches maze endpoint or there are no more directions'''
        
        # Checks that maze parameter is a Maze object
        if not isinstance(maze, Maze.Maze):
            raise 'Maze must be specified'
        
        # While person has not reached the end of the maze,
        # Get a random direction and move the person
        # If the person does not have any other direction to go
        # throw an Error to signify the end of the attempt
        while([self.x, self.y] != self.maze.end):

            # Checks that there are possible direction to use
            if self.direction_queue:
                direction = self.random_direction()
                self.direction_queue.remove(direction)
                self.move(direction)
            else:
                raise "Person has no where else to go"

            point = [self.x, self.y]
            
            # Checks if the direction the person is attempting to go is within the maze
            if point in self.path or not maze.point_in_maze(point):
                point = self.path[len(self.path) - 1]
                self.x = point[0]
                self.y = point[1]
                continue
            self.path.append(point)
            self.direction_queue = ['R', 'L', 'U', 'D']


    def set_maze(self, maze):
        '''Sets the maze for the person'''
        self.maze = maze


    def run(self):
        '''Runs the person thread to attempt to solve the maze over and over again until the maze is complete'''

        # Person will continue to attempt to solve the maze until the endpoint is reached
        while True:
            try:
                self.attempt_maze(self.maze)
                print(self.toString())
                break

            except Exception:
                self.trials += 1
                self.x = self.path[0][0]
                self.y = self.path[0][1]
                self.path = [self.path[0]]
                self.direction_queue = ['R', 'L', 'U', 'D']
        

    def toString(self):
        ''' Create String Object containing person's name, number of trials (Attempts), Path, and a CLI representatio of the maze'''
        
        self.semaphore.acquire()
        val = ''
        
        try:
            # Concatinated String with attributes :) like JAVA
            val = (
                    f'{self.name}\'s Results:\n' + 
                    f'Attempts: {self.trials}\n' + 
                    f'Path: {self.path}\n' + 
                    self.maze.get_maze_path(self) + '\n'
                )
        except Exception as e:
            print(e)
        finally:
            self.semaphore.release()
            return val