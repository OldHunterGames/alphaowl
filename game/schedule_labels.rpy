label shd_None_template(character):
    $ d = character.description()
    '[d] TOASTED!'
    return

    
label shd_batya_batya(character):
    python:
        game.torture(child, power=3, taboos=['pain'])
        game.train(child, power=3)
        mom.moral_action(child, morality='evil')
    'BATYA гандошит Cычу. Pain = [batya_force]. Злой постпок мамки в отношении Сычи. Самооценка: [mom.selfesteem]'
    return   

    
label shd_discipline_pavsykakiy(character):
    python:
        game.train(child, power=3)
    'Батюшка павсикакий накатывает стопарик\n @\n "Мать уважать надо, отрок!"\n @\n Весь борщ сожрал, падла'

    return   
    
        
label shd_discipline_kohana(character):
    python:
        game.train(child, power=5)
    'Славик Сычов до сих пор писает в кровать\n @\nМы всё исправим дорогие телезрители\n @\nСмотрите в эту субботу\n @\n"Кохана, ми вбиваємо дітей".'

    return   
    
label shd_discipline_hystery(character):
    python:
        game.train(child, power=mom_power)
    'Дисциплинарная эффекктивность мамкиной истерики [mom_power].'

    return   
    
label shd_job_homework(character):
    python:
        character.skills_used.append('coding')
    return    

label shd_job_chores(character):
    python:
        result = character.skillcheck(taboos=[('submission', 1)], needs=[('altruism', 2),('amusement', -1)])
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
    'Сычуля убирается в доме. ([result])\n Нарушается табу на подчинение матери (1), удовлетворяется альтруизм (2), подавляется развлечение (-1).'
    return


label shd_job_work(character):
    python:
        result = character.skillcheck('sport', taboos=[('submission', 2)], needs=[('activity', 2),('amusement', -3)])
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
    'Сычуля работает грузчиком. ([result])\n Нарушается табу на подчинение матери (2), удовлетворяется потребность в активности (2), подавляется развлечение (-3).\n Заработок: [gain] тенге'
    return


label shd_job_whore(character):
    python:
        result = character.skillcheck('sex', taboos=[('sexplotation', 3)], needs=[('communication', 2),('ambition', -4),('authority', -2)])
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
    'Сычуля работает на панели. ([result])\n Нарушается табу на сексуальную эксплуатацию (2), удовлетворяется потребность в общении (2), подавляются амбиции (-4) и авторитет (-2).\n Заработок: [gain] тенге'
    return
