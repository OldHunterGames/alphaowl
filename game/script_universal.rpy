#Универсальное меню управления 

label lbl_universal_menu:
    
    menu:
        "Информация":
            $ target = renpy.call_screen('sc_choose_character')
            call lbl_info_new(target)
            
        "Условия":
            menu:
                "Личные":
                    $ pass
            
        "Расписание":
            call lbl_make_shedule
                    
        "Особые события ([player.ap])" if player.ap > 0:
            $ pass
                        
        "Следующая неделя":
            # jump label_new_day
            $ pass
            
    jump lbl_universal_menu
    return
    
label lbl_make_shedule:
    menu:
        "Основное: [shedule_major]":
            $ pass
        "Дополнительно: [shedule_minor]":
            $ pass
        "Общение: [communication]":
            $ pass
        'Назад':
            jump universal_menu    
            
    jump lbl_make_shedule
        
        
label lbl_info_new(target):
    python:
        alignment = target.alignment.description() 
        job = target.job['name']
        desu = target.description()
        needs_overflow = target.show_needs('overflow')
        needs_tense = target.show_needs('tense')
        needs_relevant = target.show_needs('relevant')
        needs_statisfied = target.show_needs('satisfied')
        # taboos = child.show_taboos()
        features = target.show_features()
        focus = target.show_focus()
        rel = target.relations(player).description() if target!=player else "None"
        txt = "Настроение: " + str(target.mood()) + " | Отношение: " + str(target.stance(player).level)
    "[txt] | Энергия: [target.vigor] \n
    
     Запреты: [target.restrictions] \n 
     Условия сна: [target.accommodation]  |  Занятость: [job]       \n
     Характер: [alignment]\n
     Отношение: [rel]\n
     Фокус: [focus]\n
     Напряжения: [needs_tense]\n
     Актуальные нужды: [needs_relevant]\n
     Удовлетворённые: [needs_statisfied]\n          
     Пресыщения: [needs_overflow]\n     
     Особенности: [features]\n
     \n"

    return


screen sc_choose_character():
    python:
        plist = player.known_characters
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