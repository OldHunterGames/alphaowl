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
                child.slave_stance = 'Forced'
                child.skill('coding').training = True
                child.skill('coding').expirience = True
                child.skill('coding').specialisation = True           
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
            $ child.skill('coding').training = True
            $ child.skill('coding').expirience = True
        "ЗОЖ. Брусья-брусья-турнички. Качалочка.":
            $ child.skill('sports').training = True
            $ child.skill('sports').expirience = True
        "Тусуюсь с друзьями.":
            $ child.skill('conversation').training = True
            $ child.skill('conversation').expirience = True
        "Блядую по черному. Молодость всего одна.":
            $ child.skill('sex').training = True
            $ child.skill('sex').expirience = True
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
        "Конечно. Надо делать уроки чтобы мамуля мной гордилась.":
            $ child.slave_stance = 'Willing'
        "Конечно. Это - норма.":
            $ child.slave_stance = 'Accustomed'        
        "Ну что делать? Сяду. А то батя ремня всыпет.":
            $ child.slave_stance = 'Forced'    
        "Я скажу - женщина, пиздуй на кухню и принеси мне сырных подушечек.":
            $ child.slave_stance = 'Rebellious'
            
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
        needs = child.show_needs()
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
     Нужды: \n[needs]\n
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
        resource = getattr(character, res_to_use) if res_to_use else 0
    if failed:
        return resource, determination, sabotage
    menu:
        'Сделать спустя рукава':
            $ resource = False
            $ determination = False
        'Работать хорошо' if resource > 0:
            $ resource = True
            $ determination = False
        'Сделать волевым усилием' if character.determination > 0:
            $ resource = False
            $ determination = True
        'Выложиться полностью' if resource > 0 and character.determination > 0:
            $ resource = True
            $ determination = True
        'Саботировать':
            $ resource = False
            $ determination = False
            $ sabotage = True
    return resource, determination, sabotage
label lbl_check_result(result=0):
    'Результат проверки: [result]'
    return
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
