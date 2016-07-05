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

        

        "Воспитание":
            call lbl_discipline

            
    jump lbl_mom_manage
    
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

label lbl_rules_drugs:
    menu:
        'Пресечь любую дрочку' if 'masturbation' not in child.restrictions:
            $ child.restrictions.append('masturbation')
            $ child.schedule.add_action('fap_no')
            $ txt = 'Сыночка то наш, всё пиструнчик свой тилибонькает \n @ \n Скоро волосы на руках расти начнут \n @ \n В антимастурбационном кресте будещь спать, по совету отца Агапия'
        'Игнорировать дрочку' if 'masturbation' in child.restrictions:
            $ child.restrictions.remove('masturbation')
            $ child.schedule.add_action('fap_yes')
            $ txt = 'А что это ты в ванной столько времени сидишь, Сыча? \n @ \n И то хорошо \n @ \n Приучили к чистоте ребёнка то'            
        'Запретить алкоголь' if 'alcohol' not in child.restrictions:
            $ child.restrictions.append('alcohol')
            $ child.schedule.add_action('alcohol_no')
            $ txt = 'Ты на пиво то не заглядвайся \n @ \n Ещё нос не дорос \n @ \n Я малолетних алкоголиков в доме не потерплю'
        'Пусть накатит с BATYей' if 'alcohol' in child.restrictions:
            $ child.restrictions.remove('alcohol')
            $ child.schedule.add_action('alcohol_yes')
            $ txt = 'За дидов рюмашечку надо обязательно \n @ \n Что значит "не буду стекломой пить" \n @ \n Традиции наши не уважаешь?'                 
        'Запретить курить' if 'tobacco' not in child.restrictions:
            $ child.restrictions.append('tobacco')
            $ child.schedule.add_action('smoke_no')
            $ txt = 'Если почую табачный запах \n @ \n Всё отцу расскажу \n @ \n Неделю у меня сидеть на жопе не сможешь'
        'Пусть курит но не дома' if 'tobacco' in child.restrictions:
            $ child.restrictions.remove('tobacco')
            $ child.schedule.add_action('smoke_yes')
            $ txt = 'Сыченька то бодрячком \n @ \n Каждые пять минут в падик бегает \n @ \n Наверное друзья у него там'         
        'Запретить спайсы' if 'weed' not in child.restrictions:
            $ child.restrictions.append('weed')
            $ child.schedule.add_action('weed_no')
            $ txt = 'Чтобы я тебя с этими наркоманами не видела больше \n @ \n Пообколются своей марихуанной \n @ \n А потом ябут друг-друга в жёппы'
        'Игнорировать спайсы' if 'weed' in child.restrictions:
            $ child.restrictions.remove('weed')
            $ child.schedule.add_action('weed_yes')
            $ txt = 'Ой а что это за штучка такая у тебя, Сыча? \n @ \n Для ароматизации помещения да? \n @ \n И вот сюда вот воду заливать?'                     
        'Назад':
            jump lbl_rules
    "[txt]"
    
    return


label lbl_rules_behavior:
    menu:
        'Запретить гулять' if 'dates' not in child.restrictions:
            $ child.restrictions.append('dates')
        'Разрешить гулять до поздна' if 'dates' in child.restrictions:
            $ child.restrictions.remove('dates')
        'Запретить общаться с друзьями' if 'friends' not in child.restrictions:
            $ child.restrictions.append('friends')
        'Разрешить общаться с друзьями' if 'friends' in child.restrictions:
            $ child.restrictions.remove('friends')
        'Конплюхтерн для очобы! (блокировать интернет)' if 'pc' not in child.restrictions:
            $ child.restrictions.append('pc')
        'Ну и сиди за своим комплюктером' if 'pc' in child.restrictions:
            $ child.restrictions.remove('pc')
        'Назад':
            jump lbl_rules
            
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
        'Какус "Антирадиационный" (10 тенгэ)' if "cactus" not in game.mom_stuff:
            python:
                if game.tenge >= 10:
                    txt = "КАНПУКТЕР ОБЛУЧАЕТ РАДИАЦИЕЙ \n@\nСЫЧА, СРОЧНО ПОСТАВЬ КАКТУС К ЭКРАНУ\n@\nУЧОНЫЕ ПО РЕН-ТВ ТОЛЬКО ЧТО СКАЗАЛИ\n"
                    game.mom_stuff.append("cactus")
                    game.tenge -= 10
                else:
                    txt = "ПРИХОДИШЬ В МАГАЗ\n @\n И ДАЖЕ СРАНЫЙ КАКТУС НЕ МОЖЕШЬ КУПИТЬ\n @\n ТЕНГЕ НЕ ХВАТАЕТ"
        'Сервиз "Мойхрусталь" (25 тенгэ)' if "service" not in game.mom_stuff:
            python:
                if game.tenge >= 25:
                    txt = "ХРУСТАЛЬ - ЭТО ТВОЕ ПРИДАНОЕ. ПОСТАВЬ В СЕРВАНТ. \n@\nСЕЙЧАС ТАКОЙ НЕ ДЕЛАЮТ, ЭТО ВЕНГЕРСКИЙ! \n@\nИ ПЫЛЬ ПРОСТРИ С НЕГО, НЕ БЕРЕЖЕШЬ СОВСЕМ \n"
                    game.mom_stuff.append("service")
                    game.tenge -= 25
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
        'Ковёр "Какулюдей" (100 тенгэ)' if "carpet" not in game.mom_stuff:
            python:
                if game.tenge >= 100:
                    txt = "ПРИЕХАЛИ ДЯДЯ БАФОМЕТ И ТЁТЯ СРАКА \n@\n ОЙ СЫЧА СРОЧНО НЕСИ СВОЙ ПОЛЯРОИД\n@\n НА ФОНЕ КОВРА НАС СНИМИ. КРСИВО И БОХАТО! \n"
                    game.mom_stuff.append("carpet")
                    game.tenge -= 100
                else:
                    txt = "ПРИХОДИШЬ В МАГАЗ\n @\n И ДАЖЕ СРАНЫЙ КОВЁР НЕ МОЖЕШЬ КУПИТЬ\n @\n ТЕНГЕ НЕ ХВАТАЕТ"
        'Шубка "Кандибобер" (100 тенгэ)' if "fur" not in game.mom_stuff:
            python:
                if game.tenge >= 100:
                    txt = "ОЙ А ЧТО ЭТО ЗА МЕХ ТАКОЙ? \n@\nЭТО МЕТИС. МЕТИС. \n@\nПАПА - НОРКА. МАМА - БОБЁР \n"
                    game.mom_stuff.append("fur")
                    game.tenge -= 100
                else:
                    txt = "ПРИХОДИШЬ В МАГАЗ\n @\n И ДАЖЕ СРАНУЮ ШУБУ НЕ МОЖЕШЬ КУПИТЬ\n @\n ТЕНГЕ НЕ ХВАТАЕТ"
        'Гарнитур-стенка "Мечта застоя" (250 тенгэ)' if "furniture" not in game.mom_stuff:
            python:
                if game.tenge >= 250:
                    txt = "ОЙ Я ВСЕГДА МЕЧТАЛА О ТАКОЙ РОСКОШНОЙ СТЕНКЕ \n@\nСЫЧА, НУ КА РАСЧИСТЬ ПРОСТРАНСТВО \n@\nНЕ ВЫБРАСЫВАЙ ТОЛЬКО НИЧЕГО, НА ДАЧУ УВЕЗЁМ \n"
                    game.mom_stuff.append("furniture")
                    game.tenge -= 250
                else:
                    txt = "ПРИХОДИШЬ В МАГАЗ\n @\n И ДАЖЕ СРАНЫЙ ГАРНИТУР МОЖЕШЬ КУПИТЬ\n @\n ТЕНГЕ НЕ ХВАТАЕТ"

        'Назад':
            jump lbl_mom_manage
            
    
    '[txt]'    

    return   
    

label lbl_developement:
    menu:
        "Надо что-то сделать для развития сыночки-корзиночки."
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