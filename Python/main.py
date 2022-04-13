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
    
    

def setup(): 
    client = Client()
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
    walker = Walker(mem)
    champion_pointers = find_champion_pointers(mem, champion_stats.names())
    print(champion_pointers)

    print(champion_stats.names())

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
            active_champion = updateActiveChampion(mem, active_champion_pointer)
            gameEndedCheck = checkIfGameEnded(mem, active_champion_pointer)

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

        if(gameEndedCheckTimes > 7):
            print("GAME ENDED")
            gameEnded = True
        else: 
            time.sleep(1)
            gameEndedCheck = checkIfGameEnded(mem, active_champion_pointer)
            gameEndedCheckTimes += 1
    print("now what......")

    

if __name__ == '__main__':    
    s = random.randint(10, 35)
    windowName = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(s))
    ctypes.windll.kernel32.SetConsoleTitleW(windowName)
    time.sleep(1)
    setup()
    main()
