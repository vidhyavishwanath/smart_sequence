'''
 attribution for state image -
 “State Outlines: Blank Maps of the 50 United States.” GIS Geography, 26 Apr. 2020, https://gisgeography.com/state-outlines-blank-maps-united-states/.

 attribution for european country images -
   GISGeography. “Blank Map of Europe with Country Outlines.” GIS Geography, 23 Dec. 2023, https://gisgeography.com/europe-blank-map-country-outlines/.

 attribution for the map of georgia (country) -
“Map of Georgia (Europe).” GIS Geography, 4 July 2021, https://gisgeography.com/georgia-europe-map/.

board game image on the intro screen - "Photo by Robert Coelho on Unsplash"

All the rest of the images I created on Canva

'''

from cmu_graphics import *
import copy
import random
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from striprtf.striprtf import rtf_to_text
from card import Card
from player import Player
from game import Game
from drive import getUserContent, getImagesList


def onAppStart(app):
    app.player1 = Player(1, ['images/1.png', 'images/2.png', 'images/3.png', 'images/4.png', 'images/5.png'])
    app.player2 = Player(2, ['images/player2/1.png', 'images/player2/2.png', 'images/player2/3.png', 'images/player2/4.png', 'images/player2/5.png'])
    app.currentGame = None
    app.width = 1000
    app.height = 1000
    app.states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
    app.stateCapitals = ['Montgomery', 'Juneau', 'Phoenix', 'Little Rock', 'Sacramento', 'Denver', 'Hartford', 'Dover', 'Tallahassee', 'Atlanta', 'Honolulu',
'Boise', 'Springfield', 'Indianapolis', 'Des Moines', 'Topeka', 'Frankfort', 'Baton Rouge', 'Augusta', 'Annapolis', 'Boston', 'Lansing', 'Saint Paul', 'Jackson',
'Jefferson City', 'Helena', 'Lincoln', 'Carson City', 'Concord', 'Trenton', 'Santa Fe', 'Albany', 'Raleigh', 'Bismarck', 'Columbus', 'Oklahoma City',
'Salem', 'Harrisburg', 'Providence', 'Columbia', 'Pierre', 'Nashville', 'Austin', 'Salt Lake City', 'Montpelier', 'Richmond', 'Olympia', 'Charleston', 'Madison',
'Cheyenne']
    app.countries = ["Albania", "Andorra", "Armenia", "Austria", "Azerbaijan", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Georgia", "Germany", "Greece", "Hungary", "Iceland", "Ireland", "Italy", "Kazakhstan", "Kosovo", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "Malta", "Moldova", "Monaco", "Montenegro", "Netherlands", "North Macedonia", "Norway", "Poland", "Portugal", "Romania",
 "Russia", "San Marino", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Turkey", "Ukraine", "United Kingdom"]
    app.countryCapitals = ["Tirana", "Andorra la Vella", "Yerevan", "Vienna", "Baku", "Minsk", "Brussels", "Sarajevo", "Sofia", "Zagreb", "Nicosia", "Prague", "Copenhagen", "Tallinn", "Helsinki", "Paris", "Tbilisi", "Berlin", "Athens", "Budapest", "Reykjavik", "Dublin", "Rome",
 "Nur-Sultan", "Pristina", "Riga", "Vaduz", "Vilnius", "Luxembourg","Valletta", "Chișinău", "Monaco", "Podgorica", "Amsterdam", "Skopje", "Oslo", "Warsaw", "Lisbon", "Bucharest", "Moscow", "San Marino", "Belgrade", "Bratislava", "Ljubljana", "Madrid","Stockholm", "Bern", "Ankara", "Kyiv", "London"]
    app.board = []
    for x in range(10):
        app.board.append([None, None, None, None, None, None, None, None, None, None])
    app.rulesList = ["Each player gets 7 cards with the outline of the state and the state capital on it", "To play a card, one must correctly input the state name and state capital", "By playing a card, you can place a token for that state on the board", "To win, you must get 1 five-in-a-row anywhere on the board", "There are also special add and remove cards that you can use"]
    app.cardStack = None
    app.cards = None
    app.stepsPerSecond = 1
    app.counter = 0
    app.paused = True
    app.playerturn = 1
    app.handClicked = False
    app.cardPlayed = False
    app.cardSelected = None
    app.winner = None
    app.topicNameLabel = "Enter Key"
    app.answerLabel = "Enter Value"
    app.isCorrect = True
    app.currentBox = "name"
    app.computerGame = False
    app.newCard = None
    app.showCard = False
    app.imageOpacity = 100
    app.playingPowerups = (False, None)
    app.rectOpacity = 100
    app.userInput = ["Enter Key", "Enter Value", "Enter Images Folder Link", "Enter Info File Link"]
    app.highlighted = -1
    app.boxSelected = None
    app.imageType = None
    app.anyCardPlayed = False
def distance(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

def inOval(centerX, centerY, x2, y2, width, height):
    aSquared = (width/2)**2
    bSquared = (height/2)**2
    if (((x2-centerX)**2)/aSquared + ((y2-centerY)**2)/bSquared) <=1:
        return True
    else:
        return False

def inCircle(centerX, centerY, r, mouseX, mouseY):
    if distance(centerX, centerY, mouseX, mouseY) <= r:
        return True
    else:
        return False

def inRectangle(left, top, width, height, pointX, pointY):
    if left <= pointX <= left + width:
        if top <= pointY <= top + height:
            return True
    return False

def initializeCards(app, num, powerups):
    cardStack = []
    for i in range(len(app.currentGame.broader)):
        newCard = Card(app.currentGame.imagesList[i], app.currentGame.narrower[i], app.currentGame.broader[i], f'{app.currentGame.broader[i]}{num}',False)
        cardStack.append(newCard)
    
    if powerups:
        for i in range(2):
            addCard = Card(app.currentGame.imagesList[50], None, "Add", f'add{i}', True)
            removeCard = Card(app.currentGame.imagesList[51], None, "Remove", f'remove{i}', True)
            cardStack.append(addCard)
            cardStack.append(removeCard)
    return cardStack
'''
For the rounded rectangles I got the method from ChatGPT:
To draw a rounded rectangle using arcs and rectangles:

Corners with Arcs: Use four arcs to represent the rounded corners. Each arc should fit within a square region of the specified corner radius.
Side Edges with Rectangles: Draw vertical and horizontal rectangles to connect the arcs along the edges of the rectangle.
Central Rectangle: Fill the center of the rectangle using a larger rectangle that spans the remaining space between the arcs.
By combining these arcs and rectangles, you can create the appearance of a rounded rectangle without relying on complex shapes. Adjust the radii and dimensions to match your desired proportions.

'''
def drawRoundedRect(left, top, width, height, radius, fill, border=None):
    # skinny rectangle/side rectangles
    drawRect(left + radius, top, width - 2 * radius, height, fill=fill, border = border, borderWidth = 3)
    # large rectangle
    drawRect(left, top + radius, width, height - 2 * radius, fill=fill, border = border, borderWidth = 3)

    #draw arcs
    # top left
    drawArc( left + radius, top + radius, radius * 2, radius * 2, 90, 90, fill=fill, border=border, borderWidth = 3)
    # top right
    drawArc(left + width - radius, top +  radius,  radius * 2, radius * 2, 0,  90, fill=fill, border=border, borderWidth = 3)
    # bottom left
    drawArc(left + radius, top + height - radius,  radius * 2, radius * 2, 180, 90, fill=fill, border=border, borderWidth = 3)
    # bottom right
    drawArc(left + width - radius, top + height - radius, radius * 2, radius * 2, 270, 90, fill=fill, border=border, borderWidth = 3)


# ----- Pick Topic Screen -----
def pickTopic_redrawAll(app):
    drawImage('images/openingscreen.png', 0, 0, width = 1000, height = 1000)

def pickTopic_onMousePress(app, mouseX, mouseY):
    # initialize european countries game
    if inOval(255, 645, mouseX, mouseY, 400, 110):
        imagesList = []
        for country in app.countries:
            imagesList.append(f'images/europeancountries/{country.lower()}.png')
        imagesList.append(f'images/states/add.png')
        imagesList.append(f'images/states/remove.png')
        app.currentGame = Game("European countries and capitals", imagesList, app.countries, app.countryCapitals, "Country Name", "Country Capital", 'images/stateCapitalScreen.png')
        setActiveScreen('intro')
    # initialize states and capitals game
    elif inOval(745, 645, mouseX, mouseY, 400, 110):
        imagesList = []
        for state in app.states:
            imagesList.append(f'images/states/{state.lower()}.png')
        imagesList.append(f'images/states/add.png')
        imagesList.append(f'images/states/remove.png')
        app.currentGame = Game("US states and capitals", imagesList, app.states, app.stateCapitals, "State Name", "State Capital", 'images/stateCapitalScreen.png')
        setActiveScreen('intro')
    
    elif inOval(500,810, mouseX, mouseY, 400, 110):
        setActiveScreen('userInput')
# ---- User Input ------------
def userInput_redrawAll(app):
    drawRect(0,0, 1000, 1000, fill ="midnightBlue")
    # draw topic name box
    left = 100
    top = 100
    for x in range(4):
        if app.highlighted == x:
            drawRoundedRect(95, top-5, 805, 85, 40, fill = "white", border = "red")
        drawRoundedRect(100, top, 800, 80, 35, fill = "white")
        drawLabel(app.userInput[x], 500, top + 40)
        top += 120

    # draw type of image button
    drawOval(188, 700, 250, 125, fill = "cornflowerBlue")
    drawLabel('PNG', 188, 700, fill = "white", size = 20, font = 'grenze', bold = True)

    drawOval(500, 700, 250, 125, fill = "cornflowerBlue")
    drawLabel('JPEG', 500, 700, fill = "white", size = 20, font = "montserrat", bold = True)

    drawOval(813, 700, 250, 125, fill = "cornflowerBlue")
    drawLabel('JPG', 813, 700, fill = "white", size = 20, font = "montserrat", bold = True)

def userInput_onKeyPress(app, key):
    if app.boxSelected is None:
        app.boxSelected = 0
    currentBox = app.userInput[app.boxSelected]
    # shortcut
    if key == "up":
        app.userInput[0] = "state2"
        app.userInput[1] = "capital2"
        app.userInput[2] = "https://drive.google.com/drive/folders/1HvG5zZPNQP1o1nobaDxms2PW7Tz1aDhl"
        app.userInput[3] = "https://drive.google.com/file/d/1NrdJ-XKHthTvTikzu2iWauKjcIgDq-zb/view"
    elif currentBox == "Enter Key" or currentBox == "Enter Value" or currentBox == "Enter Images Folder Link" or currentBox == "Enter Info File Link":
        if key == "backspace" or key == "space":
            return
        else:
            app.userInput[app.boxSelected] = key
    else:
        if key == "backspace":
            app.userInput[app.boxSelected] = app.userInput[app.boxSelected][:-1]
        elif key == 'space':
            app.userInput[app.boxSelected] += " "
        else:
            app.userInput[app.boxSelected] += key

def userInput_onMousePress(app, mouseX, mouseY):
    checkBoxPress(app, mouseX, mouseY)
    if inOval(188, 700, mouseX, mouseY, 250, 125):
        if app.userInput[0]!= "Enter Key" and app.userInput[1] != "Enter Value" and app.userInput[2] != "Enter Images Folder Link" and app.userInput[3] != "Enter Info File Link":
                app.imageType = "png"
                setActiveScreen('loading')
                app.currentGame = getUserContent(app.userInput[2], app.userInput[0], app.userInput[1], app.userInput[3], app.imageType)
                setActiveScreen('intro')
    elif inOval(500, 700, mouseX, mouseY, 250, 125):
        if app.userInput[0]!= "Enter Key" and app.userInput[1] != "Enter Value" and app.userInput[2] != "Enter Images Folder Link" and app.userInput[3] != "Enter Info File Link":
                app.imageType = "jpeg"
                setActiveScreen('loading')
                app.currentGame = getUserContent(app.userInput[2], app.userInput[0], app.userInput[1], app.userInput[3], app.imageType)
                setActiveScreen('intro')
    elif inOval(813, 700, mouseX, mouseY, 250, 125):
        if app.userInput[0]!= "Enter Key" and app.userInput[1] != "Enter Value" and app.userInput[2] != "Enter Images Folder Link" and app.userInput[3] != "Enter Info File Link":
                app.imageType = "jpg"
                setActiveScreen('loading')
                app.currentGame = getUserContent(app.userInput[2], app.userInput[0], app.userInput[1], app.userInput[3], app.imageType)
                setActiveScreen('intro')

def checkBoxPress(app, mouseX, mouseY):
    left = 100
    top = 100
    for x in range(4):
        if inRectangle(left, top, 800, 80, mouseX, mouseY):
            app.boxSelected = x
            app.highlighted = x
            break
        top += 120

# ---- Filler Loading Screen while the images are fetched -------
def loading_redrawAll(app):
    drawImage('loading.png', 0, 0, width = 1000, height = 1000)
#-----Intro =Screen ------
def intro_redrawAll(app):
    drawImage('images/introbackground.jpg', 0, 0, width = 1000, height = 1000, opacity = 30)
    drawLabel("SEQUENCE", app.width/2 + 5, app.height/4, fill = 'lightGray', size=72, bold=True, font = "Dalek")
    drawLabel('SEQUENCE', app.width/2, app.height/4, size=72, bold=True, font = "Dalek", fill = 'midnightBlue')
    line1 = f'Test your knowledge of {app.currentGame.topic} while'
    line2 = 'honing your problem-solving skills'

    # draw the back button
    drawCircle(40, 40,30, fill = 'midnightBlue')
    drawLine(25,40, 50, 25,fill = "white", lineWidth = 5)
    drawLine(25,40, 50, 55,fill = "white", lineWidth = 5)

    
    # Draw each line separately
    drawLabel(line1, app.width / 2, app.height / 4 + 75, font="Dalek", size=20, fill="midnightBlue", bold = True)
    drawLabel(line2, app.width / 2, app.height / 4 + 100, font="Dalek", size=20, fill="midnightBlue", bold = True)
    # Draw nav screens
    drawOval(188, 688, 250, 125, fill = "midnightBlue")
    drawLabel('Rules', 188, 688, fill = "white", size = 20, font = 'grenze')

    drawOval(500, 688, 250, 125, fill = "midnightBlue")
    drawLabel('2 Player', 500, 688, fill = "white", size = 20, font = "montserrat")

    drawOval(813, 688, 250, 125, fill = "midnightBlue")
    drawLabel('Player vs Computer', 813, 688, fill = "white", size = 20, font = "montserrat")

    # Image Attribution
    drawLabel("Photo by Robert Coelho on Unsplash", 100, 990)

def intro_onMousePress(app, mouseX, mouseY):
    if inCircle(40,40,30, mouseX, mouseY):
        setActiveScreen('pickTopic')
    elif inOval(188, 688, mouseX, mouseY, 250, 125):
        setActiveScreen('rules')
    elif inOval(500, 688, mouseX, mouseY, 250, 125):
        app.paused = False
        setActiveScreen('twoplayer1Name')
    elif inOval(813, 688, mouseX, mouseY, 250, 125):
        setActiveScreen('userName')

def intro_onScreenActivate(app):
    # initialize board cards, cardstack
    app.cardStack = initializeCards(app, 1, False) + initializeCards(app, 2, False)
    app.cards = initializeCards(app, 1, True) + initializeCards(app, 2, True)
    app.playerturn = 1

# Rules Screen
def rules_redrawAll(app):
    # draw back button
    drawCircle(40, 40,30, fill = 'midnightBlue')
    drawLine(25,40, 50, 25,fill = "white", lineWidth = 5)
    drawLine(25,40, 50, 55,fill = "white", lineWidth = 5)

    # draw title
    drawImage('images/game rules.png', app.width/2, 100, width= 500, height=100,
          opacity=100, rotateAngle=0, align='center')
    rules_drawRules(app)

def rules_drawRules(app):
    currentHeight = 150
    for i in range(len(app.rulesList)):
        drawImage('images/blue long bg.png', app.width/2, currentHeight + 75, width = 700, height = 100, align = "center")
        drawLabel(f'{i+1}.  {app.rulesList[i]}', app.width/2, currentHeight + 75, size = 15, font = "Montserrat", bold = True, fill = 'white')
        currentHeight += 150

def rules_onMousePress(app, mouseX, mouseY):
    if inCircle(40,40,30, mouseX, mouseY):
        setActiveScreen('intro')

# two player player 1 name

def twoplayer1Name_onKeyPress(app, key):
    characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    if key == " " or key in characters:
        if app.player1.name is not None:
            app.player1.name += key
        else:
            app.player1.name = key
    # checks to make sure it's not an empty string
    elif key == "backspace" and app.player1.name is not None:
        app.player1.name = app.player1.name[:-1]
        if app.player1.name == "":
            app.player1.name = None

def twoplayer1Name_onMousePress(app, mouseX, mouseY):
    if app.player1.name is not None:
        if inOval(app.width/2,800, mouseX, mouseY, 300, 100):
            setActiveScreen("twoplayer2Name")


def twoplayer1Name_redrawAll(app):
    drawImage(app.player1.getImages()[app.counter], 0, 0, width = 1000, height = 1000)
    drawRect(150, 500, 700, 150, fill = "white")
    if app.player1.name is not None:
        drawLabel(app.player1.name, 500, 575, font = 'cursive', size = 48, bold = True)
    drawOval(app.width/2, 800, 300, 100, fill = "white")
    drawLabel("Submit", app.width/2, 800, fill = "midnightBlue", size = 20)

def twoplayer1Name_takeStep(app):
    if app.paused:
        return
    app.counter+=1
    if app.counter == 5:
        app.counter = 0

def twoplayer1Name_onScreenActivate(app):
    app.paused = False
    app.player1.name = None
    app.player2.name = None
    app.player1.cards = []
    app.player2.cards = []
    app.player1Played = []
    app.player2Played = []
def twoplayer1Name_onStep(app):
    if not app.paused:
        twoplayer1Name_takeStep(app)
# two player player 2 name
def twoplayer2Name_onKeyPress(app, key):
    characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    if key == " " or key in characters:
        if app.player2.name is not None:
            app.player2.name += key
        else:
            app.player2.name = key
    elif key == "backspace" and app.player2.name is not None:
        app.player2.name = app.player2.name[:-1]
        if app.player2.name == "":
            app.player2.name = None

def twoplayer2Name_onMousePress(app, mouseX, mouseY):
    # checks to see if it's in the submit button
    if app.player2.name is not None:
        if inOval(app.width/2,800, mouseX, mouseY, 300, 100):
            app.paused = True
            app.player1.cards = drawCards(app, 7)
            app.player2.cards = drawCards(app, 7)
            app.player1.played = []
            app.player2.played = []
            setBoard(app)
            setActiveScreen("twoplayergame")
def twoplayer2Name_onScreenActivate(app):
    app.paused = False

def twoplayer2Name_takeStep(app):
    if app.paused:
        return
    app.counter+=1
    if app.counter == 5:
        app.counter = 0
def twoplayer2Name_onStep(app):
    if not app.paused:
       twoplayer2Name_takeStep(app)

def twoplayer2Name_redrawAll(app):
    drawImage(app.player2.getImages()[app.counter], 0, 0, width = 1000, height = 1000)
    drawRect(150, 500, 700, 150, fill = "white")
    if app.player2.name is not None:
        drawLabel(app.player2.name, 500, 575, font = 'cursive', size = 48, bold = True)
    drawOval(app.width/2, 800, 300, 100, fill = "white")
    drawLabel("Submit", app.width/2, 800, fill = "midnightBlue", size = 20, font = 'Obitron font')

# two player game
def setBoard(app):
    topicsList = copy.copy(app.currentGame.broader)
    usedIndexes = []
    # loops through the first half of the board
    for row in range(len(app.board)//2):
        for col in range(len(app.board[0])):
            # randomly assigns a topic to each square of the board
            topicIndex = getNewIndex(topicsList, usedIndexes, 0, 49)
            app.board[row][col] = app.cardStack[topicIndex]
            usedIndexes.append(topicIndex)
    usedIndexes = []
    # loops through the second half of the board
    for row in range(len(app.board)//2, len(app.board)):
        for col in range(len(app.board[row])):
            # randomly assigns a topic to each square of the board
            topicIndex = getNewIndex(topicsList, usedIndexes, 50, 99)
            app.board[row][col] = app.cardStack[topicIndex]
            usedIndexes.append(topicIndex)

def getNewIndex(list1, used, start, stop):
    newIndex = random.randint(start, stop)
    while True:
        newIndex = random.randint(start, stop)
        if newIndex not in used:
            return newIndex

def drawBoard(app):
    currentLeft = 180
    currentTop = 100
    # ;loops thrpugh the 2d list of the board
    for row in range(len(app.board)):
        currentLeft = 180
        if row != 0:
            currentTop += 80
        for col in range(len(app.board[0])):
            # draws the cell
            drawRect(currentLeft, currentTop, 80, 80, borderWidth = 2, fill = "white", border = "black")
            # draws the topic image
            # attribution image - https://gisgeography.com/state-outlines-blank-maps-united-states/
            drawImage(app.board[row][col].getImage(), currentLeft, currentTop, width = 75, height = 75, opacity = 75)
            if app.board[row][col].played and app.board[row][col].playedBy == 1:
                drawCircle(currentLeft + 40, currentTop + 40, 30, fill = "midnightBlue")
                drawCircle(currentLeft + 40, currentTop+ 40, 20, fill = None, border = "white", borderWidth = 5)
            elif app.board[row][col].played and app.board[row][col].playedBy == 2:
                drawCircle(currentLeft + 40, currentTop + 40, 30, fill = "red")
                drawCircle(currentLeft + 40, currentTop+ 40, 20,  fill = None, border = "white", borderWidth = 5)
            # moves to the next cells
            currentLeft += 80

def drawDots(app, values):
    cardList = values
    usedList = []
    cardIndex = 0
    # loops through the card hand
    while cardIndex < len(cardList):
        card = cardList[cardIndex]
        currentLeft = 180
        currentTop = 20
        # loops through the rows
        for row in app.board:
            currentLeft = 180
            if row != 0:
                currentTop += 80
            # loops through the column
            for val in row:
                # checsk to see if it has a dot
                if val.id == card.id and card.id not in usedList and not val.played:
                    val.setPlayed()
                    color = None
                    if card.playedBy == 1:
                        color = "midnightBlue"
                        val.setPlayedBy(1)
                    elif card.playedBy == 2:
                        color = "red"
                        val.setPlayedBy(2)
                    if color is not None:
                        drawCircle(currentLeft + 40, currentTop+ 40, 30, fill = color)
                        drawCircle(currentLeft + 40, currentTop+ 40, 20, fill = None, border = "white", borderWidth = 2)
                    usedList.append(card.id)
                currentLeft += 80
        cardIndex +=1

def drawGame(app):
        drawBoard(app)
        # draw dots
        drawDots(app, app.player1.played)
        drawDots(app, app.player2.played)
        # draw line diving two sides of the board
        drawLine(180, 500, 980, 500, lineWidth = 5, fill = "midnightBlue")
        # draw back button
        drawCircle(40, 40,30, fill = 'midnightBlue')
        drawLine(25,40, 50, 25,fill = "white", lineWidth = 5)
        drawLine(25,40, 50, 55,fill = "white", lineWidth = 5)
        # draw player card stack
        drawRect(580, 950, 400, 50, fill = "white")
        drawImage('images/lower card hand.png', 580, 950, width = 400, height = 100, align = "center")

        # draw board outline
        drawLine(180, 100, 980, 100, lineWidth = 3, fill = "black")
        drawLine(180, 100, 180, 900, lineWidth = 3, fill = "black")
        drawLine(180, 900, 980, 900, lineWidth = 3, fill = "black")
        drawLine(980, 100, 980, 900, lineWidth = 3, fill = "black")
        
def drawCards(app, numCards):
    # draws the initial hands for the two players and the new card every time
    if numCards == 1:
        index = random.randint(0, len(app.cards)-1)
        return app.cards.pop(index)
    else:
        cards = []
        found = 0
        while found < numCards and len(app.cards) > 0:
            index = random.randint(0, len(app.cards)-1)
            cards.append(app.cards.pop(index))
            found +=1
        return cards

def twoplayergame_onStep(app):
    return

def twoplayergame_redrawAll(app):
    drawImage('images/two player.png', 580, 50, width = 900, height = 100, align = "center")
    drawGame(app)
    # draw player turn
    if app.playerturn == 1:
            drawLabel(f"{app.player1.name[0].upper()}{app.player1.name[1:]}'s", 95, 420, size = 30, fill = 'lightGray', font = "Passion_One")
            drawLabel(f"{app.player1.name[0].upper()}{app.player1.name[1:]}'s", 90, 420, size = 30, fill = 'midnightBlue')
            drawLabel("Turn", 95, 460, size = 30, fill = "lightGray")
            drawLabel("Turn", 90, 460, size = 30, fill = "midnightBlue")
    else:
            drawLabel(f"{app.player2.name[0].upper()}{app.player2.name[1:]}'s", 95, 420, size = 30, fill = 'lightGray')
            drawLabel(f"{app.player2.name[0].upper()}{app.player2.name[1:]}'s", 90, 420, size = 30, fill = 'red')
            drawLabel("Turn", 95, 460, size = 30, fill = "lightGray")
            drawLabel("Turn", 90, 460, size = 30, fill = "red")


def twoplayergame_onMousePress(app, mouseX, mouseY):
    # checks to see whether the cards are clicked
    if inRectangle(180, 850, 400, 100, mouseX, mouseY) and app.cardSelected is None:
        app.handClicked = True
        setActiveScreen('card')
    elif inCircle(40,40,30, mouseX, mouseY) and not app.handClicked:
        setActiveScreen('intro')
    else:
        if app.playerturn == 1:
            currentPlayer = app.player1
        else:
            currentPlayer = app.player2
        if app.playingPowerups[0]:
            card = app.playingPowerups[1]
            squareClicked = getSquare(app, mouseX, mouseY)
            if squareClicked is not None:
                checkAndPlayPowerups(app, card, squareClicked, currentPlayer)
        elif app.cardSelected is not None:
            squareClicked = getSquare(app, mouseX, mouseY)
            card = currentPlayer.cards[app.cardSelected]
            if squareClicked is not None:
                checkAndSetCard(app, card, squareClicked, currentPlayer)

# shortcuts
def twoplayergame_onKeyPress(app, key):
    if key == 'w' or key == 'W':
        app.winner = "No one"
        setActiveScreen('win')
    if key == 's' or key == 'S':
        setActiveScreen('stalemate')
              
              
def pickNewCard(app):
    if len(app.cards) == 0:
        # Reset the card deck if empty
        app.cards = initializeCards(app,1 ) + initializeCards(app, 2)
    newCard = app.cards.pop(random.randint(0, len(app.cards)-1))
    return newCard

def checkAndPlayPowerups(app, card, squareClicked, currentPlayer):
    # checks for add powerup
    if card.getTopic() == "Add":
        row = squareClicked[0]
        col = squareClicked[1]
        if not app.board[row][col].played:
            app.board[row][col].played = True
            app.board[row][col].setPlayedBy(app.playerturn)
            currentPlayer.played.append(app.board[row][col])
            newCard = pickNewCard(app)
            currentPlayer.cards.append(newCard)
            app.playerturn += 1
            app.playingPowerups = (False, None)
            if app.playerturn == 3:
                app.playerturn = 1
            app.cardSelected = None
            return True
        else:
            if app.playerturn == 3:
                app.playerturn = 1
            return False
    # remove powerup
    else:
        row = squareClicked[0]
        col = squareClicked[1]
        # unplays the board cell
        if app.board[row][col].played and app.anyCardPlayed:
            app.board[row][col].played = False
            app.board[row][col].playedBy = None
            newCard = pickNewCard(app)
            currentPlayer.cards.append(newCard)
            app.playerturn += 1
            app.playingPowerups = (False, None)
            if app.playerturn == 3:
                app.playerturn = 1
            app.cardSelected = None
            return True
        else:
            if app.playerturn == 3:
                app.playerturn = 1
            return False

def checkAndSetCard(app, card, coords, currentPlayer):
    row = coords[0]
    col = coords[1]
    # checks to make sure the board cell is not already occupied and it's the right key
    if not app.board[row][col].played and app.board[row][col].answer == card.answer:
        app.board[row][col].setPlayed()
        app.board[row][col].setPlayedBy(app.playerturn)
        currentPlayer.playCard(app.board[row][col])
        newCard = pickNewCard(app)
        currentPlayer.cards.append(newCard)
        app.playerturn +=1
        app.cardSelected = None
        if not app.anyCardPlayed:
            app.anyCardPlayed = True
        if app.playerturn == 3:
                app.playerturn = 1
        return True
    else:
        return False



def getSquare(app,x,y):
    top = 100
    left = 180
    squareCoords = None
    for row in range(len(app.board)):
        for col in range(len(app.board[row])):
            if inRectangle(left + col * 80, top + row * 80, 80, 80, x, y):
                return (row, col)
# ----- card screen -------
def card_redrawAll(app):
    drawCardScreen(app)

def drawCardScreen(app):
    # background image
    drawRect(0,0,1000,1000, fill = "midnightBlue")
    # draw close button
    drawCircle(40, 40,30, fill = 'cornflowerBlue')
    drawLine(20, 25, 60, 55,fill = "white", lineWidth = 3)
    drawLine(60,25, 20, 55,fill = "white", lineWidth = 3)
    left = 250
    top = 10
    # draws the player's hand
    if app.playerturn == 1:
        cards = app.player1.cards
    else:
        cards = app.player2.cards
    for i in range(3):
        if app.cardSelected == i:
            drawRoundedRect(left-5, top-5, 160, 210, 25, fill = "white", border = "red")
            drawRoundedRect(left, top, 150, 200, 20, fill = "white")
        else:
            drawRoundedRect(left-5, top-5, 160, 210, 25, fill = "white", border = "cornflowerBlue")
            drawRoundedRect(left, top, 150, 200, 20, fill = "white")
        drawImage(cards[i].getImage(), left + 75, top + 100, width = 100, height = 100, align = "center")
        left += 200
    left = 250
    top = 550
    for i in range(3,6):
        if app.cardSelected == i:
            drawRoundedRect(left-5, top-5, 160, 210, 25, fill = "white", border = "red")
            drawRoundedRect(left, top, 150, 200, 20, fill = "white")
        else:
            drawRoundedRect(left-5, top-5, 160, 210, 25, fill = "white", border = "cornflowerBlue")
            drawRoundedRect(left, top, 150, 200, 20, fill = "white")
        drawImage(cards[i].getImage(), left + 75, top + 100, width = 100, height = 100, align = "center")
        left += 200
    # draw the 7th card in the center
    if app.cardSelected == 6:
        drawRoundedRect(420, 270, 160, 210, 20, fill = "white", border = "red")
        drawRoundedRect(425, 275, 150, 200, 20, fill = "white")
    else:
        drawRoundedRect(420, 270, 160, 210, 20, fill = "white", border = 'cornflowerBlue')
        drawRoundedRect(425, 275, 150, 200, 20, fill = "white")
    drawImage(cards[6].getImage(), 500, 375, width = 100, height = 100, align = "center")
    # allows the player to play a card
    if not app.cardPlayed:
        drawOval(500, 900, 200, 75, fill = "white")
        drawLabel("Play Card", 500, 900, fill = "midnightBlue", size = 24, font = "Montserrat font")

def findCardOnBoard(app, playedCard):
    for row in range(len(app.board)):
        for col in range(len(app.board[row])):
            if app.board[row][col] == playedCard:
                return row, col
    return None

def card_onMousePress(app, mouseX, mouseY):
    if inCircle(40,40,30, mouseX, mouseY) and app.handClicked:
        app.handClicked = False
        setActiveScreen('twoplayergame')
    # checks to see if a card is played
    else:
        checkCards(app, mouseX, mouseY)
        if app.playerturn == 1 and app.player1.cards[app.cardSelected].powerups and app.cardSelected is not None and app.anyCardPlayed:
            setActiveScreen('twoplayergame')
            app.playingPowerups = (True, app.player1.cards[app.cardSelected])
            app.player1.cards.pop(app.cardSelected)
        elif app.playerturn == 2 and app.player2.cards[app.cardSelected].powerups and app.cardSelected is not None and app.anyCardPlayed:
            app.playingPowerups = (True, app.player2.cards[app.cardSelected])
            app.player2.cards.pop(app.cardSelected)
            setActiveScreen('twoplayergame')
        elif app.handClicked and inOval(500, 900, mouseX, mouseY, 100, 75) and app.cardSelected is not None:
            setActiveScreen('topicAnswer')

def checkCards(app, mouseX, mouseY):
    if inRectangle(250, 10, 150, 250, mouseX, mouseY):
            app.cardSelected = 0
    elif inRectangle(450, 10, 150, 250, mouseX, mouseY):
            app.cardSelected = 1
    elif inRectangle(650, 10, 150, 250, mouseX, mouseY):
            app.cardSelected = 2
    elif inRectangle(425, 275, 150, 250, mouseX, mouseY):
            app.cardSelected = 6
    elif inRectangle(250, 550, 150, 250, mouseX, mouseY):
            app.cardSelected = 3
    elif inRectangle(450, 550, 150, 250, mouseX, mouseY):
            app.cardSelected = 4
    elif inRectangle(650, 550, 150, 250, mouseX, mouseY):
            app.cardSelected = 5



# ----- TOPIC/ANSWER CHECKER ------
def topicAnswer_onScreenActivate(app):
    app.answerLabel = app.currentGame.label2
    app.topicNameLabel = app.currentGame.label1
    app.isCorrect = True

def topicAnswer_redrawAll(app):
    # draw the background image
    drawImage(app.currentGame.background, 0, 0, width = 1000, height = 1000)
    # draw the card selected
    drawRoundedRect(425, 50, 150, 200, 20, fill = "white")
    if app.playerturn == 1:
        drawImage(app.player1.cards[app.cardSelected].getImage(), 500, 150, width = 100, height = 100, align = "center")
    else:
        drawImage(app.player2.cards[app.cardSelected].getImage(), 500, 150, width = 100, height = 100, align = "center")

    # draw the base text/user input
    drawLabel(app.topicNameLabel, 500, 450, font = "cursive", size = 40)
    drawLabel(app.answerLabel, 500, 630, font = "cursive", size = 40)

    # draws error message
    if not app.isCorrect:
        drawImage('images/Error Message.png', 145, 705, width = 625, height = 125)

def topicAnswer_onKeyPress(app, key):
    characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    # validates user input
    if app.currentBox == "name":
        if key == " " or (key.lower() in characters):
            if app.topicNameLabel != app.currentGame.label1:
                app.topicNameLabel += key
            else:
                app.topicNameLabel = key
        elif key == "backspace" and app.topicNameLabel != app.currentGame.label1:
            app.topicNameLabel = app.topicNameLabel[:-1]
            if app.topicNameLabel == "":
                app.topicNameLabel = app.currentGame.label1
        elif key == 'space':
            app.topicNameLabel += " "
    else:
        if key == " " or (key.lower() in characters):
            if app.answerLabel != app.currentGame.label2:
                app.answerLabel += key
            else:
                app.answerLabel = key
        elif key == "backspace" and app.answerLabel != app.currentGame.label2:
            app.answerLabel = app.answerLabel[:-1]
            if app.answerLabel == "":
                app.answerLabel = app.currentGame.label2
        elif key == 'space':
            app.answerLabel += " "


def topicAnswer_onMousePress(app, mouseX, mouseY):
    if inRectangle(160, 390, 725, 118, mouseX, mouseY):
        app.currentBox = "name"
    elif inRectangle(160, 575, 725, 118, mouseX, mouseY):
        app.currentBox = "answer"

    if not checkCorrectTA(app) and inOval(500, 890, mouseX, mouseY, 365, 100):
        app.isCorrect = False
    elif app.handClicked and inOval(500, 890, mouseX, mouseY, 365, 100):
        if app.computerGame:
            setActiveScreen('automated')
        else:
            setActiveScreen("twoplayergame")

def checkCorrectTA(app):
    if app.playerturn == 1:
        correctAnswer = app.player1.cards[app.cardSelected].getAnswer()
        correctTopic = app.player1.cards[app.cardSelected].getTopic()
    else:
        correctAnswer = app.player2.cards[app.cardSelected].getAnswer()
        correctTopic = app.player2.cards[app.cardSelected].getTopic()
    if app.topicNameLabel.lower() == correctTopic.lower() and app.answerLabel.lower() == correctAnswer.lower():
        return True
    else:
        return False
# ----- STALEMATE SCREEN -------
def isStalemate(app, player):
    if player == 1:
        cards = app.player1.cards
    else:
        cards = app.player2.cards
    if not potentialSequencesPossible(app, player):
        return True
    else:
        # loops through the cards in the hand
        for card in cards:
            # loops throw the rows
            for row in range(len(app.board)):
                # loops through the columns
                for col in range(len(app.board[0])):
                    # sees if any of the cards are playable
                    if app.board[row][col].id == card.id and not app.board[row][col].played:
                        return False
        return True

def potentialSequencesPossible(app, player):
    # horizontal
    for row in range(len(app.board)):
        for col in range(len(app.board[0]) - 4):
            if checkSequence(app, row, col, 0, 1, player) >= 4:
                return True

    # vertical
    for col in range(len(app.board[0])):
        for row in range(len(app.board)-4):
            if checkSequence(app, row, col, 1, 0, player) >= 4:
                return True

    # left diagonal
    for row in range(len(app.board)-4):
        for col in range(len(app.board[0])-4):
            if checkSequence(app, row, col, 1, 1, player) >= 4:
                return True

    # right diagonal
    for row in range(len(app.board) - 4):
        for col in range(len(app.board), 3, -1):
            if checkSequence(app, row, col, 1, -1, player) >= 4:
                return True
    
    return False


def checkSequence(app, row1, col1, numRows, numCols, player):
    total = 0
    # loops through a potential sequence
    for x in range(5):
        # changes the row based on move of num rows and num cols
        currentRow = row1 + numRows * x
        currentCol = col1 + numCols * x
        if not isLegal(app, currentRow, currentCol):
            return 0
        elif app.board[currentRow][currentCol].playedBy == player:
            total +=1
    return total

def stalemate_redrawAll(app):
    drawImage('images/stalemate screen.png', 0, 0, width = 1000, height = 1000)

def stalemate_onMousePress(app, mouseX, mouseY):
    if inOval(500, 777.5, mouseX, mouseY, 390, 116):
        setActiveScreen('pickTopic')

# ----- WIN SCREEN -----
def isWin(app, player):
    numSequences = 0
    # horizontal
    for row in app.board:
        for i in range(len(row)-4):
            if row[i].playedBy is not None and row[i].playedBy == player:
                first = row[i]
                second = row[i+1]
                third = row[i+2]
                fourth = row[i+3]
                fifth = row[i+4]
                if first.playedBy == second.playedBy == third.playedBy == fourth.playedBy == fifth.playedBy:
                    numSequences += 1

    # vertical
    for col in range(len(app.board[0])):
        for row in range(len(app.board)-4):
            first = app.board[row][col]
            if first is not None and first.playedBy == player:
                second = app.board[row+1][col]
                third = app.board[row+2][col]
                fourth = app.board[row+3][col]
                fifth = app.board[row+4][col]
                if first.playedBy == second.playedBy == third.playedBy == fourth.playedBy == fifth.playedBy:
                    numSequences +=1

    # diagonal right to left
    for row in range(len(app.board) - 4):
        for col in range(len(app.board[0])-4):
            first = app.board[row][col]
            if first is not None and first.playedBy == player:
                second = app.board[row + 1][col + 1]
                third = app.board[row + 2][col + 2]
                fourth = app.board[row + 3][col + 3]
                fifth = app.board[row + 4][col + 4]
                if first.playedBy == second.playedBy == third.playedBy == fourth.playedBy == fifth.playedBy:
                    numSequneces +=1
    
    # diagonal left to right
    for row in range(len(app.board) - 4):
        for col in range(4, len(app.board[0])):
            first = app.board[row][col]
            if first is not None and first.playedBy == player:
                second = app.board[row + 1][col - 1]
                third = app.board[row + 2][col - 2]
                fourth = app.board[row + 3][col - 3]
                fifth = app.board[row + 4][col - 4]
                if first.playedBy == second.playedBy == third.playedBy == fourth.playedBy == fifth.playedBy:
                    numSequences +=1
    if numSequences >= 1:
        app.winner = player
        return True
    else:
        return False

def win_redrawAll(app):
    drawImage('images/win screen.png', 0, 0, width = 1000, height = 1000)
    drawLabel(f'{app.winner}', 500, 500, size = 56, fill = "white", font = "Montserrat font", bold = True)
    drawLabel('WINS!!',500, 575, size = 56, fill = "white", font = "Montserrat font", bold = True)
    drawOval(500, 700, 200, 100, fill = "white")
    drawLabel("Home", 500, 700, fill = "black", bold = True, size = 24)

def win_onMousePress(app, mouseX, mouseY):
    if inOval(500, 700, mouseX, mouseY, 200, 100):
        setActiveScreen('pickTopic')

#------computer vs user ------

# user name screen
def userName_onKeyPress(app, key):
    characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    if key == " " or key in characters:
        if app.player1.name is not None:
            app.player1.name += key
        else:
            app.player1.name = key
    elif key == "backspace" and app.player1.name is not None:
        app.player1.name = app.player1.name[:-1]
        if app.player1.name == "":
            app.player1.name = None

def userName_onMousePress(app, mouseX, mouseY):
    # checks to make sure user inputs a name
    if app.player1.name is not None:
        if inOval(app.width/2,800, mouseX, mouseY, 300, 100):
            app.cardStack = initializeCards(app, 1, False) + initializeCards(app, 2, False)
            app.cards = initializeCards(app, 1, True )+ initializeCards(app, 2, True)
            app.player1.cards = drawCards(app, 7)
            app.player2.cards = drawCards(app, 7)
            setBoard(app)
            setActiveScreen("automated")


def userName_redrawAll(app):
    drawImage(app.player1.getImages()[app.counter], 0, 0, width = 1000, height = 1000)
    drawRect(150, 500, 700, 150, fill = "white")
    if app.player1.name is not None:
        drawLabel(app.player1.name, 500, 575, font = 'cursive', size = 48, bold = True)
    drawOval(app.width/2, 800, 300, 100, fill = "white")
    drawLabel("Submit", app.width/2, 800, fill = "midnightBlue", size = 20)
    
def userName_takeStep(app):
    if app.paused:
        return
    app.counter+=1
    if app.counter == 5:
        app.counter = 0

def userName_onScreenActivate(app):
    app.paused = False
    app.player1.name = None
    app.player2.name = "Computer"
    app.player1Hand = []
    app.player1.played = []
    app.player2.played = []

def userName_onStep(app):
    if not app.paused:
        userName_takeStep(app)

# automated player v computer screen
def automated_onScreenActivate(app):
    app.counter = 0
    app.imageOpacity = 100
    app.rectOpacity = 100

def automated_redrawAll(app):
        drawImage('images/automated.png', 180, 0, width = 900, height = 100)
        drawGame(app)
        drawImage('images/sequence card stack.png', 15, 350, width = 150, height = 300)
        # draw player turn
        if app.playerturn == 1:
            drawLabel(f"{app.player1.name[0].upper()}{app.player1.name[1:]}'s", 95, 220, size = 30, fill = 'lightGray', font = "Passion_One")
            drawLabel(f"{app.player1.name[0].upper()}{app.player1.name[1:]}'s", 90, 220, size = 30, fill = 'midnightBlue')
            drawLabel("Turn", 95, 260, size = 30, fill = "lightGray")
            drawLabel("Turn", 90, 260, size = 30, fill = "midnightBlue")
        else:
            drawLabel(f"{app.player2.name[0].upper()}{app.player2.name[1:]}'s", 95, 220, size = 30, fill = 'lightGray')
            drawLabel(f"{app.player2.name[0].upper()}{app.player2.name[1:]}'s", 90, 220, size = 30, fill = 'red')
            drawLabel("Turn", 95, 260, size = 30, fill = "lightGray")
            drawLabel("Turn", 90, 260, size = 30, fill = "red")
        # draw card fading animation
        if app.showCard:
            drawRect(420, 340, 240, 400, fill = "white", border = "black", borderWidth = 3, opacity = app.rectOpacity)
            drawImage(app.newCard.getImage(), 540, 540, width = 100, height = 100, align = "center", opacity = app.imageOpacity)
            drawLabel(app.newCard.sideScreen, 540, 600, fill = "black", font = "cursive", size = 26)

def automated_onKeyPress(app, key):
    if key == 'w' or key == 'W':
        setActiveScreen('win')
        app.winner = "No one"
    if key == 's' or key == 'S':
        setActiveScreen('stalemate')
              

def computerTurn(app):
    bestScore = 0
    bestMove = None
    bestLocation = None
    # loops through the cards in the hand
    for card in app.player2.cards:
        # loops through the rows
        for row in range(len(app.board)):
            # loops through the columns
            for col in range(len(app.board[row])):
                # checks to see if it's the right state or has been played
                if app.board[row][col].id == card.id and app.board[row][col].isPlayed() == False:
                    # checks the score
                    score = getScore(app, row, col, 2, True)
                    if score >= bestScore:
                        bestScore = score
                        bestMove = card
                        bestLocation = (row, col)
                if card.getTopic() == "Add":
                    score = getScore(app, row, col, 2, True)
                    # using a powerup card is a higher score
                    score += 0.2
                    if score >= bestScore:
                        bestScore = score
                        bestMove = card
                        bestLocation = (row, col)
                elif card.getTopic() == "Remove" and app.board[row][col].played:
                    score = stopsOpponent(app, row, col)
                    if score >= bestScore:
                        bestMove = card
                        bestLocation = (row, col-1)

    playComputerCard(app, bestMove, bestLocation)

def getScore(app, row, col, playerNum, checkOpponent):
    score  = 0
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    # loops througb possible moves
    for r, c in moves:
        currentRow = 1
        for x in range(1, 5):
            newRow = row + r * x
            newCol = col + c * x
            # checks to see if it's on the board
            if not isLegal(app, newRow, newCol):
                break
            elif app.board[newRow][newCol].played:
                if app.board[newRow][newCol].playedBy != playerNum:
                    break
                else:
                    currentRow +=1
            else:
                currentRow += 0.5
        
        for y in range(1, 5):
            newRow = row - r * y
            newCol = col - c * y
            if not isLegal(app, newRow, newCol):
                break
            elif app.board[newRow][newCol].played:
                if app.board[newRow][newCol].playedBy != playerNum:
                    break
                else:
                    currentRow +=1
            else:
                currentRow += 0.5
        if currentRow > score:
            score = currentRow
    
    if checkOpponent:
        if getOpponentSequence(app, row, col) != 0:
            # blocking an opponent gets more point
            score += (getOpponentSequence(app, row, col) * 1.2)

    return score
    
# uses similar logic to stalemate
def stopsOpponent(app, row, col):
    directions = [(0, 1), (1,0), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1), (1, 1)]
    total = 0
    # loops through the directions
    for x in range(5):
        for row1, col1 in directions:
            for x in range(5):
                currentRow = row + row1 * x
                currentCol = col + col1 * x
                if not isLegal(app, currentRow, currentCol):
                    break
                # checks to see if it's part of the opponent sequence
                elif app.board[currentRow][currentCol].playedBy == 1:
                    total +=1
    score = total * 0.75
    return score



def getOpponentSequence(app, row, col):
    opponentScore = getScore(app, row, col, 1, False)
    return opponentScore * 0.8

def isLegal(app, row, col):
    if 0 <=  row < len(app.board) and 0 <= col < len(app.board[0]):
        return True
    return False
    
def playComputerCard(app, card, location):
    row = location[0]
    col = location[1]
    # checks to see if it's a powerups
    if card.powerups:
        app.player2.cards.remove(card)
        checkAndPlayPowerups(app, card, (row, col), app.player2)
        app.playerturn = 1
        setActiveScreen('automated')
        app.powerups = (False, None)
    # sets the board to played
    else:
        app.board[row][col].setPlayed()
        app.board[row][col].setPlayedBy(2)
        app.player2.playCard(card)
        if isWin(app, 2):
            app.winner = "Computer"
            setActiveScreen('win')
        else:
            newCard = pickNewCard(app)
            app.player2.cards.append(newCard)
            app.playerturn = 1

def automated_onMousePress(app,mouseX, mouseY):
     # checks to see whether the cards are clicked
    if inRectangle(180, 850, 400, 100, mouseX, mouseY) and app.playerturn == 1:
        app.handClicked = True
        setActiveScreen('automatedCard')
    elif inCircle(40,40,30, mouseX, mouseY):
        setActiveScreen('intro')
    else:
        if app.playerturn == 1:
            currentPlayer = app.player1
            # checks for powerup
            if app.playingPowerups[0]:
                card = app.playingPowerups[1]
                squareClicked = getSquare(app, mouseX, mouseY)
                if squareClicked is not None:
                    if checkAndPlayPowerups(app, card, squareClicked, currentPlayer):
                        computerTurn(app)
            # checks for regular card
            elif app.cardSelected is not None:
                squareClicked = getSquare(app, mouseX, mouseY)
                card = currentPlayer.cards[app.cardSelected]
                if squareClicked is not None:
                    if checkAndSetCard(app, card, squareClicked, currentPlayer):
                        computerTurn(app)

def automated_onStep(app):
    if app.newCard is not None and app.counter < 3:
        app.counter +=1
        app.imageOpacity -=30
        app.rectOpacity -= 30
    else:
        app.showCard = False

# player card screen in the automated version
def automatedCard_onMousePress(app, mouseX, mouseY):
    if inCircle(40,40,30, mouseX, mouseY) and app.handClicked:
        app.handClicked = False
        setActiveScreen('automated')
    # checks to see if a card is played
    else:
        checkCards(app, mouseX, mouseY)
        if app.cardSelected is not None and app.player1.cards[app.cardSelected].powerups:
            app.playingPowerups = (True, app.player1.cards[app.cardSelected])
            app.player1.cards.pop(app.cardSelected)
            setActiveScreen('automated')
        elif app.handClicked and inOval(500, 900, mouseX, mouseY, 100, 75) and app.cardSelected is not None:
            app.computerGame = True
            setActiveScreen('topicAnswer')

def automatedCard_redrawAll(app):
    drawCardScreen(app)
def main():
    runAppWithScreens(initialScreen='pickTopic')
main()
cmu_graphics.run()
