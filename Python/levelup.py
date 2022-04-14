import keyboard
import time

def setupLevelingPath():
    levelingPath = ['q', 'w', 'w', 'e', 'w', 'r', 'w', 'q', 'w', 'q', 'r', 'q', 'q', 'e', 'e', 'r', 'e', 'e']
    return levelingPath

def levelUp(levelingPath, lastLevel):
    key = "ctrl+" + levelingPath[lastLevel-1]
    keyboard.press(key)
    time.sleep(0.05)
    keyboard.release(key)
    print("Leveling ", levelingPath[lastLevel-1])

def tryToLevel(lastLevel, championLevel, levelingPath):
    #print("tryToLevel ", lastLevel, championLevel)
    if(lastLevel != None):
        if(lastLevel < championLevel):
            time.sleep(0.1)
            lastLevel = championLevel
            levelUp(levelingPath, lastLevel)
            return lastLevel
        else:
            return lastLevel
    elif(lastLevel == None):
        return championLevel - 1
        