#Универсальное меню управления 

label lbl_universal_menu:
    $ info_provision = game.resource('provision')
    $ info_drugs = game.resource('drugs')
    menu:
        'Тенгэ: [game.money] | Жратва: [info_provision] | Вещества: [info_drugs]'
        
        "Взаимодействия с...":
            $ target = renpy.call_screen('sc_choose_character')
            call lbl_info_new(target)
            menu:
                "Расписание":
                    call lbl_make_shedule
                "Бытовые уловия" if player != child and target == child:
                    call lbl_accommodation
                "Правила":
                    $ pass
                "Питание":
                    $ pass
                "Одежда":
                    $ pass
                "Карманные деньги":
                    $ pass
                "Особые события ([player.ap])" if player.ap > 0:
                    $ pass
                "Информация":
                    call lbl_info_new(target)
                "Назад":
                    jump lbl_universal_menu
               
        "Магазин" if player == mom:
            call lbl_shop         
            
        "Следующая неделя" if game.can_skip_turn():
            jump label_new_day
            
    jump lbl_universal_menu
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
            menu:
                'Кто этим займётся?'
                'Маман':
                    $ actor = mom
                'BATYA':
                    $ actor = batya
                'Передумать':
                    jump lbl_shedule_major
            menu:
                'Какой подход выборать?'
                'Запугивание':
                    $ moral_burden = ['evil', 'intense', 'chaotic']
                    $ token = 'conquest'
                    jump lbl_torture_choose
                'Передумать':
                    jump lbl_shedule_major                    
                
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
        'Бить ремнём':
            $ self_satisfy = ['power', 'authority']
            $ self_tension = ['altruism']
            $ skill = 'sport'
            $ target_tension = ['wellness']
    
    
    $ special_values = {'skill': skill, 'torturer': actor, 'token': token, 'target_tension': target_tension, 'self_tension': self_tension,
                        'self_satisfy': self_satisfy, 'moral_burden': moral_burden, 'beneficiar': beneficiar}
    $ target.schedule.add_action('token_check', special_values=special_values)
    
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