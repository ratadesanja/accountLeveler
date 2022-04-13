import time
import keyboard
from pymem import Pymem
from target import select_closest_target, is_alive, monsterHurtable
from world import find_champion_pointers, find_game_time, find_local_net_id, find_view_proj_matrix, read_object, world_to_screen, find_object_names, find_target_pointers, update_target_info, getHealthPercentage, updateActiveChampion
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


def getJunglePath(Side, i):
    pathing = [Side.bluebuff, Side.gromp, Side.wolves, None, Side.raptors, Side.redbuff, Side.krugs]
    if(pathing[i] == None):
        path = pathing[i+1]
    else:
        path = pathing[i]

    return path

def pathToCamps(Side, redSide, blueSide, junglingIterator, view_proj_matrix, width, height, walker, champion_stats, game_time, mem, champion_pointers, active_champion_pointer):  
    cameraLocked = True
    pathing = True
    last_pos = None
    breaksafe = 0
    
    #mem = Pymem(PROCESS_NAME)
    #champion_pointers = find_champion_pointers(mem, champion_stats.names())

    if(walker.checkRecalled(mem, active_champion_pointer)):
        junglingIterator = 0
        Side = blueSide
        clearing = False
    else: 
        clearing = True

    path = getJunglePath(Side, junglingIterator)
    pathX = path[3]
    pathY = path[4]
    walker.walk(pathX, pathY)
    
    active_champion = updateActiveChampion(mem, active_champion_pointer)
    
    if(cameraLocked == False):
            keyboard.press_and_release('y')
            cameraLocked = False
    if(getHealthPercentage(active_champion.health, active_champion.max_health) < 15):
        healthy = False
    else: 
        healthy = True

    while(pathing == True and breaksafe != 5):
        
        if(healthy == True):
            champions = [read_object(mem, pointer) for pointer in champion_pointers]
            active_champion = updateActiveChampion(mem, active_champion_pointer)
            game_time = find_game_time(mem)
            view_proj_matrix, width, height = find_view_proj_matrix(mem)

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
                    active_champion = updateActiveChampion(mem, active_champion_pointer)
                    view_proj_matrix, width, height = find_view_proj_matrix(mem)
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
                                    #print("Checked Times: ", checkedTimes)
                                    checkedTimes += 1
                                    time.sleep(0.1)
                                else:
                                    checkedThreeTimes = True
                                    print("No Camp available\n")

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
                            walker.walk(targetX, targetY)

                            
                            if(getHealthPercentage(active_champion.health, active_champion.max_health) < 15):
                                healthy = False
                            else: 
                                healthy = True


                            if(active_champion.mana > 200):
                                time.sleep(0.15)
                                walker.cast(active_champion_pointer, mem, find_game_time(mem), targetX, targetY, 'q')

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
                                    time.sleep(0.1)
                                else:
                                    monsterHealthChecks = 0
                                    
                                time.sleep(1)
                                lastMonsterHealth = monsterHealth
                                try:
                                    updatedTarget = update_target_info(mem, target_pointer)
                                    monsterAlive = is_alive(updatedTarget)
                                    monsterHealth = updatedTarget.health
                                    
                                    updatedTargetX, updatedTargetY = world_to_screen(view_proj_matrix, width, height, updatedTarget.x, updatedTarget.z, updatedTarget.y)
                                    walker.walk(updatedTargetX, updatedTargetY)
                                    
                                    walker.cast(active_champion_pointer, mem,  find_game_time(mem), updatedTargetX, updatedTargetY, 'q')

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
                            if(monsterAlive == False):
                                print(target.name + " cleared")
                            time.sleep(0.1)
                    pathing = False
                    print("")
                    if(cameraLocked == False):
                            keyboard.press_and_release('y')
                            cameraLocked = not cameraLocked
                else:
                    junglingIterator = 4
                    Side = redSide
                    pathing = False

            elif(pos == last_pos):    
                walker.walk(pathX, pathY)
                breaksafe += 1
                if(breaksafe == 5):
                    #print("BREAKING")
                    print(pos)

            
            time.sleep(0.33)
            last_pos = pos
        else:
            
            check = walker.checkRecalled(mem, active_champion_pointer)
            while(check == False):
                walker.castRecall()
                check = walker.checkRecalled(mem, active_champion_pointer)
            
            active_champion = updateActiveChampion(mem, active_champion_pointer)
            
            while(active_champion.health < active_champion.max_health):
                time.sleep(0.5)
                active_champion = updateActiveChampion(mem, active_champion_pointer)
            
            healthy = True
        time.sleep(0.1)

#def clearCamp(walker, targetX, targetY, target, game_time, active_champion):