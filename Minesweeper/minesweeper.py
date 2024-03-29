#minesweeper test
import random,pygame
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT,1000)




class NewBoard:

    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows

        self.grid = []
        self.tileMap = []
        self.endMap = []


    def placeMines(self, difficulty):
        numberOfMines = (self.cols * self.rows * difficulty) // 10

        for i in range(numberOfMines):
            x = random.randint(0,self.cols-1)
            y = random.randint(0,self.rows-1)

            if self.grid[x][y] != -1:
                self.grid[x][y] = -1  #  -1 is a mine

            else:
                numberOfMines += 1

        for i in range(0,self.cols):
            for j in range(0, self.rows):

                if self.grid[i][j] != -1:    
                    mineCount = 0
                    
                    for k in range(-1,2):
                        for l in range(-1,2):

                            try:
                                if i+k >= 0 and j+l >= 0 and self.grid[i+k][j+l] == -1:
                                    mineCount += 1
                            
                            except IndexError:
                                pass
                            
                                
                    self.grid[i][j] = mineCount
    
    def createMaps(self):
        self.tileMap.clear()
        self.grid.clear()
        self.endMap.clear()

        for i in range(0,self.cols):
            rowsArray = []
            for j in range(0, self.rows):
                rowsArray.append(1)       # 0 = empty     1 = tile     2 = flag
            
            self.tileMap.append(rowsArray)

        for i in range(0,self.cols):
            rowsArray = []
            endRowsArray = []
            for j in range(0, self.rows):
                rowsArray.append(0)       # origin is in the top left corner    self.grid[y][x]
                endRowsArray.append(0)
            self.grid.append(rowsArray)
            self.endMap.append(endRowsArray)



board = NewBoard(10,10)   #  (rows,cols) 
difficulty = 2  # 0 - 3

running = True

def startGame():
    board.createMaps()
    board.placeMines(difficulty)

    global gameOver
    global gameWon
    global timer
    global flagsLeft


    flagsLeft = 99
    timer = 0
    gameOver = False
    gameWon = False
    screen = pygame.display.set_mode(((board.cols + 1) * 25, (board.rows+3) * 25 + 13))  #  width and height

    
    

startGame()







# pygame 
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode(((board.cols + 1) * 25, (board.rows+3) * 25 + 13))   #50 for ui at top  + 12.5 for each border


# screen
pygame.display.set_caption("Minesweeper")
icon = pygame.image.load("Minesweeper/Assets/icon.png")
pygame.display.set_icon(icon)

# colours
dGrey = (128,128,128) # 7b
grey  = (192,192,192) # db
white = (255,255,255) # ff

# images
pressedTileImg = pygame.image.load("Minesweeper/Assets/pressedTile.png")
flagImg = pygame.image.load("Minesweeper/Assets/flag.png")
tileImg = pygame.image.load("Minesweeper/Assets/hiddentile.png")
deathTile = pygame.image.load("Minesweeper/Assets/deathTile.png")
cross = pygame.image.load("Minesweeper/Assets/cross.png")
edgeH = pygame.image.load("Minesweeper/Assets/edgeH.png")
edgeV = pygame.image.load("Minesweeper/Assets/edgeV.png")

happy = pygame.image.load("Minesweeper/Assets/happyFace.png")
happyPressed = pygame.image.load("Minesweeper/Assets/happyFacePressed.png")
scared = pygame.image.load("Minesweeper/Assets/scaredFace.png")
dead = pygame.image.load("Minesweeper/Assets/deadFace.png") 
deadPressed = pygame.image.load("Minesweeper/Assets/deadFacePressed.png")
win = pygame.image.load("Minesweeper/Assets/winFace.png")
winPressed = pygame.image.load("Minesweeper/Assets/winFacePressed.png")

#fonts
font = pygame.font.Font("Minesweeper/Assets/font.ttf", 15)


# pygame loop
while running:
       
    for event in pygame.event.get():
        if  event.type == pygame.QUIT:
            running = False

        #timer
        elif  event.type == pygame.USEREVENT and timer <= 998 and gameOver == False:
            timer += 1
            print(timer)
        clock.tick(60)

        
        
        #clicked tile
        if event.type == pygame.MOUSEBUTTONUP:
            x,y = pygame.mouse.get_pos()

            # face reset
            if x >= -10 + (25*board.cols)/2 and x <= 35 + (25*board.cols)/2 and y>=15 and y<=60:
                startGame()
                
            
            if event.button == 1 and x>=12.5 and x<(board.cols)*25 + 12.5 and y>75 and y<=(board.rows) * 25 + 75 and gameOver == False:
                xBox = int((x-12.5)//25)
                yBox = (y-75)//25

                if xBox < board.cols and yBox < board.rows and board.tileMap[xBox][yBox] == 1:
                    board.tileMap[xBox][yBox] = 0

                    # self searching algorithm for connecting safe tiles
                    if board.grid[xBox][yBox] == 0:
                        visited = []
                        queue = [(xBox,yBox)]

                        while len(queue) > 0:

                            for k in range(-1,2):
                                for l in range(-1,2):
                                    current = queue[0]

                                    try:
                                        if not(current in visited) and current[0]+k >= 0 and current[1]+l >= 0 and (k,l) != (0,0) and board.grid[current[0]+k][current[1]+l] == 0:
                                            queue.append(((current[0]+k),current[1]+l))
                                
                                    except IndexError:
                                        pass

                            visited.append(current)
                            board.tileMap[current[0]][current[1]] = 0
                            queue.pop(0)  
                            
                        # outer ring of numbers
                        for n in range(len(visited)):
                            current = visited[n]
                            for k in range(-1,2):
                                for l in range(-1,2):

                                    try:
                                        if current[0]+k >= 0 and current[1]+l >= 0 and (k,l) != (0,0) and board.tileMap[current[0]+k][current[1]+l] == 1:
                                            board.tileMap[current[0]+k][current[1]+l] = 0
                                    

                                    except IndexError:
                                        pass
                
                    # end game sequence
                    if board.grid[xBox][yBox] == -1:
                        gameOver = True

                        for i in range(board.rows):
                            for j in range(board.cols):
                                if board.grid[j][i] == -1:
                                    if board.tileMap[j][i] == 2:
                                        board.endMap[j][i] = 1 # 1 = cross
                                    board.tileMap[j][i] = 0
                                    
                        board.tileMap[xBox][yBox] = 3

                    
                    # win conditions
                    tilesLeft = 0
                    for i in range(board.rows):
                            for j in range(board.cols):
                                if board.tileMap[j][i] == 1 or board.tileMap[j][i] == 2 :
                                    tilesLeft += 1
                    if tilesLeft == (board.cols * board.rows * difficulty) // 10:
                        gameOver = True
                        gameWon = True
                        for i in range(board.rows):
                            for j in range(board.cols):
                                if board.grid[j][i] == -1:
                                    board.tileMap[j][i] = 0
                                    board.endMap[j][i] = 1
                                

                    



        
        #flag tile
        if event.type == pygame.MOUSEBUTTONDOWN and gameOver == False:
            x,y = pygame.mouse.get_pos()
            
            if event.button == 3 and x>=12.5 and x<(board.cols)*25 + 12.5 and y>75 and y<=(board.rows) * 25 + 75:
                xBox = int((x-12.5)//25)
                yBox = (y-75)//25

                if xBox < board.cols and yBox < board.rows:
                    if board.tileMap[xBox][yBox] == 1 and flagsLeft > 0:
                        board.tileMap[xBox][yBox] = 2
                        flagsLeft -= 1
                    elif board.tileMap[xBox][yBox] == 2:
                        board.tileMap[xBox][yBox] = 1
                        flagsLeft += 1
                    

    screen.fill(grey)

    # Game Box
    pygame.draw.line(screen, dGrey,(12.5,75),((board.cols + 1) * 25 - 12.5,75),2)
    pygame.draw.line(screen, dGrey,(12.5,(board.rows + 1) * 25 + 50),((board.cols + 1) * 25 - 12.5,(board.rows + 1) * 25 + 50),2)
    pygame.draw.line(screen, dGrey,(12.5,75),(12.5,(board.rows + 1) * 25 + 50),2)
    pygame.draw.line(screen, dGrey,((board.cols + 1) * 25 - 12.5,75),((board.cols + 1) * 25 - 12.5,(board.rows + 1) * 25 + 50),2)
    # UI Box
    pygame.draw.line(screen, dGrey,(12.5,12.5),((board.cols + 1) * 25 - 12.5,12.5),2)
    pygame.draw.line(screen, dGrey,(12.5,62.5),((board.cols + 1) * 25 - 12.5,62.5),2)
    pygame.draw.line(screen, dGrey,(12.5,12.5),(12.5,62.5),2)
    pygame.draw.line(screen, dGrey,((board.cols + 1) * 25 - 12.5,12.5),((board.cols + 1) * 25 - 12.5,62.5),2)
    # Game Grid
    for i in range(1,board.cols):
        pygame.draw.line(screen, dGrey,(12.5 + i*25, 75),(12.5 + i*25, (board.rows + 1) * 25 + 50),2)
        pygame.draw.line(screen, dGrey,(12.5, 75 + i*25),((board.cols) * 25 + 12.5, 75 + i*25),2)
    # Grid Elements
    
    

    for i in range(board.rows):
        for j in range(board.cols):
            element = str(board.grid[j][i])

            if element == "-1":
                element = "*"
                colour = (0,0,0)#black
            elif element == "0":
                element = ""
                colour = (0,0,0)#black
            elif element == "1":
                colour = (0,0,255)#blue
            elif element == "2":
                colour = (0,126,0)#green
            elif element == "3":
                colour = (255,0,0)#red
            elif element == "4":
                colour = (0,0,128)#dblue
            elif element == "5":
                colour = (128,0,0)#dred
            elif element == "6":
                colour = (0,128,128)#cyan
            elif element == "7":
                colour = (0,0,0)#black
            elif element == "8":
                colour = (128,128,128)#grey

            
            text_surface = font.render(element, False, colour)
            width, height = font.size(element)
            screen.blit(text_surface, (27 +(25*j) - (width/2) ,89.5 + (25*i) - (height/2)))   # +2 here for centering reasons


    # Hidden tiles gen
    for i in range(board.rows):
            for j in range(board.cols):
                if board.tileMap[j][i] == 1:
                    screen.blit(tileImg, (25 +(25*j) - (12.5) ,87.5 + (25*i) - (12.5)))   # +2 here for centering reasons
                if board.tileMap[j][i] == 2:
                    screen.blit(flagImg, (25 +(25*j) - (12.5) ,87.5 + (25*i) - (12.5)))   # +2 here for centering reasons
                if board.tileMap[j][i] == 3:
                    screen.blit(deathTile, (25 +(25*j) - (12.5) ,87.5 + (25*i) - (12.5)))   # +2 here for centering reasons
                    text_surface = font.render("*", False, (0,0,0))
                    width, height = font.size("*")
                    screen.blit(text_surface, (26 +(25*j) - (width/2) ,89.5 + (25*i) - (height/2)))   # can probably remove this^^
                #end game sequence
                
                if board.endMap[j][i] == 1:
                    screen.blit(cross, (25 +(25*j) - (12.5) ,87.5 + (25*i) - (12.5)))

        

    # Face Display
    if gameOver== False:
        screen.blit(happy, (-10 + (25*board.cols)/2,15))
    if gameOver== True and gameWon == False:
        screen.blit(dead, (-10 + (25*board.cols)/2,15))
    if gameOver== True and gameWon == True:
        screen.blit(win, (-10 + (25*board.cols)/2,15))   


   
            

    #pressed tile
    if pygame.mouse.get_pressed()[0]:
        x,y = pygame.mouse.get_pos()
        
        #tile press
        if x>=12.5 and x<(board.cols)*25 + 12.5 and y>75 and y<=(board.rows) * 25 + 75 and gameOver == False:
            xBox = int((x-12.5)//25)
            yBox = (y-75)//25

            if xBox < board.cols and yBox < board.rows and board.tileMap[xBox][yBox] == 1:
                screen.blit(pressedTileImg, (25 +(25*xBox) - (12.5) ,87.5 + (25*yBox) - (12.5)))   # +2 here for centering reasons
                screen.blit(scared, (-10 + (25*board.cols)/2,15)) 

        # Face Press
        if x >= -10 + (25*board.cols)/2 and x <= 35 + (25*board.cols)/2 and y>=15 and y<=60:
            if gameOver!= True:
                screen.blit(happyPressed, (-10 + (25*board.cols)/2,15))
            if gameOver== True and gameWon == False:
                screen.blit(deadPressed, (-10 + (25*board.cols)/2,15))
            if gameOver== True and gameWon == True:
                screen.blit(winPressed, (-10 + (25*board.cols)/2,15))   

    # Border Display
    for i in range(board.cols//2):
        screen.blit(edgeH,(i*12.5*board.cols/2,-1))
        screen.blit(edgeH,(i*12.5*board.cols/2,(board.cols+3) * 25))
    for i in range(board.rows):
        screen.blit(edgeV,(-3,(board.rows+3)*3*i))
        screen.blit(edgeV,((board.cols+0.5) * 25,(board.rows+3)*3*i))


   


   
            


    pygame.display.flip()
    #pygame.display.update()




