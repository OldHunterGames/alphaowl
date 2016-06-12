#Универсальное меню управления 

label lbl_universal_menu:
    
    menu:
        "Информация":
            call lbl_info
            
        "Условия":
            menu:
                "Личные":
                    $ pass
            
        "Расписание":
            call lbl_make_shedule
                    
        "Особые события ([player.ap])" if player.ap > 0:
            $ pass
                        
        "Следующая неделя":
            jump label_new_day
            
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
    

