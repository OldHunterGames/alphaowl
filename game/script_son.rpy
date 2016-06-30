# Управление от имени Сыча

label lbl_son_manage:
    
    menu:      
        "Работы по дому" if child.vigor > 0:
            call lbl_chores
            jump lbl_son_manage            

        "После учёбы":
            call lbl_job_rules
            jump lbl_son_manage
            
        "Условия жизни":
            call lbl_control_lifestyle
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

label lbl_son_events:

    menu:
        " У тебя целая неделя впереди \n @ \n Думаешь сколько всего успеешь сделать \n @ \n Эй, а куда делась неделя?"
        "Очоба" if game.studies:
            menu:
                'Запилить курсач' if 'major' in game.studies:
                    $ player.ap -= 1
                    $ EVGeneric(game, "evn_do_major").trigger(child)
                            
                'Сдать нормативы по физре' if study == 'gym':
                    $ player.ap -= 1
                    $ EVGeneric(game, "evn_do_gym").trigger(child)                            

                'Производственная практика' if study == 'practice':
                    'На заводе по сборке вёдер  \n @ \n Наша инновационная ЭВМ "Эдьбрус-М"  \n @ \n  На перфокартах'
                    menu:
                        'Отпахать по честному':
                            $ player.ap -= 1
                            $ EVGeneric(game, "evn_do_practice_programm").trigger(child)    
                        'Закорешиться с коллективом':
                            $ player.ap -= 1
                            $ EVGeneric(game, "evn_do_practice_programm_chat").trigger(child)    

                'Зачет на военной кафедре' if study == 'military':
                    'Офицеры уже с утра бухие  \n @ \n Муштра на плацу как при Павле I \n @ \n Вечером зачет по строевой'
                    menu:
                        'Держать равнение налево':
                            $ player.ap -= 1
                            $ EVGeneric(game, "evn_do_practice_military").trigger(child)    
                        'Подлизаться к товарищу подполковнику':
                            $ player.ap -= 1
                            $ EVGeneric(game, "evn_do_practice_military_chat").trigger(child)    

                'Лабы по программированию' if study == 'labs':
                    'Старый профессор-некрофил  \n @ \n Задача на фортране  \n @ \n  Как буд-то кто-то им пользуется вообще'
                    menu:
                        'Накодить убер-алгоритм':
                            $ player.ap -= 1
                            $ EVGeneric(game, "evn_do_practice_labs").trigger(child)    
                        'Скатать решение у ботанов':
                            $ player.ap -= 1
                            $ EVGeneric(game, "evn_do_practice_labs_chat").trigger(child)    
                            
                'Забить':
                    jump lbl_universal_menu                            

        "Социоблядство":
            call lbl_social
            jump lbl_universal_menu
                    
        "Потом подумаю":
            jump lbl_universal_menu

    jump lbl_universal_menu
    return

label lbl_son_major:
    $ mom_stance = mom.stance(player).value
    menu:
        'Всё сидишь как сыч, за конпуктером. Иди пробзись.' if mom_stance > 0:
            $ child.job['name'] = 'idle'
            $ child.schedule.add_action('job_idle')  
        'Уроки делай, бездельник! Зря тебя мать в интитут пристраивала?' if mom_stance > -1:
            $ child.job['name'] = 'study'
            $ child.schedule.add_action('job_study')  
        'Посудку помой. Мусор вынеси. С собакой погуляй. И за дедом прибери.':
            $ child.job['name'] = 'chores'
            $ child.schedule.add_action('job_chores')            
        'Вон здоровый какой. Иди вагоны разгружать - семье копеечка.':
            $ child.job['name'] = 'work'
            $ child.schedule.add_action('job_work')                   
        'Да хоть на панели жопой торгуй! Я на тебя батрачить не нанималась.':
            $ child.job['name'] = 'whore'
            $ child.schedule.add_action('job_whore') 
            
    jump lbl_universal_menu            
    return

label lbl_son_minor:
    
    menu:
        'Пахать на даче':
            $ shedule_minor = 'пахать на даче' 
            $ child.schedule.add_action('dayoff_dacha')
            
        'Капчевать на дваче':
            $ shedule_minor = 'капчевать на дваче' 
            $ child.schedule.add_action('dayoff_2ch')
            
        'Сычевать на хате':
            $ shedule_minor = 'сычевать' 
            $ child.schedule.add_action('dayoff_owled')
            
    jump lbl_universal_menu
    return
    
label lbl_son_social:
    menu:
        'Биопроблемы':
            'Есть одна тян - ламповая няша Енотова. Сможешь ли ты завоевать её трепетное сердце?'
            menu:
                "Альфа-стайл":
                    call lbl_enot_conquest
                    
                "Задрот-стайл":
                    call lbl_enot_convention
                    
                "Пиздолиз-стайл":
                    call lbl_enot_contribution
                    
                "Назад":
                    call lbl_son_social
                    
        'Этология человека':    
            'Главный альфач на курсе - тупой но хитрый качок и мажор Ерохин. Способен ли ты отстоять свой (омежко-)статус?'
            menu:
                "Противостояние":
                    call lbl_eroha_conquest
                    
                "Коллаборационизм":
                    call lbl_eroha_convention
                    
                "Контрибуции":
                    call lbl_eroha_contribution

                "Назад":
                    call lbl_son_social
                    
        'Траповать @ Шлюховать':
            'Есть один кун - Ашот. Торгует на рынке помидорами, ебёт всё. Даже Небо, даже Аллаха, даже тебя. Но станет ли он хорошим спонсором?'
            menu:
                "Итс э ТРАП!":
                    call lbl_ashot_conquest
                    
                "Гей-шлюха":
                    call lbl_ashot_convention
                    
                "Мамин романтик":
                    call lbl_ashot_contribution
                    
                "Назад":
                    call lbl_son_social                    
        'Забить':
            $ pass
    
    jump lbl_universal_menu
    return

label lbl_universal_interaction:
    menu:
        'Выберите объект социального взаимодействия'
        "Енотова":
            $ communication = 'Енотова'
            $ unin_target = eot
        "Ерохин":
            $ communication = 'Ерохин'
            $ unin_target = erokhin
        "Ашот":
            $ communication = 'Ашот'
            $ unin_target = ashot
            
    menu:
        'Выберите тип взаимодействия'
        'Агрессия':
            $ token_to_gain = 'conquest'
            $ moral_burden = ['evil', 'ardent']
            call lbl_son_social_uni_conquest 
        'Кооперация':
            call lbl_son_social_uni_convention 
        'Ублажение':
            call lbl_son_social_uni_contribution             
            
    $ child.schedule.add_action('social_universal', 'single')
    'Готово. Неделя будет посвящена установленному плану действий.'
    jump lbl_universal_menu
    return

label lbl_son_social_uni_conquest:
    $ self_bonus_need = 'power'
    menu:
        'Выберите силу воздействия'
        'Минимальная':
            $ used_force = 1
        'Слабая':
            $ used_force = 2
        'Средняя':
            $ used_force = 3
        'Значительная':
            $ used_force = 4
        'Максимальная':
            $ used_force = 5            
    
    menu:
        'Выберите направление удара'
        'Смысл жизни':
            $ targeted_need = 'purpose'
        'Питание':
            $ targeted_need = 'nutrition'
        'Здоровье':
            $ targeted_need = 'wellness'
        'Комфорт':
            $ targeted_need = 'comfort'
        'Подвижность':
            $ targeted_need = 'activity'
        'Общение':
            $ targeted_need = 'communication'            
        'Развлечения':
            $ targeted_need = 'amusement'
        'Богатство':
            $ targeted_need = 'prosperity'   
        'Авторитет':
            $ targeted_need = 'authority'
        'Амбиции':
            $ targeted_need = 'ambition'   
        'Секс':
            $ targeted_need = 'eros'
        'Стабильность':
            $ targeted_need = 'order'   
        'Независимость':
            $ targeted_need = 'independence'
        'Моральная поддержка':
            $ targeted_need = 'approval'   
        'Адреналин':
            $ targeted_need = 'thrill'
        'Альтруизм':
            $ targeted_need = 'altruism'  
        'Могущество':
            $ targeted_need = 'power'
            
    return

label lbl_enot_conquest:
    "Бей бабу молотом - будет баба золотом. Все говорят что девки любят плохих парней. Но дело не в любви - всё достаётся сильному!"
    menu:
        "Домогаться":
            menu:
                "Прижиматься в метро":
                    $ atrocity_force = 1
                    $ child.schedule.add_action('social_eotatroeros', 'single')
                                        
    $ communication = 'Енотова'
    jump lbl_universal_menu
    return

label lbl_control_lifestyle:
    $ mom_stance = mom.stance(player).value
    menu:
        "Количество и качество доступных для выбора вариантов заивисит от уровня благоволения Мамки!"
        'Размер пайки':
            menu:
                '"Жертва бухенвальда"':
                    $ child.ration['amount'] = "starvation"   
                    $ child.ration['food_type'] = "forage"   
                    $ child.ration['target'] = 0           
                    $ child.ration['limit'] = None      
                "Впроголодь":
                    $ child.ration['amount'] = "regime" 
                    $ child.ration['target'] = 1
                "Считать калории" if mom_stance > -1:
                    $ child.ration['amount'] = "regime" 
                    $ child.ration['target'] = 2     
                "От пуза" if mom_stance > 0:
                    $ child.ration['amount'] = "unlimited"     
                "Как на убой" if mom_stance == 'rightful':
                    $ child.ration['amount'] = "regime" 
                    $ child.ration['target'] = 3   
                    
        'Выбор продуктов' if child.ration['amount'] != "starvation":    
            menu:
                "Вот покушай ка Сычулька..."
                "Своего, с огорода-то. Витаминчики!":
                    $ child.ration['food_type'] = "sperm" 
                    'Как земля... совсем невкусно (-3)'
                "Мивины с маянезиком." if mom_stance > -1:
                    $ child.ration['food_type'] = "dry" 
                    'Бичпакет... не вкусно (-1)'
                "Тёпленького похлебай, домашнего. С хлебушком." if mom_stance > 0:
                    $ child.ration['food_type'] = "canned" 
                    'Хрючево... нормальный вкус'
                "В столовой вашей, я кухаркой не нанималась!" if mom_stance > 0:
                    $ child.ration['food_type'] = "cosine"   
                    'Пища белых людей... вкуснота (3)'                    
        
        "Внешний вид":
            menu:
                'Мамина симпатяфка':
                    $ child.appearance = 'lame'
                    $ child.schedule.add_action('outfit_lame')
                    'Вот свитерочек бабушка связала \n @ \n Штанишки тетя Ёба нам со своего оболтуса дала \n @ \n Шапку не забудь надеть! (autority -3)'
                'Да носи что хочешь' if mom_stance > -1:
                    $ child.appearance = 'normal'
                    $ child.schedule.add_action('outfit_normal')
                    'Залезаешь в шкаф чтобы найти приличную одежду \n @ \n Там какие-то обноски от Тёти Ёбы и Дяди Бафомета \n @ \n И мутантная моль размером с кошака доедает ушанку (prosperity -2)'    
                'Купим тебе модное, выбирай (25 тенгэ)' if game.tenge >= 25 and mom_stance > 0:
                    $ game.tenge -= 25
                    $ child.appearance = 'cool'
                    $ child.schedule.add_action('outfit_cool')
                    'Ой Сыченька, сейчас купим тебе модного \n @ \n Затариваетесь на рынке у Ашота, турецкими подделками \n @ \n А ты и не против (prosperity 4)'

        "Запреты и ограничения":
            menu:
                'Запретить гулять' if 'dates' not in child.restrictions:
                    $ child.restrictions.append('dates')
                'Разрешить гулять до поздна' if 'dates' in child.restrictions and mom_stance > 0:
                    $ child.restrictions.remove('dates')
                'Запретить общаться с друзьями' if 'friends' not in child.restrictions:
                    $ child.restrictions.append('friends')
                'Разрешить общаться с друзьями' if 'friends' in child.restrictions and mom_stance > -1:
                    $ child.restrictions.remove('friends')
                'Конплюхтерн для очобы! (блокировать интернет)' if 'pc' not in child.restrictions:
                    $ child.restrictions.append('pc')
                'Ну и сиди за своим комплюктером' if 'pc' in child.restrictions and mom_stance > -1:
                    $ child.restrictions.remove('pc')                
                'Пресечь любую дрочку' if 'masturbation' not in child.restrictions:
                    $ child.restrictions.append('masturbation')
                    $ child.schedule.add_action('fap_no')
                    $ txt = 'Сыночка то наш, всё пиструнчик свой тилибонькает \n @ \n Скоро волосы на руках расти начнут \n @ \n В антимастурбационном кресте будещь спать, по совету отца Агапия'
                'Игнорировать дрочку' if 'masturbation' in child.restrictions and mom_stance == 'opressive':
                    $ child.restrictions.remove('masturbation')
                    $ child.schedule.add_action('fap_yes')
                    $ txt = 'А что это ты в ванной столько времени сидишь, Сыча? \n @ \n И то хорошо \n @ \n Приучили к чистоте ребёнка то'            
                'Запретить алкоголь' if 'alcohol' not in child.restrictions:
                    $ child.restrictions.append('alcohol')
                    $ child.schedule.add_action('alcohol_no')
                    $ txt = 'Ты на пиво то не заглядвайся \n @ \n Ещё нос не дорос \n @ \n Я малолетних алкоголиков в доме не потерплю'
                'Пусть накатит с BATYей' if 'alcohol' in child.restrictions and mom_stance > 0:
                    $ child.restrictions.remove('alcohol')
                    $ child.schedule.add_action('alcohol_yes')
                    $ txt = 'За дидов рюмашечку надо обязательно \n @ \n Что значит "не буду стекломой пить" \n @ \n Традиции наши не уважаешь?'                 
                'Запретить курить' if 'tobacco' not in child.restrictions:
                    $ child.restrictions.append('tobacco')
                    $ child.schedule.add_action('smoke_no')
                    $ txt = 'Если почую табачный запах \n @ \n Всё отцу расскажу \n @ \n Неделю у меня сидеть на жопе не сможешь'
                'Пусть курит но не дома' if 'tobacco' in child.restrictions and mom_stance > 0:
                    $ child.restrictions.remove('tobacco')
                    $ child.schedule.add_action('smoke_yes')
                    $ txt = 'Сыченька то бодрячком \n @ \n Каждые пять минут в падик бегает \n @ \n Наверное друзья у него там'         
                'Запретить спайсы' if 'weed' not in child.restrictions:
                    $ child.restrictions.append('weed')
                    $ child.schedule.add_action('weed_no')
                    $ txt = 'Чтобы я тебя с этими наркоманами не видела больше \n @ \n Пообколются своей марихуанной \n @ \n А потом ябут друг-друга в жёппы'
                'Игнорировать спайсы' if 'weed' in child.restrictions and mom_stance > 0:
                    $ child.restrictions.remove('weed')
                    $ child.schedule.add_action('weed_yes')
                    $ txt = 'Ой а что это за штучка такая у тебя, Сыча? \n @ \n Для ароматизации помещения да? \n @ \n И вот сюда вот воду заливать?'                     
                'Назад':
                    jump lbl_control_lifestyle        
        
        "Достаточно":
            jump lbl_universal_menu     
    
    jump lbl_control_lifestyle
    return
    

label lbl_chores:
    menu:
        'Какие работы по дому будет выполнять Сыча чтобы повысить настроение мамке? Каждая работа в расписании требует энергии (списывается в конце хода)! Ты можешь назначить любой объём, но перебор приведёт к усталости и неэффективной работе.'

        "Готовить еду" if not child.schedule.has_action('cook_cook'):
            $ child.schedule.add_action('cook_cook')              
        "Отменить наряд по кухне" if child.schedule.has_action('cook_cook'):
            $ child.schedule.remove_action('cook_cook')    
            
        "Создать в доме уют" if not child.schedule.has_action('comfy_comfy'):
            $ child.schedule.add_action('comfy_comfy')              
        "Отменить наряд по уборке" if child.schedule.has_action('comfy_comfy'):
            $ child.schedule.remove_action('comfy_comfy')  
            
        "Делать мамке массаж" if not child.schedule.has_action('matz_matz'):
            $ child.schedule.add_action('matz_matz')              
        "Отменить массаж" if child.schedule.has_action('matz_matz'):
            $ child.schedule.remove_action('matz_matz')  
            
        "Выслушивать мамкины истории" if not child.schedule.has_action('hear_hear'):
            $ child.schedule.add_action('hear_hear')              
        "Не слушать истории" if child.schedule.has_action('hear_hear'):
            $ child.schedule.remove_action('hear_hear')  
            
        "Батрачить на мамкиной весёлой ферме" if not child.schedule.has_action('farm_farm'):
            $ child.schedule.add_action('farm_farm')              
        "Забить на всёлую ферму" if child.schedule.has_action('farm_farm'):
            $ child.schedule.remove_action('farm_farm')    
            
        "Общаься с мамкиными гостями" if not child.schedule.has_action('lik_lik'):
            $ child.schedule.add_action('lik_lik')              
        "Игнорировать на мамкиных гостей" if child.schedule.has_action('lik_lik'):
            $ child.schedule.remove_action('lik_lik')  
                        
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

        #"Клянчить (нужын AP!)" if child.ap > 0:
           # call lbl_beg
        
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
                'Наладить отношения с матерью' if mother.stance.value < 3:
                    python:
                        player.ap -= 1
                        child.use_token('accordance')
                        mom.stance.value += 1
                        stance = mom.stance.level
                    'Глобальное отношение матери изменилось. Теперь: [stance]'   
                'Соглашаться и восхищаться':
                    $ player.ap -= 1
                    $ mom.use_token('accordance')
                    $ child.relations(mom).change('congruence', '+')
                'Троллить и подъёбывать':
                    $ player.ap -= 1
                    $ mom.use_token('accordance')
                    $ child.relations(mom).change('congruence', '-')
                'Знаять мягкую позицию':
                    $ player.ap -= 1
                    $ mom.use_token('accordance')
                    $ child.relations(mom).change('fervor', '+')                            
                'Занять жесткую позицию':
                    $ player.ap -= 1
                    $ mom.use_token('accordance')
                    $ child.relations(mom).change('fervor', '-')  
                'Больше личной вовлечённости':
                    $ player.ap -= 1
                    $ mom.use_token('accordance')
                    $ child.relations(mom).change('distance', '+')
                'Формализовать отношения':
                    $ player.ap -= 1
                    $ mom.use_token('accordance')
                    $ child.relations(mom).change('distance', '-')
                'Назад':
                    jump lbl_change_relations  
                    
        'Antagonism' if mom.has_token("antagonism"):
            menu:
                'Испортить отношения с матерью' if mother.stance.value > 0:
                    python:
                        player.ap -= 1
                        child.use_token('antagonism')
                        mother.stance.value -= 1
                        stance = mom.stance.level
                    'Глобальное отношение матери изменилось. Теперь: [stance]'                     
                'Троллить и подъёбывать':
                    $ player.ap -= 1
                    $ mom.use_token('antagonism')
                    $ child.relations(mom).change('congruence', '-')
                'Занять жесткую позицию':
                    $ player.ap -= 1
                    $ mom.use_token('antagonism')
                    $ child.relations(mom).change('fervor', '-')                    
                'Формализовать отношения':
                    $ player.ap -= 1
                    $ mom.use_token('antagonism')
                    $ child.relations(mom).change('distance', '-')
                'Назад':
                    jump lbl_change_relations  
                    
        'Compassion' if mom.has_token("compassion"):
            menu:
                'Смягчить позицию мамки' if mom.stance.level == 'cruel':
                    $ player.ap -= 1
                    $ mom.use_token('compassion')
                    $ mom.stance.set_level('opressive')         
                    'Глобальное отношение мамки изменилось с жестокого на деспотичное'
                'Разжалобить мамку':
                    $ player.ap -= 1
                    $ mom.use_token('compassion')
                    $ mom.stance.add_point('compassion')                    
                'Соглашаться и восхищаться':
                    $ player.ap -= 1
                    $ mom.use_token('compassion')
                    $ mom.relations(child).change('congruence', '+')
                'Занять мягкую позицию':
                    $ player.ap -= 1
                    $ mom.use_token('compassion')
                    $ mom.relations(child).change('fervor', '+')
                'Больше личной вовлечённости':
                    $ player.ap -= 1
                    $ mom.use_token('compassion')
                    $ mom.relations(child).change('distance', '+')
                'Назад':
                    jump lbl_change_relations  
                    
        'Confidence' if mom.has_token("confidence"):
            menu:
                'Смягчить позицию мамки' if mom.stance.level == 'cruel':
                    $ player.ap -= 1
                    $ mom.use_token('confidence')
                    $ mom.stance.set_level('opressive')         
                    'Глобальное отношение мамки изменилось с жестокого на деспотичное'
                'Увеличить доверие мамки':
                    $ player.ap -= 1
                    $ mom.use_token('confidence')
                    $ mom.stance.add_point('confidence')                    
                'Соглашаться и восхищаться':
                    $ player.ap -= 1
                    $ mom.use_token('confidence')
                    $ mom.relations(child).change('congruence', '+')
                'Занять жесткую позицию':
                    $ player.ap -= 1
                    $ mom.use_token('confidence')
                    $ child.relations(mom).change('fervor', '-')   
                'Формализовать отношения':
                    $ player.ap -= 1
                    $ mom.use_token('confidence')
                    $ child.relations(mom).change('distance', '-')
                'Назад':
                    jump lbl_change_relations  
                    
        'Craving' if mom.has_token("craving"):
            menu:
                'Смягчить позицию мамки' if mom.stance.level == 'opressive' and mom.favor() > 3:
                    $ player.ap -= 1
                    $ mom.use_token('craving')
                    $ mom.stance.set_level('rightful')         
                    'Глобальное отношение мамки изменилось с деспотичного на справедливое'
                'Внушить мамке любовь':
                    $ player.ap -= 1
                    $ mom.use_token('craving')
                    $ mom.stance.add_point('craving')                    
                'Занять жесткую позицию':
                    $ player.ap -= 1
                    $ mom.use_token('craving')
                    $ mom.relations(child).change('fervor', '-')   
                'Занять мягкую позицию':
                    $ player.ap -= 1
                    $ mom.use_token('craving')
                    $ mom.relations(child).change('fervor', '+')
                'Больше личной вовлечённости':
                    $ player.ap -= 1
                    $ mom.use_token('craving')
                    $ mom.relations(child).change('distance', '+')
                'Назад':
                    jump lbl_change_relations  
                    
        "Достаточно":
            jump lbl_son_manage        
                    
    jump lbl_son_manage  
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
    