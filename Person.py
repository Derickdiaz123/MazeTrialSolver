import enum
import threading
from random import randrange
import Maze



class Person(threading.Thread):
    
    direction_queue = ['R', 'L', 'U', 'D']

    def __init__(self, name, x, y):
        threading.Thread.__init__(self)
        self.name = name
        if isinstance(x, int) and isinstance(y, int):
            self.maze = None
            self.x = x
            self.y = y
            self.path = [[x, y]]
            self.trials = 1
        else:
            raise "An integer value must be specified for both x and y"


    def move(self, direction):
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

    
    def randomDirection(self):
        return self.direction_queue[randrange(0, len(self.direction_queue))]


    def attemptMaze(self, maze):
        if not isinstance(maze, Maze.Maze):
            raise 'Maze must be specified'
        
        while([self.x, self.y] != self.maze.end):

            if self.direction_queue:
                direction = self.randomDirection()
                self.direction_queue.remove(direction)
                self.move(direction)
            else:
                raise "Person has no where else to go"

            point = [self.x, self.y]
            if point in self.path or not maze.inMaze(point):
                point = self.path[len(self.path) - 1]
                self.x = point[0]
                self.y = point[1]
                continue
            self.path.append(point)
            self.direction_queue = ['R', 'L', 'U', 'D']


    def setMaze(self, maze):
        self.maze = maze

    def run(self):
        while True:
            try:
                self.attemptMaze(self.maze)
                print(f'{self.name}: Maze Solved!')
                print(f'Attempts: {self.trials}')
                print(self.path)
                self.maze == None
                break
            except Exception as e:
                self.trials += 1
                self.x = self.path[0][0]
                self.y = self.path[0][1]
                self.path = [self.path[0]]
                self.direction_queue = ['R', 'L', 'U', 'D']
        
