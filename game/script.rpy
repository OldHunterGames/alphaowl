﻿init -10 python:
    sys.path.append(renpy.loader.transfn("scrypts"))
    from obj_character import *
    from owl_engine import *
    from events import *
    from schedule import *

init python:
    churched = False
    kohaned = False
    salary_timer = 0
    recalc_result = []
    renpy.block_rollback()
    game = Engine()
    child = game.child
    mother = game.mother
    child.master = mother
    register_actions()
    mom = game.mother
    mom.enslave(child)    
    mom.firstname = u"Маман"
    mom.surname = u"Сычова"    
    mom.alignment.activity = "ardent"
    mom.alignment.orderliness = "lawful"    
    mom.alignment.morality = 'evil'
    check_results = ['{color=#f00}failure{/color}', '{color=#ff00f3}marginal{/color}', '{color=#b700ff}normal{/color}',
                    '{color=#2600ff}fine{/color}', '{color=#2cab2c}exceptional{/color}', '{color=#dff54f}perfect{/color}']
    communication = '?'
    game.res_add_consumption('mom_food', 'provision', mom.get_food_consumption, None)
    mom.schedule.add_action('living_appartment')
    game.res_add_consumption("mom_rent", 'money', 25, time=None)
    mom.restrictions.append('alcohol')
    mom.restrictions.append('tobacco')
    mom.restrictions.append('weed')   
    mom.schedule.add_action('fap_yes')
    mom.skill('conversation').profession()
    mom.relations(child)    
    mom.add_feature('female')
    mom.add_feature('mature')
    mother.enslave(child)
    mom.stance(child).value = -1
    mom.ration['amount'] = "unlimited"   
    mom.ration['food_type'] = "cousine"
    mom.accommodation = "appartment"
    mom.schedule.add_action('living_appartment', False)
    mom.schedule.add_action('general_accounting', False)
    mom.schedule.add_action('money_wealth', False, special_values={'num': -1}) 
    mom.schedule.add_action('minor_nap', False)
    mom.schedule.add_action('job_idle', False) 
    
    #BATYA
    batya = Person()
    game.batya = batya
    batya.add_feature('male')
    batya.add_feature('mature')
    batya.firstname = u"BATYA"
    batya.surname = u"Сычов"    
    batya.alignment.orderliness = "conformal"
    batya.alignment.activity = "reasonable"
    batya.alignment.morality = "selfish" 
    batya.skill('sport').profession()
    batya.stance(child).value = 0
    batya.stance(mom).value = 1
    batya.ration['food_type'] = "cousine" 
    game.res_add_consumption('batya_food', 'provision', batya.get_food_consumption, None)
    batya.accommodation = "appartment"
    batya.schedule.add_action('living_appartment', False)
    game.res_add_consumption("batya_rent", 'money', 25, time=None)
    batya.restrictions.append('alcohol')
    batya.restrictions.append('tobacco')
    batya.restrictions.append('weed')
    batya.schedule.add_action('fap_yes')
    batya.schedule.add_action('money_wealth', False, special_values={'num': -1}) 
    batya.schedule.add_action('minor_nap', False)
    batya.schedule.add_action('job_idle', False) 
    
    #ЕНОТОВА
    eot = Person()
    eot.add_feature('female')
    eot.add_feature('junior')     
    eot.alignment.activity = "timid"
    eot.alignment.orderliness = "lawful"
    eot.alignment.morality = "good"
    eot.skill('conversation').talent = True
    eot.skill('conversation').profession()    
    eot.skill('coding').training = True
    # eot.stance(child).value = 0    
    eot.firstname = u"Наденька"
    eot.surname = u"Енотова"        

    #ЕРОХИН
    erokhin = Person()
    erokhin.add_feature('male')
    erokhin.add_feature('adolescent')    
    erokhin.alignment.activity = "ardent"
    erokhin.skill('sports').talent = True
    erokhin.skill('sports').profession()        
    erokhin.skill('conversation').training = True
    # erokhin.stance(child).value = -1
    erokhin.firstname = u"Алекс"
    erokhin.surname = u"Ерохин"     
    
    #АШОТ
    ashot = Person()
    ashot.add_feature('male')
    ashot.add_feature('mature')    
    ashot.alignment.activity = "ardent"
    ashot.alignment.orderliness = "chaotic"
    ashot.alignment.morality = "evil"
    ashot.skill('sex').talent = True
    ashot.skill('sex').profession()     
    ashot.skill('conversation').training = True
    # ashot.stance(child).value = 0     
    ashot.firstname = u"Ашот"
    ashot.surname = u"Мудлаев"     
    
    #СВЯЩЕННИК
    pavsykakiy = Person()
    pavsykakiy.skill('leadership').expert()  
    # pavsykakiy.stance(child).value = 0 
    pavsykakiy.firstname = u"Павсикакий"
    pavsykakiy.surname = u"Святомудин"      
    
    #ТЕЛЕВЕДУЩИЙ
    kohana = Person()
    kohana.skill('leadership').profession()
    kohana.spirit = 4
    # kohana.stance(child).value = 0 
    kohana.firstname = u"Кисель"
    kohana.surname = u"Телеведущев"      

    
# Игра начинается здесь.
label start:
    python:
        household = game.add_fraction('household', mother)
        household.add_member(child)
        household.add_member(batya)
        society = game.add_fraction('society', erokhin)
        society.add_member(ashot)
        society.add_member(pavsykakiy)
        society.add_member(kohana)
        society.add_member(eot)

    call init_events
    define gray = Solid("#ccc")
    show image gray as bg
    #call evn_init
    # $ a = encolor_text('хренобула', 0)
    # '[a]'
    call label_quiz
    
    return
    
label label_quiz:
    python:
        child.ration['food_type'] = "cousine" 
        child.ration['amount'] = "unlimited" 
        child.schedule.add_action('fap_yes')
        child.restrictions.append('alcohol')
        child.restrictions.append('tobacco')
        child.restrictions.append('weed')
        child.appearance = 'normal'
        shedule_minor = 'безделье'
        child.ration['food_type'] = "cousine" 
        game.res_add_consumption('child_food', 'provision', child.get_food_consumption, None)
        child.accommodation = "appartment"
        child.schedule.add_action('living_appartment', False)
        nm = child.name() + '_rent'
        game.res_add_consumption(nm, 'money', 25, time=None)
        child.alignment.activity = "timid"
        child.alignment.orderliness = "chaotic"
        child.alignment.morality = "selfish" 
        child.add_feature('male')
        child.add_feature('adolescent')
        mom.relations(child)  
        mom.relations(batya) 
        batya.relations(child) 
        child.schedule.add_action('money_wealth', False, special_values={'num': -1}) 
        child.schedule.add_action('minor_nap', False) 
           
    menu:
        "Ты мальчик или девочка-внутри?"
        "Антоша Сычов (быстрый старт)":
            python:
                batya.randomise('male', 'mature')
                child.skill('coding').profession()
                game.set_player(child)
                player = game.player                
                
                child.accommodation = "jailed"      
                child.schedule.add_action('living_jailed')
                nm = child.name() + '_rent'
                game.res_add_consumption(nm, 'money', 0, time=None)
        
                child.ration['food_type'] = "sperm"
                child.ration['target'] = 1

                child.schedule.add_action('job_chores', False)  
                child.schedule.add_action('minor_dacha', False) 
                child.restrictions.append('masturbation')
                child.schedule.add_action('fap_no')        
                child.restrictions.append('dates')
                child.restrictions.append('friends')
                child.restrictions.append('pc')
            jump label_new_day
        "Твоя Мамка (быстрый старт)":
            python:
                child.skill('coding').profession()
                game.set_player(mom)
                player = game.player
            jump label_new_day
        "Я самец - даже не смей сомневаться!":
            $ child.add_feature('male')
        "Раскусил, дай мне платице...":
            $ child.add_feature('female')     
            
    menu:
        "Волосики уже везде выросли?"
        "Маaaaм, меня комплюктор про странное спрашивает!":
            $ child.add_feature('junior')
        "Я не школота. Факт (правда)":
            $ child.add_feature('adolescent')
        "Я олдфаг. Мои муди седы как снега на склоне фудзи...":
            $ child.add_feature('mature')       

    menu:
        "Какая твоя самая сильная сторона?"
        "В компах разбираюсь с детства":
            $ child.skill('coding').talent = True
        "Отменное здоровье и энергичность":
            $ child.skill('sports').talent = True
        "Я - душа компании":
            $ child.skill('conversation').talent = True
        "Гиперсексуальность":
            $ child.skill('sex').talent = True
        "Я эксперт по ВСЕМ вопросам. Диванный.":
            $ pass

    menu:
        "Чем по жизни занимаешься?"
        "Кодю, компилю, хакаю. Не палюсь.":
            $ child.skill('coding').expert()
        "ЗОЖ. Брусья-брусья-турнички. Качалочка.":
            $ child.skill('sports').expert()
        "Тусуюсь с друзьями.":
            $ child.skill('conversation').expert()
        "Блядую по черному. Молодость всего одна.":
            $ child.skill('sex').expert()
        "Капчую. В дотан шпилю. Всё такое...":
            $ pass
            
    menu:
        "Давай вспомним твои школьные годы. Много двоек было за прогулы?"
        "Никаких прогулов. У меня расписание чёткое.":
            $ child.alignment.orderliness = "lawful"
        "А чё я? Все прогуливали и я прогуливал.":
            $ child.alignment.orderliness = "conformal"
        "Делаю что хочу. Я вообще не контролируемый!":
            $ child.alignment.orderliness = "chaotic"
            
    menu:
        "Новая знакомая в скайпе предлагает тебе зависнуть с ней и ещё двумя подругами на ночь, на незнакомой хате в Медвеково. Твои действия?"
        "Пожаловаться на спам. Скрыть.":
            $ child.alignment.activity = "timid"
        "В Медведково? Ну хрееееееен знает...":
            $ child.alignment.activity = "reasonable"
        "Я за любой кипеш, кроме голодовки!":
            $ child.alignment.activity = "ardent"
            
    menu:
        "Идёшь по улице. Кушаешь вкусный бутер с колбаской. К тебе подбегает няшный котик и просит кусочек."
        "Пнуть блохастого. Это моя колбаса. Плохая киса!":
            $ child.alignment.morality = "evil"
        "Пройти мимо. Пусть бабки подъездные его прикармливают.":
            $ child.alignment.morality = "selfish"
        "Конечно дать колбаски. Да я бы и собаке...":
            $ child.alignment.morality = "good"          
    
    menu:
        "А что если мамка уроки делать заставит?"
        "Конечно. Это - норма.":
            $ child.stance(mom).value = 1       
        "Ну что делать? Сяду. А то батя ремня всыпет.":
            $ child.stance(mom).value = 0    
        "Я скажу - женщина, пиздуй на кухню и принеси мне сырных подушечек.":
            $ child.stance(mom).value = -1
    $ alignment = child.alignment.description()
    "Твой алаймент: [alignment]"
    $ target = child

    jump lbl_features_quiz
    return

label lbl_features_quiz:
    python:
        if target.feature_by_slot('constitution'):
            constitution = consta_name[target.feature_by_slot('constitution').name]
        else:
            constitution = "Нормальное телосложение"
        
    menu:
        "Ты же у мамы особенный? Чем ты особенный?"
        "[constitution]":
            call lbl_choose_constitution

        "Достаточно":   
            jump lbl_player_side_quiz
        
    jump lbl_features_quiz
    return

label lbl_choose_constitution:
    menu:
        'Тип телосложения влияет на ловкость и физическую силу персонажа. В демонстрационной модели ловкость нигде не используется, хотя будет отображаться.'
        'Нормальное телосложение':
            $ target.remove_feature_by_slot('constitution')
        'Атлетичный':
            $ target.add_feature('athletic')
        'Здоровяк':
            $ target.add_feature('large')
        'Коренастый':
            $ target.add_feature('brawny')
        'Мелкий':
            $ target.add_feature('small')
        'Дылда':
            $ target.add_feature('lean')
        'Сколеозник':
            $ target.add_feature('crooked')
        'Широкая кость':
            $ target.add_feature('clumsy')
        
    return

label lbl_player_side_quiz:
    menu:
        "Кем ты будешь управлять?"
        "Собой":
            $ game.mode = 'son'
            $ game.set_player(child)
            $ player = game.player
            $ player.player_controlled = True
            $ child.relations(mother)
            $ mother.enslave(child)    
            $ player.schedule.add_action('general_accounting', False)
            jump label_new_day
            
        "Своей мамкой":
            $ game.mode = 'mom'
            $ game.set_player(mother)
            $ player = game.player
            $ player.player_controlled = True
            $ child.relations(mother)
            $ mother.enslave(child)    
            $ player.schedule.add_action('general_accounting', False)
            jump label_new_day

    return

label label_new_day:
    ### ПРОВЕРКА НА ЗАВЕРШЕНИЕ ИГРЫ ###
    if child.feature('dead') or  mom.feature('dead') or  batya.feature('dead'):
        'Кто-то умер. Видимо от голода...'
        jump game_over
    elif len(game.mom_stuff) > 5:
        'Теперича БОХАТО заживём!\n @ \nМамка победила.'
        jump win_wealth
    elif not game.studies:
        'Я думала ты нулёвый, а ты институт закончил!\n @ \nАнтон Сычов подебил.'        
        jump win_study
        
    
    ### ЕСЛИ ИГРА НЕ ОКОНЧЕНА
    $ study = game.choose_study()
    $ communication = '?'
    "Неделя номер [game.time]"
       
    $ gt = game.new_turn()

    $ game.end_turn_event()
    
    call lbl_universal_menu
    
    # if player == game.child:
    #    call lbl_son_manage
    #else:
    #    call lbl_mom_manage

    return        

label lbl_skill_check(action):
    python:
        renpy.call_screen('sc_skillcheck', action)
    return 
        
label lbl_action_check:
    menu:
        'Выполнить действие':
            return 1
        'Саботировать':
            return -1
label lbl_resist(effect):
    if player.vigor < 1 and player.determination < 1:
        return
    'Сопротивляться [effect]?'
    menu:
        'Энергия: [player.vigor], Решимость: [player.determination]'
        'Энергия' if player.vigor > 0:
            return 'vigor'
        'Решимость' if player.determination > 0:
            return 'determination'
        'Нет':
            return False
label lbl_resist_result(effect, success):
    if success:
        'Вы справились с [effect]'
    else:
        'Вы попытались справиться с [effect] но вам не удалось'
    return
label lbl_result(result, character=player):
    $ char_name = character.name()
    'Результат проверки:[char_name]: [result]'
    return
label lbl_notify(character, effect):
    $ n = character.name()
    '[n] получил(а) [effect]'
    return


screen sc_skillcheck(action):
    python:
        if action.skill:
            sc_check_attrname = action.actor.skill(action.skill).attribute
            sc_check_attribute = getattr(action.actor ,sc_check_attrname)
        i = len(action.pros) - len(action.cons)
        if i < 0:
            i=0
        if i > 5:
            i=5
        text = [check_results[i]]
        class Special_button(object):
            def __init__(self, button):
                self.button = button
            def __call__(self):
                self.button.click()
        class CalcResult(object):
            def __init__(self, pros, cons, text):
                self.pros = pros
                self.cons = cons
                self.text = text
            def __call__(self):
                i = len(self.pros) - len(self.cons)
                if i < 0:
                    i = 0
                elif i > 5:
                    i = 5
                if 'unlucky' in self.cons:
                    i = 0
                self.text = []
                self.text.append(check_results[i])
                renpy.restart_interaction()
        class DelFromList(object):
            def __init__(self, l, pros, text):
                self.text = text
                self.list = l
            def __call__(self):
                self.list.remove(text)
                renpy.restart_interaction()
        class AddToList(object):
            def __init__(self, l, text, cons=None):
                self.list = l
                self.text = text
                if action.cons:
                    self.cons = action.cons
            def __call__(self):
                if self.text == 'risk':
                    self.risk()
                else:
                    self.list.append(self.text)
                    renpy.restart_interaction()
            def risk(self):
                i = randint(1, 2)
                if i == 2:
                    self.list.append('lucky')
                elif i == 1:
                    self.cons.append('unlucky')
                renpy.restart_interaction()

    hbox:
        xalign 0.0
        yalign 0.0
        vbox:
            text 'cons:'
            for s in action.cons:
                text "{color=#f00}[s]{/color}"
        vbox:
            $ CalcResult(action.pros, action.cons, text)
            text action.name
            text "Опции: "
            if not('vigorous' in action.pros or 'unlucky' in action.cons or action.actor.vigor < 2):
                textbutton "Работать хорошо" action[AddToList(action.pros, 'vigorous'), CalcResult(action.pros, action.cons, text)] 
            if not('determined' in action.pros or 'unlucky' in action.cons or action.actor.determination < 1):
                textbutton "Выложиться полностью" action[AddToList(action.pros, 'determined'), CalcResult(action.pros, action.cons, text)]
            if not('lucky' in action.pros or 'unlucky' in action.cons):
                textbutton "Рискнуть" action[AddToList(action.pros, 'risk', action.cons), CalcResult(action.pros, action.cons, text)]
            for button in action.buttons:
                if button.active:
                    textbutton '[button.name]' action[Special_button(button), AddToList(button.list_to_add, button.description), CalcResult(action.pros, action.cons, text)]
            vbox:
                text "Результат действия: [text[0]]"
        vbox:
            text 'pros:'
            for s in action.pros:
                text "{color=#00ff00}[s]{/color}"
    hbox:
        xalign 0.5
        yalign 0.5
        textbutton "Выполнить работу" action[Return()]
        if action.is_skillcheck():
            textbutton "Саботировать" action[AddToList(action.cons, 'sabotage'), Return()]

    vbox:
        xalign 0.0
        yalign 0.7
        if action.skill:
            text "Скил: [action.skill], Аттрибут: [sc_check_attribute]"
            text "Сложность: [action.difficulty]"
        else:
            text "Сила: [action.power]"
            text "Интенсивность потребности: [action._compare_to_power]"
init python:
    class InfoStorage(object):
            def __init__(self, diss_inf, satisfy_inf, determination, anxiety, target):
                self.diss_inf = diss_inf
                self.satisfy_inf = satisfy_inf
                self.determination = determination
                self.anxiety = anxiety
                self.target = target
label mood_recalc_result(diss_inf=None, satisfy_inf=None, determination=None, anxiety=None, recalc=False, target=None):
    python:
        info = None 
        if recalc and target != None:
            for i in recalc_result:
                if i.target == target:
                    recalc_result.remove(i)
                    break
            info = InfoStorage(diss_inf, satisfy_inf, determination, anxiety, target)
            recalc_result.append(info)
    return
label lb_recalc_result_glue():
    call screen sc_mood_recalculation_result(recalc_result_target)
    return
screen sc_mood_recalculation_result(target=None):
    python:
        for i in recalc_result:
            if i.target==target:
                info = i
        threshold = 5-target.sensitivity
    if info == None:
        vbox:
            xalign 0.0
            yalign 0.0
            text 'Для этого персонажа инфы нет'
        hbox:
            xalign 0.5
            yalign 0.5
            textbutton 'Покинуть экран' action Return()
    else:
        python:
            key = 5
            txt = []
            txt_bad = []
            while key > 0:
                for need in info.satisfy_inf[key]:
                    text = encolor_text('%s'%(need.name), key)
                    txt.append(text)
                key -= 1
            for i in info.determination:
                text = encolor_text(i, 1)
                txt.append(text)
            for need in info.diss_inf:
                text = encolor_text('%s(%s)'%(need.name, need.level), 0)
                txt_bad.append(text)
            for i in info.anxiety:
                text = encolor_text(i, 0)
                txt_bad.append(text)
        vbox:
            xalign 0.0
            yalign 0.0
            for i in txt:
                text [i]

        vbox:
            xalign 0.3
            yalign 0.0
            for i in txt_bad:
                text [i]
        vbox:
            xalign 0.6
            yalign 0.0
            text 'Порог: [threshold]'
        hbox:
            xalign 0.5
            yalign 0.5
            textbutton 'Покинуть экран' action Return()
