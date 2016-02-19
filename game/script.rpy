init -10 python:
    sys.path.append(renpy.loader.transfn("scrypts"))
    from obj_character import *
    from owl_engine import *
    from events import *
    from schedule import *

init python:
    
    renpy.block_rollback()
    game = Engine()
    child = game.child
    mother = game.mother
    child.master = mother
    
    child.set_relations(mother)
    mother.set_relations(child)
    Schedule(mother)
    Schedule(child)
    
# Игра начинается здесь.
label start:
    
    define gray = Solid("#ccc")
    show image gray as bg
    call evn_init
    call label_quiz
    
    return
    
label label_quiz:

    menu:
        "Ты мальчик или девочка-внутри?"
        "(я не человек уже, я разработчик нахуй)":
            $ child.gender = "male"
            $ child.needs["debauch"] = {"level": 3, 'shift': 0, "status": "relevant"}
            $ child.age = "adolescent"
            $ child.alignment['Orderliness'] = "Conformal"
            $ child.alignment['Activity'] = "Resonable"
            $ child.alignment['Morality'] = "Selfish"
            $ child.slave_stance = 'Forced'
            $ game.player = child
            $ player = game.player
            $ player.player_controlled = True    
            jump label_new_day
        "Я самец - даже не смей сомневаться!":
            $ child.gender = "male"
            $ child.needs["debauch"] = {"level": 3,'shift': 0, "status": "relevant"}
        "Раскусил, дай мне платице...":
            $ child.gender = "female"     
            $ child.needs["care"] = {"level": 3,'shift': 0, "status": "relevant"}
            $ child.firstname = "Тошка"
            $ child.surname = "Сычева"
            
    menu:
        "Волосики уже везде выросли?"
        "Маaaaм, меня комплюктор про странное спрашивает!":
            $ child.age = "junior"
        "Я не школота. Факт (правда)":
            $ child.age = "adolescent"
        "Я олдфаг. Мои муди седы как снега на склоне фудзи...":
            $ child.age = "mature"        
            
    menu:
        "Давай вспомним твои школьные годы. Много двоек было за прогулы?"
        "Никаких прогулов. У меня расписание чёткое.":
            $ child.alignment['Orderliness'] = "Lawful"
            $ child.needs["care"] = {"level": 3,'shift': 0, "status": "relevant"}
        "А чё я? Все прогуливали и я прогуливал.":
            $ child.alignment['Orderliness'] = "Conformal"
        "Делаю что хочу. Я вообще не контролируемый!":
            $ child.alignment['Orderliness'] = "Chaotic"
            $ child.needs["independence"] = {"level": 3,'shift': 0, "status": "relevant"}
            
    menu:
        "Новая знакомая в скайпе предлагает тебе зависнуть с ней и ещё двумя подругами на ночь, на незнакомой хате в Медвеково. Твои действия?"
        "Пожаловаться на спам. Скрыть.":
            $ child.alignment['Activity'] = "Timid"
            $ child.needs["approval"] = {"level": 3,'shift': 0, "status": "relevant"}
        "В Медведково? Ну хрееееееен знает...":
            $ child.alignment['Activity'] = "Resonable"
        "Я за любой кипеш, кроме голодовки!":
            $ child.alignment['Activity'] = "Ardent"
            $ child.needs["trill"] = {"level": 3,'shift': 0, "status": "relevant"}
            
    menu:
        "Идёшь по улице. Кушаешь вкусный бутер с колбаской. К тебе подбегает няшный котик и просит кусочек."
        "Пнуть блохастого. Это моя колбаса. Плохая киса!":
            $ child.alignment['Morality'] = "Evil"
            $ child.needs["power"] = {"level": 3,'shift': 0, "status": "relevant"}
        "Пройти мимо. Пусть бабки подъездные его прикармливают.":
            $ child.alignment['Morality'] = "Selfish"
        "Конечно дать колбаски. Да я бы и собаке...":
            $ child.alignment['Morality'] = "Good"
            $ child.needs["altruism"] = {"level": 3,'shift': 0, "status": "relevant"}            
    
    menu:
        "А что если мамка уроки делать заставит?"
        "Конечно. Надо делать уроки чтобы мамуля мной гордилась.":
            $ child.slave_stance = 'Willing'
        "Конечно. Это - норма.":
            $ child.slave_stance = 'Accustomed'        
        "Ну что делать? Сяду. А то батя ремня всыпет.":
            $ child.slave_stance = 'Forced'    
        "Я скажу - женщина, пиздуй на кухню и принеси мне сырных подушечек.":
            $ child.slave_stance = 'Rebellious'
            
    $ alignment = child.alignment['Orderliness'] + child.alignment['Activity'] + child.alignment['Morality'] 
    "Твой алаймент: [alignment]"

    menu:
        "Кем ты будешь управлять?"
        "Собой":
            $ game.mode = 'son'
            $ game.player = child
            jump label_new_day
            
        "Своей мамкой":
            $ game.mode = 'mom'
            $ game.player = mother
            jump label_new_day

    return

label label_new_day:
    $ player = game.player
    $ player.player_controlled = True 
    "Неделя номер [game.time]"
    $ txt = player.description() + "\n Настроение: " + str(player.mood()) + "\n Подчинение: " + str(player.obedience())
    "[txt]"
    
    $ gt = game.new_turn()
    $ event = game.end_turn_event()
    
    python:
        for s in persons_schedules:
            persons_schedules[s].use_actions()
    call expression event
    
    if game.mode == 'son':
        call lbl_son_manage
    else:
        call lbl_mom_manage

    return        

label lbl_skill_check(character=player, skill_to_use=None, res_to_use=None, determination=False):
    python:
        sabotage = False
        if character.skill_level(skill_to_use) < 1:
            result_text = "Проверка провалена"
        resource = getattr(character, res_to_use) if res_to_use else 0
    menu:
        'Сделать спустя рукава':
            $ result_text = "Плохо поработал"
        'Работать хорошо' if resource > 0:
            $ resource = True
            $ determination = False
            $ result_text = "Поработал на: "
            $ result_text += str(skill_result)
        'Сделать волевым усилием' if character.determination > 0:
            $ resource = False
            $ determination = True
            $ skill_result = character.use_skill(skill_to_use, res_to_use, determination=True)
            $ result_text = "Волевое усилие прошло на: "
            $ result_text += str(skill_result)
        'Выложиться полностью' if resource > 0 and character.determination > 0:
            $ resource = True
            $ determination = True
            $ skill_result = character.use_skill(skill_to_use, res_to_use, determination=True)
            $ result_text = "Выложился на: "
            $ result_text += str(skill_result)
        'Саботировать':
            $ resource = True
            $ determination = True
            $ sabotage = True
            $ result_text = "Вы саботаровали задание"
    '[result_text]'
    return resource, determination, sabotage
label lbl_resist(effect):
    'Сопротивляться [effect]?'
    menu:
        'Сила воли: [player.willpower], Решимость: [player.determination]'
        'Сила воли':
            return 'willpower'
        'Решимость' if player.determination > 0:
            return 'determination'
        'Нет':
            return False
label lbl_resist_result(effect, success):
    if success:
        'Вы справились с [effect]'
    else:
        'Вы попытались справиться с [effect] но вам не удалось'
    return
label lbl_notify(effect):
    'Вы получили [effect]'

