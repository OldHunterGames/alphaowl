label shd_None_template(character):
    $ d = character.description()
    '[d] TOASTED!'
    return

label shd_general_accounting(character):
    # Allways active. Calculates minor issues.
    'Мать получает зарплату (+10 тенгэ)'
    $ game.money += 10
    if 'dates' in child.restrictions:
        $ child.eros.set_shift(-1)
        $ child.activity.set_shift(-1)
    if 'friends' in child.restrictions:
        $ child.communication.set_shift(-2)
        
    return


label shd_job_janitor(act):
    python:
        actor = act.actor   
        moral = actor.moral_action('lawful')
        result = game.skillcheck(actor, 'communication', difficulty = 0, tense_needs=['amusement'], satisfy_needs=[], beneficiar=actor, morality=moral, special_motivators=[], success_threshold=0)

        if result >= 0:
            renpy.call('subloc_work_perform')   
        else:
            renpy.call('subloc_work_sabotage')       
    return    

label subloc_work_sabotage:
    'Сабантуй.'
  
    return

label subloc_work_perform:
    python:
        gain = result*result*10
        game.money += gain
        actor.skill('communication').get_expirience(result)
    'Качество работы = [result]\n Заработок: [gain] тенге.'
    return



label shd_discipline_atrocity(character):
    python:
        moral = character.moral_action(moral_burden, unin_target) 
        motivation = character.motivation(needs=[(self_bonus_need, 3)], beneficiar = player, morality = moral)  
        game.atrocity(actor = character, target = unin_target, token = token_to_gain, target_tense = targeted_need, skill = skill_to_use, phobias = phobias_to_use, morality = moral, name = 'Контролируемое прямое угнетение', respect_needs = ['authority', 'power'], controlled = True)
        "Наказан"
    return   
    
label shd_discipline_intercommunion(character):
    python:
        moral = character.moral_action(moral_burden, unin_target) 
        motivation = character.motivation(needs=[(self_bonus_need, 3)], beneficiar = player, morality = moral)  
        game.intercommunion(actor = character, target = unin_target, token = token_to_gain, skill = skill_to_use, morality = moral, name = 'Дисциплина')
        'Неделя дисциплины прошла.'
    return   
    
label shd_discipline_pleasing(character):
    python:
        moral = character.moral_action(moral_burden, unin_target) 
        motivation = character.motivation(needs=[(self_bonus_need, 3)], beneficiar = player, morality = moral)  
        game.pleasing(actor = character, target = unin_target, token = token_to_gain, skill = skill_to_use, target_please = targeted_need, morality = moral, name = 'Поощрение')
    return   











    
label shd_dayoff_dacha(character):
    python:
        child.comfort.set_shift(-3)
        child.amusement.set_shift(-2)
        child.ambition.set_shift(-2)
        child.wellness.set_shift(-1)
        child.altruism.set_shift(2)        
        child.activity.set_shift(2)
        child.conditions.append(('vigor', -1))
        effect = child.physique * 2
        game.res_add('provision', effect)
    'Завтра рано вставать, а то опоздаем на поезд \n @\nПоможешь бабушке на даче \n @\nНадо огород вскопать, сорняки прополот, колорада потравить \n @\n(Ресурсы: провизия +[effect])'
    return  
    
label shd_dayoff_2ch(character):
    python:
        child.amusement.set_shift(2)
        child.communication.set_shift(2)        
    'Сосач \n @ \nЛамповый. Твой. (2) \n @ \nТут все твои друзья (общение +2).'
    return  

    
label shd_social_atrocity(character):
    python:
        moral = child.moral_action(moral_burden, unin_target) 
        motivation = character.motivation(needs=[(self_bonus_need, used_force)], beneficiar = child, morality = moral)  
        game.atrocity(actor = child, target = unin_target, token = token_to_gain, target_tense = [targeted_need], power =  used_force, skill = None, phobias = [], morality = moral, name = 'Угнетение с силой N', respect_needs = ['authority', 'power'], difficulty = 0)
    return   
    
label shd_social_pleasing(character):
    python:
        moral = child.moral_action(moral_burden, unin_target) 
        motivation = character.motivation(needs=[(self_bonus_need, used_force)], beneficiar = child, morality = moral)  
        game.pleasing(actor = child, target = unin_target, token = token_to_gain, power =  used_force, skill = None, morality = moral, name = 'Удовлетворение с силой N', respect_needs = ['communication'], difficulty = 0)
    return   
    
label shd_social_skillpleasing(character):
    python:
        moral = child.moral_action(moral_burden, unin_target) 
        motivation = character.motivation(needs=[(self_bonus_need, 2)], beneficiar = child, morality = moral)  
        game.pleasing(actor = child, target = unin_target, token = token_to_gain, power =  0, skill = chosen_skill, morality = moral, name = 'Удовлетворение с силой N', respect_needs = ['communication'], difficulty = 3)
    return   
    
label shd_social_intercommunion(character):
    python:
        moral = child.moral_action(moral_burden, unin_target) 
        motivation = character.motivation(needs=[(self_bonus_need, 3)], beneficiar = child, morality = moral)  
        game.intercommunion(actor = child, target = unin_target, token = token_to_gain, power =  0, skill = used_skill, morality = moral, name = 'интеркомушен', respect_needs = ['authority', 'power'], difficulty = 3)
    return   
    
label shd_social_misery(character):
    python:
        moral = mom.moral_action('evil', used_force) 
        motivation = character.motivation(needs=[('general', -used_force)], beneficiar = mom)  
        game.suffering(actor = child, target = batya, token = 'conquest', actor_tense = [targeted_need], power =  used_force, skill = None, phobias = [], morality = moral, name = 'Наказание', respect_needs = ['authority', 'power'], difficulty = 0, beneficiar=mom)
    return   
        
label shd_mom_abuse(character):
    python:
        game.torture(target = child, power=abuse_force, needs=['communication'])
    'Мамка хуесосит Cычу. Abuse = [abuse_force]. Пылкий поступок мамки в отношении Сычи. Самооценка: [mom.selfesteem]'
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
    
label shd_discipline_hystery(character):
    python:    
        power = game.train(child)
    'Дисциплинарная эффекктивность мамкиной истерики = [power].'

    return   

    
label shd_outfit_lame(character):
    python:
        child.authority.set_shift(-3)
    return  
    
label shd_outfit_normal(character):
    python:
        child.prosperity.set_shift(-2)
    return  
    
label shd_outfit_cool(character):
    python:
        child.prosperity.set_shift(4)
    return  
    
label shd_living_appartment(character):
    python:
        child.comfort.set_shift(5)
        child.prosperity.set_shift(2)
        child.conditions.append(('vigor', 5))
    return  
    
label shd_living_cot(character):
    python:
        child.conditions.append(('vigor', 4))
    return  
    
label shd_living_mat(character):
    python:
        child.comfort.set_shift(-2)
        child.prosperity.set_shift(-1)
        child.wellness.set_shift(-1)
        child.conditions.append(('vigor', 2))
    return  
    
label shd_living_confined(character):
    python:
        child.comfort.set_shift(-3)
        child.activity.set_shift(-3)
        child.wellness.set_shift(-2)
        child.conditions.append(('vigor', -1))
    return  
    
label shd_living_jailed(character):
    python:
        child.comfort.set_shift(-5)
        child.activity.set_shift(-4)
        child.wellness.set_shift(-3)
    return  
    
label shd_fap_no(character):
    python:
        child.eros.set_shift(-1)
    return  
    
label shd_fap_yes(character):
    python:
        child.eros.set_shift(1)
    return  
    
label shd_alcohol_no(character):
    python:
        pass
    return  
    
label shd_alcohol_yes(character):
    python:
        child.general.set_shift(3)
        child.wellness.set_shift(-1)
    return  
    
label shd_smoke_no(character):
    python:
        pass
    return  
    
label shd_smoke_yes(character):
    python:
        child.comfort.set_shift(3)
        child.wellness.set_shift(-1)
    return  

label shd_weed_no(character):
    python:
        pass
    return  
    
label shd_weed_yes(character):
    python:
        
        child.wellness.set_shift(-2)
    return  


label shd_job_idle(character):
    python:
        child.conditions.append(('vigor', 3))
        
    return    
    
label shd_job_study(character):
    python:
        character.skills_used.append('coding')
    'Домашка сделана. Порядочный и добрый поступок матери. Порядочный и кроткий поступок Сычи.'
    $ mom.moral_action('lawful', 'good', target = child)       
    $ child.moral_action('lawful', 'timid', target = mom)    
    return    
    
label shd_job_chores(character):
    python:
        moral = character.moral_action('lawful') 
        motivation = character.motivation(needs=[('altruism', 2),('amusement', -1), ('authority', -1)], beneficiar = mom, morality = moral)        
        if motivation >= 0:
            renpy.call('subloc_chores_perform')   
        else:
            renpy.call('subloc_chores_sabotage')       
    return    

label subloc_chores_sabotage:
    'Сычуля саботирует уборку чувствуя себя свободным и могучим. ([moral])\nУдовлетворяется потребность в независимости (4) \n Авторитет мамки страдает (-3)'
    $ child.independence.set_shift(4)
    $ mom.authority.set_shift(-3)    
    $ child.moral_action('chaotic', 'evil', target = mom)     
    return

label subloc_chores_perform:
    'Сычуля убирается в доме чувствуя себя правильным и хорошим. ([moral])\n Нарушается табу на подчинение матери (1), удовлетворяется альтруизм (2), подавляется развлечение (-1), усталость. Порядочный поступок матери.'
    $ child.drain_vigor()
    $ mom.moral_action('lawful', target = child)   
    $ child.moral_action('lawful', 'good', target = mom)         
    return
   
label shd_job_work(character):
    python:
        mom.moral_action('lawful', child)
        moral = character.moral_action('lawful')
        motivation = character.motivation('sport', [('authority', -2), ('activity', 2),('amusement', -3)], character, moral) 
        result = game.skillcheck(character, 'sport', motivation, moral, 'разгрузка вагонов')
        if result >= 0:
            renpy.call('subloc_work_perform')   
        else:
            renpy.call('subloc_work_sabotage')       
    return    

label subloc_work_sabotage:
    'Сычуля саботирует работу грузчика.'
    $ child.independence.set_shift(3)
    $ mom.authority.set_shift(-2)
    $ child.moral_action('chaotic', target = mom)      
    return

label subloc_work_perform:
    python:
        gain = result*result*10
        game.money += gain
        child.skill('sports').get_expirience(result)
        mom.prosperity.set_shift(result+1)     
        mom.authority.set_shift(4)        
        mom.moral_action('lawful', 'ardent', target = child)       
        child.moral_action('lawful', target = mom)          
    'Сычуля работает грузчиком себя правильным. ([result])\n Заработок (для мамы!): [gain] тенге.'
    return


label shd_job_whore(character):
    python:
        mom.moral_action('evil', child)
        moral = character.moral_action('timid', mom)
        motivation = character.motivation('sex', [('eros', -4), ('communication', 2),('ambition', -4), ('authority', -2)], character, moral) 
        result = game.skillcheck(character, 'sex', motivation, moral, 'разгрузка вагонов')        
        if result >= 0:
            renpy.call('subloc_whore_perform')   
        else:
            renpy.call('subloc_whore_sabotage')       
    return    

label subloc_whore_sabotage:
    'Сычуля саботирует работу на панели.'
    $ child.independence.set_shift(2)
    $ mom.authority.set_shift(-1)
    return

label subloc_whore_perform:
    python:
        gain = result*result*20
        game.tenge += gain
        child.skill('sex').get_expirience(result)
        mom.power.set_shift(5)           
        mom.prosperity.set_shift(result+2)    
        mom.moral_action('evil', 'lawful', 'ardent', target = child)
        child.moral_action('timid', target = mom)            
    'Сычуля работает на панели. ([result])\n Заработок (для мамы!): [gain] тенге.'
    return
