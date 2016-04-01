init -1 python:
    register_action('homework', 'lbl_make_homework')
    
label shd_None_test:
    'TOASTED!'
    return
    
label shd_job_homework(character):
    python:
        character.used_skill.append('coding')
        character.skills_used.append('coding')
    return    
    