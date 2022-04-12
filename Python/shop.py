from setup import getXYPos
import autoit
import keyboard
import time

class Item():
    x = None
    y = None
    cost = None
    def __init__(self, a, b, c):
        self.x = a
        self.y = b
        self.cost = c

def setupItems():
    itemList = []

    x, y = getXYPos(22.96, 37.12, False)
    junglingItem =  Item(x, y, 350)
    itemList.append(junglingItem)
    
    x, y = getXYPos(22.96, 47.87, False)
    vampiricScepter = Item(x, y, 900)
    itemList.append(vampiricScepter)
    
    x, y = getXYPos(25.88, 47.87, False)
    boots = Item(x, y, 1100)
    itemList.append(boots)
    
    x, y = getXYPos(28.80, 47.87, False)
    recurveBow = Item(x, y, 1000)
    itemList.append(recurveBow)

    x, y = getXYPos(31.71, 47.87, False)
    pickAxe = Item(x, y, 875)
    itemList.append(pickAxe)

    x, y = getXYPos(22.96, 58.42, False)
    botrk = Item(x, y, 525)
    itemList.append(botrk)

    hearthBoundAxe = None
    krakenSlayer = None
    witsEnd = None
    phantomDancer = None
    frozenHeart = None

    return itemList

def buyItem(itemList, index, ShopOpen):
    if(ShopOpen == False):
        keyboard.press_and_release('p')
        ShopOpen = True

    time.sleep(0.15)
    autoit.mouse_click("right", itemList[index].x, itemList[index].y, 1)
    time.sleep(0.15)

    return index, ShopOpen


    