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

    
# Игра начинается здесь.
label start:
    
    define gray = Solid("#ccc")
    show image gray as bg
    $ game.mode = 'mom'
    $ game.player = mother
    $ player = game.player
    $ player.player_controlled = True 
    #call evn_init
    call label_quiz
    
    return
    
label label_quiz:
            
    menu:
        "Ты мальчик или девочка-внутри?"
        "(я не человек уже, я разработчик нахуй)":
            $ child.gender = "male"
            $ child.age = "adolescent"
            $ child.alignment['Orderliness'] = "Conformal"
            $ child.alignment['Activity'] = "Resonable"
            $ child.alignment['Morality'] = "Selfish"
            $ child.slave_stance = 'Forced'
            $ child.skill('coding').training = True
            $ child.skill('coding').expirience = True
            $ child.skill('coding').specialisation = True           
            $ game.player = child
            $ player = game.player
            $ player.player_controlled = True    
            jump label_new_day
        "Я самец - даже не смей сомневаться!":
            $ child.gender = "male"
        "Раскусил, дай мне платице...":
            $ child.gender = "female"     
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
            $ pass
        "ЗОЖ. Брусья-брусья-турнички. Качалочка.":
            $ pass
        "Тусуюсь с друзьями.":
            $ pass
        "Блядую по черному. Молодость всего одна.":
            $ pass
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
            
    $ alignment = child.alignment['Orderliness'] + child.alignment['Activity'] + child.alignment['Morality'] 
    "Твой алаймент: [alignment]"

    menu:
        "Кем ты будешь управлять?"
        "Собой":
            $ game.mode = 'son'
            $ game.player = child
            $ player = game.player
            jump label_new_day
            
        "Своей мамкой":
            $ game.mode = 'mom'
            jump label_new_day

    return

label label_new_day:
    $ study = game.choose_study()
    "Неделя номер [game.time]"
    
    $ gt = game.new_turn()

    $ game.end_turn_event()
    $ player.schedule.add_action('homework')
    if game.mode == 'son':
        call lbl_son_manage
    else:
        call lbl_mom_manage

    return        

label lbl_owl_info:
    python:
        job = player.job['name']
        txt = "Настроение: " + str(player.mood()) + "\n Подчинение: " + str(player.obedience())
    "[txt] \n Выносливость: [child.stamina]   |   Воля: [child.willpower]  |  Концентрация: [child.concentration]  |  Очарование: [child.glamour] \n
     Тэнге: [game.tenge] \n
     Условия сна: [child.accommodation]  |  Занятость: [job]       \n
     \n"
    
    return

label lbl_skill_check(character=player, skill_to_use=None, res_to_use=None, determination=False):
    python:
        sabotage = False
        determination = False
        failed = False
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
label lbl_skill_check_result(skill=None, result=0):
    'Вы использовали скил [skill]'
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
