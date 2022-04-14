import time
import mouse
import keyboard
from pymem import Pymem
from world import find_game_time, updateActiveChampion, getHealthPercentage, getPlayerGold
from champion_stats import ChampionStats
from constants import PROCESS_NAME

from win32gui import GetWindowText, GetForegroundWindow

import shop

class Walker:
    def __init__(self, mem):
        self.mem = mem
        game_time = find_game_time(self.mem)
        self.can_attack_time = game_time
        self.can_move_time = game_time

    def walk(self, x, y):
        if (GetWindowText(GetForegroundWindow()) == "League of Legends (TM) Client"):
            stored_x, stored_y = mouse.get_position()
            mouse.move(int(x), int(y))
            mouse.right_click()
            time.sleep(0.01)
            mouse.move(stored_x, stored_y)
            # MOVE_CLICK_DELAY = 0.05
            # self.can_move_time = game_time + MOVE_CLICK_DELAY
            #print("walking to ", x, y)
            #time.sleep(0.01)
    
    @staticmethod
    def cast(active_champion_pointer, mem, game_time, x, y, spell):
        active_champion = updateActiveChampion(mem, active_champion_pointer)
        spellIndex = None 
        spellOffCooldown = None 

        if spell == 'q':
                spellIndex = 0
        elif spell == 'w':
                spellIndex = 1
        elif spell == 'e':
                spellIndex = 2
        elif spell == 'r':
                spellIndex = 3
        elif spell == 'd':
                spellIndex = 4
        elif spell == 'f':
                spellIndex = 5

        spellManaCost = 50 + (10 * (active_champion.spells[spellIndex].level - 1))

        if(active_champion.mana > spellManaCost and getHealthPercentage(active_champion.health, active_champion.max_health) < 50):

            if(active_champion.spells[spellIndex].cooldown_expire - find_game_time(mem) <= 0):
                spellOffCooldown = True

            else:
                spellOffCooldown = False
            
            if x is not None and y is not None:
                if(spellOffCooldown == True):
                    stored_x, stored_y = mouse.get_position()
                    mouse.move(int(x), int(y))
                    keyboard.press(spell)
                    time.sleep(0.07)
                    keyboard.release(spell)
                    mouse.move(stored_x, stored_y)
                    print("Casted ", spell)

    
    @staticmethod
    def castRecall():
        keyboard.press_and_release('b')
        print("Recalling")
        time.sleep(8.5)
        time.sleep(0.5)

    @staticmethod
    def recall(mem, active_champion_pointer, ShopItemList, inventoryIndex):
        check = Walker.checkRecalled(mem, active_champion_pointer)
        while(check == False):
            Walker.castRecall()
            check = Walker.checkRecalled(mem, active_champion_pointer)


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
                
        time.sleep(0.25)
        if(ShopOpen == True):
            keyboard.press_and_release('p')
            ShopOpen = False
        return inventoryIndex
        

    @staticmethod
    def checkRecalled(mem, active_champion_pointer):
        recalled = [394.0, 462.0, 182.13250732421875]
        #print("checking")

        active_champion = updateActiveChampion(mem, active_champion_pointer)
        

        #print(active_champion.x, recalled[0], active_champion.y, recalled[1], active_champion.z, recalled[2])
        if(active_champion.x == recalled[0] and active_champion.y == recalled[1] and active_champion.z == recalled[2]):
            print("Recalled")
            return True
        else:
            return False
