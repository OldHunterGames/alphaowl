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

label lbl_son_manage:
    
    menu:
        "Сосредоточиться на..." if player.ap > 0:
            $ player.ap -= 1
            jump lbl_son_manage
        "Конец недели":
            $ player.rest()
            jump label_new_day
    
    return

label lbl_mom_manage:
    menu:
        "Питание":
            call lbl_food_rules
        "Бытовые условия":
            call lbl_accomodation_rules
        "После учебы":
            call lbl_job_rules
        "В выходные":
            # call lbl_leisure_rules          
            "Упс. Не готово"
            $ pass
        "Воспитание" if game.mode == 'mom':
            call lbl_discipline
        "Магазин":
            call lbl_shop
        "Конец недели":
            $ player.rest()
            jump label_new_day
        "Проверка":
            call lbl_skill_check(skill_to_use="coding", res_to_use="concentration")
            
    jump lbl_mom_manage
    
    return

label lbl_food_rules:
    menu:
        "Тётя Срака читала - кушать надо сколько душа просит":
            $ player.ration['amount'] = "unlimited" 
        "Надо чтобы недораха!":
            $ player.ration['amount'] = "limited" 
            call lbl_food_limit
        "У Сыченьки то фигуры нет совсем...":
            $ player.ration['amount'] = "regime" 
            call lbl_diet
        "А ты вот посиди без етьбы, знать будешь как матери губить!":
            $ player.ration['amount'] = "starvation"   
            $ player.ration['food_type'] = "forage"   
            $ player.ration['target'] = 0           
            $ player.ration['limit'] = None
            jump lbl_mom_manage
    
    menu:
        "Вот покушай ка Сычулька..."
        "Совего, с огорода то. Витамины!":
            $ player.ration['food_type'] = "sperm" 
        "Тёпленького похлебай, домашнего. С хлебушком.":
            $ player.ration['food_type'] = "caned" 
        "Мивины с маянезиком.":
            $ player.ration['food_type'] = "dry" 
        "В столовой вашей, я денежку тебе дам.":
            $ player.ration['food_type'] = "cosine"         

    return

    
label lbl_food_limit:
    $ player.ration['limit'] = int(renpy.input("Сколько раз за неделю мамка будет покупать еду?"))
        
    return


label lbl_shop:
    menu:
        'Какус "Антирадиационный" (10 тенгэ)' if "cactus" not in game.mom_stuff:
            python:
                if game.tenge >= 10:
                    txt = "КАНПУКТЕР ОБЛУЧАЕТ РАДИАЦИЕЙ \n@\nСЫЧА, СРОЧНО ПОСТАВЬ КАКТУС К ЭКРАНУ\n@\nУЧОНЫЕ ПО РЕН-ТВ ТОЛЬКО ЧТО СКАЗАЛИ\n"
                    game.mom_stuff.append("cactus")
                    game.tenge -= 10
                else:
                    txt = "ПРИХОДИШЬ В МАГАЗ\n @\n И ДАЖЕ СРАНЫЙ КАКТУС НЕ МОЖЕШЬ КУПИТЬ\n @\n ТЕНГЕ НЕ ХВАТАЕТ"
        'Сервиз "Мойхрусталь" (10 тенгэ)' if "service" not in game.mom_stuff:
            python:
                if game.tenge >= 10:
                    txt = "ХРУСТАЛЬ - ЭТО ТВОЕ ПРИДАНОЕ. ПОСТАВЬ В СЕРВАНТ. \n@\nСЕЙЧАС ТАКОЙ НЕ ДЕЛАЮТ, ЭТО ВЕНГЕРСКИЙ! \n@\nИ ПЫЛЬ ПРОСТРИ С НЕГО, НЕ БЕРЕЖЕШЬ СОВСЕМ \n"
                    game.mom_stuff.append("service")
                    game.tenge -= 10
                else:
                    txt = "ПРИХОДИШЬ В МАГАЗ\n @\n И ДАЖЕ СРАНЫЙ СЕРВИЗ НЕ МОЖЕШЬ КУПИТЬ\n @\n ТЕНГЕ НЕ ХВАТАЕТ"
        'Софа "Накройчехлом" (100 тенгэ)' if "sofa" not in game.mom_stuff:
            python:
                if game.tenge >= 100:
                    txt = "В КОМНАТЕ НОВЫЙ ДИВАН, КРАСИВЫЙ, МЯГКИЙ. \n@\nНАКРОЙ ЧЕХЛОМ, ШОБ ОБИВОЧКУ НЕ ИСПАЧКАТЬ \n@\nНАКРЫВАЕШЬ ССАНОЙ ТРЯПКОЙ \n"
                    game.mom_stuff.append("sofa")
                    game.tenge -= 100
                else:
                    txt = "ПРИХОДИШЬ В МАГАЗ\n @\n И ДАЖЕ СРАНЫЙ ДИВАН НЕ МОЖЕШЬ КУПИТЬ\n @\n ТЕНГЕ НЕ ХВАТАЕТ"
        'Ковёр "Какулюдей" (10 тенгэ)' if "carpet" not in game.mom_stuff:
            python:
                if game.tenge >= 10:
                    txt = "ПРИЕХАЛИ ДЯДЯ БАФОМЕТ И ТЁТЯ СРАКА \n@\n ОЙ СЫЧА СРОЧНО НЕСИ СВОЙ ПОЛЯРОИД\n@\n НА ФОНЕ КОВРА НАС СНИМИ. КРСИВО И БОХАТО! \n"
                    game.mom_stuff.append("carpet")
                    game.tenge -= 10
                else:
                    txt = "ПРИХОДИШЬ В МАГАЗ\n @\n И ДАЖЕ СРАНЫЙ КОВЁР НЕ МОЖЕШЬ КУПИТЬ\n @\n ТЕНГЕ НЕ ХВАТАЕТ"
        'Шубка "Кандибобер" (10 тенгэ)' if "fur" not in game.mom_stuff:
            python:
                if game.tenge >= 10:
                    txt = "ОЙ А ЧТО ЭТО ЗА МЕХ ТАКОЙ? \n@\nЭТО МЕТИС. МЕТИС. \n@\nПАПА - НОРКА. МАМА - БОБЁР \n"
                    game.mom_stuff.append("fur")
                    game.tenge -= 10
                else:
                    txt = "ПРИХОДИШЬ В МАГАЗ\n @\n И ДАЖЕ СРАНУЮ ШУБУ НЕ МОЖЕШЬ КУПИТЬ\n @\n ТЕНГЕ НЕ ХВАТАЕТ"
        'Гарнитур-стенка "Мечта застоя" (10 тенгэ)' if "furniture" not in game.mom_stuff:
            python:
                if game.tenge >= 10:
                    txt = "ОЙ Я ВСЕГДА МЕЧТАЛА О ТАКОЙ РОСКОШНОЙ СТЕНКЕ \n@\nСЫЧА, НУ КА РАСЧИСТЬ ПРОСТРАНСТВО \n@\nНЕ ВЫБРАСЫВАЙ ТОЛЬКО НИЧЕГО, НА ДАЧУ УВЕЗЁМ \n"
                    game.mom_stuff.append("furniture")
                    game.tenge -= 10
                else:
                    txt = "ПРИХОДИШЬ В МАГАЗ\n @\n И ДАЖЕ СРАНЫЙ ГАРНИТУР МОЖЕШЬ КУПИТЬ\n @\n ТЕНГЕ НЕ ХВАТАЕТ"

        'Назад':
            jump lbl_mom_manage
            
    
    '[txt]'    

    return                      

label lbl_discipline:
    menu:
        "Надо сконцентрироваться на чём то одном."
        "Наказания":
            menu:
                "Отец, научи сычу уму-разуму то!":
                    menu:
                        "Подзатыльники":
                            $ persons_schedules[mother].add_action(mother.torture, 'discipline', power=1, taboos=['pain'], target=child)
                "Назад":
                    jump lbl_discipline
        "Внушение":
            $ pass
        "Подкуп":
            $ pass
        "И так неплохо":
            $ pass
        
    return
    
label lbl_diet:
    menu:
        "Мы сейчас тебе диету будем делать."
        "Чтоб здоровенький был у нас, как Ванька Ерохин":
            $ player.ration['target'] = 0
        "А то отрастил себе мамонище, девок пугать.":
            $ player.ration['target'] = -1
        "Кожа да кости же, ухватиться не за что. Девки любить не будут!":
            $ player.ration['target'] = 1
        
    return

label lbl_accomodation_rules:
    menu:
        'Вечно ты в комнате запираешься от матери! Как сыч.':
            $ player.accommodation = "appartment"
        'Комнату твою сдавать будем, поспишь у нас на диванчике.':
            $ player.accommodation = "cot"
        'Диванчик для тёти Сраки, а тебе вот раскладушечка дедова.':
            $ player.accommodation = "mat"
        'В ванной тебя запрём ночевать. Чтобы не воображал!':
            $ player.accommodation = "confined"
        'Ты у меня в шкафу сидеть будешь. Пока мать любить не научишься.':
            $ player.accommodation = "jailed"            
    
    return
                    

label lbl_job_rules:
    menu:
        'Всё сидишь как сыч, за конпуктером. Иди пробзись.':
            $ player.job = 'idle'
        'Уроки делай, бездельник! Зря тебя мать в интитут пристраивала?':
            $ player.job = 'study'
        'Посудку помой. Мусор вынеси. С собакой погуляй. И за дедом прибери.':
            $ player.job = 'chores'
        'Вон здоровый какой. Иди вагоны разгружать - семье копеечка.':
            $ player.job = 'work'
        'Да хоть на панели жопой торгуй! Я на тебя батрачить не нанималась.':
            $ player.job = 'whore'
    
    menu:           
        'Как сильно ты будешь стараться на работе?'
        'Спустя рукава':
            pass
        'Работать хорощо':
            pass
        'Волевым усилием':
            pass
        'Выкладываться полностью':
            pass
    return

label lbl_skill_check(character=player, skill_to_use=None, res_to_use=None, determination=False):
    python:
        if character.skill_level(skill_to_use) < 1:
            result_text = "Проверка провалена"
        resource = getattr(character, res_to_use) if res_to_use else 0
    menu:
        'Сделать спустя рукава':
            $ result_text = "Плохо поработал"
        'Работать хорошо' if resource > 0:
            $ skill_result = character.use_skill(skill_to_use, res_to_use, determination)
            $ result_text = "Поработал на: "
            $ result_text += str(skill_result)
        'Сделать волевым усилием' if character.determination > 0:
            $ skill_result = character.use_skill(skill_to_use, res_to_use, determination=True)
            $ result_text = "Волевое усилие прошло на: "
            $ result_text += str(skill_result)
        'Выложиться полностью' if resource > 0 and character.determination > 0:
            $ skill_result = character.use_skill(skill_to_use, res_to_use, determination=True)
            $ result_text = "Выложился на: "
            $ result_text += str(skill_result)
    "game" '[result_text]'
    return
label lbl_resist(effect):
    'Сопротивляться [effect]?'
    menu:
        'Да':
            return True
        'Нет':
            return False
label lbl_resist_result(effect, success):
    if success:
        'Вы справились с [effect]'
    else:
        'Вы попытались справиться с [effect] но вам не удалось'
    return

