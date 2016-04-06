# Управление от имени Сыча

label lbl_son_manage:
    
    menu:
        
        "Сосредоточиться на..." if player.ap > 0:
            menu:
                " У тебя целая неделя впереди \n @ \n Думаешь сколько всего успеешь сделать \n @ \n Эй, а куда делась неделя?"
                "Очоба" if game.studies:
                    menu:
                        'Запилить курсач' if 'major' in game.studies:
                            $ player.ap -= 1
                            $ EVGeneric(game, "evn_do_major").trigger()
                            jump lbl_son_manage
                            
                        'Сдать нормативы по физре' if study == 'gym':
                            $ player.ap -= 1
                            $ EVGeneric(game, "evn_do_gym").trigger()                            
                            jump lbl_son_manage

                        'Производственная практика' if study == 'practice':
                            'На заводе по сборке вёдер  \n @ \n Наша инновационная ЭВМ "Эдьбрус-М"  \n @ \n  На перфокартах'
                            menu:
                                'Отпахать по честному':
                                    $ player.ap -= 1
                                    $ EVGeneric(game, "evn_do_practice_programm").trigger()    
                                'Закорешиться с коллективом':
                                    $ player.ap -= 1
                                    $ EVGeneric(game, "evn_do_practice_programm_chat").trigger()    
                            jump lbl_son_manage

                        'Зачет на военной кафедре' if study == 'military':
                            'Офицеры уже с утра бухие  \n @ \n Муштра на плацу как при Павле I \n @ \n Вечером зачет по строевой'
                            menu:
                                'Держать равнение налево':
                                    $ player.ap -= 1
                                    $ EVGeneric(game, "evn_do_practice_military").trigger()    
                                'Подлизаться к товарищу подполковнику':
                                    $ player.ap -= 1
                                    $ EVGeneric(game, "evn_do_practice_military_chat").trigger()    
                            jump lbl_son_manage

                        'Лабы по программированию' if study == 'labs':
                            'Старый профессор-некрофил  \n @ \n Задача на фортране  \n @ \n  Как буд-то кто-то им пользуется вообще'
                            menu:
                                'Накодить убер-алгоритм':
                                    $ player.ap -= 1
                                    $ EVGeneric(game, "evn_do_practice_labs").trigger()    
                                'Скатать решение у ботанов':
                                    $ player.ap -= 1
                                    $ EVGeneric(game, "evn_do_practice_labs_chat").trigger()    
                            jump lbl_son_manage
                            
                        'Забить':
                            jump lbl_son_manage                            
                        
                "Социоблядство":
                    $ player.ap -= 1
                    jump lbl_son_manage                
                "Потом подумаю":
                    jump lbl_son_manage
        
        "Информация":
            call lbl_owl_info
            jump lbl_son_manage
        
        "Конец недели":
            jump label_new_day
    
    return