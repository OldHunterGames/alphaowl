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
        result = character.skillcheck(taboos=[('submission', 1)], needs=[('activity', 2),('amusement', -3)])
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

