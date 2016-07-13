label shd_None_template(character):
    $ d = character.description()
    '[d] TOASTED!'
    return

label shd_general_accounting(character):
    # Allways active. Calculates minor issues.
    'BATYA получает зарплату (+100 тенгэ)'
    $ game.money += 100
    if 'dates' in child.restrictions:
        $ child.eros.set_tension()
        $ child.activity.set_tension()
    if 'friends' in child.restrictions:
        $ child.communication.set_tension()
        
    return

label shd_job_supervise(action):
    $ pass
    return  
    
label shd_job_supervise_remove(act):
    # Срабатывает в случае смены расписания c supervise на другой вариант
    python:    
        for person in act.actor.job_object().special_values['slaves']:
            person.schedule.add_action('job_idle')  
    return

label shd_job_idle(action):
    $ name = action.actor.name()
    $ action.actor.add_modifier('rest', {'vitality': 4}, 1)  
    '[name] отдыхает по вечерам восстанавливая силы (vitality-фактор 4)'
    return    
    
label shd_job_study(action):
    python:
        child.skills_used.append('coding')
    'Домашка сделана. Порядочный и добрый поступок матери по отношению к нему.'
    $ mom.moral_action('lawful', 'good', target = child)  
    return    
    
label shd_job_chores(action):
    python:
        actor = action.actor
        name = actor.name()
        moral = actor.moral_action('lawful') 
        motivation = game.threshold_skillcheck(actor, 'sport', difficulty = 0, tense_needs=['amusement'], satisfy_needs=[], beneficiar=player, morality=moral, special_motivators=[], success_threshold=0)        
        if motivation[1]:
            renpy.call('subloc_chores_perform')   
        else:
            renpy.call('subloc_chores_sabotage')       
    return    

label subloc_chores_sabotage:
    "[name] саботирует работу по дому ничего не делает."

    return

label subloc_chores_perform:
    $ game.money += 10
    "[name] занимается делами по хозяйству. Тяжелый ручной труд сэкономил нам аж целых 10 тенгэ!"

    return
    
label shd_job_janitor(act):
    python:
        actor = act.actor   
        moral = actor.moral_action('lawful')
        result = game.skillcheck(actor, 'conversation', difficulty = 1, tense_needs=['amusement'], satisfy_needs=[], beneficiar=actor, morality=moral, special_motivators=[])

        if result >= 0:
            renpy.call('subloc_janitor_perform')   
        else:
            renpy.call('subloc_janitor_sabotage')       
    return    
    
label subloc_janitor_sabotage:
    'Маман саботирует подработку и ничего не зарабатывает. Зато удовлетворяет потребности в независимости и комфорте с силой 2.'  
    $ actor.comfort.satisfaction = 2
    $ actor.independence.satisfaction = 2
    $ actor.prosperity.set_tension()
    return

label subloc_janitor_perform:
    python:
        gain = result*result*10+5
        game.money += gain
        actor.skill('conversation').get_expirience(result)
        show = show_quality[result]
    'Маман [show] выкладывается на работе уборщицей. \n Заработок: [gain] тенге.'
    return
   
label shd_job_porter(action):
    python:
        actor = action.actor
        mom.moral_action('lawful', child)
        moral = actor.moral_action('lawful')
        result = game.skillcheck(actor, 'sport', difficulty = 1, tense_needs=['amusement', 'ambition'], satisfy_needs=['activity'], beneficiar=player, morality=moral, special_motivators=[])
        
        if result >= 0:
            renpy.call('subloc_porter_perform')   
        else:
            renpy.call('subloc_porter_sabotage')       
    return    

label subloc_porter_sabotage:
    'Сычуля саботирует работу грузчика, что стоит матери денег и авторитета. Это хаотичный поступок по отношению к ней. Зато Сычик удовлетворяет потребность в незавивсимости и комфорте с силой 3.'
    $ actor.comfort.satisfaction = 3
    $ actor.independence.satisfaction = 3
    $ mom.prosperity.set_tension()
    $ mom.authority.set_tension()
    $ child.moral_action('chaotic', target = mom)      
    return

label subloc_porter_perform:
    python:
        gain = result*result*10+5
        game.money += gain
        child.skill('sports').get_expirience(result)
        mom.prosperity.satisfaction = result  
        show = show_quality[result]
    'Сычуля [show] работает грузчиком себя послушным и активным. Угнетены амбиции и вообще работа скучная. \n Заработок (для мамы!): [gain] тенге.'
    return

label shd_job_whore(action):
    python:
        actor = action.actor
        mom.moral_action('evil', target = child)
        moral = character.moral_action('timid', mom)
        result = game.skillcheck(actor, 'sex', difficulty = 2, tense_needs=['eros', 'ambition'], satisfy_needs=['communication'], beneficiar=player, morality=moral, special_motivators=[])
        
        if result >= 0:
            renpy.call('subloc_whore_perform')   
        else:
            renpy.call('subloc_whore_sabotage')       
    return    

label subloc_whore_sabotage:
    'Сычуля не желает быть гей-шлюхой и игнорирует приказ злой мамки чувствуя себя независимым (2). Это ударит по авторитету и богатству мамки!'
    $ actor.independence.satisfaction = 2
    $ mom.prosperity.set_tension()
    $ mom.authority.set_tension()
    return

label subloc_whore_perform:
    python:
        gain = result*result*20+10
        game.tenge += gain
        child.skill('sex').get_expirience(result)
        mom.prosperity.satisfaction = result         
        child.moral_action('timid', target = mom)  
        show = show_quality[result]
    'Сычуля [show] работает на панели по приказу злой мамки. Это удар по его сексуальности и амбиициям, но по крайней мере это общение... (1)\n Заработок (для мамы!): [gain] тенге.'
    return
    
label shd_job_pusher(act):
    python:
        actor = act.actor   
        name = actor.name()
        moral = actor.moral_action('chaotic', 'ardent')
        result = game.skillcheck(actor, 'conversation', difficulty = 2, tense_needs=['comfort', 'wellness'], satisfy_needs=['communication'], beneficiar=player, morality=moral, special_motivators=[])

        if result >= 0:
            renpy.call('subloc_pusher_perform')   
        else:
            renpy.call('subloc_pusher_sabotage')       
    return    
    
label subloc_pusher_sabotage:
    '[name] решает не влезать в тёмные мутки. Это порядочное (1) поведение, но веществ так не намутишь...'  
    $ actor.order.satisfaction = 2
    return

label subloc_pusher_perform:
    python:
        gain = result*result*5+1
        game.drugs += gain
        actor.skill('conversation').get_expirience(result)
        show = show_quality[result]
    '[name] [show] мутит вещества - аптеку, бадягу, бухло, всё сойдёт. Напряжная и вредная для самочувствия работа, зато общение ([result]). Качество работы [result]\n Вымучено: [gain] веществ.'
    return





    
label shd_living_appartment(action):
    python:
        action.actor.comfort.satisfaction = 3
        action.actor.add_modifier('beauty_sleep', {'vitality': 2}, 1)        
        name = action.actor.name()
        '[name] живёт в апартаментах'
    return  
    
label shd_living_cot(action):
    $ action.actor.comfort.satisfaction = 1
    $ name = action.actor.name()
    '[name] спит на кушеточке'    
    return  
    
label shd_living_mat(action):
    python:
        child.comfort.set_tension()
        child.prosperity.set_tension()
        child.wellness.set_tension()    
        name = action.actor.name()
        '[name] спит на раскладушке'          
    return  
    
label shd_living_confined(action):
    python:
        child.comfort.set_tension()
        child.activity.set_tension()
        child.wellness.set_tension()
        child.amusement.set_tension()
        child.communication.set_tension()
        child.thrill.set_tension()
        action.actor.add_modifier('bad_sleep', {'vitality': -1}, 1)           
        name = action.actor.name()
        '[name] живёт в ванной'  
    return  
    
label shd_living_jailed(action):
    python:
        child.comfort.set_tension()
        child.activity.set_tension()
        child.wellness.set_tension()
        action.actor.add_modifier('bad_sleep', {'vitality': -1}, 1)           
        '[name] живёт в чулане' 
    return  

label shd_torture_check(action):
    python:
        threshold = action.actor.relations(action.special_values['beneficiar']).stability
        morality = action.actor.check_moral(action.special_values['torturer'], *action.special_values['moral_burden'])
        difficulty = game.token_difficulty(action.actor, action.special_values['token'], *action.special_values['target_tension']) 
        result = game.threshold_skillcheck(action.special_values['torturer'], action.special_values['skill'], difficulty, action.special_values['self_tension'], action.special_values['self_satisfy'], action.special_values['beneficiar'], morality, threshold)
        if result[0]:
            action.actor.add_token(action.special_values['token'])

        if result[1] > 0:
            for need in action.special_values['target_tension']:
                getattr(action.actor, need).set_tension()
    "Наказан"
    return  

label shd_pleasing_check(action):
    python:
        threshold = action.actor.relations(action.special_values['beneficiar']).stability
        morality = action.actor.check_moral(action.special_values['executor'], *action.special_values['moral_burden'])
        difficulty =  game.token_difficulty(action.actor, action.special_values['token'], *action.special_values['target_statisfy']) 
        result = game.threshold_skillcheck(action.special_values['executor'], action.special_values['skill'], difficulty, action.special_values['self_tension'], action.special_values['self_satisfy'], action.special_values['beneficiar'], morality, threshold)
        if result[0]:
            action.actor.add_token(action.special_values['token'])

        if result[1] > 0:
            for need in action.special_values['target_statisfy']:
                getattr(action.actor, need).set_satisfaction(result[1])
    "Ублажен"
    return  
    










    
label shd_dayoff_dacha(character):
    python:
        child.comfort.set_tension()
        child.amusement.set_tension()
        child.ambition.set_tension()
        child.wellness.set_tension()
        child.altruism.satisfaction = 2        
        child.activity.satisfaction = 2
        effect = child.physique * 2
    'Завтра рано вставать, а то опоздаем на поезд \n @\nПоможешь бабушке на даче \n @\nНадо огород вскопать, сорняки прополот, колорада потравить \n @\n(Ресурсы: провизия +[effect])'
    return  
    
label shd_dayoff_2ch(character):
    python:
        child.amusement.satisfaction = 2
        child.communication.satisfaction = 2       
    'Сосач \n @ \nЛамповый. Твой. (2) \n @ \nТут все твои друзья (общение +2).'
    return  

    
label shd_discipline_pavsykakiy(character):
    python:  
        game.train(child, pavsykakiy)
    'Батюшка павсикакий накатывает стопарик\n @\n "Мать уважать надо, отрок!"\n @\n Весь борщ сожрал, падла'

    return       
        
label shd_discipline_kohana(character):
    python:
        game.train(child, kohana)
    'Антоша Сычов до сих пор писает в кровать\n @\nМы это исправим дорогие телезрители\n @\nСмотрите в эту субботу\n @\n"Кохана, ми вбиваємо дітей".'

    return   

    
label shd_outfit_lame(character):
    python:
        child.authority.set_tension()
    return  
    
label shd_outfit_normal(character):
    python:
        child.prosperity.set_tension()
    return  
    
label shd_outfit_cool(character):
    python:
        child.prosperity.satisfaction = 4
    return  

        
label shd_fap_no(character):
    python:
        child.eros.set_tension()
    return  
    
label shd_fap_yes(character):
    python:
        child.eros.satisfaction = 1
    return  
    
label shd_alcohol_no(character):
    python:
        pass
    return  
    
label shd_alcohol_yes(character):
    python:
        child.general.satisfaction = 3
        child.wellness.set_tension()
    return  
    
label shd_smoke_no(character):
    python:
        pass
    return  
    
label shd_smoke_yes(character):
    python:
        child.comfort.satisfaction = 3
        child.wellness.set_tension()
    return  

label shd_weed_no(character):
    python:
        pass
    return  
    
label shd_weed_yes(character):
    python:
        
        child.wellness.set_tension()
    return  
