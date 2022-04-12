import math


def is_clone(target):
    return target.level == 0


def is_alive(target):
    return target.spawn_count % 2 == 0


def hurtable(champion, target):
    return target.team != champion.team and target.targetable and is_alive(target) and target.visibility

def monsterHurtable(champion, target):
    return target.targetable and is_alive(target) and target.visibility


def calculate_effective_damage(damage, resist):
    # todo: consider penetration
    if resist >= 0:
        return damage * 100. / (100. + resist)
    else:
        return damage * (2. - (100. / (100. - resist)))


def basic_attacks_needed(champion, target):
    damage = champion.base_attack + champion.bonus_attack
    effective_damage = calculate_effective_damage(damage, target.armor)
    return target.health / effective_damage


def distance_between(champion, target):
    return math.sqrt((champion.x - target.x)**2 + (champion.y - target.y)**2)


def in_basic_attack_range(stats, champion, target):
    # hitbox edge to edge
    entity_radius = stats.get_radius(target.name) #* target.size_multiplier
    champion_radius = stats.get_radius(champion.name) #* champion.size_multiplier
    return distance_between(champion, target) - entity_radius <= champion.attack_range + champion_radius


def in_spell_range(champion, target, spell_radius):
    # center to center
    return distance_between(champion, target) <= spell_radius


def select_lowest_target(stats, champion, entities):
    # todo: check if champion is stunned
    target = None
    min_autos = None
    for entity in entities:
        if not hurtable(champion, entity):
            continue
        if is_clone(entity):
            continue
        if not in_basic_attack_range(stats, champion, entity):
            continue
        autos = basic_attacks_needed(champion, entity)
        if target is None or 0 < autos < min_autos:
            target = entity

    return target

def select_closest_target(champion, entities, champion_names):
    # todo: check if champion is stunned
    targets = []
    for entity in entities:
        if monsterHurtable(champion, entity):
            #if is_clone(entity):
            #    continue
            if(entity.name[0:4].lower() == "sru_"): 
                if(abs(entity.x - champion.x) < 500 and abs(entity.y - champion.y) < 500 and not (entity.name in champion_names)):
                    targets.append(entity)

    return targets
