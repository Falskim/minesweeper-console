class Board:
    
    TILES = []
    FIRST_STEP = True  
    DEBUG = False #Showing mine location
        
    def __init__(self, size, mine):
        
        self.SIZE = size #Size of board
        self.MINES = mine #Total mines
        
        self.TILES = self.create_tiles()
        self.randomize_mine()
        self.draw_tiles()
    
    def create_tiles(self):
        column = []
        count = 0  
        for i in range(self.SIZE):
            row = []
            for j in range(self.SIZE):
                row.append(Tile())
            column.append(row)
        return column
        
    def draw_tiles(self):
        #Column numbering
        column_number = "    "
        for i in range(self.SIZE):
            if i < 10 :
                column_number = column_number + str(i) + ' '
            else:
                column_number = column_number + str(i)
        print(column_number)
        
        #Tiles Line Border
        line = '  +'
        for i in range(self.SIZE * 2 + 1):
            line = line + '-'
        line = line + '+'
        print(line)
        
        for i in range(self.SIZE):
            result = str(i) + " | "
            if i > 9:
                result = str(i) + "| "
            for j in range(self.SIZE):
                if self.TILES[i][j].mine and (self.TILES[i][j].revealed or self.DEBUG):
                    result = result + 'X'
                elif self.TILES[i][j].revealed:
                    result = result + self.TILES[i][j].value
                else:
                    result = result + '?'
                result = result + ' '
            result = result + '|'
            print(result)
        print(line)
        
    def randomize_mine(self):
        import random
        count = 0
        while count < self.MINES:
            x = random.randint(0, self.SIZE - 1)
            y = random.randint(0, self.SIZE - 1)
            #print("Mine Location, X : " + str(x) + " , Y : " + str(y)) #Debug
            if not self.TILES[x][y].mine:
                self.TILES[x][y].mine = True
                count = count + 1

    def count_nearby_mine(self):
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if self.TILES[i][j].mine:
                    continue
                count = 0
                #Horizontal
                if i > 0 and self.TILES[i-1][j].mine:
                        count = count + 1
                if i < self.SIZE - 1 and self.TILES[i+1][j].mine:
                        count = count + 1
                #Vertical
                if j > 0 and self.TILES[i][j-1].mine:
                        count = count + 1
                if j < self.SIZE - 1 and self.TILES[i][j+1].mine:
                        count = count + 1
                #Diagonal
                if i > 0 and j > 0 and self.TILES[i-1][j-1].mine: #Top left
                        count = count + 1
                if i < self.SIZE - 1 and j > 0 and self.TILES[i+1][j-1].mine: #Bottom left
                        count = count + 1
                if i > 0 and j < self.SIZE - 1 and self.TILES[i-1][j+1].mine: #Top right
                        count = count + 1
                if i < self.SIZE - 1 and j < self.SIZE - 1 and self.TILES[i+1][j+1].mine: #Bottom right
                        count = count + 1         
                #Set Tile Value
                if not self.TILES[i][j].mine and count != 0:
                    self.TILES[i][j].value = str(count)

    def adjacent(self, x, y, end_prev):
        end_now = False
        if x > self.SIZE - 1 or x < 0 or y > self.SIZE - 1 or y < 0:
            return
        if self.TILES[x][y].mine or self.TILES[x][y].revealed:
            return
        if self.TILES[x][y].value != ' ' and not self.TILES[x][y].mine:
            end_now = True
        if end_now and end_prev:
            return
        self.TILES[x][y].revealed = True
        self.adjacent(x, y-1, end_now)
        self.adjacent(x, y+1, end_now)
        self.adjacent(x-1, y, end_now)
        self.adjacent(x+1, y, end_now)

    def pick(self, x, y):
        if self.FIRST_STEP:
            self.first_step(x, y)
        self.reveal(x, y)
        self.draw_tiles()
        return self.win_lose(x, y)

    def reveal(self, x, y):
        if self.TILES[x][y].mine:
            self.TILES[x][y].revealed = True
        else:
            self.adjacent(x, y, False)
        
    def first_step(self, x, y):
        if self.TILES[x][y].mine:
            self.TILES[x][y].mine = False
        self.count_nearby_mine()
        self.FIRST_STEP = False
        
    def game_end(self, x, y):
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if not self.TILES[i][j].revealed and not self.TILES[i][j].mine:
                    return False
        return True

    def win_lose(self, x, y):
        if self.game_end(x, y):
            return "win"
        elif self.TILES[x][y].mine:
            return "lose"
        return None
    
class Tile:
    mine = False
    revealed = False
    value = ' '
    adjacent = False

class Game:  
    def __init__(self):
        self.__start()
    
    def __start(self):
        import re
        size = input("Enter Board Dimension : ")
        mine = input("Enter Number of Mines : ")
        if int(mine)+1 > int(size)**2:
            print("Invalid number of mines !!! (" + mine + " mines in " + str(int(size)**2) + " total tiles)")
        else:
            run = Board(int(size), int(mine))
            while True:
                inp = input("X,Y : ")
                coord = re.split(',', inp)
                result = run.pick(int(coord[0]), int(coord[1]))
                if result == "lose":
                    print("---You Lose---")
                    break
                elif result == "win":
                    print("---You Win---")
                    break

'''   Starting The Game  '''
run = Game()

