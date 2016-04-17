﻿init -10 python:
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
    register_actions()
    child.master = mother

    
# Игра начинается здесь.
label start:
    call init_events
    define gray = Solid("#ccc")
    show image gray as bg
    #call evn_init
    call label_quiz
    
    return
    
label label_quiz:
            
    menu:
        "Ты мальчик или девочка-внутри?"
        "(я не человек уже, я разработчик нахуй)":
            python:
                child.add_feature('male')
                child.add_feature('adolescent')
                child.alignment['Orderliness'] = "Conformal"
                child.alignment['Activity'] = "Resonable"
                child.alignment['Morality'] = "Selfish"
                child.slave_stance = 'forced'
                child.skill('coding').profession()
                child.skill('sex').expert()
                game.player = mother
                player = game.player
                mom = game.mother
                mom.alignment['morality'] = 'evil'
                player.player_controlled = True
                child.set_relations(mother)    
            jump label_new_day
        "Я самец - даже не смей сомневаться!":
            $ child.add_feature('male')
        "Раскусил, дай мне платице...":
            $ child.add_feature('female')     
            $ child.firstname = "Тошка"
            $ child.surname = "Сычева"
            
    menu:
        "Волосики уже везде выросли?"
        "Маaaaм, меня комплюктор про странное спрашивает!":
            $ child.add_feature('junior')
        "Я не школота. Факт (правда)":
            $ child.add_feature('adolescent')
        "Я олдфаг. Мои муди седы как снега на склоне фудзи...":
            $ child.add_feature('mature')       

    menu:
        "Какая твоя самая сильная сторона?"
        "В компах разбираюсь с детства":
            $ child.skill('coding').talent = True
        "Отменное здоровье и энергичность":
            $ child.skill('sports').talent = True
        "Я - душа компании":
            $ child.skill('conversation').talent = True
        "Гиперсексуальность":
            $ child.skill('sex').talent = True
        "Я эксперт по ВСЕМ вопросам. Диванный.":
            $ pass

    menu:
        "Чем по жизни занимаешься?"
        "Кодю, компилю, хакаю. Не палюсь.":
            $ child.skill('coding').expert()
        "ЗОЖ. Брусья-брусья-турнички. Качалочка.":
            $ child.skill('sports').expert()
        "Тусуюсь с друзьями.":
            $ child.skill('conversation').expert()
        "Блядую по черному. Молодость всего одна.":
            $ child.skill('sex').expert()
        "Капчую. В дотан шпилю. Всё такое...":
            $ pass
            
    menu:
        "Давай вспомним твои школьные годы. Много двоек было за прогулы?"
        "Никаких прогулов. У меня расписание чёткое.":
            $ child.alignment['Orderliness'] = "Lawful"
        "А чё я? Все прогуливали и я прогуливал.":
            $ child.alignment['Orderliness'] = "Conformal"
        "Делаю что хочу. Я вообще не контролируемый!":
            $ child.alignment['Orderliness'] = "Chaotic"
            
    menu:
        "Новая знакомая в скайпе предлагает тебе зависнуть с ней и ещё двумя подругами на ночь, на незнакомой хате в Медвеково. Твои действия?"
        "Пожаловаться на спам. Скрыть.":
            $ child.alignment['Activity'] = "Timid"
        "В Медведково? Ну хрееееееен знает...":
            $ child.alignment['Activity'] = "Resonable"
        "Я за любой кипеш, кроме голодовки!":
            $ child.alignment['Activity'] = "Ardent"
            
    menu:
        "Идёшь по улице. Кушаешь вкусный бутер с колбаской. К тебе подбегает няшный котик и просит кусочек."
        "Пнуть блохастого. Это моя колбаса. Плохая киса!":
            $ child.alignment['Morality'] = "Evil"
        "Пройти мимо. Пусть бабки подъездные его прикармливают.":
            $ child.alignment['Morality'] = "Selfish"
        "Конечно дать колбаски. Да я бы и собаке...":
            $ child.alignment['Morality'] = "Good"          
    
    menu:
        "А что если мамка уроки делать заставит?"
        "Конечно. Это - норма.":
            $ child.slave_stance = 'accustomed'        
        "Ну что делать? Сяду. А то батя ремня всыпет.":
            $ child.slave_stance = 'forced'    
        "Я скажу - женщина, пиздуй на кухню и принеси мне сырных подушечек.":
            $ child.slave_stance = 'rebellious'
            
    $ alignment = child.alignment['Orderliness'] +' '+ child.alignment['Activity'] +' '+ child.alignment['Morality'] 
    "Твой алаймент: [alignment]"

    menu:
        "Кем ты будешь управлять?"
        "Собой":
            $ game.mode = 'son'
            $ game.player = child
            $ player = game.player
            $ player.player_controlled = True
            $ child.set_relations(mother)
            jump label_new_day
            
        "Своей мамкой":
            $ game.mode = 'mom'
            $ game.player = mother
            $ player = game.player
            $ player.player_controlled = True
            $ child.set_relations(mother)           
            jump label_new_day

    return

label label_new_day:
    $ study = game.choose_study()
    $ game.child.rest()
    $ game.mother.rest()
    "Неделя номер [game.time]"
    $ gt = game.new_turn()
    $ game.evn_skipcheck = False

    $ game.end_turn_event()
    $ game.evn_skipcheck = True
    if player == game.child:
        call lbl_son_manage
    else:
        call lbl_mom_manage

    return        

label lbl_owl_info:
    python:
        alignment = child.alignment['Orderliness'] +' '+ child.alignment['Activity'] +' '+ child.alignment['Morality'] 
        job = child.job['name']
        desu = child.description()
        needs_overflow = child.show_needs('overflow')
        needs_frustrated = child.show_needs('frustrated')        
        needs_tense = child.show_needs('tense')
        needs_relevant = child.show_needs('relevant')
        needs_statisfied = child.show_needs('satisfied')
        taboos = child.show_taboos()
        features = child.show_features()
        focus = child.show_focus()
        rel = child.relations(mom).description()
        txt = "Настроение: " + str(child.mood()) + " | Подчинение: " + str(child.obedience())
    "[txt] \n Выносливость: [child.stamina]   |   Воля: [child.willpower]  |  Концентрация: [child.concentration]  |  Очарование: [child.glamour] \n
     Тэнге: [game.tenge] \n
     Условия сна: [child.accommodation]  |  Занятость: [job]       \n
     Характер: [alignment]\n
     Отношение: [rel]\n
     Фокус: [focus]\n
     Фрустрации: [needs_frustrated]\n
     Напряжения: [needs_tense]\n
     Актуальные нужды: [needs_relevant]\n
     Удовлетворённые: [needs_statisfied]\n          
     Пресыщения: [needs_overflow]\n     
     Табу: \n[taboos]\n
     Особенности: \n[features]\n
     \n"
     # 

    return

label lbl_skill_check(character=player, skill_to_use=None, res_to_use=None, determination=False):
    python:
        sabotage = False
        determination = False
        failed = False
        if skill_to_use:
            if character.skill(skill_to_use).level < 1:
                failed = True
    if failed:
        return vigor, determination, sabotage
    menu:
        'Сделать спустя рукава':
            $ vigor = False
            $ determination = False
        'Работать хорошо' if character.vigor > 0:
            $ vigor = True
            $ determination = False
        'Сделать волевым усилием' if character.determination > 0:
            $ vigor = False
            $ determination = True
        'Выложиться полностью' if character.vigor > 0 and character.determination > 0:
            $ vigor = True
            $ determination = True
        'Саботировать':
            $ vigor = False
            $ determination = False
            $ sabotage = True
    return vigor, determination, sabotage
label lbl_check_result(result=0):
    'Результат проверки: [result]'
    return
label lbl_resist(effect):
    if player.vigor < 1 and player.determination < 1:
        return
    'Сопротивляться [effect]?'
    menu:
        'Энергия: [player.vigor], Решимость: [player.determination]'
        'Энергия' if player.vigor > 0:
            return 'vigor'
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
    return
