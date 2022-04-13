from xmlrpc import client
import win32gui
import win32con
import win32ui 

import time
import mouse
import keyboard

import pyautogui

class Client(object):
    windowName = None
    handle = None
    dc = None

    x = None
    y = None
    width = None 
    height = None

    class Buttons:
        Play = None
        Coop = None
        Confirm = None
        FindMatch = None
        Accept = None

        ChampionSearchBar = None
        Warwick = None
        Lock = None

    
    def __init__(self):
        main()
        #Client.QueueUp(self)

    @staticmethod
    def Show():

        win32gui.SetForegroundWindow(Client.handle)
        win32gui.ShowWindow(Client.handle, win32con.SW_SHOW)
    
    @staticmethod
    def Click(x, y):
        stored_x, stored_y = mouse.get_position()
        mouse.move(int(x), int(y))
        mouse.click()
        #mouse.move(stored_x, stored_y)
        time.sleep(0.01)

    def QueueUp(self):
        delay = 0.5

        self.Show()
        time.sleep(delay * 4)

        self.Click(self.Buttons.Play[0], self.Buttons.Play[1])
        time.sleep(delay)

        self.Click(self.Buttons.Coop[0], self.Buttons.Coop[1])
        time.sleep(delay)

        self.Click(self.Buttons.Confirm[0], self.Buttons.Confirm[1])
        time.sleep(delay * 5)

        self.Click(self.Buttons.FindMatch[0], self.Buttons.FindMatch[1])
        
        queuePopped = False
        championSelectPopped = False
        while(not queuePopped):
            print("Waiting...")
            queuePopped = queuePop()
            
            time.sleep(delay)

        time.sleep(delay)
        if(queuePopped):        
            self.Click(self.Buttons.Accept[0], self.Buttons.Accept[1])

        for i in range(35):
            if(championSelectPopped == False):
                championSelectPopped = championSelectPop()
                time.sleep(delay/2)


        if(championSelectPopped):  #hasta acá por hoy
            print("ChampionSelect")
            pickChampion()
        
        hasGameStarted = False
        while(hasGameStarted == False): 
            hasGameStarted = gameStarted()

class Game(object): 
    windowName = None
    handle = None 
    dc = None 

    x = None
    y = None
    width = None 
    height = None
    
    def __init__(self):        
        Game.windowName = "League of Legends (TM) Client" 
        while (type(Game.width) != int):
            try:
                Game.handle = getHandle(Game.windowName)
                gamePos = getWindowPos(Game.handle)

                Game.x = gamePos[0]
                Game.y = gamePos[1]
                Game.width = gamePos[2]
                Game.height = gamePos[3]
            except: 
                print("Waiting")
                time.sleep(1)


def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ):
        print (hex(hwnd), win32gui.GetWindowText( hwnd ))


def getHandle(windowName):
    hWndMain = win32gui.FindWindow(None, windowName)
    return hWndMain

def getWindowPos(hwnd):    
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y

    return x, y, w, h

def getXYPos(x, y, clienting = True):
    if(clienting):
        translatedX = (Client.width / 100) * x
        translatedY = (Client.height / 100) * y
        returnX = int(Client.x + translatedX)
        returnY = int(Client.y + translatedY)

    else:
        game = Game()
        translatedX = (game.width / 100) * x
        translatedY = (game.height / 100) * y
        returnX = int(game.x + translatedX)
        returnY = int(game.y + translatedY)

    return returnX, returnY




def queuePop():

    acceptButtonX, acceptButtonY = getXYPos(50.00, 77.63)

    pixelColor = []
    color = Client.dc.GetPixel(acceptButtonX, acceptButtonY)
    r = color & 0xff
    g = color >> 8 & 0xff
    b = color >> 16 & 0xff

    if (not(pixelColor == [r, g, b])):
        pixelColor = [r, g, b]

    print(acceptButtonX, acceptButtonY, " - ", pixelColor)

    if(pixelColor == [155, 189, 190]):
        print("Queue popped")
        return True
    else: 
        return False
        
def championSelectPop():
    print("Entering championSelectPop func")

    # checkX = int((Client.width / 100) * 93.98)
    # checkY = int((Client.height / 100) * 94.86)

    checkX, checkY = getXYPos(93.98, 94.86)

    pixelColor = []
    color = Client.dc.GetPixel(checkX, checkY)
    r = color & 0xff
    g = color >> 8 & 0xff
    b = color >> 16 & 0xff

    if (not(pixelColor == [r, g, b])):
        pixelColor = [r, g, b]

    print(checkX, checkY, " - ", pixelColor)

    if(pixelColor == [205, 190, 145]):
        return True
    else: 
        return False

def pickChampion():
    
    Client.Click(Client.Buttons.ChampionSearchBar[0], Client.Buttons.ChampionSearchBar[1])
    time.sleep(0.5)
    keyboard.write("Warwick")

    time.sleep(0.5)
    Client.Click(Client.Buttons.Warwick[0], Client.Buttons.Warwick[1])
    
    time.sleep(0.5)
    Client.Click(Client.Buttons.Lock[0], Client.Buttons.Lock[1])
    
def gameStarted():
    #print("Entering gameStarted func")

    checkX, checkY = getXYPos(50.05, 98.42, False)

    im = pyautogui.screenshot()#region=(checkX-1, checkY-1, checkX+1, checkY+1)
    px = im.getpixel((checkX, checkY))
    pixelColor = None

    #print(px)
    if (pixelColor != px):
        pixelColor = px

    #print(checkX, checkY, " - ", pixelColor, px)

    time.sleep(0.5)
    #print(pixelColor)
    if(pixelColor == (31, 133, 247)): #(31, 133, 247) #(17, 112, 237)
        #print("True")
        return True
    else: 
        #print("False")
        return False


def main(): 

    try:
        gamePos = getWindowPos(getHandle("League of Legends (TM) Client"))
        print("Game is already open")
    except:
        print("Except")
        #win32gui.EnumWindows( winEnumHandler, None )
        Client.windowName = "League of Legends"
        w = win32ui.FindWindow(None, Client.windowName)
        Client.dc = w.GetWindowDC()

        Client.handle = getHandle(Client.windowName)
        print(hex(Client.handle))

        clientPos = getWindowPos(Client.handle)

        Client.x = clientPos[0]
        Client.y = clientPos[1]
        Client.width = clientPos[2]
        Client.height = clientPos[3]

        print(Client.x, Client.y, Client.width, Client.height)

        Client.Buttons.Play = getXYPos(9.3, 5.69)
        Client.Buttons.Coop = getXYPos(11.56, 13.88)
        Client.Buttons.Confirm = getXYPos(42.03, 95.55)
        Client.Buttons.FindMatch = getXYPos(41.17, 94.44)
        Client.Buttons.Accept = getXYPos(50.00, 77.63)

        Client.Buttons.ChampionSearchBar = getXYPos(62.42, 14.44)
        Client.Buttons.Warwick = getXYPos(30.23, 23.33)
        Client.Buttons.Lock = getXYPos(50.00, 84.16)

        # Client.Buttons.Play = [int(Client.x + ((Client.width / 100) * 9.3)), int(Client.y + ((Client.height / 100) * 5.69))]
        # Client.Buttons.Coop = [int(Client.x + ((Client.width / 100) * 11.56)), int(Client.y + ((Client.height / 100) * 13.88))]
        # Client.Buttons.Confirm = [int(Client.x + ((Client.width / 100) * 42.03)), int(Client.y + ((Client.height / 100) * 95.55))]
        # Client.Buttons.FindMatch = [int(Client.x + ((Client.width / 100) * 41.17)), int(Client.y + ((Client.height / 100) * 94.44))]
        # Client.Buttons.Accept = [int(Client.x + ((Client.width / 100) * 50.00)), int(Client.y + ((Client.height / 100) * 77.63))]

        # Client.Buttons.ChampionSearchBar = [int(Client.x + ((Client.width / 100) * 62.42)), int(Client.y + ((Client.height / 100) * 14.44))]
        # Client.Buttons.Warwick = [int(Client.x + ((Client.width / 100) * 30.23)), int(Client.y + ((Client.height / 100) * 23.33))]
        # Client.Buttons.Lock = [int(Client.x + ((Client.width / 100) * 50.00)), int(Client.y + ((Client.height / 100) * 84.16))]


        
        #checkX = int((Client.width / 100) * 93.98)
        #checkY = int((Client.height / 100) * 94.86)
        #print(checkX, checkY)
        Client.QueueUp(Client)
        #pickChampion()

        time.sleep(15)
        Game.windowName = "League of Legends (TM) Client" 
        while (type(Game.width) != int):
            try:
                Game.handle = getHandle(Game.windowName)
                gamePos = getWindowPos(Game.handle)

                Game.x = gamePos[0]
                Game.y = gamePos[1]
                Game.width = gamePos[2]
                Game.height = gamePos[3]
            except: 
                print("Waiting")
                time.sleep(1)


        w = win32ui.FindWindow(None, Game.windowName)
        Game.dc = w.GetWindowDC()
        print("Found Window")


        hasGameStarted = False
        while(hasGameStarted == False): 
            hasGameStarted = gameStarted()
            # print(Game.windowName)
            # print(Game.handle)
            # print(Game.dc)
            # print(Game.x)
            # print(Game.y)
            # print(Game.width)
            # print(Game.height)
            time.sleep(1)    

    
def __init__(self):
    main()


# if __name__ == "__main__":
#     main()
