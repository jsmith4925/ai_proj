import pygame
import time
import random

#Set colors.
BLACK   =(0,0,0)
WHITE   =(255,255,255)
RED     =(255,0,0)
GREEN   =(0,255,0)
BLUE    =(0,0,255)
PURPLE  =(128,0,128)
LRED    =(255,128,128)

pygame.init()

#Smallest space: 5.
space=40

length=10
width=10

sizex=200+length*space
sizey=200+width*space

#Set size.
size=(sizex, sizey)
screen=pygame.display.set_mode(size)

pygame.display.set_caption("Make Purple!")
clock = pygame.time.Clock()
screen.fill(WHITE)

pygame.draw.rect(screen,BLACK,[100,100,sizex-199,sizey-199],2)

pygame.display.flip()

#Draw the grid.
for x in range(length):
    pygame.draw.line(screen,BLACK,[(x*space+100),100],[(x*space+100),sizey-100],2)        #Vertical lines.
for x in range(width):
    pygame.draw.line(screen,BLACK,[100,(x*space+100)],[sizex-100,(x*space+100)],2)        #Horizontal lines.

pygame.display.flip()



place = [[0 for y in range(width)] for x in range(length)]
wall = [[[1 for z in range(4)] for y in range(width)] for x in range(length)]
#If wall is [0,1,2,3], 0:up 1:down 2:left 3:right.

i=0
j=0
place[i][j]=1

done=False

#Randomly generates the maze.
while not done:

    sumcheck=0

    newplace=0

    direction = random.randint(0,3) #0:up 1:down 2:left 3:right.
    if direction==0:
        if j!=0:
            if place[i][j-1]==0:
                pygame.draw.line(screen,WHITE,[space*i+102,space*j+100],[space*i+99+space,space*j+100],2)
                wall[i][j][0]=0
                j=j-1
                place[i][j]=1
                wall[i][j][1]=0
    elif direction==1:
        if j!=width-1:
            if place[i][j+1]==0:
                pygame.draw.line(screen,WHITE,[space*i+102,space*j+100+space],[space*i+99+space,space*j+100+space],2)
                wall[i][j][1]=0
                j=j+1
                place[i][j]=1
                wall[i][j][0]=0
    elif direction==2:
        if i!=0:
            if place[i-1][j]==0:
                pygame.draw.line(screen,WHITE,[space*i+100,space*j+102],[space*i+100,space*j+99+space],2)
                wall[i][j][2]=0
                i=i-1
                place[i][j]=1
                wall[i][j][3]=0
    else:
        if i!=length-1:
            if place[i+1][j]==0:
                pygame.draw.line(screen,WHITE,[space*i+100+space,space*j+102],[space*i+100+space,space*j+99+space],2)
                wall[i][j][3]=0
                i=i+1
                place[i][j]=1
                wall[i][j][2]=0

    #These statements test if place is stuck.
    if (i==0) and (j==0):
        if (place[i+1][j]==1) and (place[i][j+1]==1):
            #Top left corner
            newplace=1
    elif (i==length-1) and (j==0):
        if (place[i-1][j]==1) and (place[i][j+1]==1):
            #Top right corner
            newplace=1
    elif (i==0) and (j==width-1):
        if (place[i][j-1]==1) and (place[i+1][j]==1):
            #Bottom left corner
            newplace=1
    elif (i==length-1) and (j==width-1):
        if (place[i][j-1]==1) and (place[i-1][j]==1):
            #Bottom right corner
            newplace=1
    elif (i==0) and (place[i][j-1]==1):
        if (place[i+1][j]==1) and (place[i][j+1]==1):
            #Left edge
            newplace=1
    elif (i==length-1):
        if (place[i][j-1]==1) and (place[i-1][j]==1) and (place[i][j+1]==1):
            #Right edge
            newplace=1
    elif (j==width-1):
        if (place[i-1][j]==1) and (place[i][j-1]==1) and (place[i+1][j]==1):
            #Top edge
            newplace=1
    elif (j==0):
        if (place[i-1][j]==1) and (place[i][j+1]==1) and (place[i+1][j]==1):
            #Bottom edge
            newplace=1
    elif (i!=0) and (j!=0) and (i!=length-1) and (j!=width-1):
        if (place[i][j-1]==1) and (place[i][j+1]==1) and (place[i-1][j]==1) and (place[i+1][j]==1):
            #Everything in between
            newplace=1
    else:
        pass


    #If stuck, find a new place.
    donemini = False
    if newplace==1:
        while not donemini:
            i=random.randint(0,length-1)
            j=random.randint(0,width-1)
            if place[i][j]!=1:
                pass
            else:
                donemini=True

    pygame.display.flip()

    for x in range(length):
        for y in range(width):
            sumcheck=sumcheck+place[x][y]
    pygame.display.set_caption("Progress: "+str((int(sumcheck/(width*length)*1000))/10)+"% (Might take a while for bigger mazes)")
    if sumcheck==width*length:
        done=True


i=0
j=0
pygame.draw.rect(screen,RED,[102+i*space,102+j*space,space-2,space-2],0)

i=length-1
j=width-1
pygame.draw.rect(screen,BLUE,[102+i*space,102+j*space,space-2,space-2],0)

pygame.display.set_caption("Make Purple!")

pygame.display.flip()
done = False

i=0
j=0

win=0

escape=False

#Controlls the block through the maze.
while not done:
    for event in pygame.event.get():

        if (i==length-1) and (j==width-1):
            win=1
            pygame.draw.rect(screen,PURPLE,[102+(length-1)*space,102+(width-1)*space,space-2,space-2],0)
            print("Congradulations, you solved the maze!")
            done=True

        if event.type==pygame.QUIT:
            done=True

        #0:up 1:down 2:left 3:right.
        if win==0:
            if event.type==pygame.KEYDOWN:
                direction=-1
                if event.key==pygame.K_UP:
                    direction=0
                elif event.key==pygame.K_DOWN:
                    direction=1
                elif event.key==pygame.K_LEFT:
                    direction=2
                elif event.key==pygame.K_RIGHT:
                    direction=3
                elif event.key==pygame.K_ESCAPE:
                    direction=4
                else:
                    pass

                if direction==0:
                    if wall[i][j][0]==0:
                        pygame.draw.rect(screen,WHITE,[102+i*space,102+j*space,space-2,space-2],0)
                        j=j-1
                        pygame.draw.rect(screen,RED,[102+i*space,102+j*space,space-2,space-2],0)
                elif direction==1:
                    if wall[i][j][1]==0:
                        pygame.draw.rect(screen,WHITE,[102+i*space,102+j*space,space-2,space-2],0)
                        j=j+1
                        pygame.draw.rect(screen,RED,[102+i*space,102+j*space,space-2,space-2],0)
                elif direction==2:
                    if wall[i][j][2]==0:
                        pygame.draw.rect(screen,WHITE,[102+i*space,102+j*space,space-2,space-2],0)
                        i=i-1
                        pygame.draw.rect(screen,RED,[102+i*space,102+j*space,space-2,space-2],0)
                elif direction==3:
                    if wall[i][j][3]==0:
                        pygame.draw.rect(screen,WHITE,[102+i*space,102+j*space,space-2,space-2],0)
                        i=i+1
                        pygame.draw.rect(screen,RED,[102+i*space,102+j*space,space-2,space-2],0)
                elif direction==4:
                    #Automatically solve the maze.
                    pygame.draw.rect(screen,WHITE,[102+i*space,102+j*space,space-2,space-2],0)

                    i=0
                    j=0
                    solved=False
                    past=4
                    color=[[0 for y in range(width)] for x in range(length)]
                    newcolor=0

                    while not solved:
                        newcolor=0
                        #0:up 1:down 2:left 3:right.
                        direction=random.randint(0,3)

                        if direction==0:
                            if wall[i][j][0]==0:
                                if past==1:
                                    pass
                                else:
                                    pygame.draw.rect(screen,LRED,[102+i*space,102+j*space,space-2,space-2],0)
                                    j=j-1
                                    color[i][j]=1
                                    pygame.draw.rect(screen,RED,[102+i*space,102+j*space,space-2,space-2],0)
                                    past=0
                        elif direction==1:
                            if wall[i][j][1]==0:
                                if past==0:
                                    pass
                                else:
                                    pygame.draw.rect(screen,LRED,[102+i*space,102+j*space,space-2,space-2],0)
                                    j=j+1
                                    color[i][j]=1
                                    pygame.draw.rect(screen,RED,[102+i*space,102+j*space,space-2,space-2],0)
                                    past=1
                        elif direction==2:
                            if wall[i][j][2]==0:
                                if past==3:
                                    pass
                                else:
                                    pygame.draw.rect(screen,LRED,[102+i*space,102+j*space,space-2,space-2],0)
                                    i=i-1
                                    color[i][j]=1
                                    pygame.draw.rect(screen,RED,[102+i*space,102+j*space,space-2,space-2],0)
                                    past=2
                        else:
                            if wall[i][j][3]==0:
                                if past==2:
                                    pass
                                else:
                                    pygame.draw.rect(screen,LRED,[102+i*space,102+j*space,space-2,space-2],0)
                                    i=i+1
                                    color[i][j]=1
                                    pygame.draw.rect(screen,RED,[102+i*space,102+j*space,space-2,space-2],0)
                                    past=3

                        if (i==length-1) and (j==width-1):
                            solved=True
                            i=0
                            j=0
                            pygame.draw.rect(screen,RED,[102+i*space,102+j*space,space-2,space-2],0)
                            i=length-1
                            j=width-1
                            pygame.draw.rect(screen,BLUE,[102+i*space,102+j*space,space-2,space-2],0)
                            i=0
                            j=0

                        elif ((wall[i][j][0]==1) and (wall[i][j][2]==1) and (wall[i][j][3]==1)) or ((wall[i][j][1]==1) and (wall[i][j][2]==1) and (wall[i][j][3]==1)) or ((wall[i][j][0]==1) and (wall[i][j][1]==1) and (wall[i][j][2]==1)) or ((wall[i][j][0]==1) and (wall[i][j][1]==1) and (wall[i][j][3]==1)):                 
                            newcolor=1

                        if newcolor==1:
                            for i in range(length):
                                for j in range(width):
                                    if color[i][j]==1:
                                        pygame.draw.rect(screen,WHITE,[102+i*space,102+j*space,space-2,space-2],0)
                            i=0
                            j=0

                        pygame.display.flip()
                else:
                    pass

        pygame.display.flip()

        clock.tick(120)

time.sleep(2)
pygame.quit()