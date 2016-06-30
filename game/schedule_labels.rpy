label shd_None_template(character):
    $ d = character.description()
    '[d] TOASTED!'
    return

label shd_general_accounting(character):
    # Allways active. Calculates minor issues.
    if game.player == mom:
        'Мать получает зарплату (+10 тенгэ)'
        $ game.tenge += 10
    if 'dates' in child.restrictions:
        $ child.eros.set_shift(-1)
        $ child.activity.set_shift(-1)
    if 'friends' in child.restrictions:
        $ child.communication.set_shift(-2)
        
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

label shd_help_mom(character):
    'Мамин помощник'
    python:  
        result = game.gratifaction(help_skill, needs = [need_helped])       
    'Качество подлизывания = [result]'
    return   
    
label shd_popo_bol(character):
    python:
        game.remorse(power=butthurt_force, needs=['common'])
    'BATYA гандошит Cычу. Pain = [butthurt_force]. Злой поступок мамки в отношении Сычи. Самооценка матери: [mom.selfesteem]'
    return   
    
label shd_batya_batya(character):
    python:
        game.torture(target = child, power=batya_force, needs=['comfort'])
    'BATYA гандошит Cычу. Pain = [batya_force]. Злой поступок мамки в отношении Сычи. Самооценка: [mom.selfesteem]'
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
        moral = character.moral_action('ardent') 
        motivation = character.motivation(needs=[('altruism', 2),('amusement', -1), ('authority', -1)], beneficiar = mom, moral = moral)        
        if motivation >= 0:
            renpy.call('subloc_chores_perform')   
        else:
            renpy.call('subloc_chores_sabotage')       
    return    

label subloc_chores_sabotage:
    'Сычуля саботирует уборку чувствуя себя свободным и могучим. ([result])\nУдовлетворяется потребность в независимости (4) \n Авторитет мамки страдает (-3)'
    $ child.independence.set_shift(4)
    $ mom.authority.set_shift(-3)    
    $ child.moral_action('chaotic', 'evil', target = mom)     
    return

label subloc_chores_perform:
    'Сычуля убирается в доме чувствуя себя правильным и хорошим. ([result])\n Нарушается табу на подчинение матери (1), удовлетворяется альтруизм (2), подавляется развлечение (-1), усталость. Порядочный поступок матери.'
    $ child.drain_vigor()
    $ mom.moral_action('lawful', target = child)   
    $ child.moral_action('lawful', 'good', target = mom)         
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
        moral = character.check_moral('lawful', target = mom)
        result = character.skillcheck('sport', taboos=[('submission', 2)], needs=[('activity', 2),('amusement', -3)], forced = True, moral=moral)
        if result >= 0:
            renpy.call('subloc_work_perform')   
        else:
            renpy.call('subloc_work_sabotage')       
    return    

label subloc_work_sabotage:
    'Сычуля саботирует работу грузчика чувствуя свободу. ([result])\nУдовлетворяется потребность в независимости (3) \n Авторитет мамки страдает (-2)'
    $ child.independence.set_shift(3)
    $ mom.authority.set_shift(-2)
    $ child.moral_action('chaotic', target = mom)      
    return

label subloc_work_perform:
    python:
        gain = result*result*10
        game.tenge += gain
        child.skill('sports').get_expirience(result)
        mom.prosperity.set_shift(result+1)     
        mom.authority.set_shift(4)        
        mom.moral_action('lawful', 'ardent', target = child)       
        child.moral_action('lawful', target = mom)          
    'Сычуля работает грузчиком чувствуя себя правильным. ([result])\n Нарушается табу на подчинение матери (2), удовлетворяется потребность в активности (2), подавляется развлечение (-3).\n Заработок (для мамы!): [gain] тенге. Мамка чувствует свою власть, порядочный и энергичный поступок.'
    return


label shd_job_whore(character):
    python:
        moral = character.check_moral('timid', target=mom)
        mom.moral_action('evil', target = child)
        result = character.skillcheck('sex', taboos=[('sexplotation', 4)], needs=[('communication', 2),('ambition', -4),('authority', -2)], forced = True, moral=moral)
        if result >= 0:
            renpy.call('subloc_whore_perform')   
        else:
            renpy.call('subloc_whore_sabotage')       
    return    

label subloc_whore_sabotage:
    'Сычуля саботирует работу на панели. ([result])\nУдовлетворяется потребность в независимости (1) \n Авторитет мамки страдает (-1)'
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
    'Сычуля работает на панели, чувствуя себя timid. ([result])\n Нарушается табу на сексуальную эксплуатацию (2), удовлетворяется потребность в общении (2), подавляются амбиции (-4) и авторитет (-2).\n Заработок (для мамы!): [gain] тенге. Мамка чувствует своё могущество, энергию и власть, злой поступок.'
    return
