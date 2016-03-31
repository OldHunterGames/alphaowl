init -1 python:
    register_action('homework', 'lbl_make_homework')
label lbl_make_homework(character=player):
    $ character.skill('coding').set_focus()
    $ character.activity.set_shift(1)
    return