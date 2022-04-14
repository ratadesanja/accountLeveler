from ast import While
import time
import keyboard
from pymem import Pymem
from world import find_champion_pointers, find_game_time, find_local_net_id, find_view_proj_matrix, read_object, world_to_screen, find_object_names, getPlayerGold, find_active_champion_pointer, updateActiveChampion, checkIfGameEnded, getHealthPercentage
from champion_stats import ChampionStats
from target import select_lowest_target
from constants import PROCESS_NAME
import jungle
from walk import Walker

from target import select_closest_target

import ctypes
import string
import random
from setup import Client
import shop
import levelup

import win32gui
import win32api
import win32con
import win32process

import os
from datetime import datetime
    

def setup(): 
    client = Client()
    if(client.handle != None):
        client.PlayGame()

    time.sleep(2)
    keyboard.press_and_release('y')
    
def main():
    time.sleep(2)
    #if(gameEnded = False):
    blueSide, redSide = jungle.jungleSetup()
    Side = redSide
    
    junglingIterator = 4
    inventoryIndex = 1

    ShopItemList = shop.setupItems()

    levelingPath = levelup.setupLevelingPath()
    lastLevel = 0
    

    class keybinds:
        walk = ' '
        measure = 'l'
        jungle = 'z'
        stop = 'i'
        recall = 'k'
    key = keybinds()

    mem = Pymem(PROCESS_NAME)
    #print(mem.base_address)
    champion_stats = ChampionStats()
    print(champion_stats.names())
    walker = Walker(mem)

    # ptr = find_active_champion_pointer(mem, "warwick")
    # print(read_object(mem, ptr))

    # time.sleep(20)

    champion_pointers = find_champion_pointers(mem, champion_stats.names())
    print(champion_pointers)

    champions = [read_object(mem, pointer) for pointer in champion_pointers]
    net_id_to_champion = {c.network_id: c for c in champions}
    local_net_id = find_local_net_id(mem)
    active_champion = net_id_to_champion[local_net_id]
    active_champion_pointer= find_active_champion_pointer(mem, active_champion.name)

    print(active_champion_pointer)

    gameEndedCheck = checkIfGameEnded(mem, active_champion_pointer)
    gameEnded = gameEndedCheck
    gameEndedCheckTimes = 0

    stopping = False
    once = True
    while gameEnded == False:
        while gameEndedCheck == False:
            gameEndedCheckTimes = 0
            gameEndedCheck = checkIfGameEnded(mem, active_champion_pointer)
            active_champion = updateActiveChampion(mem, active_champion_pointer)

            view_proj_matrix, width, height = find_view_proj_matrix(mem)
            game_time = find_game_time(mem)

            stopping = keyboard.is_pressed(key.stop)
            walk = keyboard.is_pressed(key.walk)
            measure = keyboard.is_pressed(key.measure)
            junglingKey = keyboard.is_pressed(key.jungle)
            recalling = keyboard.is_pressed(key.recall)

            jungling = False

            if(junglingKey):
                jungling = not jungling
                time.sleep(1.5)
            if(once):
                print("reading inputs")
                once = False

            lastLevel = levelup.tryToLevel(lastLevel, active_champion.level, levelingPath)

            if(active_champion.level > 3):
                #keyboard.press_and_release('y')
                while jungling:
                    gameEndedCheck = checkIfGameEnded(mem, active_champion_pointer)
                    
                    active_champion = updateActiveChampion(mem, active_champion_pointer)
                    jungle.pathToCamps(Side, redSide, blueSide, junglingIterator, view_proj_matrix, width, height, walker, champion_stats, find_game_time(mem), mem, champion_pointers, active_champion_pointer)
                    lastLevel = levelup.tryToLevel(lastLevel, active_champion.level, levelingPath)
                    
                    if(getHealthPercentage(active_champion.health, active_champion.max_health) < 15):
                        inventoryIndex = walker.recall(mem, active_champion_pointer, ShopItemList, inventoryIndex)
                        
                        while(active_champion.health < active_champion.max_health):
                            time.sleep(0.5)
                            active_champion = updateActiveChampion(mem, active_champion_pointer)
                            

                    if(Side == redSide and junglingIterator == 2):
                        junglingIterator = 3
                        inventoryIndex = walker.recall(mem, active_champion_pointer, ShopItemList, inventoryIndex)
                            #if(active_champion.gold > 1):
                            #    time.sleep(10)

                    elif(junglingIterator == 6):
                        if(Side == blueSide):
                            Side = redSide

                        else:
                            Side = blueSide
                        junglingIterator = 0
                    else: 
                        junglingIterator += 1

                    if(junglingIterator == 3):
                        junglingIterator += 1
                        
                    time.sleep(0.25)

                    
            # if(walk):
            #     target = None
            #     target = select_lowest_target(champion_stats, active_champion, champions)
                
            #     x, y = None, None
            #     if target is not None:
            #         x, y = world_to_screen(view_proj_matrix, width, height, target.x, target.z, target.y)
            #         walker.walk(x, y, game_time)

            if(measure):
                active_champion = updateActiveChampion(mem, active_champion_pointer)
                print(active_champion.x, active_champion.y, active_champion.z)
                time.sleep(0.5)


            time.sleep(0.01)

        while(gameEndedCheck == True):

            print(gameEndedCheckTimes)

            if(gameEndedCheckTimes > 4):
                print("GAME ENDED")
                gameEnded = True
                break
            else: 
                time.sleep(1)
                gameEndedCheck = checkIfGameEnded(mem, active_champion_pointer)
                gameEndedCheckTimes += 1
    print("now what......")

def goToLobby():
    #time.sleep(10)
    windowName = "League of Legends"
    handle = 0
    while(handle == 0):
        handle = win32gui.FindWindow(None, windowName)

    print("Client found: ", handle)
    t, p = win32process.GetWindowThreadProcessId(handle)
    print("Client process id: ", p)

    time.sleep(1)
    newClient = Client()
    
    print("Closing Client")
    try:
        handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, p)
        if handle:
            win32api.TerminateProcess(handle,0)
            win32api.CloseHandle(handle)
    except:
        pass

    time.sleep(1)
    print("Opening Client")

    #os.system('cmd /c \"T:\\Riot Games\\League of Legends\\LeagueClient.exe --locale=en_US\"')

    time.sleep(3)



    looping = True
    print("")
    while(looping):
        time.sleep(0.5)
        #try:
        newClient.getDC()

        checkX = int((newClient.width / 100) * 34.84)
        checkY = int((newClient.height / 100) * 95.13)

        px = newClient.dc.GetPixel(checkX, checkY)
        pixelColor = []
        r = px & 0xff
        g = px >> 8 & 0xff
        b = px >> 16 & 0xff

        if (not(pixelColor == [r, g, b])):
            pixelColor = [r, g, b]

        print(checkX, checkY, " - ", pixelColor)

        if(pixelColor == [205, 190, 145]):
            looping = False
        #except:
            #print("Pass")
            #pass
    
    time.sleep(1)

    newClient.Click(newClient.Buttons.Cancel[0], newClient.Buttons.Cancel[1])

    time.sleep(2)

def gamingLoop():
    games_played = 0
    while(games_played < 2):
        setup()
        main()
        games_played += 1
        goToLobby()
    
    now = datetime.now()
    file = open('bot_log.txt', 'a')
    file.write(now.strftime("%d/%m/%Y") + "  -  Games played: " + str(games_played) + "\n")
    file.close()

if __name__ == '__main__':    
    s = random.randint(10, 35)
    windowName = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(s))
    ctypes.windll.kernel32.SetConsoleTitleW(windowName)
    time.sleep(1)

    gamingLoop()
    #goToLobby()