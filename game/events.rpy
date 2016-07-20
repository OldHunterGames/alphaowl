python:
    import sys
    sys.path.append(renpy.loader.transfn("scrypts"))
    from events import *
    
# !!!!!! REGISTER EACH EVENT HERE !!!!
label init_events:
    # $ register_event('evn_dvach_coding')
    # $ register_event('evn_dvach_conversation')
    # $ register_event('evn_dvach_sex')
    # $ register_event('evn_dvach_sports')
    # $ register_event('evn_dvach_b')
    # $ register_event('evn_dvach_fap')
    # $ register_event('evn_dvach_olgino')

    $ register_event('evn_do_practice_programm_chat')
    $ register_event('evn_do_practice_programm')
    $ register_event('evn_do_practice_labs_chat')
    $ register_event('evn_do_practice_labs')
    $ register_event('evn_do_practice_military_chat')
    $ register_event('evn_do_practice_military')
    $ register_event('evn_do_gym')
    $ register_event('evn_do_major')

    $ register_event('evn_angst_minor')
    $ register_event('evn_angst_major')

    $ register_event('evn_bugurt_gazeta') 
    $ register_event('evn_bugurt_dildak') 
    $ register_event('evn_bugurt_dindin') 
    $ register_event('evn_bugurt_topor') 
    $ register_event('evn_bugurt_church')     
    
    return True
    
#TESTS & TEMPLATES 

label evn_blank:
   $pass   
   return True
  
label evn_template(event):
    
    #Проверка для турн энда
    if not event.skipcheck:
        if True:
            $ event.skipcheck = True
    # Вообще это должно делаться не так, но в сыче пойдет
    if event.target != child:
        $ event.skipcheck = False 
    
    # Отсечка
    if not event.skipcheck:
        return False
       
        
    #тело эвента
    return True


###################### ПРОКАЧКА НАВЫКОВ ################################## 

label evn_teach_coding(event):
    if event.target != child:
        $ event.skipcheck = False    
    if not event.skipcheck:
        return False    
    python:
        event.target.skill('coding').training = True
    'С++ для чайников! Получен базовый навык программирования.'
    return True

label evn_teach_conversation(event):
    if event.target != child:
        $ event.skipcheck = False    
    if not event.skipcheck:
        return False    
    python:
        event.target.skill('conversation').training = True
    'Чтобы справиться с Ерохой, надо мыслить как Ероха! Получен базовый навык социоблядства.'
    return True

label evn_teach_sex(event):
    if event.target != child:
        $ event.skipcheck = False    
    if not event.skipcheck:
        return False            
    python:
        event.target.skill('sex').training = True
    'BATYA знает как долго не кончать! Получена базовая сексуальная грамотность.'
    return True

label evn_teach_sports(event):
    if event.target != child:
        $ event.skipcheck = False    
    if not event.skipcheck:
        return False            
    python:
        event.target.skill('sport').training = True
    'Соблюдает дня режим - дЖым! Получены базовые знания о ЗОЖ.'
    return True
    

#################### ОЧОБА #########################


label evn_do_major(event):
    if not event.skipcheck:
        if 'major' in game.studies:
            $ event.skipcheck = True
    if event.target != child or 'major' not in game.studies:
        $ event.skipcheck = False    
            
    
    if not event.skipcheck:
        return False 
    'Пора делать курсовую, курсовая сама себя не сделает.'
    
    python:
        actor = event.target
        threshold = 3
        difficulty = 2 
        morality = actor.check_moral('lawful')
        result = game.threshold_skillcheck(actor = actor, skill = 'coding', difficulty = difficulty, tense_needs=['amusement', 'activity'], satisfy_needs=['ambition'], beneficiar=actor, morality=morality, success_threshold=threshold)
        if result[0]:
            txt = "Берешь себя за задницу покрепче \n @ \n Делаешь курсач как надо  \n @ \n Потом ещё неделю ловишь научрука... "
            game.studies.remove('major')        
            event.target.skill('coding').get_expirience(4)
            actor.merit = 5
            actor.add_condition('merit')
        else:
            txt = "Твёрдо решаешь засесть за курсовую \n @ \n Что-то сложновато  \n @ \n Завтра сделаю  \n @ \n За неделю - два параграфа..."
   
    '[txt]'
   
    return True

label evn_do_gym(event):
    if not event.skipcheck:
        if 'gym' in game.studies:
            $ event.skipcheck = True
    if event.target != child or 'gym' not in game.studies:
        $ event.skipcheck = False    
            
    
    if not event.skipcheck:
        return False
        
    'Зачёт по физре'
    python:
        actor = event.target
        threshold = 2
        difficulty = 1 
        morality = actor.check_moral('ardent')
        result = game.threshold_skillcheck(actor = actor, skill = 'sport', difficulty = difficulty, tense_needs=['comfort'], satisfy_needs=['activity','ambition'], beneficiar=actor, morality=morality, success_threshold=threshold)
        
        if not result[0]:
            txt = "Лазаем по канату \n @ \n Ебнулся на копчик  \n @ \n Группа ржёт как стадо гиен"
            actor.add_condition('sin')
        else:
            txt = "Четко подтягиваешься \n @ \n Стометровка в нормативе  \n @ \n Фазген-семпай хвалит - ай, братуха-борцуха!"
            game.studies.remove('gym')       
            event.target.skill('sport').get_expirience(2)
            actor.add_condition('merit')
   
    '[txt]'
   
    return True

label evn_do_practice_military(event):
    if not event.skipcheck:
        if 'military' in game.studies:
            $ event.skipcheck = True
    if event.target != child or 'military' not in game.studies:
        $ event.skipcheck = False    
            
    
    if not event.skipcheck:
        return False
   
    'Зачёт на военной кафедре (строевая)'
    python:
        actor = event.target
        threshold = 2
        difficulty = 1 
        morality = actor.check_moral('lawful')
        result = game.threshold_skillcheck(actor = actor, skill = 'sport', difficulty = difficulty, tense_needs=['comfort'], satisfy_needs=['activity','ambition'], beneficiar=actor, morality=morality, success_threshold=threshold)
        
        if not result[0]:
            txt = "В колонну по двое \n @ \n Равнение на знамя \n @ \n Отдавил ноги впереди идущему \n @ \n Из-за тебя вся группа идет на пересдачу"
            actor.add_condition('sin')
        else:
            txt = "Вспоминаешь видос про парад в лучшей Корее \n @ \n В голове играет hellmarch \n @ \n Шаг печаетается сам собой "
            game.studies.remove('military')  
            event.target.skill('sport').get_expirience(2)
            actor.add_condition('merit')
   
    '[txt]'
   
    return True

label evn_do_practice_military_chat(event):
    if not event.skipcheck:
        if 'military' in game.studies:
            $ event.skipcheck = True
    if event.target != child or 'military' not in game.studies:
        $ event.skipcheck = False    
            
    
    if not event.skipcheck:
        return False
   
    'Зачёт на военной кафедре (общение)'
   
    python:
        actor = event.target
        threshold = 2
        difficulty = 2 
        morality = actor.check_moral('chaotic')
        result = game.threshold_skillcheck(actor = actor, skill = 'conversation', difficulty = difficulty, tense_needs=[], satisfy_needs=['communication'], beneficiar=actor, morality=morality, success_threshold=threshold)
        
        if not result[0]:
            txt = "Пытаешься подружиться с подполканом \n @ \n А он вообще контуженный \n @ \n По итогам разговора - драишь до вечера очки"
            actor.add_condition('sin')
        else:
            txt = "Расспрашиваешь старого подполкана про боевой опыт \n @ \n Он пускает скупую слезу по авганским друзьям \n @ \n И рисует тебе зачёт автоматом"
            game.studies.remove('military')    
            event.target.skill('conversation').get_expirience(3)
            actor.add_condition('merit')
   
    '[txt]'
   
    return True
   
label evn_do_practice_labs(event):
    if not event.skipcheck:
        if 'labs' in game.studies:
            $ event.skipcheck = True
    if event.target != child or 'labs' not in game.studies:
        $ event.skipcheck = False    
            
    
    if not event.skipcheck:
        return False
        
    'Лабораторная по программированию (брутфорс)'
   
    python:
        actor = event.target
        threshold = 2
        difficulty = 1 
        morality = actor.check_moral('lawful', 'timid')
        result = game.threshold_skillcheck(actor = actor, skill = 'coding', difficulty = difficulty, tense_needs=['amusement'], satisfy_needs=['ambition'], beneficiar=actor, morality=morality, success_threshold=threshold)
        
        if not result[0]:
            txt = "Пытаешься понять как это вообще работает \n @ \n Создаёшь велосипед на костыльной тяге  \n @ \n Но у тебя даже баги не фурычат"
            actor.add_condition('sin')
        else:
            txt = "Вспоминаешь чему вас учили \n @ \n Сдаёшь профессору кривое но рабочее решение  \n @ \n А он и не против!"
            game.studies.remove('labs')     
            event.target.skill('coding').get_expirience(2)
            actor.add_condition('merit')
   
    '[txt]'
   
    return True

label evn_do_practice_labs_chat(event):
    if not event.skipcheck:
      if 'labs' in game.studies:
          $ event.skipcheck = True
    if event.target != child or 'labs' not in game.studies:
        $ event.skipcheck = False    
            

    if not event.skipcheck:
        return False
        
    'Лабораторная по программированию (попытка списать)'
   
    python:
        actor = event.target
        threshold = 3
        difficulty = 2 
        morality = actor.check_moral('chaotic', 'ardent')
        result = game.threshold_skillcheck(actor = actor, skill = 'conversation', difficulty = difficulty, tense_needs=['ambition'], satisfy_needs=['communication'], beneficiar=actor, morality=morality, success_threshold=threshold)
        
        if not result[0]:
            txt = "Просишь у ботанов решение \n @ \n Послан нахуй  \n @ \n Даже ебаные задроты считают что они лучше тебя"
            actor.add_condition('sin')
        else:
            txt = "Среди ботанов все свои \n @ \n Один из них такой же некрофил как профессор \n @ \n Можно самому и не напрягаться"
            game.studies.remove('labs')  
            event.target.skill('conversation').get_expirience(3)
            actor.add_condition('merit')
   
    '[txt]'
   
    return True

label evn_do_practice_programm(event):        
    if not event.skipcheck:
        if 'practice' in game.studies:
            $ event.skipcheck = True
    if event.target != child or 'practice' not in game.studies:
        $ event.skipcheck = False

    if not event.skipcheck:
        return False
        
    'Производственная практика'
   
    python:
        actor = event.target
        threshold = 3
        difficulty = 2 
        morality = actor.check_moral('lawful', 'timid')
        result = game.threshold_skillcheck(actor = actor, skill = 'coding', difficulty = difficulty, tense_needs=['amusement'], satisfy_needs=['ambition'], beneficiar=actor, morality=morality, success_threshold=threshold)
        
        if not result[0]:
            txt = "Весь день носишь ящики с перфокартами \n @ \n Роняешь один себе на ногу  \n @ \n Ренген показывает трещину \n @ \n  Неделю свободен"
            actor.add_condition('sin')
        else:
            txt = "Скармлваешь Эльбрусу ящик перфокарт \n @ \n Понимаешь что это прикольно \n @ \n Как рулон бумаги в унитаз смыть  \n @ \n Руководитель подмахивает зачёт за усидчивость"
            game.studies.remove('practice')   
            event.target.skill('coding').get_expirience(3)
            actor.add_condition('merit')
   
    '[txt]'
   
    return True 

label evn_do_practice_programm_chat(event):          
    if not event.skipcheck:
        if 'practice' in game.studies:
            $ event.skipcheck = True
    if event.target != child or 'practice' not in game.studies:
        $ event.skipcheck = False

    if not event.skipcheck:
        return False
        
    'Производственная практика (общение)'
    python:
        actor = event.target
        threshold = 2
        difficulty = 1 
        morality = actor.check_moral('chaotic', 'ardent')
        result = game.threshold_skillcheck(actor = actor, skill = 'conversation', difficulty = difficulty, tense_needs=[], satisfy_needs=['communication'], beneficiar=actor, morality=morality, success_threshold=threshold)
        
        if not result[0]:
            txt = "Коллектив в перерыве расслабляется \n @ \n Пьют технические жидкости \n @ \nСблеванул \n @ \ncлабоват ещё для взрослой работы"
            actor.add_condition('sin')
        else:
            txt = "Забухал с коллективом в подсобке \n @ \n Рассказал охуительных историй с учёбы \n @ \n Подписали весь лист практики на год вперёд"
            game.studies.remove('practice')        
            event.target.skill('conversation').get_expirience(2)
            actor.add_condition('merit')
   
    '[txt]'
   
    return True   

#################### ЖЕТОНЫ ##########################   
  
label evn_angst_minor(event):
    
    #Проверка для турн энда
    if not event.skipcheck:
        if True:
            $ event.skipcheck = True
    # Вообще это должно делаться не так, но в сыче пойдет
    if event.target != child:
        $ event.skipcheck = False
    if event.target.anxiety < 1:
        $ event.skipcheck = False
    
    # Отсечка
    if not event.skipcheck:
        return False
        
    #тело эвента
    python:
        event.target.anxiety -= 1
    'Сработал ангст Сычика. Он впадает в истерику... (потрачен 1 ангст)'
    return True   
  
label evn_angst_major(event):
    
    #Проверка для турн энда
    if not event.skipcheck:
        if True:
            $ event.skipcheck = True
    # Вообще это должно делаться не так, но в сыче пойдет
    if event.target != child:
        $ event.skipcheck = False
    if event.target.anxiety < event.target.spirit:
        $ event.skipcheck = False
    
    # Отсечка
    if not event.skipcheck:
        return False
        
    #тело эвента
    python:
        event.target.anxiety -= 1
        child.feature.append('dead')
    'Ангст Сычика больше его силы воли./n @ /nСлучайное событие Сычик выпиливается.)'
    return True   
      
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
####################### ФИЛЛЕРЫ   
   
label evn_bugurt_gazeta(event):
   "К НАМ СКОРО ЕРОХИНЫ ПРИДУТ \n @ \nГАЗЕТКИ ИЗ ТУАЛЕТА УБЕРИ \n @ \nПОЛОЖИ БУМАГУ ТУАЛЕТНУЮ \n @ \n И САМ В ТУАЛЕТЕ ОСТАВАЙСЯ\n @ \n ЧТОБЫ МАТЕРИ ЗА ТЕБЯ НЕ СТЫДИТЬСЯ"
   
   return True

label evn_bugurt_dildak(event):
   "СЫНА, Я У ТЕБЯ В ШКАФУ НАШЕЛ КОЕ-ЧТО\n @ \nЗАЧЕМ ТЕБЕ ЭТО?\n @ \n  ТЫ ЧТО ГОМОСЕК? ЗАЧЕМ ТЕБЕ ЧЛЕН РЕЗИНОВЫЙ? \n @ \nМАТЕРИ НЕ СКАЖУ, НО ЗАБИРАЮ!"
   
   return True

label evn_bugurt_dindin(event):
   "У ТЕБЯ ХОТЬ С ДЕВОЧКОЙ-ТО БЫЛО \n @ \nНУ ЭТО, ДИНЬ-ДИНЬ ТАМ \n @ \nИЛИ ТОЛЬКО С ЛОШАДЬМИ ЦВЕТНЫМИ?"
   
   return True
   
label evn_bugurt_topor(event):
   "ОТКРОЙ! НЕМЕДЛЕННО ОТКРОЙ!\n @ \n Я ДОЛЖНА ЗНАТЬ, МОЙ СЫН ДЕЛОМ ЗАНЯТ ИЛИ ОПЯТЬ БАЛДУ ПИНАЕШЬ!\n @ \n ТАК, НУ ВСЕ, ОТЕЦ ЗА ТОПОРОМ ПОШЕЛ\n @ \n СЕЙЧАС ДВЕРЬ ВЫНОСИТЬ БУДЕМ!"
   
   return True
   
label evn_bugurt_church(event):
   "ЗАВТРА ИДЕШЬ В ЦЕРКОВЬ ИСПОВЕДЫВАТЬСЯ\n @ \nРАСКАЖЕШЬ БАТЮШКЕ ПРО ВСЕ СВОИ ТЕМНЫЕ ДЕЛА\n @ \nИ КАК ЧЕРТЕЙ ПО ЭКРАНУ ГОНЯЕШЬ\n @ \nИ КАК ТИЛИБОНЬКАЕШЬ\n @ \nИ КАК У ДЕДА ПОСЛЕДНЮЮ КОСТЬ ОТОБРАЛ!"

   return True
   
label evn_bugurt_build:
   "СВОЙ ДОМ ОН ХОЧЕТ\n @ \n ЧТО ТЫ ПОСТРОИШЬ?! НИЧЕГО ТЫ НЕ ПОСТРОИШЬ!\n @ \n ПОСТРОИТ ОН\n @ \n ТЫ ХОТЬ КОПЕЕЧКУ ТО В ДОМ ПРИНЁС?"
   
   return True
   
label evn_bugurt_stulchak:
   "ОПЯТЬ СТУЛЬЧАК ОБОССАЛ\n @ \nНЕ ТЫ КОНЕЧНО!ОТЕЦ СИДЯ СИКАЕТ\n @ \nА ТЫ ВСЁ ОБОССЫВАЕШЬ В ТУАЛЕТЕ \n @ \nЯ ВЫТИРАТЬ ЗА ТОБОЙ ДОЛЖНА?!"
   
   return True
   
label evn_bugurt_b:
   "ЗАЩЕЛ В /b \n @ \nПОСТЯТ ОДНО РАКОВОЕ ГОВНО\n @ \n ВЫШЕЛ \n @ \nЧЕРЕЗ ПЯТЬ МИНУТ СНОВА ЗАХОДИШЬ\n @ \n О! РУЛЕТОЧКА!!!"
   python:
       pass
   
   return True
   
label evn_bugurt_pasta:
   "ИДЕШЬ ПО УЛИЦЕ\n @ \nВСПОМИНАЕШЬ СМЕШНУЮ ПАСТУ ИЛИ ПИКЧУ С ДВОЩИКА\n @ \nПРОИГРЫВАЕШЬ НА ВСЮ УЛИЦУ\n @ \nЛЮДИ ВОКРУГ СМОТРЯТ КАК НА ИДИОТА"
   python:
       pass
   
   return True
   
label evn_bugurt_sol:
   "МАМКА ПРОСИТ ПЕРЕДАТЬ СОЛЬ\n @ \nСЛУЧАЙНО РОНЯЕШЬ И РАССЫПАЕШЬ \n @ \nНУ ВОТ....ОПЯТЬ....КРИВОРУКИЙ \n @ \nПОТИХОНЬКУ НАЧИНАЕТ НАГНЕТАТЬ ОБСТАНОВКУ \n @ \n ЧЕРЕЗ ПЯТЬ МИНУТ УЖЕ ВОВСЮ ОРЁТ И ПРИЧИТАЕТ ПОЧЕМУ ТЫ НЕ КАК ЕРОХИН, ПОЧЕМУ ТЫ ТАКОЙ ТУПОЙ\n @ \nЗАЯВЛЯЕТ, ЧТО В ОДИН ПРЕКРАСНЫЙ МОМЕНТ НЕ ВЫДЕРЖИТ И ВЫКИНЕТ ТЕБЯ ИЗ КВАРТИРЫ"
   python:
       pass
   
   return True
   
label evn_bugurt_pozdno:
   "КУДА СОБРАЛСЯ ТАК ПОЗДНО?\n @ \n КТО ТАМ БУДЕТ?\n @ \n ПРОДИКТУЙ ТЕЛЕФОН И КАК ЗОВУТ\n @ \nА ДЕВОЧКИ БУДУТ? \n @ \n СМОТРИ У МЕНЯ, ЕСЛИ ЧТО НАТВОРИШЬ МЫ ТЕБЯ ОТМАЗЫВАТЬ ОТ ТЮРЬМЫ НЕ БУДЕМ"
   python:
       pass
   
   return True
          





















label evn_dvach_coding(event):
    if not event.target.skill('coding').training and event.target == event.target and 'pc' not in event.target.restrictions:
        $ event.skipcheck = True
    
    if event.target != child:
        $ event.skipcheck = False    
            

    if not event.skipcheck:
        return False
        
    python:
        event.target.skill('coding').training = True
    'Двач = образовательный! Получен базовый навык программирования.'
    return True

label evn_dvach_conversation(event):
    if not event.skipcheck:
        if not event.target.skill('conversation').training and 'pc' not in event.target.restrictions:
            $ event.skipcheck = True
    
    if event.target != child:
        $ event.skipcheck = False    
            
    
    if not event.skipcheck:
        return False
        
    python:
        event.target.skill('conversation').training = True
    'Двач = образовательный! Получен базовый навык социоблядства.'
    return True

label evn_dvach_sex(event):
    if not event.skipcheck:
        if not event.target.skill('sex').training and 'pc' not in event.target.restrictions:
            $ event.skipcheck = True
    if event.target != child:
        $ event.skipcheck = False    
            
    
    if not event.skipcheck:
        return False
        
    python:
        event.target.skill('sex').training = True
    'Двач = образовательный! Получена базовая сексуальная грамотность.'
    return True

label evn_dvach_sports(event):
    if not event.skipcheck:
        if not event.target.skill('sport').training and 'pc' not in event.target.restrictions:
            $ event.skipcheck = True
    if event.target != child:
        $ event.skipcheck = False    
            
    
    if not event.skipcheck:
        return False
        
    python:
        event.target.skill('sport').training = True
    'Двач = образовательный! Получены базовые знания о ЗОЖ.'
    return True

label evn_dvach_b(event):
    if not event.skipcheck:
        if 'pc' not in event.target.restrictions:
            $ event.skipcheck = True
    if event.target != child:
        $ event.skipcheck = False    
            
    
    if not event.skipcheck:
        return False
        
    python:
        event.target.amusement.satisfaction = 2
        event.target.communication.satisfaction = 2     
    'Сосач \n @ \nЛамповый. Твой. (2) \n @ \nТут все твои друзья (общение +2).'
    return True

label evn_dvach_fap(event):
    if not event.skipcheck:
        if 'pc' not in event.target.restrictions:
            $ event.skipcheck = True

    if event.target != child:
        $ event.skipcheck = False    
            
    
    if not event.skipcheck:
        return False
        
    $ event.target.eros.satisfaction = 1
    'Обмалафился. Половое удовлетворение (1)'
    return True

label evn_dvach_olgino(event):
    if not event.skipcheck:
        if 'pc' not in event.target.restrictions:
            $ event.skipcheck = True
    if event.target != child:
        $ event.skipcheck = False    
            
    
    if not event.skipcheck:
        return False
        
    python:
        game.tenge += 15
    'Понадусёровые швайнокараси порвались. +15!'
    return True
  
   