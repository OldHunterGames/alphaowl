#Универсальное меню управления 

label lbl_universal_menu:
    $ info_provision = game.resource('provision')
    $ info_drugs = game.resource('drugs')
    menu:
        'Тенгэ: [game.money] | Жратва: [info_provision] | Вещества: [info_drugs]'
        
        "Взаимодействия с...":
            $ target = renpy.call_screen('sc_choose_character')
            call lbl_info_new(target)
            call lbl_target_menu
               
        "Магазин" if player == mom:
            call lbl_shop         
            
        "Следующая неделя" if game.can_skip_turn():
            jump label_new_day
            
    jump lbl_universal_menu
    return

label lbl_target_menu:
    menu:
        name = target.name()
        'Объект деятельности: [name]'
        "Расписание":
            call lbl_make_shedule
        "Важные события (AP:[player.ap])" if player.ap > 0:
            $ pass
        "Бытовые уловия" if player != child and target == child:
            call lbl_accommodation
        "Питание":
            call lbl_food_universal
        "Правила":
            $ pass
        "Одежда":
            $ pass
        "Карманные деньги":
            $ pass
        "Информация":
            call lbl_info_new(target)
        "Назад":
            jump lbl_universal_menu    
    
    jump lbl_target_menu
    return

label lbl_make_shedule:
        
    $ schedule_major = dname[player.job]
    
    menu:
        "По вечерам: [schedule_major]":
            if player == child:
                call lbl_son_major
            else:
                call lbl_shedule_major
        "В выходные: [shedule_minor]":
            if player == child:
                call lbl_son_minor
            else:
                $ pass
        "Общение: [communication]" if player != mom:
            call lbl_universal_interaction
            
        'Назад':
            jump lbl_universal_menu    
            
    jump lbl_make_shedule
        
label lbl_shedule_major:
    menu:
        'Воспитывать Сыченьку' if target == child:
            $ beneficiar = target.master
            $ code = None
            menu:
                'Кто этим займётся? Распиание основного времени этого персонажа изменится на "Воспитание". Если вы измените потом расписание, то воспитания не произойдёт.'
                'Маман':
                    $ mom.schedule.add_action('job_supervise')
                    $ mom.job_object().add_special_list_value('slaves', child)
                    $ actor = mom
                'BATYA':
                    $ batya.schedule.add_action('job_supervise')
                    $ actor = batya
                'Передумать':
                    jump lbl_shedule_major
            menu:
                'Какой подход выборать?'
                'Запугивание':
                    $ moral_burden = ['evil', 'intense', 'chaotic']
                    $ token = 'conquest'
                    jump lbl_torture_choose
                'Наказание':
                    $ moral_burden = ['evil', 'intense', 'lawful']
                    $ token = 'convention'
                    jump lbl_torture_choose
                'Поощрение':
                    $ moral_burden = ['good', 'timid', 'lawful']
                    $ token = 'convention'
                    jump lbl_pleasing_choose
                'Ублажение':
                    $ moral_burden = ['good', 'timid', 'chaotic']
                    $ token = 'contribution'
                    jump lbl_pleasing_choose
                'Передумать':
                    jump lbl_shedule_major                    
        "Назначить воспитателем" if player == mom:
            $ target.schedule.add_action('job_supervise')
        'Безделье':
            $ target.schedule.add_action('job_idle') 
        'Подрабатывать уборщицей' if target == mom:
            $ target.schedule.add_action('job_janitor') 
        'Делать уроки' if target == child:
            $ target.schedule.add_action('job_study') 
        "Назад":
            call lbl_make_shedule
    
    return

label lbl_torture_choose:
    menu:
        'Выберите основной способ давления.'
        'Бить ремнём (спорт)':
            $ self_satisfy = ['power', 'authority']
            $ self_tension = ['altruism']
            $ skill = 'sport'
            $ target_tension = ['wellness']
        'Хуесосить (коммуникация)':
            $ self_satisfy = ['power', 'authority']
            $ self_tension = ['altruism']
            $ skill = 'conversation'
            $ target_tension = ['authority', 'ambition']    
        'Ставить в угол (коммуникация)':
            $ self_satisfy = ['authority', 'order']
            $ self_tension = ['thrill']
            $ skill = 'conversation'
            $ target_tension = ['comfort', 'amusement', 'activity'] 
            
    $ special_values = {'skill': skill, 'torturer': actor, 'token': token, 'target_tension': target_tension, 'self_tension': self_tension,
                        'self_satisfy': self_satisfy, 'moral_burden': moral_burden, 'beneficiar': beneficiar}
    $ target.schedule.add_action('torture_check', special_values=special_values)
    
    jump lbl_universal_menu
    return

label lbl_pleasing_choose:
    menu:
        'Выберите основной способ ублажения.'
        'Похвала и доброта (коммуникация)':
            $ self_satisfy = ['altruism', 'communication']
            $ self_tension = ['power']
            $ skill = 'conversation'
            $ target_statisfy = ['communication', 'approval']
        'Поощрить самостоятельность (коммуникация)':
            $ self_satisfy = ['independence']
            $ self_tension = ['order', 'authority']
            $ skill = 'conversation'
            $ target_statisfy = ['independence', 'authority']            
        'Подарки (коммуникация, 5 тенгэ)':
            $ self_satisfy = ['altruism', 'communication']
            $ self_tension = ['power', 'prosperity']
            $ skill = 'conversation'
            $ target_statisfy = ['communication', 'approval']    
    
    $ special_values = {'skill': skill, 'executor': actor, 'token': token, 'target_statisfy': target_statisfy, 'self_tension': self_tension,
                        'self_satisfy': self_satisfy, 'moral_burden': moral_burden, 'beneficiar': beneficiar}
    $ target.schedule.add_action('pleasing_check', special_values=special_values)
    
    jump lbl_universal_menu
    return
    
label lbl_accommodation:
    menu:
        'Вечно ты в комнате запираешься от матери! Как сыч.':
            $ child.schedule.add_action('living_appartment')  
        'Комнату твою сдавать будем, поспишь у нас на диванчике.':
            $ child.schedule.add_action('living_cot')  
        'Диванчик для тёти Сраки, а тебе вот раскладушечка дедова.':
            $ child.schedule.add_action('living_mat')  
        'В ванной тебя запрём ночевать. Чтобы не воображал!':
            $ child.schedule.add_action('living_jailed')    
        'Ты у меня в шкафу сидеть будешь. Пока мать любить не научишься.':
            $ child.schedule.add_action('living_confined')    
    
    return

label lbl_food_universal:
    menu:
        'Размер пайки.'
        '"Не кормить (starvation)"':
            $ target.ration['amount'] = "starvation"   
            $ target.ration['food_type'] = "forage"   
            $ target.ration['target'] = 0           
            $ target.ration['limit'] = None      
        "На худобу (regime 1)":
            $ target.ration['amount'] = "regime" 
            $ target.ration['target'] = 1
        "На норму (regime 2)":
            $ target.ration['amount'] = "regime" 
            $ target.ration['target'] = 2     
        "На своё усмотрение (unlimited)":
            $ target.ration['amount'] = "unlimited"     
        "На ЖЫРЧИК (regime 3)":
            $ target.ration['amount'] = "regime" 
            $ target.ration['target'] = 3               
  
    if target.ration['amount'] != "starvation":    
        menu:
            "Качество питания."
            "Отбросы":
                $ target.ration['food_type'] = "sperm" 
                'Как земля... совсем невкусно (-3)'
            "Бичпакеты":
                $ target.ration['food_type'] = "dry" 
                'Мивина с майонезом... не вкусно (-1)'
            "Консервы":
                $ target.ration['food_type'] = "canned" 
                'Из банки... нормальный вкус'
            "Домашнее, тепленькое, с хлебушком":
                $ target.ration['food_type'] = "cosine"   
                'Пища белых людей... вкуснота (3)'    
    
    return

label lbl_activate_ap:
    menu:
        'Эти действия тратят AP вашего персонажа.'
        'Сдвиг в отношениях (нужны жетоны отношений)':
            menu:
                'Доступны только те опции для которых с выбранным персонажем есть непотраченные жетоны отношений: antagonism, accordance, contribution, conquer или convention.'
                'Гармония (Accordance)' if target.has_token("accordance"):
                    menu:
                        'Закрепить привычку подчиняться' if target.stance(player).level == 'forced':
                            $ player.ap -= 1
                            $ target.use_token('accordance')
                            $ target.stance(player).set_level('accustomed')  
                            'Глобальное отношение ребёнка к подчинению изменилось с вынужденного подчинения на привычное подчинение'   
                        'Гармонизовать позиции':
                            $ player.ap -= 1
                            $ target.use_token('accordance')
                            $ target.relations(player).change('congruence', '+')
                        'Создать напряжение':
                            $ player.ap -= 1
                            $ target.use_token('accordance')
                            $ target.relations(player).change('congruence', '-')                            
                        'Внушить уважение':
                            $ player.ap -= 1
                            $ target.use_token('accordance')
                            $ target.relations(player).change('fervor', '+')      
                        'Внушить спокойствие':
                            $ player.ap -= 1
                            $ target.use_token('accordance')
                            $ target.relations(player).change('fervor', '-')  
                        'Сблизиться':
                            $ player.ap -= 1
                            $ target.use_token('accordance')
                            $ target.relations(player).change('distance', '+')
                        'Формализовать отношения':
                            $ player.ap -= 1
                            $ target.use_token('accordance')
                            $ target.relations(player).change('distance', '-')
                        'Передумать':
                            jump lbl_activate_ap    
                'Раздор (Antagonism)' if target.has_token("antagonism"):
                    menu:
                        'Усилить враждебность':
                            $ player.ap -= 1
                            $ target.use_token('antagonism')
                            $ target.relations(player).change('congruence', '-')                            
                        'Накалить страсти':
                            $ player.ap -= 1
                            $ target.use_token('antagonism')
                            $ target.relations(player).change('fervor', '+')      
                        'Формализовать отношения':
                            $ player.ap -= 1
                            $ target.use_token('antagonism')
                            $ target.relations(player).change('distance', '-')
                        'Передумать':
                            jump lbl_activate_ap                    
                'Доминирование (conquest)' if target.has_token("conquest"):
                    menu:
                        'Создать напряжение':
                            $ player.ap -= 1
                            $ target.use_token('conquest')
                            $ target.relations(player).change('congruence', '-')                            
                        'Накалить страсти':
                            $ player.ap -= 1
                            $ target.use_token('conquest')
                            $ target.relations(player).change('fervor', '+')      
                        'Теперь это личное':
                            $ player.ap -= 1
                            $ target.use_token('conquest')
                            $ target.relations(player).change('distance', '+')
                        'Передумать':
                            jump lbl_activate_ap    
                'Сотрудничество (convention)' if target.has_token("convention"):
                    menu:
                        'Гармонизовать позиции':
                            $ player.ap -= 1
                            $ target.use_token('convention')
                            $ target.relations(player).change('congruence', '+')
                        'Охладить пыл':
                            $ player.ap -= 1
                            $ target.use_token('convention')
                            $ target.relations(player).change('fervor', '-')  
                        'Формализовать отношения':
                            $ player.ap -= 1
                            $ target.use_token('convention')
                            $ target.relations(player).change('distance', '-')
                        'Передумать':
                            jump lbl_activate_ap    
                'Благодарность (contribution)' if target.has_token("contribution"):
                    menu:
                        'Гармонизовать позиции':
                            $ player.ap -= 1
                            $ target.use_token('contribution')
                            $ target.relations(player).change('congruence', '+')
                        'Накалить страсти':
                            $ player.ap -= 1
                            $ target.use_token('contribution')
                            $ target.relations(player).change('fervor', '+')      
                        'Сблизиться':
                            $ player.ap -= 1
                            $ target.use_token('contribution')
                            $ target.relations(player).change('distance', '+')
                        'Передумать':
                            jump lbl_activate_ap                                
                'Назад':
                    jump lbl_activate_ap
        'Назад':
            jump lbl_target_menu
    
    return

label lbl_info_new(target):
    python:
        alignment = target.alignment.description() 
        job = target.show_job()
        desu = target.description()
        # taboos = child.show_taboos()
        features = target.show_features()
        tokens = target.tokens
        focus = target.show_focus()
        rel = target.relations(player).description() if target!=player else None
        stance = target.stance(player).level if target!=player else None
        skills = target.show_skills()
        tendency = target.attitude_tendency()
        txt = "Настроение: " + str(target.mood)
        if stance:
            txt += " | Отношение: " + str(stance) +'\n'
        txt += " | Здоровье: %s \n "%(target.vitality)
        txt += "Запреты: %s \n "%(target.restrictions)
        txt += "Условия сна: %s  |  %s       \n"%(target.accommodation, job)
        txt += "Характер: %s, %s, %s\n"%(target.alignment.description())
        if rel:
            txt += "Отношение: %s, %s, %s\n"%(rel)
            txt += "Гармония: %s, %s\n"%(target.relations(player).harmony()[0], target.relations(player).harmony()[1])
        else:
            txt += "Деньги: %s, Провизия: %s, Вещества: %s \n"%(game.money, game.resource("provision"), game.resource("drugs"))
        txt += "Фокус: %s\n"%(focus)
        txt += "Особенности: %s\n"%(features)
        txt += "Аттрибуты: %s\n"%(target.show_attributes())
        if tendency:
            txt += "Тенденция: %s\n"%(tendency)
        if skills:
            txt += "Навыки: %s\n"%(skills)
        if tokens:
            txt += "Токены: %s\n"%(tokens)
        txt += "Ангст: %s, Решимость: %s"%(target.anxiety, target.determination)
    "[txt]"

    return


screen sc_choose_character():
    python:
        plist = [person for person in player.known_characters]
        plist.append(player)
        ileft = 0
        iright = 4 if len(plist) > 4 else len(plist)-1
        def change_i(value):
            ileft += value
            iright += value
    vbox:
        for i in plist:
            $ t = i.name()
            textbutton t action Return(i)