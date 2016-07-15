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
            
    jump lbl_universal_menu
    
    return
    

label lbl_slave_train:
    menu:
        "Нужно выбрать концептуальный подход к воспитанию."
        "Наказания":
            $ token_to_gain = 'conquest'
            $ moral_burden = ['evil', 'ardent'] 
            $ self_bonus_need = 'power'
            call lbl_slave_torture
        "Дисциплина":
            $ token_to_gain = 'convention'
            $ moral_burden = ['lawful'] 
            $ self_bonus_need = 'order'
            call lbl_slave_discipline            
        "Поощрения":
            $ token_to_gain = 'contribution'
            $ moral_burden = ['good'] 
            $ self_bonus_need = 'altruism'
            call lbl_slave_encourage            
    return

label lbl_slave_torture:
    menu:            
        'Ругать':
            $ skill_to_use = 'conversation'
            $ phobias_to_use = ['abuse']
            $ targeted_need = ['communication', 'approval']    
            $ player.schedule.add_action('discipline_atrocity', 'single')

        'Чморить':
            $ skill_to_use = 'conversation'
            $ phobias_to_use = ['abuse']
            $ targeted_need = ['authority', 'ambition']    
            $ player.schedule.add_action('discipline_atrocity', 'single')
            
        'Пороть (батя)':
            $ skill_to_use = 'sport'
            $ phobias_to_use = ['pain']
            $ targeted_need = ['wellness']    
            $ batya.schedule.add_action('discipline_atrocity', 'single')
            
        'Поставить в угол (батя)':
            $ skill_to_use = 'sport'
            $ phobias_to_use = ['deprevation']
            $ targeted_need = ['comfort', 'activity']    
            $ batya.schedule.add_action('discipline_atrocity', 'single')
            
        'Хвататься за сердце':
            $ skill_to_use = 'conversation'
            $ phobias_to_use = ['brutality']
            $ targeted_need = ['altruism']    
            $ player.schedule.add_action('discipline_atrocity', 'single')
            
    'Стратегия наказаний определена'
    jump lbl_universal_menu
    return

label lbl_slave_discipline:
    $ skill_to_use = 'conversation'
    $ targeted_need = 'wellness'    
    $ player.schedule.add_action('discipline_intercommunion', 'single')
    
    'Будем воспитывать...'
    jump lbl_universal_menu
    return

label lbl_slave_encourage:
    menu:
        'Хвалить':
            $ skill_to_use = 'conversation'
            $ targeted_need = ['ambition', 'approval']    
            $ player.schedule.add_action('discipline_pleasing', 'single')

        'Давать вкусняшки':
            $ skill_to_use = 'conversation'
            $ targeted_need = ['nutrition']    
            $ player.schedule.add_action('discipline_pleasing', 'single')

        'Отпустить в кино':
            $ skill_to_use = 'conversation'
            $ targeted_need = ['amusement']    
            $ player.schedule.add_action('discipline_pleasing', 'single')
            
        'Карманные расходы (10 тенгэ)' if game.money > 9:
            $ game.money -= 10
            $ skill_to_use = 'conversation'
            $ targeted_need = ['prosperity']    
            $ player.schedule.add_action('discipline_pleasing', 'single')
            
    'Стратения поощрений определена'
    jump lbl_universal_menu
    return
    
label lbl_food_rules:
    menu:
        "Тётя Срака читала - кушать надо сколько душа просит":
            $ child.ration['amount'] = "unlimited" 
        "У Сыченьки то фигуры нет совсем...":
            $ child.ration['amount'] = "regime" 
            call lbl_diet
        "А ты вот посиди без етьбы, знать будешь как матери губить!":
            $ child.ration['amount'] = "starvation"   
            $ child.ration['food_type'] = "forage"   
            $ child.ration['target'] = 0           
            $ child.ration['limit'] = None
            jump lbl_mom_manage
    
    menu:
        "Вот покушай ка Сычулька..."
        "Своего, с огорода-то. Витаминчики!":
            $ child.ration['food_type'] = "sperm" 
            'Как земля... совсем невкусно (-3)'
        "Мивины с маянезиком.":
            $ child.ration['food_type'] = "dry" 
            'Бичпакет... не вкусно (-1)'
        "Тёпленького похлебай, домашнего. С хлебушком.":
            $ child.ration['food_type'] = "canned" 
            'Хрючево... нормальный вкус'
        "В столовой вашей, я кухаркой не нанималась!":
            $ child.ration['food_type'] = "cosine"   
            'Пища белых людей... вкуснота (3)'

    return

label lbl_diet:
    menu:
        "Мы сейчас тебе диету будем делать."
        "Чтоб здоровенький был у нас, как Ванька Ерохин":
            $ child.ration['target'] = 2
        "А то отрастил себе мамонище, девок пугать.":
            $ child.ration['target'] = 1
        "Кожа да кости же, ухватиться не за что. Девки любить не будут!":
            $ child.ration['target'] = 3
        
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
            $ child.schedule.add_action('outfit_lame')
            $ txt = 'Вот свитерочек бабушка связала \n @ \n Штанишки тетя Ёба нам со своего оболтуса дала \n @ \n Шапку не забудь надеть! (autority -3)'
        'Да носи что хочешь':
            $ child.appearance = 'normal'
            $ child.schedule.add_action('outfit_normal')
            $ txt = 'Залезаешь в шкаф чтобы найти приличную одежду \n @ \n Там какие-то обноски от Тёти Ёбы и Дяди Бафомета \n @ \n И мутантная моль размером с кошака доедает ушанку (prosperity -2)'    
        'Купим тебе модное, выбирай (25 тенгэ)' if game.tenge >= 25:
            $ game.tenge -= 25
            $ child.appearance = 'cool'
            $ child.schedule.add_action('outfit_cool')
            $ txt = 'Ой Сыченька, сейчас купим тебе модного \n @ \n Затариваетесь на рынке у Ашота, турецкими подделками \n @ \n А ты и не против (prosperity 4)'
            
    "[txt]"
    
    return


label lbl_accomodation_rules:
    menu:
        'Вечно ты в комнате запираешься от матери! Как сыч.':
            $ child.accommodation = "appartment"
            $ child.schedule.add_action('living_appartment')  
        'Комнату твою сдавать будем, поспишь у нас на диванчике.':
            $ child.accommodation = "cot"
            $ child.schedule.add_action('living_cot')  
        'Диванчик для тёти Сраки, а тебе вот раскладушечка дедова.':
            $ child.accommodation = "mat"
            $ child.schedule.add_action('living_mat')  
        'В ванной тебя запрём ночевать. Чтобы не воображал!':
            $ child.accommodation = "jailed"      
            $ child.schedule.add_action('living_jailed')    
        'Ты у меня в шкафу сидеть будешь. Пока мать любить не научишься.':
            $ child.accommodation = "confined"
            $ child.schedule.add_action('living_confined')
    
    return
                    

label lbl_job_rules:
    menu:
        'Всё сидишь как сыч, за конпуктером. Иди пробзись.':
            $ child.job['name'] = 'idle'
            $ child.schedule.add_action('job_idle')  
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
    
label lbl_shop:
    menu:
        'Маман очень хочет жить БОХАТО. Скупи весь магазин и это будет блистательный WIN.'
        'Какус "Антирадиационный" (10 тенгэ)' if "cactus" not in game.mom_stuff:
            python:
                if game.money >= 10:
                    txt = "КАНПУКТЕР ОБЛУЧАЕТ РАДИАЦИЕЙ \n@\nСЫЧА, СРОЧНО ПОСТАВЬ КАКТУС К ЭКРАНУ\n@\nУЧОНЫЕ ПО РЕН-ТВ ТОЛЬКО ЧТО СКАЗАЛИ\n"
                    game.mom_stuff.append("cactus")
                    game.money -= 10
                else:
                    txt = "ПРИХОДИШЬ В МАГАЗ\n @\n И ДАЖЕ СРАНЫЙ КАКТУС НЕ МОЖЕШЬ КУПИТЬ\n @\n ТЕНГЕ НЕ ХВАТАЕТ"
        'Сервиз "Мойхрусталь" (25 тенгэ)' if "service" not in game.mom_stuff:
            python:
                if game.money >= 25:
                    txt = "ХРУСТАЛЬ - ЭТО ТВОЕ ПРИДАНОЕ. ПОСТАВЬ В СЕРВАНТ. \n@\nСЕЙЧАС ТАКОЙ НЕ ДЕЛАЮТ, ЭТО ВЕНГЕРСКИЙ! \n@\nИ ПЫЛЬ ПРОСТРИ С НЕГО, НЕ БЕРЕЖЕШЬ СОВСЕМ \n"
                    game.mom_stuff.append("service")
                    game.money -= 25
                else:
                    txt = "ПРИХОДИШЬ В МАГАЗ\n @\n И ДАЖЕ СРАНЫЙ СЕРВИЗ НЕ МОЖЕШЬ КУПИТЬ\n @\n ТЕНГЕ НЕ ХВАТАЕТ"
        'Софа "Накройчехлом" (100 тенгэ)' if "sofa" not in game.mom_stuff:
            python:
                if game.money >= 100:
                    txt = "В КОМНАТЕ НОВЫЙ ДИВАН, КРАСИВЫЙ, МЯГКИЙ. \n@\nНАКРОЙ ЧЕХЛОМ, ШОБ ОБИВОЧКУ НЕ ИСПАЧКАТЬ \n@\nНАКРЫВАЕШЬ ССАНОЙ ТРЯПКОЙ \n"
                    game.mom_stuff.append("sofa")
                    game.money -= 100
                else:
                    txt = "ПРИХОДИШЬ В МАГАЗ\n @\n И ДАЖЕ СРАНЫЙ ДИВАН НЕ МОЖЕШЬ КУПИТЬ\n @\n ТЕНГЕ НЕ ХВАТАЕТ"
        'Ковёр "Какулюдей" (100 тенгэ)' if "carpet" not in game.mom_stuff:
            python:
                if game.money >= 100:
                    txt = "ПРИЕХАЛИ ДЯДЯ БАФОМЕТ И ТЁТЯ СРАКА \n@\n ОЙ СЫЧА СРОЧНО НЕСИ СВОЙ ПОЛЯРОИД\n@\n НА ФОНЕ КОВРА НАС СНИМИ. КРСИВО И БОХАТО! \n"
                    game.mom_stuff.append("carpet")
                    game.money -= 100
                else:
                    txt = "ПРИХОДИШЬ В МАГАЗ\n @\n И ДАЖЕ СРАНЫЙ КОВЁР НЕ МОЖЕШЬ КУПИТЬ\n @\n ТЕНГЕ НЕ ХВАТАЕТ"
        'Шубка "Кандибобер" (100 тенгэ)' if "fur" not in game.mom_stuff:
            python:
                if game.money >= 100:
                    txt = "ОЙ А ЧТО ЭТО ЗА МЕХ ТАКОЙ? \n@\nЭТО МЕТИС. МЕТИС. \n@\nПАПА - НОРКА. МАМА - БОБЁР \n"
                    game.mom_stuff.append("fur")
                    game.money -= 100
                else:
                    txt = "ПРИХОДИШЬ В МАГАЗ\n @\n И ДАЖЕ СРАНУЮ ШУБУ НЕ МОЖЕШЬ КУПИТЬ\n @\n ТЕНГЕ НЕ ХВАТАЕТ"
        'Гарнитур-стенка "Мечта застоя" (250 тенгэ)' if "furniture" not in game.mom_stuff:
            python:
                if game.money >= 250:
                    txt = "ОЙ Я ВСЕГДА МЕЧТАЛА О ТАКОЙ РОСКОШНОЙ СТЕНКЕ \n@\nСЫЧА, НУ КА РАСЧИСТЬ ПРОСТРАНСТВО \n@\nНЕ ВЫБРАСЫВАЙ ТОЛЬКО НИЧЕГО, НА ДАЧУ УВЕЗЁМ \n"
                    game.mom_stuff.append("furniture")
                    game.money -= 250
                else:
                    txt = "ПРИХОДИШЬ В МАГАЗ\n @\n И ДАЖЕ СРАНЫЙ ГАРНИТУР МОЖЕШЬ КУПИТЬ\n @\n ТЕНГЕ НЕ ХВАТАЕТ"

        'Назад':
            jump lbl_universal_menu
            
    
    '[txt]'    

    return   
    

label lbl_developement:
    menu:
        "Надо что-то сделать для развития сыночки-корзиночки."
        "Прорыв в отношениях":
            $ target = child
            call lbl_change_relations
        
        "Основные навыки":
            menu:
                'Хоть бы книжку почитал!' if not child.skill('coding').training:
                    $ player.ap -= 1
                    $ EVGeneric(game, "evn_teach_coding").trigger(child)
                'Тебе бы общаться поуверенней, как Ерохин!' if not child.skill('conversation').training:
                    $ player.ap -= 1
                    $ EVGeneric(game, "evn_teach_conversation").trigger(child)
                'Батя, поговори с ребёнком про ЭТО...' if not child.skill('sex').training:
                    $ player.ap -= 1
                    $ EVGeneric(game, "evn_teach_sex").trigger(child)
                'Зарядку у меня делать будешь. Кажное утро.' if not child.skill('sports').training:
                    $ player.ap -= 1
                    $ EVGeneric(game, "evn_teach_sports").trigger(child)
                'Да чему тебы учить. Ты же НУЛЕВОЙ!!!':
                    call lbl_developement
                
        "Институт (учёба)":
            menu:
                'Делай курсовую' if 'major' in game.studies:
                    $ player.ap -= 1
                    $ EVGeneric(game, "evn_do_major").trigger()
                    
                'Сдай нормативы по физре' if  'gym' in game.studies:
                    $ player.ap -= 1
                    $ EVGeneric(game, "evn_do_gym").trigger()                            

                'Производственная практика' if 'practice' in game.studies:
                    'На заводе по сборке вёдер  \n @ \n Наша инновационная ЭВМ "Эдьбрус-М"  \n @ \n  На перфокартах'
                    menu:
                        'Отпахать по честному':
                            $ player.ap -= 1
                            $ EVGeneric(game, "evn_do_practice_programm").trigger(child)    
                        'Закорешиться с коллективом':
                            $ player.ap -= 1
                            $ EVGeneric(game, "evn_do_practice_programm_chat").trigger(child)    

                'Зачет на военной кафедре' if 'military' in game.studies:
                    'Офицеры уже с утра бухие  \n @ \n Муштра на плацу как при Павле I \n @ \n Вечером зачет по строевой'
                    menu:
                        'Держать равнение налево':
                            $ player.ap -= 1
                            $ EVGeneric(game, "evn_do_practice_military").trigger(child)    
                        'Подлизаться к товарищу подполковнику':
                            $ player.ap -= 1
                            $ EVGeneric(game, "evn_do_practice_military_chat").trigger(child)    

                'Лабы по программированию' if 'labs' in game.studies:
                    'Старый профессор-некрофил  \n @ \n Задача на фортране  \n @ \n  Как буд-то кто-то им пользуется вообще'
                    menu:
                        'Накодить убер-алгоритм':
                            $ player.ap -= 1
                            $ EVGeneric(game, "evn_do_practice_labs").trigger(child)    
                        'Скатать решение у ботанов':
                            $ player.ap -= 1
                            $ EVGeneric(game, "evn_do_practice_labs_chat").trigger(child)    
                    
                'Совсем не учишься же, корзиночка...':
                    jump lbl_developement 
                
        "Институт (коррупция)":
            menu:
                'Купим курсовую (250 тенге)' if 'major' in game.studies and game.tenge >= 250:
                    $ player.ap -= 1
                    $ game.tenge -= 250
                    $ game.studies.remove('major')
                    'Бабло победит Зло.  \n @ \n Вопрос с курсовой закрыт.  \n @ \n Потрачено 100 тенге'
                    
                'Оформим освобождение от физкультуры (100 тенге)' if 'gym' in game.studies and game.tenge >= 100:
                    $ player.ap -= 1
                    $ game.tenge -= 100
                    $ game.studies.remove('gym')
                    'Бабло победит Зло.  \n @ \n Вопрос с физкульутрой закрыт.  \n @ \n Потрачено 100 тенге'
                   
                'Договоримся с начальником проф-практики (100 тенге)' if 'practice' in game.studies and game.tenge >= 100:
                    $ player.ap -= 1
                    $ game.tenge -= 100
                    $ game.studies.remove('practice')
                    'Бабло победит Зло.  \n @ \n Вопрос с производственной практикой закрыт.  \n @ \n Потрачено 100 тенге'
                   
                'Полковнику дадим на лапу (100 тенге)' if 'military' in game.studies and game.tenge >= 100:
                    $ player.ap -= 1
                    $ game.tenge -= 100
                    $ game.studies.remove('military')
                    'Бабло победит Зло.  \n @ \n Вопрос с военной кафедрой закрыт.  \n @ \n Потрачено 100 тенге'
                   
                'С лабораторными порешаем как нибудь (100 тенге)' if 'labs' in game.studies and game.tenge >= 100:
                    $ player.ap -= 1
                    $ game.tenge -= 100
                    $ game.studies.remove('labs')
                    'Бабло победит Зло.  \n @ \n Вопрос с лабами закрыт.  \n @ \n Потрачено 100 тенге'
                            
                'Никто тебя за уши тянуть не будет, Сыченька!':
                    jump lbl_developement 
                    
        "Назад":
            call lbl_universal_menu

    jump lbl_universal_menu  
    return    