import time
import mouse
import keyboard
from pymem import Pymem
from world import find_champion_pointers, find_game_time, find_local_net_id, find_view_proj_matrix, read_object, world_to_screen, world_to_minimap, find_object_names
from champion_stats import ChampionStats
from constants import PROCESS_NAME

from win32gui import GetWindowText, GetForegroundWindow

class Walker:
    def __init__(self, mem):
        self.mem = mem
        game_time = find_game_time(self.mem)
        self.can_attack_time = game_time
        self.can_move_time = game_time

    def walk(self, x, y, game_time):
        if (GetWindowText(GetForegroundWindow()) == "League of Legends (TM) Client"):
            stored_x, stored_y = mouse.get_position()
            mouse.move(int(x), int(y))
            mouse.right_click()
            time.sleep(0.01)
            game_time = find_game_time(self.mem)
            mouse.move(stored_x, stored_y)
            # MOVE_CLICK_DELAY = 0.05
            # self.can_move_time = game_time + MOVE_CLICK_DELAY
            #print("walking to ", x, y)
            #time.sleep(0.01)
    
    @staticmethod
    def cast(active_champion, x, y, spell):
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

        #active_champion.spells[spellIndex[1]] <= game_time:
        #    spellOffCooldown = True

        if x is not None and y is not None:
            if(spellOffCooldown == True):
                stored_x, stored_y = mouse.get_position()
                mouse.move(int(x), int(y))
                keyboard.press_and_release(spell)
                time.sleep(0.01)
                mouse.move(stored_x, stored_y)

    
    def recall(self):
        keyboard.press_and_release('b')
        print("Recalling")
        time.sleep(8.5)
        time.sleep(0.5)
        

    @staticmethod
    def checkRecalled(mem, champion_pointers):
        recalled = [394.0, 462.0, 182.13250732421875]
        #print("checking")

        champions = [read_object(mem, pointer) for pointer in champion_pointers]
        net_id_to_champion = {c.network_id: c for c in champions}
        local_net_id = find_local_net_id(mem)
        active_champion = net_id_to_champion[local_net_id]

        #print(active_champion.x, recalled[0], active_champion.y, recalled[1], active_champion.z, recalled[2])
        if(active_champion.x == recalled[0] and active_champion.y == recalled[1] and active_champion.z == recalled[2]):
            print("Recalled")
            return True
        else:
            return False
