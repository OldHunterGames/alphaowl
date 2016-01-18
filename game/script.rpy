init -10 python:
    sys.path.append(renpy.loader.transfn("scrypts"))
    from obj_character import *
    from owl_engine import *

init python:
    renpy.block_rollback()
    game = Engine()
    player = game.player
    
# Игра начинается здесь.
label start:
    
    define gray = Solid("#ccc")
    show image gray as bg
    call label_quiz
    
    return
    
label label_quiz:

    menu:
        "Ты мальчик или девочка-внутри?"
        "Я самец - даже не смей сомневаться!":
            $ player.gender = "male"
            $ player.needs["debauch"] = {"level": 3, "status": "relevant"}
        "Раскусил, дай мне платице...":
            $ player.gender = "female"     
            $ player.needs["care"] = {"level": 3, "status": "relevant"}
            $ player.firstname = "Тошка"
            $ player.surname = "Сычева"
            
    menu:
        "Волосики уже везде выросли?"
        "Маaaaм, меня комплюктор про странное спрашивает!":
            $ player.age = "junior"
        "Я не школота. Факт (правда)":
            $ player.age = "adolescent"
        "Я олдфаг. Мои муди седы как снега на склоне фудзи...":
            $ player.age = "mature"        
            
    menu:
        "Давай вспомним твои школьные годы. Много двоек было за прогулы?"
        "Никаких прогулов. У меня расписание чёткое.":
            $ player.alignment['stability'] = "Lawful"
            $ player.needs["care"] = {"level": 3, "status": "relevant"}
        "А чё я? Все прогуливали и я прогуливал.":
            $ player.alignment['Orderliness'] = "Conformal"
        "Делаю что хочу. Я вообще не контролируемый!":
            $ player.alignment['Orderliness'] = "Chaotic"
            $ player.needs["independence"] = {"level": 3, "status": "relevant"}
            
    menu:
        "Новая знакомая в скайпе предлагает тебе зависнуть с ней и ещё двумя подругами на ночь, на незнакомой хате в Медвеково. Твои действия?"
        "Пожаловаться на спам. Скрыть.":
            $ player.alignment['Activity'] = "Timid"
            $ player.needs["approval"] = {"level": 3, "status": "relevant"}
        "В Медведково? Ну хрееееееен знает...":
            $ player.alignment['Activity'] = "Resonable"
        "Я за любой кипеш, кроме голодовки!":
            $ player.alignment['Activity'] = "Ardent"
            $ player.needs["trill"] = {"level": 3, "status": "relevant"}
            
    menu:
        "Идёшь по улице. Кушаешь вкусный бутер с колбаской. К тебе подбегает няшный котик и просит кусочек."
        "Пнуть блохастого. Это моя колбаса. Плохая киса!":
            $ player.alignment['Morality'] = "Evil"
            $ player.needs["power"] = {"level": 3, "status": "relevant"}
        "Пройти мимо. Пусть бабки подъездные его прикармливают.":
            $ player.alignment['Morality'] = "Selfish"
        "Конечно дать колбаски. Да я бы и собаке...":
            $ player.alignment['Morality'] = "Good"
            $ player.needs["altruism"] = {"level": 3, "status": "relevant"}            
    
    
    $ alignment = player.alignment['Orderliness'] + player.alignment['Activity'] + player.alignment['Morality'] 
    "Твой алаймент: [alignment]"

    menu:
        "Кем ты будешь управлять?"
        "Собой":
            call label_new_day
            
        "Своей мамкой":
            "Низззя"
            jump label_quiz

    return

label label_new_day:
    "Неделя номер [game.time]"
    $ txt = player.description()
    "[txt]"
    
    $ gt = game.new_turn()
    call expression gt

    return        