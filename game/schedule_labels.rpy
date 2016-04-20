label shd_None_template(character):
    $ d = character.description()
    '[d] TOASTED!'
    return

label shd_general_accounting(character):
    # Allways active. Calculates minor issues.
    'Мать получает зарплату (+50 тенгэ)'
    $ game.tenge += 50
    if 'dates' in child.restrictions:
        $ child.eros.set_shift(-1)
        $ child.activity.set_shift(-1)
    if 'friends' in child.restrictions:
        $ child.communication.set_shift(-2)
        
    return
    
label shd_help_mom(character):
    'Мамин помощник'
    python:
        moral = child.moral_action('good', target = mom)
        result = child.skillcheck(help_skill, moral = moral, needs=[('ambition', -3),('altruism', 2)])     
        game.gratifaction(target = mom, power=result, needs = [need_helped])
    'Качество подлизывания = [result]'
    return   
    
label shd_popo_bol(character):
    python:
        game.remorse(target = mom, power=butthurt_force)
        child.wellness.set_shift(-butthurt_force)
        mom.moral_action('evil', target = child)
    'BATYA гандошит Cычу. Pain = [butthurt_force]. Злой постпок мамки в отношении Сычи. Самооценка матери: [mom.selfesteem]'
    return   
    
label shd_batya_batya(character):
    python:
        game.torture(target = child, power=batya_force, taboos=['pain'])
        child.wellness.set_shift(-batya_force)
        mom.moral_action('evil', target = child)
    'BATYA гандошит Cычу. Pain = [batya_force]. Злой постпок мамки в отношении Сычи. Самооценка: [mom.selfesteem]'
    return   
    
label shd_mom_abuse(character):
    python:
        game.torture(target = child, power=abuse_force, taboos=['abuse'])
        child.ambition.set_shift(-abuse_force)
        mom.moral_action('ardent', target = child)
    'Мамка хуесосит Cычу. Abuse = [abuse_force]. Пылкий постпок мамки в отношении Сычи. Самооценка: [mom.selfesteem]'
    return   
    
label shd_discipline_pavsykakiy(character):
    python:
        mom.moral_action('lawful', target = child)         
        game.train(child, power=3)
    'Батюшка павсикакий накатывает стопарик\n @\n "Мать уважать надо, отрок!"\n @\n Весь борщ сожрал, падла'

    return   
    
        
label shd_discipline_kohana(character):
    python:
        game.train(child, power=5)
    'Антоша Сычов до сих пор писает в кровать\n @\nМы всё исправим дорогие телезрители\n @\nСмотрите в эту субботу\n @\n"Кохана, ми вбиваємо дітей".'

    return   
    
label shd_discipline_hystery(character):
    python:
        mom.moral_action('ardent', target = child)        
        game.train(child, power=mom_power)
    'Дисциплинарная эффекктивность мамкиной истерики = [mom_power].'

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
    'Нофапофон'
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
    'Домашка сделана.'
        
    return    
    
label shd_job_chores(character):
    python:
        mom.moral_action('lawful', target = child)        
        result = character.action(taboos=[('submission', 1)], needs=[('altruism', 2),('amusement', -1)], forced = True)
        if result >= 0:
            renpy.call('subloc_chores_perform')   
        else:
            renpy.call('subloc_chores_sabotage')       
    return    

label subloc_chores_sabotage:
    'Сычуля саботирует уборку. ([result])\nУдовлетворяется потребность в независимости (2)'
    $ child.independence.set_shift(2)
    return

label subloc_chores_perform:
    'Сычуля убирается в доме. ([result])\n Нарушается табу на подчинение матери (1), удовлетворяется альтруизм (2), подавляется развлечение (-1), усталость.'
    $ child.drain_vigor()
    return

label shd_learn_good(character):
    "ВРЕМЯ ИДТИ В ИНСТИТУТ \n @ \n ИНСТИТУТ САМ В СЕБЯ НЕ ПОЙДЁТ"
    python:
        child.moral_action('lawful', target = mom)
        result = child.skillcheck('coding', needs=[('activity', -2),('amusement', -3)])
    if result >= 0:
        $ game.duty(target = mom, power = result)   
        '\n @ \nИ неплохо учишься! \n @ \nКак маме обещал (confidence = [result])'
    else:
        '\n @ \nИ ОПЯТЬ НИЗАЧОТ! \n @ \nА ВЕДЬ МАМЕ ОБЕЩАЛ...)' 
        $ child.independence.set_shift(2)
            
    return    
    

label shd_job_work(character):
    python:
        mom.moral_action('lawful', target = child)
        result = character.skillcheck('sport', taboos=[('submission', 2)], needs=[('activity', 2),('amusement', -3)], forced = True)
        if result >= 0:
            renpy.call('subloc_work_perform')   
        else:
            renpy.call('subloc_work_sabotage')       
    return    

label subloc_work_sabotage:
    'Сычуля саботирует работу грузчика. ([result])\nУдовлетворяется потребность в независимости (2)'
    $ child.independence.set_shift(2)
    return

label subloc_work_perform:
    python:
        gain = result*10
        game.tenge += gain
        child.skill('sports').expert(result)
    'Сычуля работает грузчиком. ([result])\n Нарушается табу на подчинение матери (2), удовлетворяется потребность в активности (2), подавляется развлечение (-3).\n Заработок: [gain] тенге'
    return


label shd_job_whore(character):
    python:
        mom.moral_action('evil', target = child)
        result = character.skillcheck('sex', taboos=[('sexplotation', 4)], needs=[('communication', 2),('ambition', -4),('authority', -2)], forced = True)
        if result >= 0:
            renpy.call('subloc_whore_perform')   
        else:
            renpy.call('subloc_whore_sabotage')       
    return    

label subloc_whore_sabotage:
    'Сычуля саботирует работу на панели. ([result])\nУдовлетворяется потребность в независимости (1)'
    $ child.independence.set_shift(2)
    return

label subloc_whore_perform:
    python:
        gain = result*20
        game.tenge += gain
        child.skill('sex').expert(result)
    'Сычуля работает на панели. ([result])\n Нарушается табу на сексуальную эксплуатацию (2), удовлетворяется потребность в общении (2), подавляются амбиции (-4) и авторитет (-2).\n Заработок: [gain] тенге'
    return
