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
                    call lbl_control_lifestyle                
       
        "Расписание":
            call lbl_make_shedule
                    
        "Особые события ([player.ap])" if player.ap > 0:
            if player == child:
                call lbl_son_events
            else:
                $ pass
                        
        "Следующая неделя" if game.can_skip_turn():
            jump label_new_day
            
    jump lbl_universal_menu
    return
    
label lbl_make_shedule:
        
    $ shedule_major = dname[player.job['name']]
    
    menu:
        "После учебы: [shedule_major]":
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
            if player == child:
                call lbl_universal_interaction
            else:
                $ pass
        'Назад':
            jump lbl_universal_menu    
            
    jump lbl_make_shedule
        
        
label lbl_info_new(target):
    python:
        alignment = target.alignment.description() 
        job = dname[target.job['name']]
        desu = target.description()
        needs_overflow = target.show_needs('overflow')
        needs_tense = target.show_needs('tense')
        needs_relevant = target.show_needs('relevant')
        needs_statisfied = target.show_needs('satisfied')
        # taboos = child.show_taboos()
        features = target.show_features()
        focus = target.show_focus()
        rel = target.relations(player).description() if target!=player else None
        stance = target.stance(player).level if target!=player else None
        txt = "Настроение: " + str(target.mood())
        if stance:
            txt += " | Отношение: " + str(stance) +'\n'
        txt += " | Энергия: %s \n "%(target.vigor)
        txt += "Запреты: %s \n "%(target.restrictions)
        txt += "Условия сна: %s  |  %s       \n"%(target.accommodation, job)
        txt += "Характер: %s, %s, %s\n"%(target.alignment.description())
        if rel:
            txt += "Отношение: %s, %s, %s\n"%(rel)
        else:
            txt += "Деньги: %s, Провизия: %s, Вещества: %s \n"%(game.money, game.resource("provision"), game.resource("drugs"))
        txt += "Фокус: %s\n"%(focus)
        txt += "Напряжения: %s\n"%(needs_tense)
        txt += "Актуальные нужды: %s\n"%(needs_relevant)
        txt += "Удовлетворённые: %s\n"%(needs_statisfied)
        txt += "Пресыщения: %s\n"%(needs_overflow)
        txt += "Особенности: %s\n"%(features)
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