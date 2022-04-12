import keyboard
import time

def setupLevelingPath():
    levelingPath = ['w', 'q', 'w', 'e', 'w', 'r', 'w', 'q', 'w', 'q', 'r', 'q', 'q', 'e', 'e', 'r', 'e', 'e']
    return levelingPath

def levelUp(levelingPath, lastLevel):
    key = "ctrl+" + levelingPath[lastLevel-1]
    keyboard.press_and_release(key)
    print("Leveling ", levelingPath[lastLevel-1])

def tryToLevel(lastLevel, championLevel, levelingPath):
    if(lastLevel != None):
        if(lastLevel < championLevel):
            time.sleep(0.1)
            lastLevel = championLevel
            levelUp(levelingPath, lastLevel)
            time.sleep(0.2)
            return lastLevel
        else:
            return championLevel
    elif(lastLevel == None):
        return championLevel - 1
        