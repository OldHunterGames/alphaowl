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
            "Низззя"
            jump label_quiz
            
        "Своей мамкой":
            call label_new_day

    return

label label_new_day:
    "Неделя номер [game.time]"
    call lbl_mom_manage
    $ txt = player.description()
    "[txt]"
    
    $ gt = game.new_turn()
    call expression gt

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
        "Конец недели":
            $ player.rest()
            jump label_new_day
            
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
            $ player.job = "idle"
        'Уроки делай, бездельник! Зря тебя мать в интитут пристраивала?':
            $ player.job = "study"
        'Посудку помой. Мусор вынеси. С собакой погуляй. И за дедом прибери.':
            $ player.job = "chores"
        'Вон здоровый какой. Иди вагоны разгружать - семье копеечка.':
            $ player.job = "work"
        'Да хоть на панели жопой торгуй! Я на тебя батрачить не нанималась.':
            $ player.job = "whore"            
    
    return
    