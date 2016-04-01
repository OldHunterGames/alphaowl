label shd_None_test(character):
    $ d = character.description()
    '[d] TOASTED!'
    return
    
label shd_job_homework(character):
    python:
        character.skills_used.append('coding')
    return    
    