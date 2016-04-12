python:
    import sys
    sys.path.append(renpy.loader.transfn("scrypts"))
    from events import *
    
# !!!!!! REGISTER EACH EVENT HERE !!!!
label init_events:
    $ register_event('evn_dvach_coding')
    $ register_event('evn_dvach_conversation')
    $ register_event('evn_dvach_sex')
    $ register_event('evn_dvach_sports')
    $ register_event('evn_dvach_b')
    $ register_event('evn_dvach_fap')
    $ register_event('evn_dvach_olgino')

    $ register_event('evn_bugurt_gazeta') 
    return True
    
#TESTS & TEMPLATES 

label evn_blank:
   $pass   
   return True
  
label evn_template(character):
    
    #Проверка для турн энда
    if not game.evn_skipcheck:
        if True:
            $ game.evn_skipcheck = True
    
    # Отсечка
    if not game.evn_skipcheck:
        return False
        
    #тело эвента
    return True


######################################################## 


label evn_dvach_coding(character):
    
    if not game.evn_skipcheck:
        if not character.skill('coding').training and character == child and 'pc' not in child.restrictions:
            $ game.evn_skipcheck = True

    if not game.evn_skipcheck:
        return False
        
    python:
        character.skill('coding').training = True
    'Двач = образовательный! Получен базовый навык программирования.'
    return True

label evn_dvach_conversation(character):
    
    if not game.evn_skipcheck:
        if not child.skill('conversation').training and 'pc' not in child.restrictions:
            $ game.evn_skipcheck = True

    if not game.evn_skipcheck:
        return False
        
    python:
        child.skill('conversation').training = True
    'Двач = образовательный! Получен базовый навык социоблядства.'
    return True

label evn_dvach_sex(character):
    
    if not game.evn_skipcheck:
        if not child.skill('sex').training and 'pc' not in child.restrictions:
            $ game.evn_skipcheck = True

    if not game.evn_skipcheck:
        return False
        
    python:
        child.skill('sex').training = True
    'Двач = образовательный! Получена базовая сексуальная грамотность.'
    return True

label evn_dvach_sports(character):
    
    if not game.evn_skipcheck:
        if not child.skill('sports').training and 'pc' not in child.restrictions:
            $ game.evn_skipcheck = True

    if not game.evn_skipcheck:
        return False
        
    python:
        child.skill('sports').training = True
    'Двач = образовательный! Получены базовые знания о ЗОЖ.'
    return True

label evn_dvach_b(character):
    
    if not game.evn_skipcheck:
        if 'pc' not in child.restrictions:
            $ game.evn_skipcheck = True

    if not game.evn_skipcheck:
        return False
        
    python:
        child.amusement.set_shift(2)
        child.communication.set_shift(2)        
    'Сосач \n @ \nРазвлечение (2) \n @ \nОбщение (2).'
    return True

label evn_dvach_fap(character):
    
    if not game.evn_skipcheck:
        if 'pc' not in child.restrictions:
            $ game.evn_skipcheck = True

    if not game.evn_skipcheck:
        return False
        
    $ child.debauch.set_shift(1)
    'Обмалафился. Удовлетворение потребности в дебоше (1)'
    return True

label evn_dvach_olgino(character):
    
    if not game.evn_skipcheck:
        if 'pc' not in child.restrictions:
            $ game.evn_skipcheck = True

    if not game.evn_skipcheck:
        return False
        
    python:
        game.tenge += 15
    'Понадусёровые швайнокараси порвались. +15!'
    return True

label evn_do_major:
   $ result = child.use_skill('coding')
   
   python:
       if result < 5:
           txt = "Твёрдо решаешь засесть за курсовую \n @ \n Что-то сложновато  \n @ \n Завтра сделаю  \n @ \n За неделю - два параграфа..."
       else:
           txt = "Берешь себя за задницу покрепче \n @ \n Делаешь курсач как надо  \n @ \n Потом ещё неделю ловишь научрука... "
           game.studies.remove('major')        
   
   '[txt]'
   
   return True

label evn_do_gym:
   $ result = child.use_skill('sport')
   
   python:
       if result < 5:
           txt = "Лазаем по канату \n @ \n Ебнулся на копчик  \n @ \n Группа ржёт как стадо гиен"
       else:
           txt = "Четко подтягиваешься \n @ \n Стометровка в нормативе  \n @ \n Фазген-семпай хвалит - ай, братуха-борцуха!"
           game.studies.remove('gym')        
   
   '[txt]'
   
   return True

label evn_do_practice_military:
   $ result = child.use_skill('sport')
   
   python:
       if result < 5:
           txt = "В колонну по двое \n @ \n Равнение на знамя \n @ \n Отдавил ноги впереди идущему \n @ \n Из-за тебя вся группа идет на пересдачу"
       else:
           txt = "Вспоминаешь видос про парад в лучшей Корее \n @ \n В голове играет hellmarch \n @ \n Шаг печаетается сам собой "
           game.studies.remove('military')        
   
   '[txt]'
   
   return True

label evn_do_practice_military_chat:
   $ result = child.use_skill('communication')
   
   python:
       if result < 5:
           txt = "Пытаешься подружиться с подполканом \n @ \n А он вообще контуженный \n @ \n По итогам разговора - драишь до вечера очки"
       else:
           txt = "Расспрашиваешь старого подполкана про боевой опыт \n @ \n Он пускает скупую слезу по авганским друзьям \n @ \n И рисует тебе зачёт автоматом"
           game.studies.remove('military')        
   
   '[txt]'
   
   return True
   
label evn_do_practice_labs:
   $ result = child.use_skill('coding')
   
   python:
       if result < 5:
           txt = "Пытаешься понять как это вообще работает \n @ \n Создаёшь велосипед на костыльной тяге  \n @ \n Но у тебя даже баги не фурычат"
       else:
           txt = "Вспоминаешь чему вас учили \n @ \n Сдаёшь профессору кривое но рабочее решение  \n @ \n А он и не против!"
           game.studies.remove('labs')        
   
   '[txt]'
   
   return True

label evn_do_practice_labs_chat:
   $ result = child.use_skill('communication')
   
   python:
       if result < 5:
           txt = "Просишь у ботанов решение \n @ \n Получаешь кукишь с м  \n @ \n Даже ебаные задроты считают что они лучше тебя"
       else:
           txt = "Среди ботанов все свои \n @ \n Один из них такой же некрофил как профессор \n @ \n Можно самому и не напрягаться"
           game.studies.remove('labs')        
   
   '[txt]'
   
   return True

label evn_do_practice_programm:
   $ result = child.use_skill('coding')
   
   python:
       if result < 5:
           txt = "Весь день носишь ящики с перфокартами \n @ \n Роняешь один себе на ногу  \n @ \n Ренген показывает трещину \n @ \n  Неделю свободен"
       else:
           txt = "Скармлваешь Эльбрусу ящик перфокарт \n @ \n Понимаешь что это прикольно \n @ \n Как рулон бумаги в унитаз смыть  \n @ \n Руководитель подмахивает зачёт за усидчивость"
           game.studies.remove('practice')        
   
   '[txt]'
   
   return True 

label evn_do_practice_programm_chat:
   $ result = child.use_skill('communication')
   
   python:
       if result < 5:
           txt = "Коллектив в перерыве расслабляется \n @ \n Пьют технические жидкости  \n @ \n Сблеванул = слабоват ещё для взрослой работы"
       else:
           txt = "Забухал с коллективом в подсобке \n @ \n Рассказал охуительных историй с учёбы \n @ \n Подписали весь лист практики на год вперёд"
           game.studies.remove('practice')        
   
   '[txt]'
   
   return True   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
label evn_bugurt_gazeta(character):
   "К НАМ СКОРО ЕРОХИНЫ ПРИДУТ \n @ \nГАЗЕТКИ ИЗ ТУАЛЕТА УБЕРИ \n @ \nПОЛОЖИ БУМАГУ ТУАЛЕТНУЮ \n @ \n И САМ В ТУАЛЕТЕ ОСТАВАЙСЯ\n @ \n ЧТОБЫ МАТЕРИ ЗА ТЕБЯ НЕ СТЫДИТЬСЯ"
   python:
       pass
   
   return True

label evn_bugurt_dildak:
   "СЫНА, Я У ТЕБЯ В ШКАФУ НАШЕЛ КОЕ-ЧТО\n @ \nЗАЧЕМ ТЕБЕ ЭТО?\n @ \n  ТЫ ЧТО ГОМОСЕК? ЗАЧЕМ ТЕБЕ ЧЛЕН РЕЗИНОВЫЙ? \n @ \nМАТЕРИ НЕ СКАЖУ, НО ЗАБИРАЮ!"
   python:
       pass
   
   return True

label evn_bugurt_dindin:
   "У ТЕБЯ ХОТЬ С ДЕВОЧКОЙ-ТО БЫЛО \n @ \nНУ ЭТО, ДИНЬ-ДИНЬ ТАМ \n @ \nИЛИ ТОЛЬКО С ЛОШАДЬМИ ЦВЕТНЫМИ?"
   python:
       pass
   
   return True
   
label evn_bugurt_topor:
   "ОТКРОЙ! НЕМЕДЛЕННО ОТКРОЙ!\n @ \n Я ДОЛЖНА ЗНАТЬ, МОЙ СЫН ДЕЛОМ ЗАНЯТ ИЛИ ОПЯТЬ БАЛДУ ПИНАЕШЬ!\n @ \n ТАК, НУ ВСЕ, ОТЕЦ ЗА ТОПОРОМ ПОШЕЛ\n @ \n СЕЙЧАС ДВЕРЬ ВЫНОСИТЬ БУДЕМ!"
   python:
       pass
   
   return True
   
label evn_bugurt_kafe:
   "ЗАЧЕМ ТЕБЕ С ДЕВУШКОЙ В КАФЕ ИДТИ?\n @ \n ТОЛЬКО ДЕНЬГИ ПЕРЕВОДИТЬ.\n @ \n Я ВАС И ДОМА ПРЕКРАСНО НАКОРМЛЮ!\n @ \n КИДАЕТ В КИПЯТОК КУПЛЕННУЮ В МАГАЗИНЕ ПАЧКУ ПЕЛЬМЕНЕЙ"
   python:
       pass
   
   return True
   
label evn_bugurt_church:
   "ЗАВТРА ИДЕШЬ В ЦЕРКОВЬ ИСПОВЕДЫВАТЬСЯ\n @ \nРАСКАЖЕШЬ БАТЮШКЕ ПРО ВСЕ СВОИ ТЕМНЫЕ ДЕЛА\n @ \nИ КАК ЧЕРТЕЙ ПО ЭКРАНУ ГОНЯЕШЬ\n @ \nИ КАК ТИЛИБОНЬКАЕШЬ\n @ \nИ КАК У ДЕДА ПОСЛЕДНИЙ КУСОК ХЛЕБА ОТОБРАЛ!"
   python:
       pass
   
   return True
   
label evn_bugurt_build:
   "СВОЙ ДОМ ОН ХОЧЕТ\n @ \n ЧТО ТЫ ПОСТРОИШЬ?! НИЧЕГО ТЫ НЕ ПОСТРОИШЬ!\n @ \n ПОСТРОИТ ОН\n @ \n ТЫ ХОТЬ КОПЕЕЧКУ ТО В ДОМ ПРИНЁС?"
   python:
       pass
   
   return True
   
label evn_bugurt_stulchak:
   "ОПЯТЬ СТУЛЬЧАК ОБОССАЛ\n @ \nНЕ ТЫ КОНЕЧНО!ОТЕЦ СИДЯ СИКАЕТ\n @ \nА ТЫ ВСЁ ОБОССЫВАЕШЬ В ТУАЛЕТЕ \n @ \nЯ ВЫТИРАТЬ ЗА ТОБОЙ ДОЛЖНА?!"
   python:
       pass
   
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
      
   