# Управление за мать


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
        "Информация":
            call lbl_owl_info
            jump lbl_mom_manage        
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
                "Отец, научи Cычу уму-разуму то!":
                    menu:
                        "Подзатыльники":
                            $ persons_schedules[mother].add_action(mother.torture, 'obedience', power=1, taboos=['pain'], target=child)
                        "Драть за уши":
                            $ persons_schedules[mother].add_action(mother.torture, 'obedience', power=2, taboos=['pain'], target=child)
                        "Пороть ремнём":
                            $ persons_schedules[mother].add_action(mother.torture, 'obedience', power=3, taboos=['pain'], target=child)                            
                        "Поздить":
                            $ persons_schedules[mother].add_action(mother.torture, 'obedience', power=4, taboos=['pain'], target=child)
                        "Поздить ногами":
                            $ persons_schedules[mother].add_action(mother.torture, 'obedience', power=5, taboos=['pain'], target=child)  
                "Назад":
                    jump lbl_discipline
        "Внушение":
            menu:
                'Привечать батюшку Павсикакия (10 тенге)' if game.tenge > 9:
                    $ game.tenge -= 10
                'Организовать "Кохана ми вбиваємо дітей" (100 тенге)' if game.tenge > 99:
                    $ game.tenge -= 10
                'Ежедневыне истерики (бесценно)':
                    $ pass

        "Подкуп":
            menu:
                'Можно активировать/деактивировать любое количество обещаний.'
                'Закончить':
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
            $ player.job['name'] = 'idle'
        'Уроки делай, бездельник! Зря тебя мать в интитут пристраивала?':
            $ player.job['name'] = 'study'
        'Посудку помой. Мусор вынеси. С собакой погуляй. И за дедом прибери.':
            $ player.job['name'] = 'chores'
        'Вон здоровый какой. Иди вагоны разгружать - семье копеечка.':
            $ player.job['name'] = 'work'
        'Да хоть на панели жопой торгуй! Я на тебя батрачить не нанималась.':
            $ player.job['name'] = 'whore'
    
    return