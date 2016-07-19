label shd_None_template(character):
    $ d = character.description()
    '[d] TOASTED!'
    return

label shd_general_accounting(character):
    # Allways active. Calculates minor issues.
    if player = child:
        if salary_timer == 0:
            'BATYA получает зарплату (+250 тенгэ). Следующая зарплата через месяц (4 недели).'
            $ game.money += 250
            $ salary_timer = 3
        else:
            $ salary_timer -= 1
    else:
        if game.money < 100000:
            $ game.money = 10000
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
    # '[name] отдыхает по вечерам восстанавливая силы (vitality-фактор 4)'
    return    
    
label shd_job_study(action):
    python:
        child.skills_used.append('coding')
        actor.add_condition('merit') 
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
    $ actor.add_condition('sin')
    "[name] саботирует работу по дому ничего не делает."

    return

label subloc_chores_perform:
    $ actor = action.actor
    $ name = actor.name()    
    $ game.money += 10
    $ actor.add_condition('merit') 
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
        gain = result*result*5+5
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
    $ actor.add_condition('sin')
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
        actor.add_condition('merit') 
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
    $ actor.add_condition('sin')
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
        actor.add_condition('merit') 
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
        actor.add_condition('merit')        
    '[name] [show] мутит вещества - аптеку, бадягу, бухло, всё сойдёт. Напряжная и вредная для самочувствия работа, зато общение ([result]). Качество работы [result]\n Вымучено: [gain] веществ.'
    return

label shd_None_alcohol(action):
    python:
        action.actor.general.satisfaction = 5
    return  

label shd_None_smoke(action):
    python:
        action.actor.comfort.satisfaction = 5
    return  
    
label shd_None_weed(action):
    python:        
        action.actor.purpose.satisfaction = 5
    return  
       
label shd_fap_no(character):
    python:
        child.eros.set_tension()
    return  
    
label shd_fap_yes(character):
    python:
        child.eros.satisfaction = 1
    return  
    
label shd_money_wealth(action):
    python:        
        if action.special_values['num'] >= 0:
            action.actor.prosperity.satisfaction = action.special_values['num']
        else:
            child.prosperity.set_tension()
    return  

label shd_living_appartment(action):
    python:
        action.actor.comfort.satisfaction = 3
        action.actor.add_modifier('beauty_sleep', {'vitality': 2}, 1)        
        name = action.actor.name()
    # '[name] живёт в апартаментах'
    return  
    
label shd_living_cot(action):
    $ action.actor.comfort.satisfaction = 1
    $ name = action.actor.name()
    '[name] спит на кушеточке'    
    return  
    
label shd_living_mat(action):
    python:
        action.actor.comfort.set_tension()
        action.actor.prosperity.set_tension()
        action.actor.wellness.set_tension()    
        name = action.actor.name()
    # '[name] спит на раскладушке'          
    return  
    
label shd_living_confined(action):
    python:
        action.actor.comfort.set_tension()
        action.actor.activity.set_tension()
        action.actor.wellness.set_tension()
        action.actor.amusement.set_tension()
        action.actor.communication.set_tension()
        action.actor.thrill.set_tension()
        action.actor.add_modifier('bad_sleep', {'vitality': -1}, 1)           
        name = action.actor.name()
    #'[name] живёт в ванной'  
    return  
    
label shd_living_jailed(action):
    python:
        action.actor.comfort.set_tension()
        action.actor.activity.set_tension()
        action.actor.wellness.set_tension()
        action.actor.add_modifier('bad_sleep', {'vitality': -1}, 1)           
    #'[name] живёт в чулане' 
    return  

label shd_job_torture(action):
    python:
        failed = False
        if is_needs_used(action.actor, action.special_values['token'], action.special_values['target_tension']):
            failed = True
    if failed:
        'Это пройденный этап'
        return
    python:
        threshold = action.actor.relations(action.special_values['beneficiar']).stability
        morality = action.actor.check_moral(action.special_values['torturer'], *action.special_values['moral_burden'])
        difficulty = game.token_difficulty(action.actor, action.special_values['token'], *action.special_values['target_tension']) 
        result = game.threshold_skillcheck(action.special_values['torturer'], action.special_values['skill'], difficulty, action.special_values['self_tension'], action.special_values['self_satisfy'], action.special_values['beneficiar'], morality, threshold)
        if result[0]:
            action.actor.add_token(action.special_values['token'])
            remember_needs(action.actor, action.special_values['token'], action.special_values['target_tension'])
        else:
            action.actor.add_token('antagonism')
        if result[1] > 0:
            for need in action.special_values['target_tension']:
                getattr(action.actor, need).set_tension()
    return  

label shd_job_pleasing(action):
    python:
        failed = False
        if is_needs_used(action.actor, action.special_values['token'], action.special_values['target_statisfy']):
            failed = True
    if failed:
        'Это пройденный этап'
        return
    python:
        threshold = action.actor.relations(action.special_values['beneficiar']).stability
        morality = action.actor.check_moral(action.special_values['executor'], *action.special_values['moral_burden'])
        difficulty =  game.token_difficulty(action.actor, action.special_values['token'], *action.special_values['target_statisfy']) 
        result = game.threshold_skillcheck(action.special_values['executor'], action.special_values['skill'], difficulty, action.special_values['self_tension'], action.special_values['self_satisfy'], action.special_values['beneficiar'], morality, threshold)
        if result[0]:
            action.actor.add_token(action.special_values['token'])
            remember_needs(action.actor, action.special_values['token'], action.special_values['target_tension'])
        else:
            action.actor.add_token('antagonism')
        if result[1] > 0:
            for need in action.special_values['target_statisfy']:
                getattr(action.actor, need).set_satisfaction(result[1])
    return  


label shd_job_slavepleasing(action):
    python:
        failed = False
        if is_needs_used(action.actor.master, action.special_values['token'], action.special_values['target_statisfy']):
            failed = True
    if failed:
        'Это пройденный этап'
        return
    python:
        master = action.actor.master
        threshold = action.actor.relations(master).stability
        morality = action.actor.check_moral(master, *action.special_values['moral_burden'])
        difficulty =  game.token_difficulty(master, action.special_values['token'], *action.special_values['target_statisfy']) 
        result = game.threshold_skillcheck(action.actor, action.special_values['skill'], difficulty, action.special_values['self_tension'], action.special_values['self_satisfy'], action.special_values['beneficiar'], morality, threshold)
        if result[0]:
            master.add_token(action.special_values['token'])
            remember_needs(action.actor, action.special_values['token'], action.special_values['target_tension'])
        else:
            master.actor.add_token('antagonism')
        if result[1] > 0:
            for need in action.special_values['target_statisfy']:
                getattr(master, need).set_satisfaction(result[1])
    return  


label shd_job_suffer(action):
    python:
        failed = False
        if is_needs_used(action.actor.master, action.special_values['token'], action.special_values['self_tension']):
            failed = True
    if failed:
        'Это пройденный этап'
        return
    python:
        master = action.actor.master
        threshold = action.actor.relations(master).stability
        morality = master.moral_action(action.actor, *action.special_values['moral_burden'])
        difficulty =  game.token_difficulty(master, action.special_values['token'], *action.special_values['self_tension']) 
        result = game.threshold_skillcheck(action.actor, action.special_values['skill'], difficulty, action.special_values['self_tension'], [], action.special_values['beneficiar'], 0, threshold)
        if result[0]:
            master.add_token(action.special_values['token'])
            remember_needs(master, action.special_values['token'], action.special_values['self_tension'])
        else:
            master.add_token('antagonism')
        if result[1] > 0:
            for need in action.special_values['master_tension']:
                getattr(master, need).set_tension()
            for need in action.special_values['master_satisfy']:
                getattr(master, need).set_satisfaction(result[1])
    return 
    
label shd_job_pavsykakiy(action):
    'Батюшка павсикакий накатывает стопарик\n @\n "Мать уважать надо, отрок!"\n @\n "Целуй крест! Да ты же хуже грешника-рукоблуда!"'
    python:
        churched = True
        if action.actor.relations(player).stability < 4:
            action.actor.add_token('convention')
        else:
            action.actor.add_token('antagonism')
    return       
        
label shd_job_kohana(action):
    'Антоша Сычов до сих пор писает в кровать\n @\nМы это исправим дорогие телезрители\n @\nСмотрите в эту субботу\n @\n"Кохана, ми вбиваємо дітей".'
    python:
        kohaned = True
        if action.actor.relations(player).stability < 5:
            action.actor.add_token('convention')
        else:
            action.actor.add_token('antagonism')    
    return      

label shd_minor_nap(action):
    python:
        action.actor.comfort.satisfaction = 1
        action.actor.add_modifier('beauty_sleep', {'vitality': 1}, 1)       
    # 'Легкий отдых. Фактор здоровья 1'

    return

label shd_minor_fun(action):
    python:
        action.actor.amusement.satisfaction = 4
        action.actor.independence.satisfaction = 1
        action.actor.general.satisfaction = 1
    return

label shd_minor_sport(action):
    python:
        action.actor.activity.satisfaction = 4
        action.actor.skills_used.append('sport')
    return

label shd_minor_chat(action):
    python:
        action.actor.communication.satisfaction = 4
        action.actor.skills_used.append('conversation')
    return

label shd_minor_dacha(action):
    python:
        name = action.actor.name()
        action.actor.amusement.set_tension()
        action.actor.wellness.set_tension()
        action.actor.independence.set_tension()        
        action.actor.thrill.set_tension()   
        nyam = action.actor.physique + action.actor.mood + action.actor.vitality
        game.provision += nyam
    '[name] проводит все выходные на даче, словно негр на плантациях. Скучно, всё тело болит и никакой свободы или новизны. Зато своё, с огрода, витамины (продукты +[nyam]) '
    return
    
label shd_job_sport(action):
    python:
        actor = action.actor
        name = actor.name()
        motivation = game.threshold_skillcheck(actor, 'sport', difficulty = 0, tense_needs=['comfort'], satisfy_needs=['activity'], beneficiar=player, success_threshold=0)        
    if motivation[0]:
        $ actor.skill('sport').training = True
        $ actor.ambition.satisfaction = action.actor.physique  
        'Соблюдает дня режим - дЖым ([name])! Получены базовые знания о ЗОЖ, амбиции удовлетворены.' 
    else:
        '[name] не хочет ничему учиться...'             
  
    return

label shd_job_coding(action):
    python:
        actor = action.actor
        name = actor.name()
        motivation = game.threshold_skillcheck(actor, 'coding', difficulty = 0, tense_needs=['amusement'], satisfy_needs=[], beneficiar=player, success_threshold=0)        
    if motivation[0]:
        $ actor.skill('coding').training = True
        $ actor.ambition.satisfaction = action.actor.mind  
        '"RenPy для пускающих слюни дегенератов". [name] получает базовый навык программирования, амбиции удовлетворены.'
    else:
        '[name] не хочет ничему учиться...'             
  
    return

label shd_job_conversation(action):
    python:
        actor = action.actor
        name = actor.name()
        motivation = game.threshold_skillcheck(actor, 'conversation', difficulty = 0, tense_needs=['authority'], satisfy_needs=['communication'], beneficiar=player, success_threshold=0)        
    if motivation[0]:
        $ actor.skill('conversation').training = True
        $ actor.ambition.satisfaction = action.actor.spirit  
        'Чтобы справиться с Ерохой, надо мыслить как Ероха! [name] получает базовый навык социоблядства, амбиции удовлетворены.'
    else:
        '[name] не хочет ничему учиться...'             
  
    return

label shd_job_sex(action):
    python:
        actor = action.actor
        name = actor.name()
        motivation = game.threshold_skillcheck(actor, 'sex', difficulty = 0, tense_needs=['wellness'], satisfy_needs=['eros'], beneficiar=player, success_threshold=0)        
    if motivation[0]:
        $ actor.skill('sex').training = True
        $ actor.ambition.satisfaction = action.actor.sensitivity  
        'Теперь [name] знает как долго не кончать! Получена базовая сексуальная грамотность, амбиции удовлетворены.'
    else:
        '[name] не хочет ничему учиться...'             
  
    return

label shd_job_impress(action):
    $ mom.add_token(action.special_values['token'])
    $ txt = action.special_values['txt']
    "[txt]"
    return

