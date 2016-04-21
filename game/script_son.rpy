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
        
        "Работы по дому" if child.vigor > 0:
            call lbl_chores
            jump lbl_son_manage            

        "После учёбы":
            call lbl_job_rules
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

label lbl_chores:
    menu:
        'Какие работы по дому будет выполнять Сыча чтобы повысить настроение мамке? Каждая работа в расписании требует энергии (списывается в конце хода)! Ты можешь назначить любой объём, но перебор приведёт к усталости и неэффективной работе.'
        "Готовить еду" if in 'chores_cook':
            $ child.schedule.add_action('cook_cook')              
        "Отменить наряд по кухне" if 'cook_cook' not in child.schedule:
            $ child.schedule.remove_action('cook_cook')    
        "Достаточно":
            jump lbl_son_manage        
    jump lbl_chores
    return

label lbl_surrender:
    menu:
        "Давить на жалость":
            call lbl_misery
            
        "Вкалывать":
            'СКАЗАЛ МАМЕ \n @ \nЧТО БУДЕШЬ УЧИТЬСЯ НА ЧЕТВЁРКИ И ПЯТЁРКИ \n @ \nДА КОККОЕ ТЕБЕ УЧИТЬСЯ КОРЗИНОЧКА \n @ \nТЫ ЖЕ У НАС НУЛЕВОЙ!'
            $ child.schedule.add_action('learn_good', 'single')
        
        "Подлизываться":
            call lbl_asslick
            
        "Условия жизни":
            call lbl_slave_lifestyle

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
    
label lbl_change_relations:
    menu:
        'Выбрать используемый жетон.'
        'Accordance' if child.has_token("accordance"):
            menu:
                'Наладить отношения с матерью' if mother.master_stance() < 3:
                    python:
                        player.ap -= 1
                        child.use_token('accordance')
                        if mom.relations_player().master_stance == 'rightful':
                            mom.relations_player().master_stance = 'benevolent'
                        if mom.relations_player().master_stance == 'opressive':
                            mom.relations_player().master_stance = 'rightful'
                        if mom.relations_player().master_stance == 'cruel':
                            mom.relations_player().master_stance = 'opressive'
                        stance = mom.relations_player().master_stance
                    'Глобальное отношение матери изменилось. Теперь: [stance]'   
                'Соглашаться и восхищаться':
                    $ player.ap -= 1
                    $ child.use_token('accordance')
                    $ child.relations(mom).change('congruence', '+')
                'Троллить и подъёбывать':
                    $ player.ap -= 1
                    $ child.use_token('accordance')
                    $ child.relations(mom).change('congruence', '-')
                'Знаять мягкую позицию':
                    $ player.ap -= 1
                    $ child.use_token('accordance')
                    $ child.relations(mom).change('fervor', '+')                            
                'Занять жесткую позицию':
                    $ player.ap -= 1
                    $ child.use_token('accordance')
                    $ child.relations(mom).change('fervor', '-')  
                'Больше личной вовлечённости':
                    $ player.ap -= 1
                    $ child.use_token('accordance')
                    $ child.relations(mom).change('distance', '+')
                'Формализовать отношения':
                    $ player.ap -= 1
                    $ child.use_token('accordance')
                    $ child.relations(mom).change('distance', '-')
                'Назад':
                    jump lbl_change_relations  
                    
        'Antagonism' if mom.has_token("antagonism"):
            menu:
                'Испортить отношения с матерью' if mother.master_stance() > 0:
                    python:
                        player.ap -= 1
                        child.use_token('accordance')
                        if mom.relations_player().master_stance == 'opressive':
                            mom.relations_player().master_stance = 'cruel'
                        if mom.relations_player().master_stance == 'rightful':
                            mom.relations_player().master_stance = 'opressive'
                        if mom.relations_player().master_stance == 'benevolent':
                            mom.relations_player().master_stance = 'rightful'
                        stance = mom.relations_player().master_stance
                    'Глобальное отношение матери изменилось. Теперь: [stance]'                     
                'Троллить и подъёбывать':
                    $ player.ap -= 1
                    $ child.use_token('antagonism')
                    $ child.relations(mom).change('congruence', '-')
                'Занять жесткую позицию':
                    $ player.ap -= 1
                    $ child.use_token('accordance')
                    $ child.relations(mom).change('fervor', '-')                    
                'Формализовать отношения':
                    $ player.ap -= 1
                    $ child.use_token('antagonism')
                    $ child.relations(mom).change('distance', '-')
                'Назад':
                    jump lbl_change_relations  
                    
        'Compassion' if mom.has_token("compassion"):
            menu:
                'Смягчить позицию мамки' if mom.relations_player().master_stance == 'cruel':
                    $ player.ap -= 1
                    $ child.use_token('dread')
                    $ mom.relations_player().master_stance = 'opressive'         
                    'Глобальное отношение мамки изменилось с жестокого на деспотичное'
                'Разжалобить мамку':
                    $ player.ap -= 1
                    $ child.use_token('compassion')
                    $ mom.compassion += 1                    
                'Соглашаться и восхищаться':
                    $ player.ap -= 1
                    $ child.use_token('compassion')
                    $ mom.relations(mom).change('congruence', '+')
                'Занять мягкую позицию':
                    $ player.ap -= 1
                    $ child.use_token('compassion')
                    $ mom.relations(mom).change('fervor', '+')
                'Больше личной вовлечённости':
                    $ player.ap -= 1
                    $ child.use_token('compassion')
                    $ mom.relations(mom).change('distance', '+')
                'Назад':
                    jump lbl_change_relations  
                    
        'Confidence' if mom.has_token("confidence"):
            menu:
                'Смягчить позицию мамки' if mom.relations_player().master_stance == 'cruel':
                    $ player.ap -= 1
                    $ child.use_token('dread')
                    $ mom.relations_player().master_stance = 'opressive'         
                    'Глобальное отношение мамки изменилось с жестокого на деспотичное'
                'Увеличить доверие мамки':
                    $ player.ap -= 1
                    $ child.use_token('confidence')
                    $ mom.confidence += 1                    
                'Соглашаться и восхищаться':
                    $ player.ap -= 1
                    $ child.use_token('confidence')
                    $ mom.relations(mom).change('congruence', '+')
                'Занять жесткую позицию':
                    $ player.ap -= 1
                    $ child.use_token('confidence')
                    $ child.relations(mom).change('fervor', '-')   
                'Формализовать отношения':
                    $ player.ap -= 1
                    $ child.use_token('confidence')
                    $ child.relations(mom).change('distance', '-')
                'Назад':
                    jump lbl_change_relations  
                    
        'Craving' if mom.has_token("craving"):
            menu:
                'Смягчить позицию мамки' if mom.relations_player().master_stance == 'opressive' and mom.favor() > 3:
                    $ player.ap -= 1
                    $ child.use_token('dread')
                    $ mom.relations_player().master_stance = 'rightful'         
                    'Глобальное отношение мамки изменилось с деспотичного на справедливое'
                'Внушить мамке любовь':
                    $ player.ap -= 1
                    $ child.use_token('craving')
                    $ mom.craving += 1                    
                'Занять жесткую позицию':
                    $ player.ap -= 1
                    $ child.use_token('craving')
                    $ child.relations(mom).change('fervor', '-')   
                'Занять мягкую позицию':
                    $ player.ap -= 1
                    $ child.use_token('craving')
                    $ mom.relations(mom).change('fervor', '+')
                'Больше личной вовлечённости':
                    $ player.ap -= 1
                    $ child.use_token('craving')
                    $ mom.relations(mom).change('distance', '+')
                'Назад':
                    jump lbl_change_relations  
                    
        "Достаточно":
            jump lbl_son_manage        
                    
    jump lbl_change_relations  
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
        'Нехило вообще-то припекает...':
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

label lbl_asslick:
    menu:
        "СЫЧА СЕГОДНЯ У МАМЫ ПОМОЩНИК!"
        'Процессор не влючается! Сыча, тыжпрогроммист.':
            $ help_skill = 'coding'
            $ need_helped = 'comfort'
            $ child.schedule.add_action('help_mom', 'single')
        'BATYA пьяный опять. Хоть ты со мной поговори.':
            $ help_skill = 'conversation'
            $ need_helped = 'communication'
            $ child.schedule.add_action('help_mom', 'single')
        'Надо холодильник на дачу отвезти. На поезде.':
            $ help_skill = 'sports'
            $ need_helped = 'authority'            
            $ child.schedule.add_action('help_mom', 'single')
        'Помассируй маме ножки, корзиночка.':
            $ help_skill = 'sex'
            $ need_helped = 'wellness'            
            $ child.schedule.add_action('help_mom', 'single')            
        'Ой всё':
            $ child.schedule.remove_action('help_mom')
            
    jump lbl_surrender
    return

label lbl_slave_lifestyle:
    menu:
        'Корзиночка может поменять условия своей жизни, но только в тех пределах что ему разрешает мамка. Для расширения вариантов надо улучшать её master_stance или выклянчивать отдельные разрешения.'
        "Питание (количество)":
            menu:
                "А ты вот посиди без етьбы, знать будешь как матери губить!":   
                    $ child.ration['amount'] = "starvation"   
                    $ child.ration['food_type'] = "forage"   
                    $ child.ration['target'] = 0           
                    $ child.ration['limit'] = None
                    jump lbl_mom_manage  
                "Ой отрастил себе мамонище, девок пугать. Худей!":      
                    $ child.ration['amount'] = "regime"
                    $ child.ration['target'] = 1
                "Чтоб здоровенький был у нас, как Ванька Ерохин" if mother.master_stance() > 0 or 'food_ammount_healty' in player.availabe_actions:       
                    $ child.ration['amount'] = "regime"
                    $ child.ration['target'] = 2
                "Кожа да кости же, ухватиться не за что. Кушай лучше!" if mother.master_stance() > 1 or 'food_ammount_chuby' in player.availabe_actions: 
                    $ child.ration['amount'] = "regime"
                    $ child.ration['target'] = 3
                "Тётя Срака читала - кушать надо сколько душа просит" if mother.master_stance() > 2 or 'food_ammount_any' in player.availabe_actions:  
                    $ child.ration['amount'] = "unlimited"           

        "Достаточно":
            jump lbl_son_manage
            
    jump lbl_slave_lifestyle
    return
    