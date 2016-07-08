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
                "Бытовые уловия":
                    $ pass
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
        "По вечерам: [shedule_major]":
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
        'Воспитывать Сыченьку' if target != child:
            $ pass
        'Безделье':
            $ target.schedule.add_action('job_idle') 
        'Подрабатывать уборщицей' if target == mom:
            $ target.schedule.add_action('job_janitor') 
        'Делать уроки' if target == child:
            $ target.schedule.add_action('job_study') 
        "Назад":
            call lbl_make_shedule
    
        job = target.show_job()
    
    return