import time
import keyboard
from pymem import Pymem
from Rating.world import getHealthPercentage
from target import select_closest_target, is_alive, monsterHurtable
from world import find_champion_pointers, find_game_time, find_local_net_id, find_view_proj_matrix, read_object, world_to_screen, find_object_names, find_target_pointers, update_target_info
from champion_stats import ChampionStats
from constants import PROCESS_NAME

class Jungle:
    Side = "blueSide"
    bluebuff = None
    gromp = None
    wolves = None
    raptors = None
    redbuff = None
    krugs = None

def jungleSetup():    
    blueSide = Jungle()
    blueSide.bluebuff = [3748.0, 8048.0, 52.006439208984375, 1718, 930]
    blueSide.gromp = [2192.0, 8454.0, 51.77732849121094, 1691, 923]
    blueSide.wolves = [3692.0, 6312.0, 52.46904754638672, 1717, 960]

    blueSide.raptors = [7152.0, 5212.0, 48.527000427246094, 1777, 979]       
    blueSide.redbuff = [7496.0, 3996.0, 54.83290100097656, 1783, 1000]
    blueSide.krugs = [8476.0, 2490.0, 50.30636978149414, 1800, 1026]
    
    redSide = Jungle()
    redSide.bluebuff = [11186.0, 6950.0, 51.721317291259766, 1847, 949]
    redSide.gromp = [12628.0, 6428.0, 51.71710205078125, 1872, 958]
    redSide.wolves = [11072.0, 8396.0, 60.22582244873047, 1845, 924]

    redSide.raptors = [7726.0, 9670.0, 52.18537139892578, 1787, 902]        
    redSide.redbuff = [7324.0, 11000.0, 56.859886169433594, 1780, 879]
    redSide.krugs = [6460.0, 12274.0, 56.47679901123047, 1765, 857]
    
    return blueSide, redSide


def getJunglePath(Side, view_proj_matrix, width, height, i):
    pathing = [Side.bluebuff, Side.gromp, Side.wolves, None, Side.raptors, Side.redbuff, Side.krugs]
    path = pathing[i]

    x, y = path[3], path[4]
    #print(x, y)
    return path

def pathToCamps(Side, redSide, blueSide, junglingIterator, view_proj_matrix, width, height, walker, champion_stats, active_champion, game_time):  
    cameraLocked = True
    pathing = True
    last_pos = None
    breaksafe = 0
    
    mem = Pymem(PROCESS_NAME)
    champion_pointers = find_champion_pointers(mem, champion_stats.names())

    if(walker.checkRecalled(mem, champion_pointers)):
        junglingIterator = 0
        Side = blueSide
        clearing = False
    else: 
        clearing = True

    path = getJunglePath(Side, view_proj_matrix, width, height, junglingIterator) #mejorar
    pathX, pathY = path[3], path[4]
    walker.walk(pathX, pathY, game_time)
    
    if(cameraLocked == False):
            keyboard.press_and_release('y')
            cameraLocked = False
            
    while(pathing == True and breaksafe != 5):
        
        champions = [read_object(mem, pointer) for pointer in champion_pointers]
        net_id_to_champion = {c.network_id: c for c in champions}
        local_net_id = find_local_net_id(mem)
        active_champion = net_id_to_champion[local_net_id]
        view_proj_matrix, width, height = find_view_proj_matrix(mem)
        game_time = find_game_time(mem)

        pos = [active_champion.x, active_champion.y, active_champion.z, pathX, pathY]
        #print(pos)

        if(pos == path):
            print("ARRIVED")
            if(clearing == True):
                if(cameraLocked):
                    keyboard.press_and_release('y')
                    cameraLocked = False
                objectPointers = find_object_names(mem)
                entities = [read_object(mem, pointer) for pointer in objectPointers]

                targetsLeftBool = True
                targetsLeft = 0

                checkedThreeTimes = False
                checkedTimes = 0

                #if (getHealthPercentage(active_champion.health, active_champion.max_health) < 20):  #Continue
                #    walker.recall()

                while(targetsLeftBool and not checkedThreeTimes):

                    try:
                        objectPointers = find_object_names(mem)
                        entities = [read_object(mem, pointer) for pointer in objectPointers]
                    except: 
                        print("no object pointers/entities")

                    targets = select_closest_target(active_champion, entities, champion_stats.names())
                    targetsLeft = len(targets) - 1
                    #print("Targets left: ", targetsLeft)
                    if(targetsLeft == -1):
                        if(checkedThreeTimes == False):
                            if(checkedTimes < 3):
                                print("Checked Times: ", checkedTimes)
                                checkedTimes += 1
                                time.sleep(0.1)
                            else:
                                checkedThreeTimes = True
                                print("No Camp available")

                    if(targetsLeft > -1):
                        targetNames = []

                        for target in targets:
                            targetNames.append(target.name)
                        #print("\n\n")
                        #print(targetNames)
                        
                        target_pointers, target_pointer_names = find_target_pointers(mem, targetNames)
                        #print(target_pointers, target_pointer_names)
                        
                        index = targetNames.index(min(targetNames, key=len))
                        
                        target = targets[index]
                        print("Targeting: ", target.name)
                        
                        #index = target_pointer_names.index(target.name)
                        index = target_pointer_names.index(target.name)
                        target_pointer = target_pointers[index]

                        targetX, targetY = world_to_screen(view_proj_matrix, width, height, target.x, target.z, target.y)
                        
                        #print("Clearing...")
                        walker.walk(targetX, targetY, game_time)
                        if(active_champion.mana > 200):
                            walker.cast(active_champion, targetX, targetY, 'q')

                        monsterAlive = is_alive(target)
                        monsterHealth = target.health

                        lastMonsterHealth = 999999
                        monsterHealthChecks = 0
                        #temp, target_pointer_updated = find_target_pointers(mem, targetNames) #sleepy
                        while((monsterAlive == True) and (monsterHealth > 0.1) and (monsterHealthChecks < 3)):
                            print(monsterHealth)
                            if(monsterHealth == lastMonsterHealth and lastMonsterHealth != None):
                                print("monsterHealthChecks:", monsterHealthChecks)
                                monsterHealthChecks += 1
                            else:
                                monsterHealthChecks = 0
                                
                            time.sleep(1)
                            lastMonsterHealth = monsterHealth
                            try:
                                updatedTarget = update_target_info(mem, target_pointer)
                                monsterAlive = is_alive(updatedTarget)
                                monsterHealth = updatedTarget.health
                                
                                updatedTargetX, updatedTargetY = world_to_screen(view_proj_matrix, width, height, updatedTarget.x, updatedTarget.z, updatedTarget.y)
                                walker.walk(updatedTargetX, updatedTargetY, game_time)

                            except: 
                                print("updateHealth bug")
                                print(target_pointer, " - ", target_pointers)
                                monsterHealthChecks += 3
                            #print(updatedTarget.health)
                            if(monsterHealth < 0.1):
                                monsterAlive = False

                        if(monsterHealthChecks == 4):
                            print("monsterHealthCheck bug")

                        checkedTimes = 0
                        
                        
                        # objectPointers = find_object_names(mem)
                        # entities = [read_object(mem, pointer) for pointer in objectPointers]

                        # targets = select_closest_target(active_champion, entities, champion_stats.names())
                        # targetsLeft = len(targets) - 1

                        print(target.name + " cleared")
                        time.sleep(0.1)
                pathing = False
                print("")
                if(cameraLocked == False):
                        keyboard.press_and_release('y')
                        cameraLocked = not cameraLocked
            else:
                junglingIterator = 3
                Side = redSide
                pathing = False

        elif(pos == last_pos):    
            walker.walk(pathX, pathY, game_time)
            breaksafe += 1
            if(breaksafe == 5):
                #print("BREAKING")
                print(pos)

        
        time.sleep(0.33)
        last_pos = pos

    time.sleep(0.1)

#def clearCamp(walker, targetX, targetY, target, game_time, active_champion):