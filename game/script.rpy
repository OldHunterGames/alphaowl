init -10 python:
    sys.path.append(renpy.loader.transfn("scrypts"))
    from obj_character import *
    from owl_engine import *

init python:
    default_relations = {"connection": "unrelated",          
                "consideration": "respectful",     
                "distance": "close",                
                "affection": "associate",}
    
    renpy.block_rollback()
    game = Engine()
    player = game.player
    player.master = Person()
    mother = player.master
    player.relations[mother] = deepcopy(default_relations)
    
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
            $ player.alignment['Orderliness'] = "Lawful"
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
            "Низззя"
            jump label_quiz
            
        "Своей мамкой":
            jump label_new_day

    return

label label_new_day:
    "Неделя номер [game.time]"
    $ txt = player.description()
    "[txt]"
    
    $ gt = game.new_turn()
    $ money = player.eval_job()
    $ game.tenge += money
    call lbl_mom_manage

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
            $ player.set_job('idle')
        'Уроки делай, бездельник! Зря тебя мать в интитут пристраивала?':
            $ player.set_job("study")
        'Посудку помой. Мусор вынеси. С собакой погуляй. И за дедом прибери.':
            $ player.set_job('chores')
        'Вон здоровый какой. Иди вагоны разгружать - семье копеечка.':
            $ player.set_job('work', 'sport', 10, auto=True)
        'Да хоть на панели жопой торгуй! Я на тебя батрачить не нанималась.':
            $ player.set_job('whore', 'sex', 20, auto=True)
    
    menu:           
        'Как сильно ты будешь стараться на работе?'
        'Спустя рукава':
            $ player.job['effort'] = 'bad'
        'Работать хорощо':
            $ player.job['effort'] = 'good'
        'Волевым усилием':
            $ player.job['effort'] = 'will'
        'Выкладываться полностью':
            $ player.job['effort'] = 'full'
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


