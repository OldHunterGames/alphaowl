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
        "Расписание":
            call lbl_make_shedule
        "Важные события (AP:[player.ap])" if player.ap > 0:
            call lbl_activate_ap
        "Бытовые уловия" if player != child and target == child:
            call lbl_accommodation
        "Питание":
            call lbl_food_universal
        "Правила":
            $ pass
        "Карманные деньги":
            $ pass
        "Информация":
            call lbl_info_new(target)
        "Назад":
            jump lbl_universal_menu    
    
    jump lbl_target_menu
    return

label lbl_make_shedule:
        
    $ schedule_major = dname[target.job]
    
    menu:
        "По вечерам: [schedule_major]":
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
        'Воспитывать Сыченьку' if target == child:
            $ beneficiar = target.master
            $ code = None
            menu:
                'Кто этим займётся? Распиание основного времени этого персонажа изменится на "Воспитание". Если вы измените потом расписание, то воспитания не произойдёт.'
                'Маман':
                    $ mom.schedule.add_action('job_supervise', False)
                    $ mom.job_object().add_special_list_value('slaves', child)
                    $ actor = mom
                'BATYA':
                    $ batya.schedule.add_action('job_supervise', False)
                    $ batya.job_object().add_special_list_value('slaves', child)
                    $ actor = batya
                'Передумать':
                    jump lbl_shedule_major
            menu:
                'Какой подход выборать?'
                'Запугивание':
                    $ moral_burden = ['evil', 'intense', 'chaotic']
                    $ token = 'conquest'
                    jump lbl_torture_choose
                'Наказание':
                    $ moral_burden = ['evil', 'intense', 'lawful']
                    $ token = 'convention'
                    jump lbl_torture_choose
                'Поощрение':
                    $ moral_burden = ['good', 'timid', 'lawful']
                    $ token = 'convention'
                    jump lbl_pleasing_choose
                'Ублажение':
                    $ moral_burden = ['good', 'timid', 'chaotic']
                    $ token = 'contribution'
                    jump lbl_pleasing_choose
                'Передумать':
                    jump lbl_shedule_major                    
        "Назначить воспитателем" if player == mom and target != child:
            $ target.schedule.add_action('job_supervise', False)
        'Безделье':
            $ target.schedule.add_action('job_idle', False) 
        'Подрабатывать уборщицей' if target == mom:
            $ target.schedule.add_action('job_janitor', False) 
        'Делать уроки' if target == child:
            $ target.schedule.add_action('job_study', False) 
        'Бытовое рабство (+10 тенге/нед)':
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
    $ target.schedule.add_action('torture_check', special_values=special_values)
    
    jump lbl_universal_menu
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
            $ target_statisfy = ['communication', 'approval']    
    
    $ special_values = {'skill': skill, 'executor': actor, 'token': token, 'target_statisfy': target_statisfy, 'self_tension': self_tension,
                        'self_satisfy': self_satisfy, 'moral_burden': moral_burden, 'beneficiar': beneficiar}
    $ target.schedule.add_action('pleasing_check', special_values=special_values)
    
    jump lbl_universal_menu
    return
    
label lbl_accommodation:
    menu:
        'Вечно ты в комнате запираешься от матери! Как сыч. (25 тенгэ/нед)':
            $ target.schedule.add_action('living_appartment')  
            $ game.res_add_consumption("rent", 'money', 25, time=None)
        'Комнату твою сдавать будем, поспишь у нас на диванчике. (10 тенгэ/нед)':
            $ target.schedule.add_action('living_cot')  
            $ game.res_add_consumption("rent", 'money', 10, time=None)
        'Диванчик для тёти Сраки, а тебе вот раскладушечка дедова. (5 тенгэ/нед)':
            $ target.schedule.add_action('living_mat')  
            $ game.res_add_consumption("rent", 'money', 5, time=None)
        'В ванной тебя запрём ночевать. Чтобы не воображал!':
            $ target.schedule.add_action('living_jailed')    
            $ game.res_add_consumption("rent", 'money', 0, time=None)
        'Ты у меня в шкафу сидеть будешь. Пока мать любить не научишься.':
            $ target.schedule.add_action('living_confined')    
            $ game.res_add_consumption("rent", 'money', 0, time=None)
    
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
    menu:
        'Эти действия тратят AP вашего персонажа.'
        'Сдвиг в отношениях (нужны жетоны отношений)':
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
                            $ target.relations(player).change('distance', '+')
                        'Формализовать отношения' if not target.relations(player).is_max('distance', '-'):
                            $ player.ap -= 1
                            $ target.use_token('accordance')
                            $ target.relations(player).change('distance', '-')
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
                            $ target.relations(player).change('distance', '-')
                        'Передумать':
                            jump lbl_activate_ap                    
                'Доминирование (conquest)' if target.has_token("conquest"):
                    menu:
                        'Глобальный позитивный сдвиг отношений' if target.stance(player).value < min(1, target.relations(player).harmony()[0] - 1) and target.relations(player).is_harmony_points('passionate', 'contradictor'):
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
                        'Теперь это личное' if not target.relations(player).is_max('distance', '+'):
                            $ player.ap -= 1
                            $ target.use_token('conquest')
                            $ target.relations(player).change('distance', '+')
                        'Передумать':
                            jump lbl_activate_ap    
                'Сотрудничество (convention)' if target.has_token("convention") and target.stance(player).value < min(1, target.relations(player).harmony()[0] - 1) and target.relations(player).is_harmony_points('formal', 'delicate'):
                    menu:
                        'Гармонизовать позиции' if not target.relations(player).is_max('congruence', '+'):
                            $ player.ap -= 1
                            $ target.use_token('convention')
                            $ target.relations(player).change('congruence', '+')
                        'Охладить пыл' if not target.relations(player).is_max('fervor', '-'):
                            $ player.ap -= 1
                            $ target.use_token('convention')
                            $ target.relations(player).change('fervor', '-')  
                        'Формализовать отношения' if not target.relations(player).is_max('distance', '-'):
                            $ player.ap -= 1
                            $ target.use_token('convention')
                            $ target.relations(player).change('distance', '-')
                        'Передумать':
                            jump lbl_activate_ap    
                'Благодарность (contribution)' if target.has_token("contribution") and target.stance(player).value < min(1, target.relations(player).harmony()[0] - 1) and target.relations(player).is_harmony_points('supporter', 'intimate'):
                    menu:
                        'Гармонизовать позиции' if not target.relations(player).is_max('congruence', '+'):
                            $ player.ap -= 1
                            $ target.use_token('contribution')
                            $ target.relations(player).change('congruence', '+')
                        'Накалить страсти' if not target.relations(player).is_max('fervor', '+'):
                            $ player.ap -= 1
                            $ target.use_token('contribution')
                            $ target.relations(player).change('fervor', '+')      
                        'Сблизиться' if not target.relations(player).is_max('distance', '+'):
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
        txt = "Настроение: " + encolor_text(target.show_mood(), target.mood) + '{a=lb_recalc_result_glue}?{/a}'
        if stance:
            txt += " | Поза: " + str(stance) +'\n'
        txt += " | Здоровье: %s \n "%(target.vitality)
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






