# Управление от имени Сыча

label lbl_son_manage:
    
    menu:
        "Сосредоточиться на..." if player.ap > 0:
            menu:
                " У тебя целая неделя впереди \n @ \n Думаешь сколько всего успеешь сделать \n @ \n Эй, а куда делась неделя?"
                "Очоба" if game.studies:
                    $ player.ap -= 1
                    jump lbl_son_manage
                "Социоблядство":
                    $ player.ap -= 1
                    jump lbl_son_manage                
                "Потом подумаю":
                    jump lbl_son_manage
        "Конец недели":
            $ player.rest()
            jump label_new_day
    
    return