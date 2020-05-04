import math, copy, time, string, random
import os

from cmu_112_graphics import *
from tkinter import *

#Citation:
#colors = http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter

#Initial Step: 
# 1) create a screen for the user to input their data
class StartScreenMode (Mode):
    def appStarted(mode):
        # print this number in the user input box
        mode.varNum = ""
        # creates an instance for a button class
        mode.userEnterButton = EnterButton(mode.width, mode.height)
        mode.userInputBox = UserVarNum(mode.width, mode.height)
        mode.finalNum = 0
        mode.buttonCX = 0
        mode.buttonCY = 0
        mode.bR = 0
        mode.canType = False
        mode.varNum = ""

    def mousePressed(mode, event):
        #if the user presses the button:
        if mode.userInputBox.touchingTextBox(event.x, event.y):
            print("YOU CAN TYPE NOW")
            mode.canType = True

        elif mode.helpMode(event.x, event.y):
            print("HELP MODE NEED TO BE IMPLEMENTED")
            #changes the screen to helpMode:
            mode.app.setActiveMode(mode.app.helpMode)

        elif mode.userEnterButton.buttonTouching(event.x, event.y):
            print("TRUTHTABLE NEED TO BE IMPLEMENTED")
            mode.finalNum = int(mode.varNum)
            mode.app.finalNum = int(mode.varNum)
            #print(f"mode.finalNum is {mode.finalNum}")
            mode.app.setActiveMode(mode.app.truthTable)

    def keyPressed(mode, event):
        #print(event.key)
        string = "abcdefghijklmnopqrstuwxyz"
        stringSet = set(string)
        if mode.canType == True:
            if event.key in stringSet:
                print("That is not an acceptable value. Put in int value.")
            elif event.key == "Backspace":
                #deletes the last piece
                if mode.varNum != "": #as long as it is not an empty string, we can pop it
                    mode.varNum = mode.varNum [:-1]  
                else:
                    print("Type in number!!!")
            else:
                mode.varNum += str(event.key)
        
        '''
        REVISION NEEDED:
        elif isinstance(event.key, int): #can't get this work for now! Have to figure this out!!!
            mode.varNum += str(event.key)
            print(mode.varNum)
        '''

    def redrawAll(mode, canvas):
        #Title of the game: De Morgan's Logic Gates Generator
        canvas.create_text(mode.width//2, mode.height//8, text = "De Morgan's Logic Gates Generator", font = "Arial 40")
        # Ask for number of variables:
        canvas.create_text(mode.width//2, 2*mode.height//8, text = "Type in the number of variables (2 ~ 4):", font = "Arial 25" )
        #Help Button
        #to get it at x = 1300, y = 200
        mode.buttonCY = mode.height//8 # y = 200
        mode.buttonCX = mode.width - mode.buttonCY # x = 1300
        mode.bR = 60
        canvas.create_oval(mode.buttonCX - mode.bR, mode.buttonCY - mode.bR, 
                            mode.buttonCX + mode.bR, mode.buttonCY + mode.bR, fill = "red")
        #Question mark (?) is at x = 1300, 100
        canvas.create_text(mode.buttonCX, mode.buttonCY, text = "?", font = "Arial 60", fill = "yellow" )
        #textBox:
        mode.userInputBox.drawBox(canvas)
        #textNum:
        mode.userInputBox.writeText(canvas, mode.varNum)
        #Enter Button:
        mode.userEnterButton.drawButton(canvas)


    def buttonForStartScreenMode(mode, x, y):
        if mode.buttonForStartIns.buttonTouching(x,y) == True:
            mode.varTyped = True

    def distance(mode, x, y, cX, cY):
        return ((cX - x)**2 + (cY - y)**2)**0.5

    def helpMode(mode, x, y):
        if mode.distance(x, y, mode.buttonCX, mode.buttonCY) <= mode.bR: #this shows that the mouse clicked the ? circle:
            return True
        else:
            return False

class EnterButton(App):
    def __init__ (self, width, height):
        self.width = width
        self.height = height
        self.cX = self.width//2
        self.cY = self.height//2
        self.topX = 0
        self.topY = 0
        self.bottomX = 0
        self.bottomY = 0

    def drawButton(self, canvas):
        margin = 50
        size = 100
        self.topX = self.cX - size
        self.topY = self.height - 3*margin
        self.bottomX = self.cX + size
        self.bottomY = self.height - margin
        canvas.create_rectangle(self.topX, self.topY, self.bottomX, self.bottomY, fill = "light blue")
        canvas.create_text(self.cX, self.height - margin*2, text = "ENTER", font = "Arial 40")

    def buttonTouching(self, x, y):
        if self.topX <= x <= self.bottomX:
            if self.topY <= y <= self.bottomY:
                return True
        return False

class UserVarNum (App):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cX = self.width//2
        self.marY = self.height//8
        self.topX = 0
        self.topY = 0
        self.bottomX = 0
        self.bottomY = 0

    def drawBox(self, canvas):
        margin = 25
        size = 150
        self.topX = self.cX - size
        self.topY = self.marY*4 + margin
        self.bottomX = self.cX + size
        self.bottomY = self.marY*6 - margin
        canvas.create_rectangle(self.topX, self.topY, self.bottomX, self.bottomY)

    def writeText(self, canvas, num):
        canvas.create_text(self.width//2, self.marY*5, text = num, font = "Arial 50")

    def touchingTextBox(self, x, y):
        if self.topX <= x <= self.bottomX:
            if self.topY <= y <= self.bottomY:
                return True
        return False

#Another Mode:
class TruthTable(Mode):
    def appStarted(mode):
        #NOT SURE IF THIS WOULD WORK:
        #mode.numVar = StartScreenMode.parameters
        mode.inst = StartScreenMode()        
        mode.numVar = mode.app.finalNum
        #StartScreenMode.parameters() #should return the number of variables!
        mode.rows = mode.numVar
        mode.cols = 2**mode.rows + 1
        mode.rows += 1
        mode.app.rows = mode.rows
        mode.app.cols = mode.cols
        mode.cX = mode.width//2
        mode.dictVal = dict()
        mode.dictOfQVals = dict()
        mode.doneButton = DoneButton(mode.width, mode.height)
        #mode.drawingTruthTable = DrawTruthTable()
        mode.canDrawKMap = False
        #Where the Q val will be placed at:
        mode.nRow = 0
        mode.nCol = 0

        #Combined the TruthTable Mode with this:
        mode.topX = 50
        mode.topY = 50
        mode.margin = 50
        mode.bottomX = mode.width//2 - mode.margin
        mode.bottomY = mode.height - 2*mode.margin
        mode.xMargin = (mode.bottomX - mode.topX)//mode.rows
        mode.yMargin = (mode.bottomY - mode.topY)//mode.cols
        mode.dictQVal = dict()
        mode.listOfPairs = list()
        
        #KMap Mode:
        mode.logicGatesButton = LogicEquation(mode.width, mode.height)
        mode.midX = mode.width//2
        mode.numOfVar = mode.app.finalNum
        mode.size = 100 
        mode.kTopX = mode.midX + mode.margin #X = 800
        mode.kTopY = mode.margin*1.5 #Y = 75
        mode.kBottomX = mode.width - mode.margin*2 - mode.size #X = 1300
        mode.kBottomY = mode.height//2 #Y = 400
        #Size of the KMap will be (800, 75, 1300, 325)
        mode.buttonMarg = 100
        mode.buttonWidth = 80
        #SOP Button: (1350, 100, 1450, 180)
        #POS Button: (1350, 220, 1450, 300)
        mode.dictTotalVals = dict()
        mode.kRows = 0
        mode.kCols = 0
        mode.twoDList = list()

        #status: SOP or POS:
        mode.status = None
        mode.kMap = None
        mode.colorGroup = ["deep sky blue", "gold", "seashell", "slate blue2", "lightblue3", "pink3", "PaleVioletRed1", "cyan"]
        mode.groupName = ["First", "Second","Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth"]
        mode.turn = 0 #start with -1 because of the list indexing
        mode.touching = 0
        mode.cRow = 0
        mode.cCol = 0
        mode.currColor = mode.colorGroup[mode.turn]
        mode.setOfBoxes = set() #set of clicked boxes -- will include row, col
        mode.group = dict() #dictionary format: {"First": (row, col), "Second": (row, col) ...}

        #finding equation:
        mode.equation = []
        mode.strEquation = ""
        mode.equationAvail = False


    def mousePressed(mode, event):
        sizeBut = 200
        topYButt = mode.width - sizeBut
        if event.y <= topYButt:
            if mode.rows - 1 == 2:
                if mode.twoVarTouching(event.x, event.y):
                    (mode.nRow, mode.nCol) = mode.twoVarRowCol(event.x, event.y)
            elif mode.rows - 1 == 3:
                if mode.threeVarTouching(event.x, event.y):
                    (mode.nRow, mode.nCol) = mode.threeVarRowCol(event.x, event.y)
            elif mode.rows - 1 == 4:
                if mode.fourVarTouching(event.x, event.y):
                    (mode.nRow, mode.nCol) = mode.fourVarRowCol(event.x, event.y)

        print(event.x, event.y)
        if mode.doneButton.pressingDone(event.x, event.y):
            print("Pressed the DONE Button")
            mode.canDrawKMap = True

        if mode.logicGatesButton.pressingSOP(event.x, event.y):
            #call a method that will calculate the SOP in the truth table!
            mode.status = True
            mode.app.status = True
            print("SOP will be performed!")
            mode.kMap = True

        elif mode.logicGatesButton.pressingPOS(event.x, event.y):
            mode.status = False
            mode.app.status = False
            print("POS will be performed!")
            mode.kMap = True

        if mode.kMap == True:
            if mode.touchingBox(event.x, event.y):
                print("it's touching the kmap")
                (mode.cRow, mode.cCol) = mode.rowAndCol(event.x, event.y)
                print(f"mode.rowAndCol is called! => row, col = {mode.cRow, mode.cCol}")
                mode.setOfBoxes.add((mode.cRow, mode.cCol))
                #this will return that currentColor = mode.colorGroup[mode.turns]

            #touchingGroupBox is a method that detects whether event.x and event.y is within the boundary of the box w group name
            if mode.touchingGroupBox(event.x, event. y):
                if mode.turn + 1 < len(mode.groupName):
                    #thus increasing the group too
                    currentGroupName = mode.groupName[mode.turn]
                    mode.group[currentGroupName] = mode.setOfBoxes
                    print(mode.group)
                    #increments!
                    mode.turn += 1 
                    mode.currColor = mode.colorGroup[mode.turn]
                    mode.setOfBoxes = set() #empties the set

            
            if mode.touchingDG (event.x, event.y):
                mode.touching += 1
                if mode.touching == 1:
                    #thus increasing the group too
                    currentGroupName = mode.groupName[mode.turn]
                    mode.group[currentGroupName] = mode.setOfBoxes
                    #increments!
                    mode.currColor = mode.colorGroup[mode.turn]
                    mode.setOfBoxes = set()
                    #gotta convert this to the variables!
                    #call a method that calculates the equation!
                    mode.solveForEquation()

            if mode.touchingSolutionButton(event.x, event.y):
                mode.app.setActiveMode(mode.app.solutionMode) 
            if mode.pressingDrawingPad(event.x, event.y):
                mode.app.setActiveMode(mode.app.drawingPad)

    #NEED REVISION:    
    def solveForEquation(mode):
        listOfLoc = list()
        setOfGroups = set()
        returnList = list()
        newList = list()
        equationList = list()
        print(f"mode.group = {mode.group}")
        for group in mode.group: #loops through every color group
            print(f"{group}'s TURN:'")
            setOfGroups = mode.group[group]
            print(setOfGroups)
            
            for (row, col) in setOfGroups:
                #first and second 
                firstList = []
                secondList = []
                newVarPair = []
                first = mode.twoDList[col][0] #Y axis vairable
                second = mode.twoDList[0][row]
                print(f"totalVarPair => {second + first}")
                #mode.numOfVar:
                if mode.numOfVar == 2: #first will be either one or two:
                    firstList.append(first)
                elif mode.numOfVar == 3:
                    firstList.append(first)
                elif mode.numOfVar == 4:
                    #now we need to count:
                    if len(first) == 2:
                        newVarPair = first[0]
                        firstList.append(newVarPair)
                        newVarPair = first[1]
                        firstList.append(newVarPair)
                    elif len(first) == 4: #then both variables are prime'd
                        newVarPair = first[:2]
                        firstList.append(newVarPair)
                        newVarPair = first[2:]
                        firstList.append(newVarPair)
                    elif len(first) == 3:
                        if first[-1] == "'": #then only last one is prime'd:
                            newVarPair = first[0]
                            firstList.append(newVarPair)
                            newVarPair = first[1:]
                            firstList.append(newVarPair)
                        else:
                            newVarPair = first[:2]
                            firstList.append(newVarPair)
                            newVarPair = first[-1]
                            firstList.append(newVarPair)
                print(f"firstList = {firstList}")
                print(f"second ==> {second}")
                if mode.numOfVar == 2: #second will be either one or two:
                    secondList.append(second)
                elif mode.numOfVar == 3:
                    if len(second) == 2:
                        newVarPair = second[0]
                        secondList.append(newVarPair)
                        newVarPair = second[1]
                        secondList.append(newVarPair)
                    if len(second) == 4: #then both variables are prime'd
                        newVarPair = second[:2]
                        secondList.append(newVarPair)
                        newVarPair = second[2:]
                        secondList.append(newVarPair)
                    elif len(second) == 3:
                        if second[-1] == "'": #then only last one is prime'd:
                            newVarPair = second[0]
                            secondList.append(newVarPair)
                            newVarPair = second[1:]
                            secondList.append(newVarPair)
                        else:
                            newVarPair = second[:2]
                            secondList.append(newVarPair)
                            newVarPair = second[-1]
                            secondList.append(newVarPair) 
                elif mode.numOfVar == 4:
                    #now we need to count:
                    if len(second) == 2:
                        newVarPair = second[0]
                        secondList.append(newVarPair)
                        newVarPair = second[1]
                        secondList.append(newVarPair)
                    elif len(second) == 4: #then both variables are prime'd
                        newVarPair = second[:2]
                        secondList.append(newVarPair)
                        newVarPair = second[2:]
                        secondList.append(newVarPair)
                    elif len(second) == 3:
                        if second[-1] == "'": #then only last one is prime'd:
                            newVarPair = second[0]
                            secondList.append(newVarPair)
                            newVarPair = second[1:]
                            secondList.append(newVarPair)
                        else:
                            newVarPair = second[:2]
                            secondList.append(newVarPair)
                            newVarPair = second[-1]
                            secondList.append(newVarPair)    
                print(f"secondList = {secondList}")
                
                #fist = A, second = B --> location = AB
                listOfLoc += secondList
                listOfLoc += firstList
            
            print(f"printing final version of listOfLoc = {listOfLoc}")
            returnList = mode.commonVar(listOfLoc)
            listOfLoc = [] #empties the list
        
            print(f"returnList = {returnList}")
           #now mode.status:
            for ind in range(len(returnList)):
                var = returnList[ind]
                if mode.status == True: # add *
                    newList.append(var)
                    newList.append("*")
                elif mode.status == False: #it's already done!
                    newList.append(var)
                #elif mode.status == False:
                #    newList.append(var)
                #    newList.append("+")
                
                if ind == len(returnList) - 1:
                    print(f"last term in newList = {newList}")
                    if mode.status == True: # + 
                        newList.pop()
                        newList += "+"
                    elif mode.status == False: # *
                        newList += "*"
            
            returnList = []
            equationList += newList
            newList = []
            print(f"group: {group} --> returnList = {equationList}")
            
            print(equationList)
        equationList.pop()
        print(f"equationList --> {equationList}")
        mode.equation = equationList #now we can print it!
        mode.app.finalEquation = mode.equation
        mode.app.finalEquationList = equationList
        mode.equationAvail = True

    def showEquation(mode, canvas):
        result = ""
        for var in mode.equation:
            result = result + var + " "
        
        margin = 50
        topX = mode.width//2 + margin #X = 800 
        topY = mode.height//2 + margin*3 #Y = 550
        botX = mode.width - margin #X = 1050
        botY = mode.height//2 + margin*5 #Y = 650
        #mode.equation is a list
        #mode.strEquation:
        mode.strEquation = result
        if len(mode.strEquation) > 20:
            size = "Arial 15"
        else:
            size = "Arial 25"
        canvas.create_text((topX + botX)//2, (topY + botY)//2, text = f"EQUATION = {mode.strEquation}", font = size)
        #mode.equation needs to be printed!!!
    
    def drawSolutionButton(mode, canvas):
        margin = 50
        sizeX = 200
        sizeY = 75
        topX = mode.width - sizeX - margin
        topY = mode.height - sizeY - margin
        botX = mode.width - margin
        botY = mode.height - margin
        canvas.create_rectangle(topX, topY, botX, botY, fill = "khaki")
        canvas.create_text((topX + botX)//2, (topY + botY)//2, text = "SOLUTION", font = "Arial 25")

    def touchingSolutionButton(mode, x, y):
        margin = 50
        sizeX = 200
        sizeY = 100
        topX = mode.width - sizeX - margin
        topY = mode.height - sizeY - margin
        botX = mode.width - margin
        botY = mode.height - margin

        if topX <= x <= botX:
            if topY <= y <= botY:
                return True

    #color citation: http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
    def drawDrawingPad(mode, canvas):
        margin = 50
        sizeX = 300
        sizeY = 75
        topX = mode.width//2 + margin
        topY = mode.height - sizeY - margin
        botX = mode.width//2 + margin + sizeX
        botY = mode.height - margin
        canvas.create_rectangle(topX, topY, botX, botY, fill = "LightPink3")
        canvas.create_text((topX + botX)//2, (topY + botY)//2, text = "DRAWING PAD", font = "Arial 25")

    def pressingDrawingPad(mode, x, y):
        margin = 50
        sizeX = 200
        sizeY = 75
        topX = mode.width//2 + margin
        topY = mode.height - sizeY - margin
        botX = mode.width//2 + margin + sizeX
        botY = mode.height - margin
        if topX <= x <= botX:
            if topY <= y <= botY:
                return True

    def commonVar(mode, setOfLoc):
        #setOfLoc includes A'B, AB, A'B' and such...
        numDict = dict()
        for letter in setOfLoc: #setOfLocation includes a set of tuples
            if letter in numDict:
                numDict[letter] += 1
            else:
                numDict[letter] = 1
        
    #now loop through numDict:
        maxNum = 0
        maxVar = []
        print(f"initial maxVar = {maxVar}")
        print(f"numDict ==> {numDict}")
        for var in numDict: #numDict = {A:1, B:1, ... such }
            if numDict[var] > maxNum:
                maxNum = numDict[var]
                if len(maxVar) >= 1:
                    maxVar = []
                maxVar.append(var)
                if mode.status == False:
                    maxVar.append("+")
            elif numDict[var] == maxNum:
                maxVar.append(var)
                if mode.status == False:
                    maxVar.append("+")
        if maxVar[-1] == "+":
            maxVar.pop()

        print(f"maxVar -> {maxVar}")
        return maxVar

    def drawGroupBox(mode, canvas):
        half = mode.width//2
        margin = 50
        sizeX = 300
        sizeY = 80
        topX = half + margin
        topY = mode.height//2 + margin
        botX = topX + sizeX
        botY = topY + sizeY
        color = mode.colorGroup[mode.turn]
        canvas.create_rectangle(topX, topY, botX, botY, fill = color)
        currGroupName = mode.groupName[mode.turn]
        canvas.create_text((topX + botX)//2, (topY + botY)//2, text = f"{currGroupName} GROUP", 
                            font = "Arial 25")

    def touchingGroupBox(mode, x, y):
        half = mode.width//2
        margin = 50
        sizeX = 300
        sizeY = 100
        topX = half + margin #800
        topY = mode.height//2 #400
        botX = topX + sizeX #1100
        botY = topY + sizeY #500
        if topX <= x <= botX:
            if topY <= y <= botY:
                return True

    #color citation = http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
    def doneGrouping(mode, canvas):
        margin = 50
        sizeX = 200
        sizeY = 80
        ogX = 1100

        topX = ogX + margin*2
        topY = mode.height//2 + margin
        botX = topX + sizeX
        botY = topY + sizeY

        canvas.create_rectangle(topX, topY, botX, botY, fill = "salmon")
        canvas.create_text((topX + botX)//2, (topY + botY)//2, text = "FINISHED", font = "Arial 25")
    
    def touchingDG (mode, x, y):
        margin = 50
        sizeX = 150
        sizeY = 100
        ogX = 1100

        topX = ogX + margin*2
        topY = mode.height//2
        botX = topX + sizeX
        botY = topY + sizeY

        if topX <= x <= botX:
            if topY <= y <= botY:
                return True

    def keyPressed(mode, event):
        #can only type either 1, 0, or X:
        if event.key == "1":
            mode.dictVal[(mode.nRow, mode.nCol)] = 1
        elif event.key == "0":
            mode.dictVal[(mode.nRow, mode.nCol)] = 0
        elif event.key == "X" or event.key == "x":
            mode.dictVal[(mode.nRow, mode.nCol)] = "X"
        #Removes the value in the dictionary:
        elif event.key == "Backspace":
            if (mode.nRow, mode.nCol) in mode.dictVal:
                del mode.dictVal[(mode.nRow, mode.nCol)]
            else:
                print("Can delete the value")
        else:
            print("Type in either 1, 0, or X (x is also okay)")

        if event.key == "d":
            #deletes the last element in the setOfBoxes
            if len(mode.setOfBoxes) > 0:
                newSetBoxes = set()
                for box in mode.setOfBoxes:
                    if box != (mode.cRow, mode.cCol):
                        newSetBoxes.add(box)
                mode.setOfBoxes = newSetBoxes

        if event.key == "Left":
            mode.turn -= 1
            mode.currColor = mode.colorGroup[mode.turn]
            mode.setOfBoxes = mode.group[mode.turn]

    def redrawAll(mode, canvas):
        #Table itself:
        mode.drawingTable(canvas)
        #DONE Button:
        mode.doneButton.drawDoneButton(canvas)
        #numbers:
        if mode.numVar == 2:
            mode.twoVar(canvas)
        elif mode.numVar == 3:
            mode.threeVar(canvas)
        elif mode.numVar == 4:
            mode.fourVar(canvas)
        #mode.writingQVals is the reason why I am getting MVP Error!!!
        mode.writingQVals(canvas)
        if mode.canDrawKMap == True:
            #Then we can draw the KMap
            mode.logicGatesButton.drawAll(canvas)
            mode.drawAll(canvas)
            #drawing other features like done grouping and stuff:
            mode.doneGrouping(canvas)
            mode.drawGroupBox(canvas)
            mode.drawSolutionButton(canvas)
            mode.drawDrawingPad(canvas)

            if mode.equationAvail == True:
                mode.showEquation(canvas)
            
    def drawingTable(mode, canvas):
        '''
        mode.margin = 50
        mode.bottomX = mode.width//2 - mode.margin
        mode.bottomY = mode.height - 2*mode.margin
        mode.xMargin = (mode.bottomX - mode.topX)//mode.rows
        mode.yMargin = (mode.bottomY - mode.topY)//mode.cols
        '''
        for row in range(mode.rows):
            for col in range(mode.cols):
                canvas.create_rectangle(mode.topX + row*(mode.xMargin),
                                        mode.topY + col*(mode.yMargin),
                                        mode.topX + (row+1)*mode.xMargin,
                                        mode.topY + (col+1)*mode.yMargin)

    def fontChange(mode):
        if mode.numVar == 2:
            mode.varFont = "Arial 25"
        elif mode.numVar == 3:
            mode.varFont = "Arial 20"
        elif mode.numVar == 4:
            mode.varFont = "Arial 10"

    #The Q values in the truth table:
    def writingQVals(mode, canvas):
        #dictOfVal has a q value with the location
        #dictOfVal's key is the location of row, col and value is Q val
        #mode.dictVal, mode.varFont
        mode.fontChange()
        for (row, col) in mode.dictVal:
            qVal = mode.dictVal[(row,col)]
            canvas.create_text(mode.topX + (row+0.5)*mode.xMargin, mode.topY + (col+0.5)*mode.yMargin,
                                            text = qVal, font = mode.varFont)
            #Need to save which variable this includes to:
            #var = mode.listOfPairs[col - 1] #because the col = 0 is just a letter variable
            index = mode.listOfPairs[col - 1]
            mode.dictQVal[index] = qVal

        #Pass in the mode.dictQVal dictionary parameters which includes qval
        #mode.app.dictOfQValues = mode.dictQVal

    def fillQVals(mode,canvas):
        for (row, col) in mode.dictVal:
            qVal = mode.dictVal[(row,col)]
            canvas.create_text(mode.topX + (row+0.5)*mode.xMargin, mode.topY + (col+0.5)*mode.yMargin,
                                            text = qVal, font = mode.varFont) 

    #For now I will just do twoVar, threeVar, fourVar:
    #TWO VAR - Font = "Arial 25"
    def twoVar(mode, canvas):
        letterOrd = ord("A") - 1
        numVal = 0
        numPairs = tuple()
        mode.listOfPairs = [(0,0), (0,1), (1,1), (1,0)]
        #pairSet = set()
        #setOfNum = mode.createPairs(pairSet)
        #listOfNum = mode.varPairs(setOfNum)
        #Will assume that the variables are A and B --> Q
        #filling in with values:
        for col in range(mode.cols):
            for row in range(mode.rows):
                if col == 0:
                    letterOrd += 1
                    if row == mode.rows - 1: #last one has to be Q all the times:
                        canvas.create_text(mode.topX + (row+0.5)*mode.xMargin, mode.topY + (col+0.5)*mode.yMargin,
                                            text = "Q", font = "Arial 25")
                    
                    else:
                        canvas.create_text(mode.topX + (row+0.5)*mode.xMargin, mode.topY + (col+0.5)*mode.yMargin,
                                            text = chr(letterOrd), font = "Arial 25") 
                else:
                    if col >= 1 and row == 0:
                        numPairs = mode.listOfPairs[col-1]
                        numVal = numPairs[0]
                        canvas.create_text(mode.topX + (row+0.5)*mode.xMargin, mode.topY + (col+0.5)*mode.yMargin,
                                            text = numVal, font = "Arial 25")
                    
                    elif col>= 1 and row == 1:
                        numPairs = mode.listOfPairs[col-1]
                        numVal = numPairs[1]
                        canvas.create_text(mode.topX + (row+0.5)*mode.xMargin, mode.topY + (col+0.5)*mode.yMargin,
                                            text = numVal, font = "Arial 25")


    #Two Var Touching:
    def twoVarTouching(mode, x, y):
        for row in range(mode.rows):
            for col in range(mode.cols):
                if mode.topX + row*(mode.xMargin) <= x <= mode.topX + (row+1)*mode.xMargin:
                    if mode.topY + col*(mode.yMargin) <= y <= mode.topY + (col+1)*mode.yMargin:
                        return True

    def twoVarRowCol(mode, x, y):
        for row in range(mode.rows):
            for col in range(mode.cols):
                if mode.topX + row*(mode.xMargin) <= x <= mode.topX + (row+1)*mode.xMargin:
                    if mode.topY + col*(mode.yMargin) <= y <= mode.topY + (col+1)*mode.yMargin:
                        return (row, col)

    #ThreeVar - font = "20 Arial"      
    def threeVar(mode, canvas):
        letterOrd = ord("A") - 1
        numVal = 0
        numPairs = tuple()
        mode.listOfPairs = [(0,0,0), (0,0,1), (0,1,0), (0,1,1),
                        (1,0,0), (1,0,1), (1,1,0), (1,1,1)]
        #pairSet = set()
        #setOfNum = mode.createPairs(pairSet)
        #listOfNum = mode.varPairs(setOfNum)
        #Will assume that the variables are A and B --> Q
        #filling in with values:
        for col in range(mode.cols):
            for row in range(mode.rows):
                if col == 0:
                    letterOrd += 1
                    if row == 3: #last one has to be Q all the times:
                        canvas.create_text(mode.topX + (row+0.5)*mode.xMargin, mode.topY + (col+0.5)*mode.yMargin,
                                            text = "Q", font = "Arial 20")
                    else:
                        canvas.create_text(mode.topX + (row+0.5)*mode.xMargin, mode.topY + (col+0.5)*mode.yMargin,
                                        text = chr(letterOrd), font = "Arial 20")
                    
                
                else:
                    if col >= 1 and row == 0:
                        numPairs = mode.listOfPairs[col-1]
                        numVal = numPairs[0]
                        canvas.create_text(mode.topX + (row+0.5)*mode.xMargin, mode.topY + (col+0.5)*mode.yMargin,
                                            text = numVal, font = "Arial 20")

                    elif col >= 1 and row == 1:
                        numPairs = mode.listOfPairs[col-1]
                        numVal = numPairs[1]
                        canvas.create_text(mode.topX + (row+0.5)*mode.xMargin, mode.topY + (col+0.5)*mode.yMargin,
                                            text = numVal, font = "Arial 20")

                    elif col >= 1 and row == 2:
                        numPairs = mode.listOfPairs[col-1]
                        numVal = numPairs[2]
                        canvas.create_text(mode.topX + (row+0.5)*mode.xMargin, mode.topY + (col+0.5)*mode.yMargin,
                                            text = numVal, font = "Arial 20")

    #Three Var touching:
    def threeVarTouching(mode, x, y):
        for row in range(mode.rows):
            for col in range(mode.cols):
                if mode.topX + row*(mode.xMargin) <= x <= mode.topX + (row+1)*mode.xMargin:
                    if mode.topY + col*(mode.yMargin) <= y <= mode.topY + (col+1)*mode.yMargin:
                        return True

    def threeVarRowCol(mode, x, y):
        for row in range(mode.rows):
            for col in range(mode.cols):
                if mode.topX + row*(mode.xMargin) <= x <= mode.topX + (row+1)*mode.xMargin:
                    if mode.topY + col*(mode.yMargin) <= y <= mode.topY + (col+1)*mode.yMargin:
                        return (row, col)
    
    #NO CHANGE FOR THIS
    def fourVar(mode, canvas):
        letterOrd = ord("A") - 1
        numVal = 0
        numPairs = tuple()
        mode.listOfPairs = [(0,0,0,0), (0,0,0,1), (0,0,1,0), (0,0,1,1),
                        (0,1,0,0), (0,1,0,1), (0,1,1,0), (0,1,1,1),
                        (1,0,0,0), (1,0,0,1), (1,0,1,0), (1,0,1,1),
                        (1,1,0,0), (1,1,0,1), (1,1,1,0), (1,1,1,1)]

        for col in range(mode.cols):
            for row in range(mode.rows):
                if col == 0:
                    letterOrd += 1
                    #CHANGED THE INDEX
                    if row == 4: #last one has to be Q all the times:
                        canvas.create_text(mode.topX + (row+0.5)*mode.xMargin, mode.topY + (col+0.5)*mode.yMargin,
                                            text = "Q")
                    else:
                        canvas.create_text(mode.topX + (row+0.5)*mode.xMargin, mode.topY + (col+0.5)*mode.yMargin,
                                            text = chr(letterOrd))
                    
                else:
                    if col >= 1 and row == 0:
                        numPairs = mode.listOfPairs[col-1]
                        numVal = numPairs[0]
                        canvas.create_text(mode.topX + (row+0.5)*mode.xMargin, mode.topY + (col+0.5)*mode.yMargin,
                                            text = numVal)

                    elif col >= 1 and row == 1:
                        numPairs = mode.listOfPairs[col-1]
                        numVal = numPairs[1]
                        canvas.create_text(mode.topX + (row+0.5)*mode.xMargin, mode.topY + (col+0.5)*mode.yMargin,
                                            text = numVal)

                    if col >= 1 and row == 2:
                        numPairs = mode.listOfPairs[col-1]
                        numVal = numPairs[2]
                        canvas.create_text(mode.topX + (row+0.5)*mode.xMargin, mode.topY + (col+0.5)*mode.yMargin,
                                            text = numVal)
                                        
                    if col >= 1 and row == 3:
                        numPairs = mode.listOfPairs[col-1]
                        numVal = numPairs[3]
                        canvas.create_text(mode.topX + (row+0.5)*mode.xMargin, mode.topY + (col+0.5)*mode.yMargin,
                                            text = numVal)

    #Four Variables touching:
    def fourVarTouching(mode, x, y):
        for row in range(mode.rows):
            for col in range(mode.cols):
                if mode.topX + row*(mode.xMargin) <= x <= mode.topX + (row+1)*mode.xMargin:
                    if mode.topY + col*(mode.yMargin) <= y <= mode.topY + (col+1)*mode.yMargin:
                        return True

    def fourVarRowCol(mode, x, y):
        for row in range(mode.rows):
            for col in range(mode.cols):
                if mode.topX + row*(mode.xMargin) <= x <= mode.topX + (row+1)*mode.xMargin:
                    if mode.topY + col*(mode.yMargin) <= y <= mode.topY + (col+1)*mode.yMargin:
                        return (row, col)

    def drawAll(mode, canvas):
        margin = 70
        var = ""
        #write Truth Table --> KMap
        canvas.create_text(mode.midX + mode.midX//2 - margin, mode.margin, text = "Truth Table → KMap", font = "Arial 30")

        #drawing a table:
        if mode.numOfVar == 2:
            #the graph will be 3*3
            mode.kCols = 3
            mode.kRows = 3
            #Create a 2D list: from https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#creating2dLists
            mode.twoDList = [([]* mode.kCols) for row in range(mode.kRows )]
            #Hardcoding it if that works better:
            mode.twoDList = [[None, "A'", "A"],
                             ["B'", None, None],
                             ["B", None, None]]
            #mode.twoDList[1] = "A'"
            #mode.twoDList[2] = "A"
            #mode.twoDList[3] = "B'"
            #mode.twoDList[6] = "B"
            #listOfNum = [1,2,3,6]
            #i = 
                    #index = listOfNum[i]
                    #i += 1
                    #canvas.create_text(midX, midY, text = mode.twoDList[index], font = "Arial 25")

                    #canvas.create_text(midX, midY, text = var, font = "Arial 25")

            #The graph will graph this soon:
            for vars in mode.dictQVal:
                first = vars[0]
                second = vars[1]
                if first == 0:
                    first = "A'"
                elif first == 1:
                    first = "A"
                if second == 0:
                    second = "B'"
                elif second == 1:
                    second = "B"
                result = first + second
                #print(result)
                #Using mode.dictTotalVals to map out the location of output logics
                #print(mode.dictQVal[vars])
                mode.dictTotalVals[result] = mode.dictQVal[vars]
            mode.qValTable()
            
            for row in range(mode.kRows):
                for col in range(mode.kCols):
                    #↓ for down arrow & → for right arrow
                    #will change the color =
                    if (row, col) in mode.setOfBoxes:
                        color = mode.currColor
                    else:
                        color = "White"
                    margX = (mode.kBottomX - mode.kTopX) // (mode.numOfVar + 1)
                    margY = (mode.kBottomY - mode.kTopY) // (mode.numOfVar + 1)
                    canvas.create_rectangle(mode.kTopX + row*margX, mode.kTopY + col*margY, 
                                            mode.kTopX + (row+1)*margX, mode.kTopY + (col+1)*margY, fill = color)
                    #Will fill the table:
                    #↓ for down arrow & → for right arrow
                    
                    if mode.twoDList[col][row] != None:
                        midX = (mode.kTopX + row*margX + mode.kTopX + (row+1)*margX)//2
                        midY = (mode.kTopY + col*margY + mode.kTopY + (col+1)*margY)//2    
                        canvas.create_text(midX, midY, text = mode.twoDList[col][row], font = "Arial 25")

        elif mode.numOfVar == 3:
            #the graph will be 5 * 3
            mode.kRows = 5
            mode.kCols = 3
            #Create a two list: from https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#creating2dLists
            mode.twoDList = [([] * mode.kCols) for row in range(mode.kRows)]
            mode.twoDList = [[None, "A'B'", "A'B", "AB", "AB'"],
                             ["C'", None, None, None, None],
                             ["C", None, None, None, None]]
            
            for vars in mode.dictQVal:
                first = vars[0]
                second = vars[1]    
                third = vars[2]
                if first == 0:
                    first = "A'"
                elif first == 1:
                    first = "A"
                if second == 0:
                    second = "B'"
                elif second == 1:
                    second = "B"
                if third == 0:
                    third = "C'"
                elif third == 1:
                    third = "C"
                result = first + second + third
                #print(mode.dictQVal[vars])
                mode.dictTotalVals[result] = mode.dictQVal[vars]       
            mode.qValTable()
            
            for row in range(mode.kRows): 
                for col in range(mode.kCols):
                    if (row, col) in mode.setOfBoxes:
                        color = mode.currColor
                    else:
                        color = "White"
                    margX = (mode.kBottomX - mode.kTopX) // (mode.numOfVar + 2)
                    margY = (mode.kBottomY - mode.kTopY) // (mode.numOfVar)
                    canvas.create_rectangle(mode.kTopX + row*margX, mode.kTopY + col*margY, 
                                            mode.kTopX + (row+1)*margX, mode.kTopY + (col+1)*margY, fill = color)
                
                    if mode.twoDList != None:
                        midX = (mode.kTopX + row*margX + mode.kTopX + (row+1)*margX)//2
                        midY = (mode.kTopY + col*margY + mode.kTopY + (col+1)*margY)//2    
                        canvas.create_text(midX, midY, text = mode.twoDList[col][row], font = "Arial 20")
                
        elif mode.numOfVar == 4:
            #the graph will be 5 * 5
            mode.kRows = 5
            mode.kCols = 5

            #Create a two list: from https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#creating2dLists
            mode.twoDList = [([] * mode.kCols) for row in range(mode.kRows)]
            mode.twoDList = [[None, "A'B'", "A'B", "AB", "AB'"],
                             ["C'D'", None, None, None, None],
                             ["C'D", None, None, None, None],
                             ["CD", None, None, None, None],
                             ["CD'", None, None, None, None]]

            #Whereas mode.dictQVal has {(row,col): output value}

            for vars in mode.dictQVal:
                first = vars[0]
                second = vars[1]    
                third = vars[2]
                fourth = vars[3]
                if first == 0:
                    first = "A'"
                elif first == 1:
                    first = "A"
                if second == 0:
                    second = "B'"
                elif second == 1:
                    second = "B"
                if third == 0:
                    third = "C'"
                elif third == 1:
                    third = "C"
                if fourth == 0:
                    fourth = "D'"
                elif fourth == 1:
                    fourth = "D"
                result = first+second+third+fourth
                mode.dictTotalVals[result] = mode.dictQVal[vars]
            mode.qValTable()

            for row in range(mode.kRows):
                for col in range(mode.kCols):
                    if (row, col) in mode.setOfBoxes:
                        color = mode.currColor
                    else:
                        color = "White"
                    margX = (mode.kBottomX - mode.kTopX) // (mode.numOfVar + 1)
                    margY = (mode.kBottomY - mode.kTopY) // (mode.numOfVar + 1)
                    canvas.create_rectangle(mode.kTopX + row*margX, mode.kTopY + col*margY, 
                                            mode.kTopX + (row+1)*margX, mode.kTopY + (col+1)*margY, fill = color)
        

                    if mode.twoDList != None:
                        midX = (mode.kTopX + row*margX + mode.kTopX + (row+1)*margX)//2
                        midY = (mode.kTopY + col*margY + mode.kTopY + (col+1)*margY)//2 
                        canvas.create_text(midX, midY, text = mode.twoDList[col][row], font = "Arial 25")

                    if mode.status == True:
                        if mode.twoDList[col][row] == "0":   
                            canvas.create_text(midX, midY, text = mode.twoDList[col][row], font = "Arial 25", fill = "grey")
                        elif mode.twoDList[col][row] == "1":
                            canvas.create_text(midX, midY, text = mode.twoDList[col][row], font = "Arial 25")
                    elif mode.status == False:
                        if mode.twoDList[col][row] == "1":   
                            canvas.create_text(midX, midY, text = mode.twoDList[col][row], font = "Arial 25", fill = "grey")
                        elif mode.twoDList[col][row] == "0":
                            canvas.create_text(midX, midY, text = mode.twoDList[col][row], font = "Arial 25")

            #mode.dictTotalVals is a dictionary that has {A'B'C'D': 1 or 0 or X}

    #This method will finalize defining mode.twoDList[row][col]
    def qValTable(mode):
        #self.twoDList
        for row in range(mode.kRows):
            for col in range(mode.kCols):
                if row > 0 and col > 0:
                    vars1 = mode.twoDList[col][0] #mode.twoDList[][] includes input signals in alphabet
                    #Ex) 2 input would be like A' A and B' B
                    vars2 = mode.twoDList[0][row] 
                    result =  vars2 + vars1
                    qVal = mode.dictTotalVals[result] #find the q value in there!
                    #Error: Exception: "A'B'" because mode.dictTotalVals is empty!!!
                    mode.twoDList[col][row] = qVal

    def touchingBox(mode, x, y):
        #as long as the mouse is touching the rectangular box:
        for row in range(mode.kRows):
            for col in range(mode.kCols):
                #↓ for down arrow & → for right arrow
                if mode.numOfVar == 2:
                    margX = (mode.kBottomX - mode.kTopX) // (mode.numOfVar + 1)
                    margY = (mode.kBottomY - mode.kTopY) // (mode.numOfVar + 1)
                
                elif mode.numOfVar == 3:
                    margX = (mode.kBottomX - mode.kTopX) // (mode.numOfVar + 2)
                    margY = (mode.kBottomY - mode.kTopY) // (mode.numOfVar)

                elif mode.numOfVar == 4:
                    margX = (mode.kBottomX - mode.kTopX) // (mode.numOfVar + 1)
                    margY = (mode.kBottomY - mode.kTopY) // (mode.numOfVar + 1)
                
                if mode.kTopX + row*margX <= x <= mode.kTopX + (row+1)*margX:
                    if mode.kTopY + col*margY <= y <= mode.kTopY + (col+1)*margY:
                        return True
    
    def rowAndCol(mode, x, y):
        #print(f"printing mode.numOfVar = {mode.numOfVar}")
        if mode.numOfVar == 2:
            margX = (mode.kBottomX - mode.kTopX) // (mode.numOfVar + 1)
            margY = (mode.kBottomY - mode.kTopY) // (mode.numOfVar + 1)
        
        elif mode.numOfVar == 3:
            margX = (mode.kBottomX - mode.kTopX) // (mode.numOfVar + 2)
            margY = (mode.kBottomY - mode.kTopY) // (mode.numOfVar)

        elif mode.numOfVar == 4:
            margX = (mode.kBottomX - mode.kTopX) // (mode.numOfVar + 1)
            margY = (mode.kBottomY - mode.kTopY) // (mode.numOfVar + 1)
        
        for row in range(mode.kRows):
            for col in range(mode.kCols):
                if mode.kTopX + row*margX <= x <= mode.kTopX + (row+1)*margX:
                    if mode.kTopY + col*margY <= y <= mode.kTopY + (col+1)*margY:
                        return (row, col)

        '''
        mode.kTopX + row*margX, mode.kTopY + col*margY, 
                                            mode.kTopX + (row+1)*margX, mode.kTopY + (col+1)*margY
        '''
        
class DoneButton(App):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def drawDoneButton(self, canvas):
        margin = 25
        sizeX = 150
        sizeY = 50
        topX = self.width//2 - 2*margin - sizeX
        topY = self.height - margin - sizeY
        bottomX = self.width//2 - 2*margin
        bottomY = self.height - margin
        canvas.create_rectangle(topX, topY, bottomX, bottomY, fill = "light blue")
        canvas.create_text(topX + (bottomX - topX)//2, topY + sizeY//2, text = "DONE", fill = "black", font = "Arial 25")

    def pressingDone(self, x, y):
        margin = 25
        sizeX = 150
        sizeY = 50
        topX = self.width//2 - 2*margin - sizeX
        topY = self.height - margin - sizeY
        bottomX = self.width//2 - 2*margin
        bottomY = self.height - margin
        if topX <= x <= bottomX: 
            #print("It's within the X boundary")
            if topY <= y <= bottomY:
                #print("Done button is pressed!")
                return True

class LogicEquation(App):
    def __init__ (self, width, height):
        self.width = width
        self.height = height
        self.margin = 50
        self.buttonWidth = 80
        self.size = 100 
        self.bottomX = self.width - self.margin*2 - self.size #X = 1300
        self.buttonMarg = 100

        self.sopTopX = self.bottomX + self.margin
        self.sopTopY = self.buttonMarg
        self.sopBotX = self.sopTopX + self.size
        self.sopBotY = self.buttonWidth + self.sopTopY

        self.posTopX = self.sopTopX
        self.posTopY = self.sopBotY + self.buttonWidth//2
        self.posBotX = self.sopBotX
        self.posBotY = self.posTopY + self.buttonWidth

    def drawAll(self, canvas):
        #SOP or POS button:
        #SOP
        canvas.create_rectangle(self.sopTopX, self.sopTopY, self.sopBotX, self.sopBotY, fill = "light pink")
        canvas.create_text((self.sopTopX + self.sopBotX)//2, (self.sopTopY + self.sopBotY)//2, text = "SOP", font = "Arial 30")
        #POS
        canvas.create_rectangle(self.posTopX, self.posTopY, self.posBotX, self.posBotY, fill = "light green")
        canvas.create_text((self.posTopX + self.posBotX)//2, (self.posTopY + self.posBotY)//2, text = "POS", font = "Arial 30")

    def pressingSOP(self, x, y):
        if self.sopTopX <= x <= self.sopBotX:
            if self.sopTopY <= y <= self.sopBotY:
                return True
                #This should make all 0's grey
    
    def pressingPOS(self, x, y):
        if self.posTopX <= x <= self.posBotX:
            if self.posTopY <= y <= self.posBotY:
                return True
                #This should make all 1's grey
    

class HelpMode(Mode):
    def appStarted(mode):
        #instruction Mode
        mode.doneButton = HelpDone(mode.width, mode.height)
        #Add instructions:
        mode.start = 60
        mode.margin = 50
        mode.listOfInstructions = ["When you are typing Q values on the truth table, use O for 1 and Z for 0 and X for x",
                                    "SOP is only consisted of 1's"
                                    "Currently POS is not implemented"]
    
    def mousePressed(mode, event):
        if mode.doneButton.buttonTouching(event.x, event.y):
            mode.app.setActiveMode(mode.app.startScreenMode)        
            #mode.app.setActiveMode(mode.app.helpMode)

    def redrawAll(mode, canvas):
        mode.doneButton.drawButton(canvas)
        #Just instructions from here:
        canvas.create_text(mode.width//2, mode.start, text = "INSTRUCTION", font = "Arial 40")
        for i in range(len(mode.listOfInstructions)):
            canvas.create_text(mode.width//2, mode.start + mode.margin*(i + 1), text = mode.listOfInstructions[i], font = "Arial 25")

class HelpDone(App):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.marg = 25
        self.sizeX = 100
        self.sizeY = 50
        self.topX = self.width - self.marg - self.sizeX
        self.topY = self.height - self.marg - self.sizeY
        self.botX = self.width - self.marg
        self.botY = self.height - self.marg

    def drawButton(self, canvas):
        #print("button is being drawn")
        canvas.create_rectangle(self.topX, self.topY, self.botX, self.botY, fill = "light blue")
        canvas.create_text((self.topX + self.botX)//2, (self.topY + self.botY)//2, text = "BACK", font = "Arial 25")
    
    def buttonTouching(self, x, y):
        if self.topX <= x <= self.botX:
            if self.topY <= y <= self.botY:
                return True

class Solution(Mode):
    def appStarted(mode):
        mode.status = mode.app.status
        mode.equation = mode.app.finalEquation
        mode.solutionSimple = False
        mode.solutionStep = False
        mode.output = mode.writeOutPut()
        mode.status = mode.app.status
        mode.drawingApp = DrawingGates(mode.width, mode.height, mode.output, mode.equation, mode.status)
        mode.turn = 0

    def mousePressed(mode, event):
        print(f"mousePressed: {event.x, event.y}")
        if mode.pressingBack(event.x, event.y):
            #mode.app.setActiveMode(mode.app.startScreenMode)
            mode.app.setActiveMode(mode.app.truthTable)
        if mode.pressingSimple(event.x, event.y):
            print("Simple Solution Option is selected")
            mode.solutionSimple = True
        elif mode.pressingStep(event.x, event.y):
            print("Step Solution Option is selected")
            mode.solutionStep = True

    def keyPressed(mode, event):
        if event.key == "Left":
            if mode.turn > 0:
                mode.turn -= 1
        elif event.key == "Right":
            mode.turn += 1


    def redrawAll(mode, canvas):
        mode.backButton(canvas)
        mode.simpleSolution(canvas)
        mode.stepSolution(canvas)
        mode.drawOutPut(canvas)

        if mode.solutionSimple == True:
            mode.drawingApp.drawingSimpleSolution(canvas)
        elif mode.solutionStep == True:
            mode.drawingApp.drawingStepSolution(canvas, mode.turn)


    #color citation: http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
    def backButton(mode, canvas):
        margin = 25
        sizeX = 100
        sizeY = 75
        topX = margin #25 
        topY = margin #25
        botX = topX + sizeX #125
        botY = topY + sizeY #100
        canvas.create_rectangle(topX, topY, botX, botY, fill = "steel blue")
        canvas.create_text((topX + botX)//2, (topY + botY)//2, text = "BACK", font = "Arial 25")

    def pressingSimple(mode, x, y):
        margin = 25
        sizeX = 400
        sizeY = 75
        totalWidth = mode.width - 150 
        topX = 350 + totalWidth//4 - sizeX 
        topY = margin 
        botX = topX + sizeX 
        botY = margin + sizeY
        print(f"x range: {topX, botX}")
        print(f"y range: {topY, botY}")
        if topX <= x <= botX:
            if topY <= y <= botY:
                return True

    def pressingStep(mode, x, y):
        margin = 25
        sizeX = 200
        sizeY = 75
        totalWidth = mode.width - 150 
        topX = 150 + totalWidth*(3/4) - sizeX
        topY = margin
        botX = topX + sizeX
        botY = margin + sizeY
        if topX <= x <= botX:
            if topY <= y <= botY:
                return True        

    def pressingBack(mode, x, y):
        margin = 25
        sizeX = 100
        sizeY = 75
        topX = margin #25 
        topY = margin #25
        botX = topX + sizeX #125
        botY = topY + sizeY #100
        if topX <= x <= botX:
            if topY <= y <= botY:
                return True

    #color citation: http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
    def simpleSolution(mode, canvas):
        margin = 25
        sizeX = 400
        sizeY = 75
        totalWidth = mode.width - 150 
        topX = 350 + totalWidth//4 - sizeX 
        topY = margin 
        botX = topX + sizeX 
        botY = margin + sizeY
        canvas.create_rectangle(topX, topY, botX, botY, fill = "turquoise")
        canvas.create_text((topX + botX)//2, (topY + botY)//2, text = "SIMPLE SOLUTION", font = "Arial 25")
        canvas.create_line(0, botY + margin, mode.width, botY + margin)

    def writeOutPut(mode):
        result = ""
        for var in mode.equation:
            #print(f"printing var = {var}")
            result = result + var + " "
        return result 

    def drawOutPut(mode, canvas):
        margin = 150
        yLine = mode.height - margin
        margin = 25
        #marginX = 100
        #yLine = 650
        canvas.create_line(0, yLine, mode.width, yLine)
        canvas.create_text(mode.width//2, yLine + 100, text = f"OUTPUT = {mode.output}", font = "Arial 25")
    
    #color citation: http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
    def stepSolution(mode, canvas):
        margin = 25
        sizeX = 300
        sizeY = 75
        totalWidth = mode.width - 150 
        topX = 150 + totalWidth*(3/4) - sizeX
        topY = margin
        botX = topX + sizeX
        botY = margin + sizeY
        canvas.create_rectangle(topX, topY, botX, botY, fill = "pale violet red")
        canvas.create_text((topX + botX)//2, (topY + botY)//2, text = "STEP BY STEP", font = "Arial 25")

class DrawingGates(App):
    def __init__ (self, width, height, equation, equationList, status):
        self.width = width
        self.height = height
        self.side = 150
        self.equation = equation
        self.equationList = equationList
        self.status = status
        self.inputs = self.findingInputs()
        self.squareX = 75
        self.inputX = 50
        self.squareY = 50
        self.numOfInputs = len(self.inputs)
        self.stepInstructions = list()
        self.groups = self.findFirstGroups()
        self.gates = dict()
        self.endGate = list()
        self.singleGroup = list()
        self.sizeAdjust = False
        self.lastGate = list()

    def findingInputs(self):
        print(f"self.equationList --> {self.equationList}")
        setOfOperators = ["+", "*"]
        inputList = []
        for var in self.equationList:
            print(f"var --> {var}")
            if var not in setOfOperators:
                if var not in inputList:
                    inputList.append(var)
        return inputList

    def inputDrawing(self, canvas):
        #draw all the inputs at X = 100
        realH = self.height - 2*self.side
        margin = (realH - self.numOfInputs*self.squareY) // (self.numOfInputs + 1)
        if margin <= self.squareY:
            self.squareY //= 2
            self.squareX //= 2
            self.sizeAdjust = True
        margin = (realH - self.numOfInputs*self.squareY) // (self.numOfInputs + 1)
        
        #color citation: http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
        for i in range(len(self.inputs)):
            #X = 100
            currInput = self.inputs[i]
            topX = 100 #always 100
            #topY starts at Y = 150 + margin 
            topY = self.side + margin*(i + 1)
            botX = topX + self.inputX
            botY = topY + self.squareY
            #ALL INPUTS ARE Dark Sea Green1
            canvas.create_rectangle(topX, topY, botX, botY, fill = "Dark Sea Green1")
            canvas.create_text((topX + botX)//2, (topY + botY)//2, text = currInput, font = "Arial 15")
            instruction = ("Rectangle", topX, topY, botX, botY, currInput) 
            self.stepInstructions.append(instruction)
            gateInst = (topX, topY, botX, botY)
            self.gates[currInput] = gateInst

    def findFirstGroups(self):
        newList = []
        if self.status == True:
            newList += self.equation.split("+") #this will give a good understanding of which input needs to added
        elif self.status == False:
            newList += self.equation.split("*")

        print(f"newList = > {newList}")
        return newList

    def combineFirstGroups(self, canvas):
        combinedGroups = []
        self.singleGroup = []
        #loop through self.groups:
        for var in self.groups:
            if self.status == True: #then look for *
                operator = "*"
                if operator in var:
                    var = var.split(" * ")
                    if var not in combinedGroups:
                        combinedGroups += var
                else:
                    self.singleGroup.append(var)

            elif self.status == False: #then look for +
                operator = "+"
                if operator in var:
                    var = var.split(" + ")
                    if var not in combinedGroups:
                        combinedGroups += var
                else:
                    self.singleGroup.append(var)
        #print(f"combinedGroups ==> {combinedGroups}")
        #print(f"self.singleGroup ==> {self.singleGroup}")
        locationList = []
        for pair in combinedGroups:
            newPair = pair.strip(" ")
            #print(f"newPair --> {newPair}")
            location = self.gates[newPair]
            locationList.append(location)

        #create a GATE:
        distance = 100
        for loc in range(len(locationList) - 1):
            loc1 = locationList[loc]
            loc2 = locationList[loc + 1]
            if self.status == True: #create AND gate:
                gateName = "AND"

            elif self.status == False:
                gateName = "OR"

            yVal = (loc1[1] + loc2[3])//2 #centerX
            xVal = loc1[2] + distance #centerY

            topX = xVal - self.squareX//2 
            topY = yVal - self.squareY//2
            botX = xVal + self.squareX//2
            botY = yVal + self.squareY//2
            if self.sizeAdjust == False:
                topX = xVal - self.squareX//4 
                topY = yVal - self.squareY//4
                botX = xVal + self.squareX//4
                botY = yVal + self.squareY//4

            #color citation: http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
            canvas.create_rectangle(topX, topY, botX, botY, fill = "light sea green")
            canvas.create_text((topX + botX)//2, (topY + botY)//2, text = gateName)
            instruction = ("Rectangle", topX, topY, botX, botY, gateName) 
            self.stepInstructions.append(instruction)
            finalLoc = (topX, topY, botX, botY)
            self.endGate.append(finalLoc)

            #now on to lines:
            #firstLine to the gate:
            nTopX = loc1[2]
            nTopY = (loc1[1] + loc1[3])//2
            nBotX = topX
            nBotY = yVal
            canvas.create_line(nTopX, nTopY, nBotX, nBotY)
            instruction = ("Line", nTopX, nTopY, nBotX, nBotY)
            self.stepInstructions.append(instruction)
            #secondLine to the gate:
            nTopX = loc2[2]
            nTopY = (loc2[1] + loc2[3])//2
            nBotX = topX
            nBotY = yVal
            canvas.create_line(nTopX, nTopY, nBotX, nBotY)
            instruction = ("Line", nTopX, nTopY, nBotX, nBotY)
            self.stepInstructions.append(instruction)

        if len(self.singleGroup) == len(self.groups):
            print("ONLY SINGLE VARS!")

    def connectEndGate(self, canvas):
        margin = 100
        if self.status == True: #OR gate
            gateName = "OR"
        elif self.status == False:
            gateName = "AND"
        
        if len(self.endGate) == 0: #meaning there's no combined gates:
            if len(self.singleGroup) == 1:
                gate = self.singleGroup[0]
                gate = gate.strip(" ")
                self.lastGate = self.gates[gate]
                return 

            elif len(self.singleGroup) > 1:
                first = self.singleGroup[0]
                first = first.strip(" ")
                firstLoc = self.gates[first]
                lastVar = self.singleGroup[-1]
                lastVar = lastVar.strip(" ")
                lastLoc = self.gates[lastVar]

        else:
            firstLoc = self.endGate[0]
            if len(self.singleGroup) >= 1:
                lastVar = self.singleGroup[-1]
                lastVar = lastVar.strip(" ")
                print(f"lastVar = {lastVar}")
                lastLoc = self.gates[lastVar]
            else:
                lastLoc = self.endGate[-1]

        xVal = firstLoc[2] + margin
        yVal = (firstLoc[1] + lastLoc[3])//2

        topX = xVal - self.squareX//2 
        topY = yVal - self.squareY//2
        botX = xVal + self.squareX//2
        botY = yVal + self.squareY//2
            
        #color citation: http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
        canvas.create_rectangle(topX, topY, botX, botY, fill = "cornflower blue")
        canvas.create_text((topX + botX)//2, (topY + botY)//2, text = gateName)
        instruction = ("Rectangle", topX, topY, botX, botY, gateName)
        self.stepInstructions.append(instruction)
        self.lastGate = (topX, topY, botX, botY)
        
        #now comes the lines:
        if len(self.singleGroup) > 0:
            for var in self.singleGroup:
                #print(f"var in self.singleGroup = {var}")
                var = var.strip(" ")
                location = self.gates[var]
                topX = location[2]
                topY = (location[1] + location[3])//2
                botX = xVal - self.squareX//2
                botY = ((yVal - self.squareY//2) + (yVal + self.squareX//2))//2
                canvas.create_line(topX, topY, botX, botY)
                instruction = ("Line", topX, topY, botX, botY)
                self.stepInstructions.append(instruction)
        
        for var in self.endGate:
            #print(f"var in self.endGate = {var}")
            location = var
            topX = location[2]
            topY = (location[1] + location[3])//2
            botX = xVal - self.squareX//2
            botY = yVal
            canvas.create_line(topX, topY, botX, botY)
            instruction = ("Line", topX, topY, botX, botY)
            self.stepInstructions.append(instruction)

    def lastOutput(self, canvas):
        end = 150
        topX = self.lastGate[2]
        topY = (self.lastGate[1] + self.lastGate[3])//2
        botX = self.width - end
        botY = (self.lastGate[1] + self.lastGate[3])//2
        canvas.create_line(topX, topY, botX, botY, width = 5, fill = "red")

    def drawingSimpleSolution(self, canvas):
        self.inputDrawing(canvas)
        self.combineFirstGroups(canvas)
        self.connectEndGate(canvas)
        self.lastOutput(canvas)

    def drawingStepSolution(self, canvas, turn):
        self.drawingSimpleSolution(canvas)
        #draw a one big white screen:
        side = 150
        topX = 0 
        topY = side
        botX = self.width
        botY = self.height - side
        canvas.create_rectangle(topX, topY, botX, botY, fill = "white")
        
        if turn >= len(self.stepInstructions):
            turn = len(self.stepInstructions) - 1
            print("THIS IS THE END!!!")

        step = self.stepInstructions[turn]
        topX = step[1]
        topY = step[2]
        botX = step[3]
        botY = step[4]
        if step[0] == "Rectangle":
            nameGate = step[-1]
            canvas.create_rectangle(topX, topY, botX, botY, fill = "cornflower blue")
            #color citation: http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
            canvas.create_text((topX + botX)//2, (topY + botY)//2, text = nameGate)

        elif step[0] == "Line":
            canvas.create_line(topX, topY, botX, botY)

class DrawingPad(Mode):
    def appStarted(mode):
        mode.start = True
        mode.squareX = 70
        mode.squareY = 70
        mode.marginX = 35
        mode.marginY = 50//4
        mode.gateSize = 100
        mode.currGate = None
        mode.canDraw = True
        mode.canConnect = True
        mode.gateX = 0
        mode.gateY = 0
        mode.color = None
        mode.locX = 0
        mode.locY = 0
        mode.sLocX = 0
        mode.sLocY = 0
        mode.lines = list()
        mode.gates = list()
        mode.currLoc = tuple()
        mode.gate1 = ()
        mode.gate2 = ()
        mode.gateList = list()
        mode.inputList = mode.gettingInputs()            
        #{(x1, y1, x2, y2): NAND, ...}
        mode.drawingLine = False
        mode.drawingGate = False
        
    def drawingGates(mode, canvas):
        #print("drawingGates is called")
        if mode.canDraw == True:
            #print("canDraw is True")
            #drawGates
            for gate in mode.gates:
                print
                topX = gate[0]
                topY = gate[1]
                botX = gate[2]
                botY = gate[3]
                gateName = gate[4]
                canvas.create_rectangle(topX, topY, botX, botY, fill = mode.color)
                canvas.create_text((topX + botX)//2, (topY + botY)//2, text = gateName)
    
    def redrawAll(mode, canvas):
        mode.backButton(canvas)
        mode.resetButton(canvas)
        mode.drawAndGates(canvas)
        mode.drawNandGates(canvas)
        mode.drawNorGates(canvas)
        mode.drawOrGates(canvas)
        mode.drawLine(canvas)
        mode.drawingGates(canvas)
        mode.drawingInputs(canvas)
        if mode.canConnect == True:
            #mode.connectLine(canvas)
            for line in mode.lines:
                topX = line[0]
                topY = line[1]
                botX = line[2]
                botY = line[3]
                canvas.create_line(topX, topY, botX, botY)

    def gettingInputs(mode):
        inputs = mode.app.finalEquationList
        print(f"equationList --> {inputs}")
        setOfOperators = ["+", "*"]
        listOfInputs = []
        for ind in range(len(inputs)):
            var = inputs[ind]
            print(f"var --> {var}")
            if var not in setOfOperators:
                listOfInputs.append(var)
        return listOfInputs

    def drawingInputs(mode, canvas):
        margin = 50
        realH = mode.height - 2*margin
        moreY = realH - (len(mode.inputList)*mode.squareY//2)
        if len(mode.inputList) == 1:
            marginY = moreY // (len(mode.inputList))
        else:
            marginY = moreY // (len(mode.inputList) - 1)
        for i in range(len(mode.inputList)):
            inputVar = mode.inputList[i]
            topX = margin
            topY = margin + i*(mode.squareY//2) + marginY*i
            botX = margin + mode.squareX//2
            botY = topY + mode.squareY//2
            pair = (topX, topY, botX, botY, inputVar)
            mode.gates.append(pair)
            canvas.create_rectangle(topX, topY, botX, botY, fill = "steel blue")
            #color citation: http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
            canvas.create_text((topX + botX)//2, (topY + botY)//2, text = inputVar)

    def mousePressed(mode, event):
        if mode.pressingNand(event.x, event.y):
            mode.currGate = "NAND"
            mode.drawingLine = False
            #mode.drawingLine = False
            #mode.drawingGate = False
        elif mode.pressingAnd(event.x, event.y):
            mode.currGate = "AND"
            mode.drawingLine = False
        elif mode.pressingNor(event.x, event.y):
            mode.currGate = "NOR"
            mode.drawingLine = False
        elif mode.pressingOr(event.x, event.y):
            mode.currGate = "OR"
            mode.drawingLine = False
        #print(f"mode.currGate = {mode.currGate}")
        
        if mode.pressingLine(event.x, event.y):
            mode.drawingLine = True
            if event.x <= mode.width - 300:
                mode.locX = event.x
                mode.locY = event.y

        if mode.pressingBack(event.x, event.y):
            mode.app.setActiveMode(mode.app.truthTable)
        
        if mode.pressingReset(event.x, event.y):
            mode.gates = []
            mode.lines = []
            mode.currGate = []

        if mode.drawingLine == True: #now we can select the box!
            if mode.isGate(event.x, event.y):
                gateLoc = mode.gateLocation(event.x, event.y)
                mode.gateList.append(gateLoc) #gateLoc = tuple()
                if len(mode.gateList) == 2:
                    #compareGates:
                    location1 = mode.gateList[0]
                    location2 = mode.gateList[1]
                    print(f"printing location1 = {location1} , location 2 = {location2}")
                    if location1[0] > location2[0]: #if location1's topX is greater than location2's topX,
                        mode.gate1 = (location1[0], (location1[1] + location1[3])//2)
                        mode.gate2 = (location2[2], (location2[1] + location2[3])//2)
                        pair = (location1[0], (location1[1] + location1[3])//2, location2[2], (location2[1] + location2[3])//2)
                    else:
                        mode.gate1 = (location2[0], (location2[1] + location2[3])//2)
                        mode.gate2 = (location1[2], (location1[1] + location1[3])//2)
                        pair = (location2[0], (location2[1] + location2[3])//2, location1[2], (location1[1] + location1[3])//2)
                    mode.gateList = [] #empties the list for mode.gateList
                    mode.lines.append(pair)

        if mode.drawingBoard(event.x, event.y):
            if mode.drawingLine == False:
                mode.drawingGate = True
                #as long as as it is not on the box:
                if event.x <= mode.width - 300:
                    mode.gateX = event.x
                    mode.gateY = event.y
                mode.drawGates()
        #else:
        #    mode.canDraw = False

    def isGate(mode, x, y):
        for gate in mode.gates:
            #gate = (topX, topY, botX, botY, gateName)
            topX = gate[0]
            topY = gate[1]
            botX = gate[2]
            botY = gate[3]
            if topX <= x <= botX:
                if topY <= y <= botY:
                    return True
    
    def gateLocation(mode, x, y):
        for gate in mode.gates:
            #gate = (topX, topY, botX, botY, gateName)
            topX = gate[0]
            topY = gate[1]
            botX = gate[2]
            botY = gate[3]
            if topX <= x <= botX:
                if topY <= y <= botY:
                    return gate[:-1]


    def drawGates(mode):
        topX = mode.gateX - mode.squareX//2
        topY = mode.gateY - mode.squareY//2
        botX = mode.gateX + mode.squareX//2
        botY = mode.gateY + mode.squareX//2
        gate = mode.currGate
        option = (topX, topY, botX, botY, gate)
        mode.gates.append(option)
       
    def distance(mode, x1, y1, x2, y2):
        return ((x2 - x1)**2 - (y2 - y1)**2)**(0.5) 

    def drawingBoard(mode, x, y):
        size = 300
        topX = 0
        topY = 0 
        botX = mode.width - size
        botY = mode.height
        if topX <= x <= botX:
            if topY <= y <= botY:
                return True

    def keyPressed(mode, event):
        if event.key == "d":
            if len(mode.gates) > len(mode.inputList):
                mode.gates.pop() #popping the list

        elif event.key == "l":
            if mode.lines != []:
                mode.lines.pop() #popping the list

    def drawNandGates(mode, canvas):
        ogTopY = 100
        size = 300
        margin = 25
        topX = mode.width - size + mode.marginX 
        topY = ogTopY + margin
        botX = mode.width - mode.marginX
        botY = topY + mode.gateSize 
        # (1235, 125, 1465, 225)
        canvas.create_rectangle(topX, topY, botX, botY, fill = "light slate blue")
        #color citation: http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
        mode.color = "light slate blue"
        canvas.create_text((topX + botX)//2, (topY + botY)//2, text = "NAND", font = "Arial 25")

    def pressingNand(mode, x, y):
        ogTopY = 100
        size = 300
        margin = 25
        topX = mode.width - size + mode.marginX 
        topY = ogTopY + margin
        botX = mode.width - mode.marginX
        botY = topY + mode.gateSize
        if topX <= x <= botX:
            if topY <= y <= botY:
                return True

    def drawAndGates(mode, canvas):
        ogTopY = 225
        size = 300
        margin = 25
        topX = mode.width - size + mode.marginX 
        topY = ogTopY + mode.marginY
        botX = mode.width - mode.marginX
        botY = topY + mode.gateSize 
        # (1465, 237, 1465, 337)
        canvas.create_rectangle(topX, topY, botX, botY, fill = "dark khaki")
        #color citation: http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
        mode.color = "dark khaki"
        canvas.create_text((topX + botX)//2, (topY + botY)//2, text = "AND", font = "Arial 25")
    
    def pressingAnd(mode, x, y):
        ogTopY = 225
        size = 300
        margin = 25
        topX = mode.width - size + mode.marginX 
        topY = ogTopY + mode.marginY
        botX = mode.width - mode.marginX
        botY = topY + mode.gateSize 
        # (1465, 237, 1465, 337)
        if topX <= x <= botX:
            if topY <= y <= botY:
                return True

    def drawNorGates(mode, canvas):
        ogTopY = 337
        size = 300
        topX = mode.width - size + mode.marginX 
        topY = ogTopY + mode.marginY
        botX = mode.width - mode.marginX
        botY = topY + mode.gateSize 
        # (1465, 349, 1465, 449)
        canvas.create_rectangle(topX, topY, botX, botY, fill = "medium purple")
        #color citation: http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
        mode.color = "medium purple"
        canvas.create_text((topX + botX)//2, (topY + botY)//2, text = "NOR", font = "Arial 25")

    def pressingNor(mode, x, y):
        ogTopY = 337
        size = 300
        topX = mode.width - size + mode.marginX 
        topY = ogTopY + mode.marginY
        botX = mode.width - mode.marginX
        botY = topY + mode.gateSize 
        # (1465, 349, 1465, 449)
        if topX <= x <= botX:
            if topY <= y <= botY:
                return True

    def drawOrGates(mode, canvas):
        ogTopY = 449
        size = 300
        topX = mode.width - size + mode.marginX 
        topY = ogTopY + mode.marginY
        botX = mode.width - mode.marginX
        botY = topY + mode.gateSize 
        # (1465, 461, 1465, 573)
        canvas.create_rectangle(topX, topY, botX, botY, fill = "MistyRose3")
        #color citation: http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
        mode.color = "MistyRose3"
        canvas.create_text((topX + botX)//2, (topY + botY)//2, text = "OR", font = "Arial 25")

    def pressingOr(mode, x, y):
        ogTopY = 449
        size = 300
        topX = mode.width - size + mode.marginX 
        topY = ogTopY + mode.marginY
        botX = mode.width - mode.marginX
        botY = topY + mode.gateSize 
        if topX <= x <= botX:
            if topY <= y <= botY:
                return True

    def drawLine(mode, canvas):
        ogTopY = 573
        size = 300
        topX = mode.width - size + mode.marginX 
        topY = ogTopY + mode.marginY
        botX = mode.width - mode.marginX
        botY = topY + mode.gateSize 
        # (1465, 585, 1465, 685)
        canvas.create_rectangle(topX, topY, botX, botY, fill = "LightSteelBlue1")
        #color citation: http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
        canvas.create_text((topX + botX)//2, (topY + botY)//2, text = "LINE", font = "Arial 25")

    def pressingLine(mode, x, y):
        ogTopY = 573
        size = 300
        topX = mode.width - size + mode.marginX 
        topY = ogTopY + mode.marginY
        botX = mode.width - mode.marginX
        botY = topY + mode.gateSize 
        if topX <= x <= botX:
            if topY <= y <= botY:
                mode.canConnect = True
                return True

    def backButton(mode, canvas):
        #Y = 1500-300 = 1200
        sizeX = 300
        sizeY = 75
        margin = 25
        topX = mode.width - sizeX #1200
        topY = margin #25
        botX = mode.width - margin #1475
        botY = margin + sizeY #100
        canvas.create_rectangle(topX, topY, botX, botY, fill = "gold")
        canvas.create_text((topX + botX)//2, (topY + botY)//2, text = "BACK", font = "Arial 25")
        
    def pressingBack(mode, x, y):
        sizeX = 300
        sizeY = 75
        margin = 25
        topX = mode.width - sizeX #1200
        topY = margin #25
        botX = mode.width - margin #1475
        botY = margin + sizeY #100
        if topX <= x <= botX:
            if topY <= y <= botY:
                return True

    def resetButton(mode, canvas):
        sizeX = 300
        sizeY = 75
        margin = 25
        topX = mode.width - sizeX #1200
        topY = mode.height - margin - sizeY #700
        botX = mode.width - margin #1475
        botY = mode.height - margin #775
        canvas.create_rectangle(topX, topY, botX, botY, fill = "steel blue")
        #color citation: http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
        canvas.create_text((topX + botX)//2, (topY + botY)//2, text = "RESET" , font = "Arial 25")

    def pressingReset(mode, x, y):
        sizeX = 300
        sizeY = 75
        margin = 25
        topX = mode.width - sizeX #1200
        topY = mode.height - margin - sizeY #700
        botX = mode.width - margin #1475
        botY = mode.height - margin #775
        if topX <= x <= botX:
            if topY <= y <= botY:
                return True

class MyModalApp(ModalApp):
    def appStarted(app):
        #app.startScreenMode will ask the user to input how many variables there are,
        #and direct to the app.truthTable
        app.startScreenMode = StartScreenMode()
        #app.truthTable will map out the table for the user to put in the variable
        #logics
        app.finalNum = 0
        #app.dictOfQvalues is a dictionary of A, B, C, D
        app.dictOfQValues = dict()
        app.truthTable = TruthTable()
        #app.drawingTruthTable = DrawTruthTable()
        app.rows = 0
        app.cols = 0
        app.dictVal = dict()
        app.finalEquation = list()
        app.finalEquationList = list()
        app.status = None
        app.drawingPad = DrawingPad()
        app.solutionMode = Solution()
        app.helpMode = HelpMode()
        app.setActiveMode(app.startScreenMode)
        print("Started")
        app.timerDelay = 10

#size of my computer's full screen
#width = 1531 and height = 801

app = MyModalApp(width=1500, height=800)
