# Управление за мать


label lbl_mom_manage:
    menu:
        "Питание":
            call lbl_food_rules
        "Бытовые условия":
            call lbl_accomodation_rules
        "Правила и запреты":
            call lbl_rules            
        "После учебы":
            call lbl_job_rules
        "В выходные":
            # call lbl_leisure_rules          
            "Упс. Не готово"
            $ pass
        "Воспитание":
            call lbl_discipline
        "Магазин":
            call lbl_shop
        "Информация":
            call lbl_owl_info
            jump lbl_mom_manage        
        "Конец недели":
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

label lbl_rules:
    menu:
        'Внешний вид':
            call lbl_rules_clothes
        'Вредные привычки':
            call lbl_rules_drugs
        'Правила поведения':
            call lbl_rules_behavior
        'Назад':
            jump lbl_mom_manage
            
    jump lbl_rules
    
    return

label lbl_rules_clothes:
    menu:
        'Мамина симпатяфка':
            $ child.appearance = 'lame'
            $ txt = 'Вот свитерочек бабушка связала \n @ \n Штанишки тетя Ёба нам со своего оболтуса дала \n @ \n Шапку не забудь надеть!'
        'Да носи что хочешь':
            $ child.appearance = 'normal'
            $ txt = 'Залезаешь в шкаф чтобы найти приличную одежду \n @ \n Там какие-то обноски от Тёти Ёбы и Дяди Бафомета \n @ \n И мутантная моль размером с кошака доедает ушанку'    
        'Купим тебе модное, выбирай (20 т/нед)':
            $ child.appearance = 'cool'
            $ txt = 'Ой Сыченька, сейчас купим тебе модного \n @ \n Затариваетесь на рынке у Ашота, турецкими подделками \n @ \n А ты и не против'
            
    "[txt]"
    
    return

label lbl_rules_drugs:
    menu:
        'Запретить фапать' if 'masturbation' not in child.restrictions:
            $ child.restrictions.append('masturbation')
            $ txt = 'Сыночка то наш, всё пиструнчик свой тилибонькает \n @ \n Скоро волосы на руках расти начнут \n @ \n В антимастурбационном кресте будещь спать, по совету отца Агапия'
        'Забить на дрочку' if 'masturbation' in child.restrictions:
            $ child.restrictions.remove('masturbation')
            $ txt = 'А что это ты в ванной столько времени сидишь, Сыча? \n @ \n И то хорошо \n @ \n Приучили к чистоте ребёнка то'            
        'Запретить алкоголь' if 'alcohol' not in child.restrictions:
            $ child.restrictions.append('alcohol')
            $ txt = 'Ты на пиво то не заглядвайся \n @ \n Ещё нос не дорос \n @ \n Я малолетних алкоголиков в доме не потерплю'
        'Забить на алкоголь' if 'alcohol' in child.restrictions:
            $ child.restrictions.remove('alcohol')
            $ txt = 'За дидов рюмашечку надо обязательно \n @ \n Что значит "не буду стекломой пить" \n @ \n Традиции наши не уважаешь?'                 
        'Запретить курить' if 'tobacco' not in child.restrictions:
            $ child.restrictions.append('tobacco')
            $ txt = 'Если почую табачный запах \n @ \n Всё отцу расскажу \n @ \n Неделю у меня сидеть на жопе не сможешь'
        'Забить на курение' if 'tobacco' in child.restrictions:
            $ child.restrictions.remove('tobacco')
            $ txt = 'Сыченька то бодрячком \n @ \n Каждые пять минут в падик бегает \n @ \n Наверное друзья у него там'         
        'Запретить спайсы' if 'weed' not in child.restrictions:
            $ child.restrictions.append('weed')
            $ txt = 'Чтобы я тебя с этими наркоманами не видела больше \n @ \n Пообколются своей марихуанной \n @ \n А потом ябут друг-друга в жёппы'
        'Забить на спайсы' if 'weed' in child.restrictions:
            $ child.restrictions.remove('weed')
            $ txt = 'Ой а что это за штучка такая у тебя, Сыча? \n @ \n Для ароматизации помещения да? \n @ \n И вот сюда вот воду заливать?'                     
        'Назад':
            jump lbl_rules
    "[txt]"
    
    return


label lbl_rules_behavior:
    menu:
        'Запретить общаться с девочками' if 'dates' not in child.restrictions:
            $ child.restrictions.append('dates')
        'Разрешить общаться с девочками' if 'dates' in child.restrictions:
            $ child.restrictions.remove('dates')
            $ txt = ' \n @ \n \n @ \n '            
        'Запретить общаться с мальчиками' if 'friends' not in child.restrictions:
            $ child.restrictions.append('friends')
        'Разрешить общаться с мальчиками' if 'friends' in child.restrictions:
            $ child.restrictions.remove('friends')
        'Конплюхтерн для очобы! (блокировать интернет)' if 'pc' not in child.restrictions:
            $ child.restrictions.append('pc')
        'Ну и сиди за своим комплюктером' if 'pc' in child.restrictions:
            $ child.restrictions.remove('pc')
            
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
                            $ batya_force = 1
                            $ child.schedule.add_action('batya_batya', 'single')
                        "Драть за уши":
                            $ batya_force = 2
                            $ child.schedule.add_action('batya_batya', 'single')
                        "Пороть ремнём":
                            $ batya_force = 3
                            $ child.schedule.add_action('batya_batya', 'single')                    
                        "Поздить":
                            $ batya_force = 4
                            $ child.schedule.add_action('batya_batya', 'single')
                        "Поздить ногами":
                            $ batya_force = 5
                            $ child.schedule.add_action('batya_batya', 'single')
                        "Ой-всё. Хватит. ОНЖИРИБЁНОК!":
                            $ child.schedule.remove_action('batya_batya')
                "Назад":
                    jump lbl_discipline
        "Внушение":
            menu:
                'Привечать батюшку Павсикакия (10 тенге)' if game.tenge > 9:
                    $ game.tenge -= 10
                    $ child.schedule.add_action('discipline_pavsykakiy', 'single')
                'Организовать "Кохана ми вбиваємо дітей" (100 тенге)' if game.tenge > 99:
                    $ game.tenge -= 100
                    $ child.schedule.add_action('discipline_kohana', 'single')
                'Ежедневыне истерики (бесценно)':
                    $ mom_power = 1
                    $ child.schedule.add_action('discipline_hystery', 'single')

        "Подкуп":
            menu:
                'Можно активировать любое количество обещаний. Если будешь вести себя хорошо то...'
                'Ешь свои чипсы сколько влезет' if not ('pringles', "nutrition") in child.used_rewards:
                    $ child.add_reward('pringles', "nutrition")
                'Разрешим тебе кофе по утрам' if not ('coffe', "wellness") in child.used_rewards:
                    $ child.add_reward('coffe', "wellness")
                'Отдам тебе пледик клетчатый' if not ('pledik', "comfort") in child.used_rewards:
                    $ child.add_reward('pledik', "comfort")
                'И тогда можешь записываться в споротклуб' if not ('sportklub', "activity") in child.used_rewards:
                    $ child.add_reward('sportklub', "activity")
                'Не будем тебе запрещать с друзьями по телефону болтать' if not ('telefon', "communication") in child.used_rewards:
                    $ child.add_reward('telefon', "communication")                    
                'Разрешим на комплюктере игрушки играть' if not ('pcgames', "amusement") in child.used_rewards:
                    $ child.add_reward('pcgames', "amusement")
                'Будем тебе на карманные давать, немного' if not ('poketmoney', "prosperity") in child.used_rewards:
                    $ child.add_reward('poketmoney', "prosperity")
                'Сам себе будешь расписание составлять' if not ('shedule_power', "authority") in child.used_rewards:
                    $ child.add_reward('shedule_power', "authority")
                'Мы с батей будем тобой гордиться!' if not ('mom_aprove', "ambition") in child.used_rewards:
                    $ child.add_reward('mom_aprove', "ambition")                                   
                'Закончить':
                    $ pass
        
        "Отношение" if player.ap > 0:
            menu:
                'Выбрать используемый жетон.'
                'Dread' if child.has_token("dread"):
                    menu:
                        'Повысить уровень страха':
                            $ player.ap -= 1
                            $ child.use_token('dread')
                            $ child.dread += 1
                        'Внушить уважение':
                            $ player.ap -= 1
                            $ child.use_token('dread')
                            $ child.relations(mom).change('consideration', '+')
                        'Усилить вражду':
                            $ player.ap -= 1
                            $ child.use_token('dread')
                            $ child.relations(mom).change('affection', '-')
                        'Назад':
                            jump lbl_discipline  
                'Discipline' if child.has_token("discipline"):
                    menu:
                        'Повысить уровень дисциплины':
                            $ player.ap -= 1
                            $ child.use_token('discipline')
                            $ child.discipline += 1
                        'Внушить уважение':
                            $ player.ap -= 1
                            $ child.use_token('discipline')
                            $ child.relations(mom).change('consideration', '+')
                        'Формализовать отношения':
                            $ player.ap -= 1
                            $ child.use_token('discipline')
                            $ child.relations(mom).change('distance', '-')
                        'Назад':
                            jump lbl_discipline  
                'Dependance' if child.has_token("dependance"):
                    menu:
                        'Повысить уровень зависимости':
                            $ player.ap -= 1
                            $ child.use_token('dependance')
                            $ child.dependance += 1
                        'Внушить уважение':
                            $ player.ap -= 1
                            $ child.use_token('dependance')
                            $ child.relations(mom).change('consideration', '+')
                        'Сблизиться':
                            $ player.ap -= 1
                            $ child.use_token('dependance')
                            $ child.relations(mom).change('distance', '+')
                        'Назад':
                            jump lbl_discipline  
                            
                            
                "Назад":
                    jump lbl_discipline                
        
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
            $ child.job['name'] = 'idle'
        'Уроки делай, бездельник! Зря тебя мать в интитут пристраивала?':
            $ child.job['name'] = 'study'
            $ child.schedule.add_action('job_study')  
        'Посудку помой. Мусор вынеси. С собакой погуляй. И за дедом прибери.':
            $ child.job['name'] = 'chores'
            $ child.schedule.add_action('job_chores')            
        'Вон здоровый какой. Иди вагоны разгружать - семье копеечка.':
            $ child.job['name'] = 'work'
            $ child.schedule.add_action('job_work')                   
        'Да хоть на панели жопой торгуй! Я на тебя батрачить не нанималась.':
            $ child.job['name'] = 'whore'
            $ child.schedule.add_action('job_whore') 
    
    return