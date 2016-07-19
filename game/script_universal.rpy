#Универсальное меню управления 

label lbl_universal_menu:
    $ consumption_provision = game.resource_consumption('provision')
    $ consumption_drugs = game.resource_consumption('drugs')
    $ money_consumption = game.resource_consumption('money')
    menu:
        'Тенгэ: [game.money] (-[money_consumption]) | Жратва: [game.provision] (-[consumption_provision]) | Вещества: [game.drugs] (-[consumption_drugs]) \nЖратва и вещества будут приобретаться по цене 3 монеты если их не хватает на текущее потребление. Если покрыть потребление невозможно, пропустить ход нельзя. Урезайте потребление.'
        
        "Взаимодействия с...":
            $ target = renpy.call_screen('sc_choose_character')
            call lbl_info_new(target)
            call lbl_target_menu
               
        "Магазин" if player == mom:
            call lbl_shop         
            
        "Следующая неделя" if game.can_skip_turn():
            jump label_new_day
            
    jump lbl_universal_menu
    return

label lbl_target_menu:
    $ name = target.name()
    menu:
        'Объект деятельности: [name]'
        "Расписание" if player == mom or target == child:
            call lbl_make_shedule
        "Важные события (AP:[player.ap])" if player.ap > 0:
            call lbl_activate_ap
        "Бытовые уловия" if target == child:
            call lbl_accommodation
        "Питание":
            call lbl_food_universal
        "Правила" if target == child:
            call lbl_rules_behavior
        "Вещества":
            call lbl_rules_drugs            
        "Карманные деньги":
            call lbl_personal_wealth
        "Информация":
            call lbl_info_new(target)
        "Назад":
            jump lbl_universal_menu    
    
    jump lbl_target_menu
    return

label lbl_make_shedule:
        
    $ schedule_major = dname[target.job]
    $ schedule_minor = dname[target.minor]
    
    menu:
        "По вечерам: [schedule_major]":
            call lbl_shedule_major
        "В выходные: [schedule_minor]":
            call lbl_shedule_minor
        "Общение: [communication]" if player != mom:
            call lbl_universal_interaction
            
        'Назад':
            jump lbl_universal_menu    
            
    jump lbl_make_shedule
        
label lbl_shedule_major:
    menu:
        'Воспитывать Сыченьку' if target == child and player == mom:
            $ beneficiar = target.master
            $ code = None
            menu:
                'Кто этим займётся? Распиание основного времени этого персонажа изменится на "Воспитание". Если вы измените потом расписание, то воспитания не произойдёт.'
                'Маман':
                    python:
                        if mom.job != 'supervise':
                            mom.schedule.add_action('job_supervise', False)
                    $ mom.job_object().add_special_list_value('slaves', child)
                    $ actor = mom
                'BATYA':
                    python:
                        if batya.job != 'supervise':
                            batya.schedule.add_action('job_supervise', False)
                    $ batya.job_object().add_special_list_value('slaves', child)
                    $ actor = batya
                'Компетентные органы':
                    jump lbl_special_discipline
                'Передумать':
                    jump lbl_shedule_major
            menu:
                'Какой подход выборать?'
                'Запугивание':
                    $ moral_burden = ['evil', 'ardent', 'chaotic']
                    $ token = 'conquest'
                    jump lbl_torture_choose
                'Наказание (есть грех)' if target.has_condition('sin'):
                    $ moral_burden = ['evil', 'ardent', 'lawful']
                    $ token = 'convention'
                    jump lbl_torture_choose
                'Поощрение (есть заслуга)' if target.has_condition('merit'):
                    $ moral_burden = ['good', 'timid', 'lawful']
                    $ token = 'convention'
                    jump lbl_pleasing_choose
                'Ублажение':
                    $ moral_burden = ['good', 'timid', 'chaotic']
                    $ token = 'contribution'
                    jump lbl_pleasing_choose
                'Передумать':
                    jump lbl_shedule_major           
                    
        'Подвергаться воспитанию' if target == mom and player == child:
            $ beneficiar = target.master
            $ code = None
            $ mentxt = encolor_text('Добиться признания', player.merit)
            if mom.stance(player).value == -1 and mom.relations(child).stability == 0:
                jump lbl_first_impression
            menu:
                'Что будем делать?'
                'Страдать и плакать':
                    $ moral_burden = ['ardent', 'chaotic']
                    $ token = 'conquest'
                    jump lbl_suffer_choose
                '[mentxt] (AP, заслуга)' if player.merit > 0 and player.ap > 0:
                    $ player.ap -= 1
                    if player.merit > mom.relations(player).stability:
                        mom.add_token('convention')
                    else:
                        'Этого не достаточно чтобы продвинуть отношения. Нужно добиться более серьёзных успехов.'
                    player.merit = 0
                    jump lbl_shedule_major
                'Ублажать и подлизываться':
                    $ moral_burden = ['good', 'timid']
                    $ token = 'contribution'
                    jump lbl_fawn_choose
                'Передумать':
                    jump lbl_shedule_major                         
                    
        "Обучение навыкам" if target == player or player == mom:
            call lbl_skill_train
        "Назначить воспитателем" if player == mom and target != child:
            $ target.schedule.add_action('job_supervise', False)
        'Безделье':
            $ target.schedule.add_action('job_idle', False) 
        'Подрабатывать уборщицей' if target == mom and player == mom:
            $ target.schedule.add_action('job_janitor', False) 
        'Делать уроки' if target == child:
            $ target.schedule.add_action('job_study', False) 
        'Бытовое рабство (+10 тенге/нед)' if player == mom or target == child:
            $ target.schedule.add_action('job_chores', False)     
        'Тёмные мутки (коммуникация, +вещества)' if target != mom:
            $ target.schedule.add_action('job_pusher', False)               
        'Работать грузчиком (спорт, малый заработок)' if target == child:
            $ target.schedule.add_action('job_porter', False)    
        'Работать гей-шлюхой (секс, хороший заработок)' if target == child:
            $ target.schedule.add_action('job_whore', False)                
        "Назад":
            call lbl_make_shedule
            
    return
        
label lbl_shedule_minor:
    menu:
        'Отдыхать':
            $ target.schedule.add_action('minor_nap', False)   
        'Развлекаться':
            $ target.schedule.add_action('minor_fun', False)   
        'Общаться':
            $ target.schedule.add_action('minor_chat', False)  
        'Брусья-брусья-турнички':
            $ target.schedule.add_action('minor_sport', False)   
        'Еду на дачу и батрачу, еды нахуячу':
            $ target.schedule.add_action('minor_dacha', False)
              
    return
    
label lbl_special_discipline:
    $ special_values = {}
    menu:
        'Компетентные органы могут за определённую плату дать жетон, но только при условии что стабильность отношений ещё не слишком высока и только по одному разу.'
        'Батюшка Павсикакий (24 бутылки кагора)' if not churched:
            $ game.res_add_consumption("discipline", 'drugs', 24, time=1)
            $ special_values = {}
            $ target.schedule.add_action('job_church', special_values=special_values)
        '"Кохана ми вбиваємо дітей" (300 тенгэ)' if not kohaned:
            $ game.res_add_consumption("discipline", 'money', 300, time=1)
            $ special_values = {}
            $ target.schedule.add_action('job_kohana', special_values=special_values)            
    jump lbl_shedule_major    
    return

label lbl_skill_train:
    menu:
        'ЗОЖ' if not target.skill('sport').training:
            $ target.schedule.add_action('job_sport')            
        'Социоблядство' if not target.skill('conversation').training:
            $ target.schedule.add_action('job_conversation')   
        'Быдлокодинг' if not target.skill('coding').training:
            $ target.schedule.add_action('job_coding')   
        'Пикап' if not target.skill('sex').training:
            $ target.schedule.add_action('job_sex')               
        'Назад':
            jump lbl_shedule_major
            
    jump lbl_target_menu
    return

label lbl_first_impression:
    menu:
        'Мамка относится к Сычуле просто невыносимо. Что будем делать?'
        'Макимальная агрессия и конфликт':
            $ token = 'conquest'
            $ txt = 'Первое впечатление - враждебное. Нейтральные тенденции мамки изменены на страсть и злобу. Заработан жетон доминирования.'
        'Разумный и взвешенный подход':
            $ token = 'convention'
            $ txt = 'Первое впечатление - рациональное. Нейтральные тенденции мамки изменены на вкрадчивость и порядочность. Заработан жетон сотрудничества.'
        'Любить маму несмотря ни на что':
            $ token = 'contribution'
            $ txt = 'Первое впечатление - мягкое. Нейтральные тенденции мамки изменены на близость и доброту. Заработан жетон благодарности.' 
    $ special_values = {'token': token, 'txt': txt}        
    $ target.schedule.add_action('job_impress', special_values=special_values)
            
    jump lbl_make_shedule
    return

label lbl_free_stance:
    menu:
        'Мамка имеет слишком много власти. Идти против неё значит испортить себе жизнь. Если сдаться - есть надежда смягчить её.'
        'Обещать быть послушным':
            if player.master.alignment.orderliness > 0 or child.attitude_tendency() == 'convention':
                $ player.ap -= 1
                $ mom.stance(child).value = 0  
                "Сычик нашёл правильный подход и теперь у них с мамкой терпимые отношения... но расслабляться рано."    
            else:
                $ player.ap -= 1
                "Мамка непреклонна. Надо найти к ней другой подход..."   
        'Подстраиваться под настроение мамки':
            if player.master.alignment.orderliness < 0 or child.attitude_tendency() == 'contribution':
                $ player.ap -= 1
                $ mom.stance(child).value = 0  
                "Сычик нашёл правильный подход и теперь у них с мамкой терпимые отношения... но расслабляться рано."
            else:
                $ player.ap -= 1
                "Мамка непреклонна. Надо найти к ней другой подход..." 
        'Доказать свою полезность':
            if player.master.alignment.activity > 0 or child.attitude_tendency() == 'conquest':
                $ player.ap -= 1
                $ mom.stance(child).value = 0  
                "Сычик нашёл правильный подход и теперь у них с мамкой терпимые отношения... но расслабляться рано."
            else:
                $ player.ap -= 1
                "Мамка непреклонна. Надо найти к ней другой подход..." 
        'Покориться и смириться':
            if player.master.alignment.activity < 0 or child.attitude_tendency() == 'convention':
                $ player.ap -= 1
                $ mom.stance(child).value = 0  
                "Сычик нашёл правильный подход и теперь у них с мамкой терпимые отношения... но расслабляться рано."
            else:
                $ player.ap -= 1
                "Мамка непреклонна. Надо найти к ней другой подход..." 
        'Униженно умолять о пощаде':
            if player.master.alignment.morality < 0 or child.attitude_tendency() == 'conquest':
                $ player.ap -= 1
                $ mom.stance(child).value = 0  
                "Сычик нашёл правильный подход и теперь у них с мамкой терпимые отношения... но расслабляться рано."
            else:
                $ player.ap -= 1
                "Мамка непреклонна. Надо найти к ней другой подход..." 
        'Вести себя хорошо':
            if player.master.alignment.morality > 0 or child.attitude_tendency() == 'contribution':
                $ player.ap -= 1
                $ mom.stance(child).value = 0  
                "Сычик нашёл правильный подход и теперь у них с мамкой терпимые отношения... но расслабляться рано."
            else:
                $ player.ap -= 1
                "Мамка непреклонна. Надо найти к ней другой подход..."                     
        'Nyet, Molotoff!':
            jump lbl_shedule_major
                
    return

label lbl_torture_choose:
    menu:
        'Выберите основной способ давления.'
        'Бить ремнём (спорт)':
            $ self_satisfy = ['power', 'authority']
            $ self_tension = ['altruism']
            $ skill = 'sport'
            $ target_tension = ['wellness']
        'Хуесосить (коммуникация)':
            $ self_satisfy = ['power', 'authority']
            $ self_tension = ['altruism']
            $ skill = 'conversation'
            $ target_tension = ['authority', 'ambition']    
        'Ставить в угол (коммуникация)':
            $ self_satisfy = ['authority', 'order']
            $ self_tension = ['thrill']
            $ skill = 'conversation'
            $ target_tension = ['comfort', 'amusement', 'activity'] 
            
    $ special_values = {'skill': skill, 'torturer': actor, 'token': token, 'target_tension': target_tension, 'self_tension': self_tension,
                        'self_satisfy': self_satisfy, 'moral_burden': moral_burden, 'beneficiar': beneficiar}
    $ target.schedule.add_action('job_torture', special_values=special_values)
    
    jump lbl_target_menu
    return

label lbl_pleasing_choose:
    menu:
        'Выберите основной способ ублажения.'
        'Похвала и доброта (коммуникация)':
            $ self_satisfy = ['altruism', 'communication']
            $ self_tension = ['power']
            $ skill = 'conversation'
            $ target_statisfy = ['communication', 'approval']
        'Поощрить самостоятельность (коммуникация)':
            $ self_satisfy = ['independence']
            $ self_tension = ['order', 'authority']
            $ skill = 'conversation'
            $ target_statisfy = ['independence', 'authority']            
        'Подарки (коммуникация, 5 тенгэ)':
            $ game.res_add_consumption("gifts", 'money', 5, time=1)
            $ self_satisfy = ['altruism', 'communication']
            $ self_tension = ['power', 'prosperity']
            $ skill = 'conversation'
            $ target_statisfy = ['prosperity']    
    
    $ special_values = {'skill': skill, 'executor': actor, 'token': token, 'target_statisfy': target_statisfy, 'self_tension': self_tension,
                        'self_satisfy': self_satisfy, 'moral_burden': moral_burden, 'beneficiar': beneficiar}
    $ target.schedule.add_action('job_pleasing', special_values=special_values)
    
    jump lbl_target_menu
    return

label lbl_suffer_choose:
    menu:
        'От чего страдаем?'
        'Избиения':
            $ actor_satisfy = ['power', 'authority']
            $ actor_tension = ['altruism']
            $ skill = 'conversation'
            $ self_tension = ['wellness']
        'Унижения':
            $ actor_satisfy = ['power', 'authority']
            $ actor_tension = ['altruism']
            $ skill = 'conversation'
            $ self_tension = ['authority', 'ambition']    
        'Ограничения':
            $ actor_satisfy = ['authority', 'order']
            $ actor_tension = ['thrill']
            $ skill = 'conversation'
            $ self_tension = ['comfort', 'amusement', 'activity'] 
            
    $ special_values = {'skill': skill, 'victim': child, 'token': token, 'self_tension': self_tension, 'actor_tension': actor_tension,
                        'actor_satisfy': actor_satisfy, 'moral_burden': moral_burden, 'beneficiar': beneficiar}
    $ target.schedule.add_action('job_suffer', special_values=special_values)
    
    jump lbl_target_menu
    return

label lbl_fawn_choose:
    menu:
        'Выберите основной способ ублажения мамки.'
        'Льстить (коммуникация)':
            $ self_satisfy = []
            $ self_tension = ['authority']
            $ skill = 'conversation'
            $ target_statisfy = ['communication', 'approval']
        'Развлекать (коммуникация)':
            $ self_satisfy = ['approval']
            $ self_tension = ['anusement', 'independence']
            $ skill = 'conversation'
            $ target_statisfy = ['communication', 'amusement']            
        'Делать массаж ног (секс)':
            $ self_satisfy = ['altruism']
            $ self_tension = ['eros', 'independence']
            $ skill = 'sex'
            $ target_statisfy = ['comfort', 'eros']    
    
    $ special_values = {'skill': skill, 'executor': actor, 'token': token, 'target_statisfy': target_statisfy, 'self_tension': self_tension,
                        'self_satisfy': self_satisfy, 'moral_burden': moral_burden, 'beneficiar': beneficiar}
    $ target.schedule.add_action('job_pleasing', special_values=special_values)
    
    jump lbl_target_menu
    return
    
label lbl_accommodation:
    $ nm = target.name() + '_rent'
    menu:
        'Вечно ты в комнате запираешься от матери! Как сыч. (25 тенгэ/нед)':
            $ target.accommodation = "appartment"
            $ target.schedule.add_action('living_appartment', False)  
            $ summ = 25
        'Комнату твою сдавать будем, поспишь у нас на диванчике. (10 тенгэ/нед)':
            $ target.accommodation = "cot"
            $ target.schedule.add_action('living_cot', False)  
            $ summ = 10
        'Диванчик для тёти Сраки, а тебе вот раскладушечка дедова. (5 тенгэ/нед)':
            $ target.accommodation = "mat"
            $ target.schedule.add_action('living_mat', False)  
            $ summ = 5
        'В ванной тебя запрём ночевать. Чтобы не воображал!':
            $ target.accommodation = "jailed"
            $ target.schedule.add_action('living_jailed', False)    
            $ summ = 0
        'Ты у меня в шкафу сидеть будешь. Пока мать любить не научишься.':
            $ target.accommodation = "confined"
            $ target.schedule.add_action('living_confined', False)    
            $ summ = 0
            
    $ game.res_add_consumption(nm, 'money', summ, time=None)
    return

label lbl_food_universal:
    menu:
        'Размер пайки.'
        '"Не кормить (starvation)"':
            $ target.ration['amount'] = "starvation"   
            $ target.ration['food_type'] = "forage"   
            $ target.ration['target'] = 0           
            $ target.ration['limit'] = None      
        "На худобу (regime 1)":
            $ target.ration['amount'] = "regime" 
            $ target.ration['target'] = 1
        "На норму (regime 2)":
            $ target.ration['amount'] = "regime" 
            $ target.ration['target'] = 2     
        "На своё усмотрение (unlimited)":
            $ target.ration['amount'] = "unlimited"     
        "На ЖРЧИК (regime 3)":
            $ target.ration['amount'] = "regime" 
            $ target.ration['target'] = 4               
  
    if target.ration['amount'] != "starvation":    
        menu:
            "Качество питания."
            "Отбросы":
                $ target.ration['food_type'] = "sperm" 
                'Как земля... совсем невкусно (-3)'
            "Бичпакеты":
                $ target.ration['food_type'] = "dry" 
                'Мивина с майонезом... не вкусно (-1)'
            "Консервы":
                $ target.ration['food_type'] = "canned" 
                'Из банки... нормальный вкус'
            "Домашнее, тепленькое, с хлебушком":
                $ target.ration['food_type'] = "cousine"   
                'Пища белых людей... вкуснота (3)'    
    
    return

label lbl_activate_ap:
    $ a = target.relations(player).harmony()[0] - 1
    menu:
        'Эти действия тратят AP вашего персонажа.'
        'Найти к чему придраться' if player == mom and target == child:
            $ player.ap -= 1
            $ target.add_condition('sin')
            'Теперь можно наказывать.'
        'Сдвиг в отношениях (нужны жетоны отношений)':
            if mom.stance(player).value == -1:
                jump lbl_free_stance
            menu:
                'Доступны только те опции для которых с выбранным персонажем есть непотраченные жетоны отношений: antagonism, accordance, contribution, conquer или convention.'
                'Гармония (Accordance)' if target.has_token("accordance"):
                    menu:
                        'Глобальный позитивный сдвиг отношений'if target.stance(player).value < min(1, target.relations(player).harmony()[0] - 1):
                            $ player.ap -= 1
                            $ target.use_token('accordance')
                            $ target.stance(player).value +=1  
                            'Глобальное отношение (stance) улучшилось.'   
                        'Гармонизовать позиции' if not target.relations(player).is_max('congruence', '+'):
                            $ player.ap -= 1
                            $ target.use_token('accordance')
                            $ target.relations(player).change('congruence', '+')
                        'Создать напряжение' if not target.relations(player).is_max('congruence', '-'):
                            $ player.ap -= 1
                            $ target.use_token('accordance')
                            $ target.relations(player).change('congruence', '-')                            
                        'Внушить уважение' if not target.relations(player).is_max('fervor', '+'):
                            $ player.ap -= 1
                            $ target.use_token('accordance')
                            $ target.relations(player).change('fervor', '+')      
                        'Внушить спокойствие' if not target.relations(player).is_max('fervor', '-'):
                            $ player.ap -= 1
                            $ target.use_token('accordance')
                            $ target.relations(player).change('fervor', '-')  
                        'Сблизиться' if not target.relations.is_max('distance', '+'):
                            $ player.ap -= 1
                            $ target.use_token('accordance')
                            $ target.relations(player).change('distance', '-')
                        'Формализовать отношения' if not target.relations(player).is_max('distance', '-'):
                            $ player.ap -= 1
                            $ target.use_token('accordance')
                            $ target.relations(player).change('distance', '+')
                        'Передумать':
                            jump lbl_activate_ap    
                'Раздор (Antagonism)' if target.has_token("antagonism"):
                    menu:
                        'Глобально испортить отношение' if target.stance(player).value > -1:
                            $ player.ap -= 1
                            $ target.use_token('antagonism')
                            $ target.stance(player).value -=1  
                            'Глобальное отношение (stance) улучшилось.'                           
                        'Усилить враждебность' if not target.relations(player).is_max('congruence', '-'):
                            $ player.ap -= 1
                            $ target.use_token('antagonism')
                            $ target.relations(player).change('congruence', '-')                            
                        'Накалить страсти' if not target.relations(player).is_max('fervor', '+'):
                            $ player.ap -= 1
                            $ target.use_token('antagonism')
                            $ target.relations(player).change('fervor', '+')      
                        'Формализовать отношения' if not target.relations(player).is_max('distance', '-'):
                            $ player.ap -= 1
                            $ target.use_token('antagonism')
                            $ target.relations(player).change('distance', '+')
                        'Передумать':
                            jump lbl_activate_ap                    
                'Доминирование (conquest)' if target.has_token("conquest"):
                    menu:
                        'Глобальный позитивный сдвиг отношений' if target.stance(player).value < min(1, a) and target.relations(player).is_harmony_points('passionate', 'contradictor'):
                            $ player.ap -= 1
                            $ target.use_token('conquest')
                            $ target.stance(player).value +=1  
                            'Глобальное отношение (stance) улучшилось.'                           
                        'Создать напряжение' if not target.relations(player).is_max('congruence', '-'):
                            $ player.ap -= 1
                            $ target.use_token('conquest')
                            $ target.relations(player).change('congruence', '-')                            
                        'Накалить страсти' if not target.relations(player).is_max('fervor', '+'):
                            $ player.ap -= 1
                            $ target.use_token('conquest')
                            $ target.relations(player).change('fervor', '+')      
                        'Теперь это личное' if not target.relations(player).is_max('distance', '-'):
                            $ player.ap -= 1
                            $ target.use_token('conquest')
                            $ target.relations(player).change('distance', '+')
                        'Передумать':
                            jump lbl_activate_ap    
                'Сотрудничество (convention)' if target.has_token("convention"):
                    menu:
                        'Глобальный позитивный сдвиг отношений' if target.stance(player).value < min(1, a) and target.relations(player).is_harmony_points('formal', 'delicate'):
                            $ player.ap -= 1
                            $ target.use_token('convention')
                            $ target.stance(player).value +=1  
                            'Глобальное отношение (stance) улучшилось.'                                    
                        'Гармонизовать позиции' if not target.relations(player).is_max('congruence', '+'):
                            $ player.ap -= 1
                            $ target.use_token('convention')
                            $ target.relations(player).change('congruence', '+')
                        'Охладить пыл' if not target.relations(player).is_max('fervor', '-'):
                            $ player.ap -= 1
                            $ target.use_token('convention')
                            $ target.relations(player).change('fervor', '-')  
                        'Формализовать отношения' if not target.relations(player).is_max('distance', '+'):
                            $ player.ap -= 1
                            $ target.use_token('convention')
                            $ target.relations(player).change('distance', '-')
                        'Передумать':
                            jump lbl_activate_ap    
                'Благодарность (contribution)' if target.has_token("contribution") :
                    menu:
                        'Глобальный позитивный сдвиг отношений' if target.stance(player).value < min(1, a) and target.relations(player).is_harmony_points('supporter', 'intimate'):
                            $ player.ap -= 1
                            $ target.use_token('contribution')
                            $ target.stance(player).value +=1  
                            'Глобальное отношение (stance) улучшилось.'                          
                        'Гармонизовать позиции' if not target.relations(player).is_max('congruence', '+'):
                            $ player.ap -= 1
                            $ target.use_token('contribution')
                            $ target.relations(player).change('congruence', '+')
                        'Накалить страсти' if not target.relations(player).is_max('fervor', '+'):
                            $ player.ap -= 1
                            $ target.use_token('contribution')
                            $ target.relations(player).change('fervor', '+')      
                        'Сблизиться' if not target.relations(player).is_max('distance', '-'):
                            $ player.ap -= 1
                            $ target.use_token('contribution')
                            $ target.relations(player).change('distance', '+')
                        'Передумать':
                            jump lbl_activate_ap                                
                'Назад':
                    jump lbl_activate_ap
        'Назад':
            jump lbl_target_menu
    
    return

label lbl_rules_drugs:
    menu:
        'Запретить курить' if 'tobacco' not in target.restrictions:
            $ target.restrictions.append('tobacco')
            $ resname = target.name() + '_tobacco'
            $ game.res_add_consumption(resname, 'drugs', 0, time=None)            
            $ txt = 'Если почую табачный запах \n @ \n Всё отцу расскажу \n @ \n Неделю у меня сидеть на жопе не сможешь'
        'Парю где хочу, не запрещено (1/нед)' if 'tobacco' in target.restrictions:
            $ target.restrictions.remove('tobacco')
            $ target.schedule.add_action('None_smoke', False)
            $ resname = target.name() + '_tobacco'
            $ game.res_add_consumption(resname, 'drugs', 1, time=None)            
            $ txt = 'Сыченька то бодрячком \n @ \n Каждые пять минут в падик бегает \n @ \n Наверное друзья у него там'       
            
        'Cухой закон' if 'alcohol' not in target.restrictions:
            $ target.restrictions.append('alcohol')
            $ resname = target.name() + '_alco'
            $ game.res_add_consumption(resname, 'drugs', 0, time=None)
            $ txt = 'Ты на пиво то не заглядвайся \n @ \n Ишь чего удумал прохиндей \n @ \n Я алкоголиков в доме не потерплю!'
        'Накатывать за дидов (3/нед)' if 'alcohol' in target.restrictions:
            $ target.restrictions.remove('alcohol')
            $ target.schedule.add_action('None_alcohol', False)
            $ resname = target.name() + '_alco'
            $ game.res_add_consumption(resname, 'drugs', 3, time=None)
            $ txt = 'За дидов рюмашечку надо обязательно \n @ \n Что значит "не буду стекломой пить" \n @ \n Традиции наши не уважаешь?'     
            
  
        'Запретить наркотики' if 'weed' not in target.restrictions:
            $ target.restrictions.append('weed')
            $ resname = target.name() + '_weed'
            $ game.res_add_consumption(resname, 'drugs', 0, time=None)            
            $ txt = 'Чтобы я тебя с этими наркоманами не видела больше \n @ \n Пообколются своей марихуанной \n @ \n А потом ябут друг-друга в жёппы'
        'Соли, миксы, спайсы (5/нед)' if 'weed' in target.restrictions:
            $ target.restrictions.remove('weed')
            $ target.schedule.add_action('None_weed', False)
            $ resname = target.name() + '_weed'
            $ game.res_add_consumption(resname, 'drugs', 5, time=None)            
            $ txt = 'Ой а что это за штучка такая у тебя, Сыча? \n @ \n Для ароматизации помещения да? \n @ \n И вот сюда вот воду заливать?'                     
        'Назад':
            jump lbl_target_menu
    # "[txt]"
    
    jump lbl_rules_drugs
    return

label lbl_rules_behavior:
    $ txt = None
    menu:
        'Пресечь любую дрочку' if 'masturbation' not in target.restrictions:
            $ target.restrictions.append('masturbation')
            $ target.schedule.add_action('fap_no', False)
            $ txt = 'Сыночка то наш, всё пиструнчик свой тилибонькает \n @ \n Скоро волосы на руках расти начнут \n @ \n В антимастурбационном кресте будещь спать, по совету отца Агапия'
        'Игнорировать дрочку' if 'masturbation' in target.restrictions:
            $ target.restrictions.remove('masturbation')
            $ target.schedule.add_action('fap_yes', False)
            $ txt = 'А что это ты в ванной столько времени сидишь, Сыча? \n @ \n И то хорошо \n @ \n Приучили к чистоте ребёнка то'    
        'Запретить гулять' if 'dates' not in target.restrictions:
            $ target.restrictions.append('dates')
        'Разрешить гулять до поздна' if 'dates' in target.restrictions:
            $ target.restrictions.remove('dates')
        'Запретить общаться с друзьями' if 'friends' not in target.restrictions:
            $ target.restrictions.append('friends')
        'Разрешить общаться с друзьями' if 'friends' in target.restrictions:
            $ target.restrictions.remove('friends')
        'Конплюхтерн для очобы! (блокировать интернет)' if 'pc' not in target.restrictions:
            $ target.restrictions.append('pc')
        'Ну и сиди за своим комплюктером' if 'pc' in target.restrictions:
            $ target.restrictions.remove('pc')
        'Назад':
            jump lbl_target_menu
            
    if txt:
        '[txt]'
    jump lbl_rules_behavior    
    return  

label lbl_personal_wealth:
    $ resname = target.name() + '_wealth'
    menu:
        'Чем больше тенгэ персонаж может тратить на личные нужды, тем выше будет его удовлетворение процветанием (prosperity)'
        'Не жили бохато, неча и начинать!':
            $ special_values = {'num': -1}
            $ summ = 0
        '5 тенгэ / нед':
            $ special_values = {'num': 0}
            $ summ = 5   
        '10 тенгэ / нед':
            $ special_values = {'num': 1}            
            $ summ = 10
        '25 тенгэ / нед':
            $ special_values = {'num': 2}
            $ summ = 25  
        '50 тенгэ / нед':
            $ special_values = {'num': 3}
            $ summ = 50   
        '100 тенгэ / нед':
            $ special_values = {'num': 4}
            $ summ = 100 
        '250 тенгэ / нед':
            $ special_values = {'num': 5}
            $ summ = 100 
            
    $ game.res_add_consumption(resname, 'money', summ, time=None) 
    $ target.schedule.add_action('money_wealth', False, special_values=special_values)    
    return

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
        needs = target.get_needs()
        recalc_result_target = target
        vitality_info_target = target
        txt = "Настроение: " + encolor_text(target.show_mood(), target.mood) + '{a=lb_recalc_result_glue}?{/a}'
        if stance:
            txt += " | Поза: " + str(stance) +'\n'
        txt += " | Здоровье: %s "%(target.vitality) + '{a=lbl_vitality_info}?{/a}' + '\n'
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
            txt += "Тенденция: %s\n"%(tendency)
        if skills:
            txt += "Навыки: %s\n"%(skills)
        if tokens:
            txt += "Токены: %s\n"%(tokens)
        txt += 'Потребности: '
        # for need in needs:
        #    txt += '%s: [%s, %s, %s], '%(need, needs[need].level, needs[need].satisfaction, needs[need].tension)
        # txt += '\n'
        txt += "Ангст: %s, Решимость: %s\n"%(target.anxiety, target.determination)
        consumption = target.get_food_consumption(True)
        txt += 'Жрет: %s(%s)'%(consumption[0], consumption[1])
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


label lbl_skillcheck_info(result, stats, skill, used, threshold=None, difficulty=0):
    python:
        if result < 0:
            result = 0
        info_show_quality = [encolor_text('провально', 0), 
                            encolor_text('слабенько', 1),
                            encolor_text('удовлетворительно', 2),
                            encolor_text('хорошо', 3),
                            encolor_text('отлично', 4),
                            encolor_text('идеально', 5),
                            encolor_text('Impossible', 6)]
        txt = 'Сложность: %s\n'%(difficulty)
        txt += 'Результат: %s\n'%(info_show_quality[result])
        if threshold != None:
            txt += 'Требуется: %s\n'%(info_show_quality[threshold])
        txt += 'Лимитирующий фактор: %s(%s) \n'%(encolor_text(skill.name, skill.level+1), skill.level+1)
        txt += '+++++++ \n'
        unused = []
        for key in stats.keys():
            if key != 'level':
                if key in used:
                    txt += '%s \n'%(encolor_text(key, stats[key]))
                else:
                    unused.append('%s'%(encolor_text(key, stats[key])))
        txt += '---------- \n'
        for text in unused:
            txt += '%s \n'%(text)
        if stats['motivation'] <= 0:
            txt = 'Проверка провалена из-за низкой мотивации'
    '[txt]'
    return


label lbl_vitality_info():
    python:
        txt_good = ""
        txt_bad = ""
        zero_factors = ""
        d, l = vitality_info_target.vitality_info()
        items = list(d.items())
        for i in l:
            items.append(i)
        for k, v in items:
            if v > 0:
                txt_good += encolor_text(k, v) + '\n'
            elif v < 0:
                txt_bad += encolor_text(k, 0) + '\n'
            else:
                zero_factors += encolor_text(k, 6) + '\n'
        txt_good += '---------- \n'
        txt_good += txt_bad
        txt_good += '---------- \n'
        txt_good += zero_factors
    '[txt_good]'
    return






