import time
import keyboard
from pymem import Pymem
from world import find_champion_pointers, find_game_time, find_local_net_id, find_view_proj_matrix, read_object, world_to_screen, find_object_names, getPlayerGold, find_active_champion_pointer, updateActiveChampion
from champion_stats import ChampionStats
from target import select_lowest_target
from constants import PROCESS_NAME
import jungle
from walk import Walker

import ctypes
import string
import random
from setup import Client
import shop
import levelup
    
    

def setup(): 
    s = random.randint(10, 35)
    windowName = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(s))
    ctypes.windll.kernel32.SetConsoleTitleW(windowName)

    client = Client()

    time.sleep(2)
    
    keyboard.press_and_release('y')
    
def main():
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

    # while(True):
    #     active_champion = updateActiveChampion(mem, active_champion_pointer)
    #     print(active_champion.x, active_champion.y)
    #     time.sleep(1)

    stopping = False
    once = True
    while stopping == False:       
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

        # if(recalling):
        #     walker.recall()
        #     check = walker.checkRecalled(mem, champion_pointers)
        #     while(not check):
        #         walker.recall()
        #         check = walker.checkRecalled(mem, champion_pointers)

        #         time.sleep(0.25)
        #         ShopOpen = False

        #         buying = True
        #         print("Buying...")
        #         while(buying):
        #             if(inventoryIndex < 6):
        #                 if(getPlayerGold(mem) > ShopItemList[inventoryIndex].cost):
        #                     inventoryIndex, ShopOpen = shop.buyItem(ShopItemList, inventoryIndex, ShopOpen)
        #                     #print(inventoryIndex)
        #                     inventoryIndex += 1

        #                     time.sleep(0.25)

        #                 else: 
        #                     if(ShopOpen == True):
        #                         keyboard.press_and_release('p')
        #                         ShopOpen = not ShopOpen

        #             buying = False
            

        #try:
        #    targetTemp = select_closest_target(active_champion, objectNames)
        #    print(targetTemp[len(targetTemp)])
        #except:
            #print("Target not found")
        #    continue
        #time.sleep(0.5)
        
        # q = active_champion.spells[0]
        # q = q[1]

        # if(q <= game_time):
        #     print("Off cooldown", q, game_time)
        # else:
        #     print("On cooldown")

        # print(q, game_time)
        #print(active_champion.spells[0])
        #print(game_time, " - ", game_time/60)
        #time.sleep(0.5)

        lastLevel = levelup.tryToLevel(lastLevel, active_champion.level, levelingPath)

        if(active_champion.level > 2):
            #keyboard.press_and_release('y')
            while jungling:
                jungle.pathToCamps(Side, redSide, blueSide, junglingIterator, view_proj_matrix, width, height, walker, champion_stats, find_game_time(mem), mem, champion_pointers, active_champion_pointer)
                lastLevel = levelup.tryToLevel(lastLevel, active_champion.level, levelingPath)
                
                if(Side == redSide and junglingIterator == 2):
                    junglingIterator = 3
                    walker.recall()
                    check = walker.checkRecalled(mem, active_champion_pointer)
                    while(check == False):
                        walker.recall()
                        check = walker.checkRecalled(mem, active_champion_pointer)
                        #if(active_champion.gold > 1):
                        #    time.sleep(10)
                    
                    time.sleep(0.25)
                    ShopOpen = False

                    buying = True
                    print("Buying...")
                    while(buying):
                        if(inventoryIndex < 6):
                            if(getPlayerGold(mem) > ShopItemList[inventoryIndex].cost):
                                inventoryIndex, ShopOpen = shop.buyItem(ShopItemList, inventoryIndex, ShopOpen)
                                #print(inventoryIndex)
                                inventoryIndex += 1

                                time.sleep(0.25)

                            else: 
                                buying = False
                        else: 
                            buying = False
                            
                    if(ShopOpen == True):
                        keyboard.press_and_release('p')
                        ShopOpen = False
                    

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


if __name__ == '__main__':
    time.sleep(1)
    setup()
    main()
