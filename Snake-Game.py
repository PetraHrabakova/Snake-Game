import math
import random
import pygame
import sys

# In this program we have two classes = objects - the snake and the cubes.
# The snake body contains the cubes.
class cube(object):
    rows = 20
    w = 500

    # The reason why we set dirnx and dirny to 1 and 0 is because we want
    # The snake to start moving when the program starts running
    # If both variables were 0, we would have to click a key in order
    # for the snake to start moving
    def __init__(self, start, dirnx=1, dirny=0, color=(105, 210, 242)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        # We need to make sure that the direction of the snake stays with each cube
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows    # Distance between our x and y values
        i = self.pos[0]
        j = self.pos[1]

        # We draw a rectangle. The reason why we add 1 to each value and take away 2
        # From each value is because we want to be able to see te grid. If we didn't
        # Do it, we draw a rectangle and filled it all up with the colour including
        # the grid.
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))

        # We draw the eyes
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)   # Drawing one black eye
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)  # Drawing the other black eye


class snake(object):
    body = []   # We create a list for the body where we "store" all the cubes we collect
    turns = {}  # We create a dictionary where we "store" all the moves the snake makes

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)       # The snake's head equals the cube's position
        self.body.append(self.head) # We append the head to the body

        # These two functions describe in which direction is the snake moving.
        # The specific direction is defined in move() function.
        self.dirnx = 0              # Direction x
        self.dirny = 1              # Direction y

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # We insert the dictionary that has all the keys values and
            # And if they were pressed or not.
            # In real life, if we press more keys in the same time,
            # the program will adjust to that.
            keys = pygame.key.get_pressed()

            # In this for loop we define what is going to happen after we
            # press each key - left, right, up and down
            for key in keys:
                # We change the direction of the snake after we press each key.
                # The x works normal. If we move from 0 to the left, we go to the negative
                # value. If we move from 0 to the right, it goes to the positive value.
                # The y direction works opposite. If we go from 0 to the top, we move to
                # the negative value. If we go to the bottom, we add numbers.
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0

                    # We add a key which is the current position of the snake's head and we set it equal
                    # to the direction the snake just turned
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        # We get index and cube in self.body. We grab each cube and see if it's in
        # the list turns[].
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                # This line of code mean that if the program is on the last cube, it will remove
                # the turn from the list.
                if i == len(self.body) - 1:
                    self.turns.pop(p)

            # If our position is not in the list turns[], we still need to move the snake.
            # With this piece of code we check if the snake reached the edge of the screen and
            # We tell it what to do if it happens.
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1: c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows - 1)

                # If none of the things above are true, we just keep going
                # in the same direction of the previous movement.
                else: c.move(c.dirnx, c.dirny)


    # With this function we figure out where we are adding the cube to the snake
    def addCube(self):
        # We figure out where the tail is and we add it to the end of the tail
        tail = self.body[-1]
        # Direction x, direction y = x direction of the tail, y direction of the tail
        dx, dy = tail.dirnx, tail.dirny

        # Here the function checks in which direction is the tail moving
        # So we know where to add another cube
        # If the snake is moving to the right
        if dx == 1 and dy == 0:
            # We append a cube to the left side of the tail
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        # If the snake is moving to the left
        elif dx == -1 and dy == 0:
            # We append a cube to the right side of the tail
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        # If the snake is moving down
        elif dx == 0 and dy == 1:
            # We append a cube to the top of the tail
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        # If the snake is moving up
        elif dx == 0 and dy == -1:
            # We append a cube to the bottom of the tail
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        # Here we make sure the cube is moving in the same direction if the snake's body
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            # This basically says to draw eyes on the cube if it's the first cube
            if i == 0:
                c.draw(surface, True)  # Draws eyes on the cube
            else:
                c.draw(surface)        # No eyes

# This function draws the grid
def drawGrid(w, rows, surface):
    # We draw the grid by defining the size of the space between rows
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        # We draw two lines
        # (0, 0, 0) is for black colour because I want the grid to be black
        # but we can choose any other colour
        # The first line goes from one side of the window to the other
        pygame.draw.line(surface, (0, 0, 0), (x, 0), (x, w))
        # The second line is horizontal. Only y value will be changing, we keep x on 0 and w = width of the screen
        pygame.draw.line(surface, (0, 0, 0), (0, y), (w, y))


def redrawWindow(surface):
    # We pass the global variables
    global rows, width, s, snack
    surface.fill((247, 252, 179))      # We choose colour of the surface
    s.draw(surface)                    # We draw the snake
    snack.draw(surface)                # We draw the snack
    drawGrid(width, rows, surface)     # The program draws the grid
    pygame.display.update()            # This function updates the pygame window

# This function generates random snacks
def randomSnack(rows, item):
    positions = item.body

    while True:
        # We display a snack in a random row
        x = random.randrange(rows)
        y = random.randrange(rows)
        # We get a list of a filtered list and we see if any of the positions
        # is the same positions as the snake's body so we don't put a snack where
        # the snake's body is
        # If the lenght of the body is in the position below, the function continues
        # to generate a different snack.
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)



def main():
    global width, rows, s, snack

    # The size of the window
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))

    # Colour of snake's body
    s = snake((105, 210, 242), (10, 10))
    # We generate a random snack
    snack = cube(randomSnack(rows, s), color=(247, 128, 196))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        # These two functions decide about snake's speed
        pygame.time.delay(50)    # The lower number this one is, the faster the snake will be
        clock.tick(10)           # The lower this number is, the slower the snake will be
        s.move()                 # This function moves the whole snake after we press a key
        # If the snack hits the snake's head, we add another cube to the the snake's body
        if s.body[0].pos == snack.pos:
            s.addCube()
            # And generate a new snack
            snack = cube(randomSnack(rows, s), color=(247, 128, 196))   # Here we choose the colour of the snack

        for x in range(len(s.body)):
            # Basically here we check if the snake hit its own body
            # If yes, the game is over
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print('I am sorry, you lost.')
                print('Your score is:', len(s.body))
                pygame.quit()        # We quit pygame
                sys.exit()           # We exit the system


        redrawWindow(win)

    pass


main()