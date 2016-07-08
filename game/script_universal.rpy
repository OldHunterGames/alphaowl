#Универсальное меню управления 

label lbl_universal_menu:
    $ info_provision = game.resource('provision')
    $ info_drugs = game.resource('drugs')
    menu:
        'Тенгэ: [game.money] | Жратва: [info_provision] | Вещества: [info_drugs]'
        "Информация":
            $ target = renpy.call_screen('sc_choose_character')
            call lbl_info_new(target)
            
        "Условия":
            menu:
                "Личные" if player == child:
                    call lbl_control_lifestyle
                "Сычик" if player == mom:
                    call lbl_mom_manage    
       
        "Общение" if player == mom:
            call lbl_universal_interaction
            
        "Расписание" if player == child:
            call lbl_make_shedule
                    
        "Особые события ([player.ap])" if player.ap > 0:
            if player == child:
                call lbl_son_events
            else:
                call lbl_developement 
                
        "Магазин" if player == mom:
            call lbl_shop         
            
        "Следующая неделя" if game.can_skip_turn():
            jump label_new_day
            
    jump lbl_universal_menu
    return
    
label lbl_make_shedule:
        
    $ shedule_major = dname[player.job['name']]
    
    menu:
        "По вечерам: [shedule_major]":
            if player == child:
                call lbl_son_major
            else:
                $ pass
        "В выходные: [shedule_minor]":
            if player == child:
                call lbl_son_minor
            else:
                $ pass
        "Общение: [communication]":
            call lbl_universal_interaction
            
        'Назад':
            jump lbl_universal_menu    
            
    jump lbl_make_shedule
        
        
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
            txt += "Тенденция: %s\n"(tendency)
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