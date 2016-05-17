### ЗАВЕРШАЕМ ИГРОВУЮ СЕССИЮ

label game_over:
    'Ох, Сыночка-Корзиночка, на кого же ты меня покинул. \n @\n Не уберегла кровиночку. \n @\n Оставил мать сиротой на старости лет!'    
    show text "{b}GAME OVER{/b}" at truecenter
    with dissolve
    pause 1
    hide text
    with dissolve
    $ renpy.full_restart()
    return

label win_study:
    'Успешная концовка: "АСПИРАНТУРА".'    
    show text "{b}YOU WIN{/b}" at truecenter
    with dissolve
    pause 1
    hide text
    with dissolve
    $ renpy.full_restart()
    return
    
label win_wealth:
    'Успешная концовка: "БОХАТО ЖИВЁМ".'    
    show text "{b}YOU WIN{/b}" at truecenter
    with dissolve
    pause 1
    hide text
    with dissolve
    $ renpy.full_restart()
    return    