label shd_None_template(character):
    $ d = character.description()
    '[d] TOASTED!'
    return
    
label shd_job_homework(character):
    python:
        character.skills_used.append('coding')
    return    

label shd_job_chores(character):
    python:
        motivation = character.motivation(taboos=['submission'], needs=[('altruism', 2),('amusement', -1)])
        if motivation >= 0:
            renpy.call('subloc_chores_perform')   
        else:
            renpy.call('subloc_chores_sabotage')       
    return    

label subloc_chores_sabotage:
    'Сычуля саботирует уборку. ([motivation])\nУдовлетворяется потребность в независимости (2)'
    $ child.independence.set_shift(2)
    return

label subloc_chores_perform:
    'Сычуля убирается в доме. ([motivation])\n Нарушается табу на подчинение матери (1), удовлетворяется альтруизм (2), подавляется развлечение (-1).'
    python:
        child.altruism.set_shift(2)
        child.amusement.set_shift(-1)   
        child.taboo('submission').use(1)
    return


label shd_job_work(character):
    python:
        motivation = character.motivation(taboos=['submission'], needs=[('activity', 2),('amusement', -3)])
        if motivation >= 0:
            renpy.call('subloc_work_perform')   
        else:
            renpy.call('subloc_work_sabotage')       
    return    

label subloc_work_sabotage:
    'Сычуля саботирует работу грузчика. ([motivation])\nУдовлетворяется потребность в независимости (2)'
    $ child.independence.set_shift(2)
    return

label subloc_work_perform:
    python:
        child.altruism.set_shift(2)
        child.amusement.set_shift(-3)   
        child.taboo('submission').use(1)
        performance = child.use_skill('sport', taboos=['submission'], needs=[('activity', 2),('amusement', -3)])
        gain = performance*10
        game.tenge += gain
    'Сычуля работает грузчиком. ([motivation])\n Нарушается табу на подчинение матери (2), удовлетворяется потребность в активности (2), подавляется развлечение (-3).\n Заработок: [gain] тенге'
    return

