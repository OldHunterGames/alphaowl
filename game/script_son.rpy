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
                
                "Капчевание":
                    menu:
                        'Вкатиться в /pr/' if not child.skill('coding').training:
                            $ player.ap -= 1
                            $ EVGeneric(game, "evn_dvach_coding").trigger()
                            jump lbl_son_manage
                        'Создать ЕОТ тред. Просить помощи.' if not child.skill('conversation').training:
                            $ player.ap -= 1
                            $ EVGeneric(game, "evn_dvach_conversation").trigger()
                            jump lbl_son_manage
                        'Создать тред как дольше не кончать' if not child.skill('sex').training:
                            $ player.ap -= 1
                            $ EVGeneric(game, "evn_dvach_sex").trigger()
                            jump lbl_son_manage
                        'Вкатиться в /fiz/' if not child.skill('sports').training:
                            $ player.ap -= 1
                            $ EVGeneric(game, "evn_dvach_sports").trigger()
                            jump lbl_son_manage
                        'Засмеялся-обосрался. Рулеточки. ЦУИНЬ.':
                            $ player.ap -= 1
                            $ EVGeneric(game, "evn_dvach_b").trigger()
                            jump lbl_son_manage
                        'Не найти фап-тред. Создать.':
                            $ player.ap -= 1
                            $ EVGeneric(game, "evn_dvach_fap").trigger()
                            jump lbl_son_manage                            
                        'Работать на Ольгино за 15 тенгэ':
                            $ player.ap -= 1
                            $ EVGeneric(game, "evn_dvach_olgino").trigger()
                            jump lbl_son_manage

                "Социоблядство":
                    jump lbl_son_manage
                    
                "Потом подумаю":
                    jump lbl_son_manage
        
        "Отношения в семье":
            call lbl_surrender
            jump lbl_son_manage
        
        "Смотреть в зеркало":
            call lbl_owl_info
            jump lbl_son_manage
        
        "Конец недели":
            jump label_new_day
    
    return

label lbl_misery:
    menu:
        "Опишите тип исыпытваемой попоболи, когда BATYA применяет к вам меры дисциплинарного воздействия."
        'Да не бомбит у меня!':
            $ butthurt_force = 1
            $ child.schedule.add_action('popo_bol', 'single')
        'Ну таак... припекает':
            $ butthurt_force = 2
            $ child.schedule.add_action('popo_bol', 'single')
        'Нехило так припекает...':
            $ butthurt_force = 3
            $ child.schedule.add_action('popo_bol', 'single')
        'ПИЧОТ... МАМ ПРЯМ ПИЧОТ!':
            $ butthurt_force = 4
            $ child.schedule.add_action('popo_bol', 'single')
        'POOKAN BOBMBANULO':
            $ butthurt_force = 5
            $ child.schedule.add_action('popo_bol', 'single')            
        'Да не, я прикалываюсь ^_^':
            $ child.schedule.remove_action('popo_bol')
            
    jump lbl_surrender
    return

label lbl_surrender:
    menu:
        "Давить на жалость":
            call lbl_misery
            
        "Вкалывать":
            call lbl_serve
        
        "Подлизываться":
            call lbl_asslick

        "Клянчить (нужын AP!)" if child.ap > 0:
            call lbl_beg
        
        "Прорыв в отношениях (нужны AP)" if child.ap > 0:
            call lbl_change_relations
            
        "Оценить настроение мамки":
            call lbl_mom_info
            jump lbl_son_manage

        "Достаточно":
            jump lbl_son_manage
            
    call lbl_surrender
            
    return
    