init -10 python:
    sys.path.append(renpy.loader.transfn("scrypts"))
    from obj_character import *
    from owl_engine import *
    from events import *
    from schedule import *

init python:
    
    renpy.block_rollback()
    game = Engine()
    child = game.child
    mother = game.mother
    child.master = mother
    register_actions()
    mother.enslave(child)
    mom = mother
    mom.firstname = u"Маман"
    mom.surname = u"Сычова"        
    check_results = ['{color=#f00}failure{/color}', '{color=#ff00f3}marginal{/color}', '{color=#b700ff}normal{/color}',
                    '{color=#2600ff}fine{/color}', '{color=#2cab2c}exceptional{/color}', '{color=#dff54f}perfect{/color}']
    #BATYA
    batya = Person()
    batya.add_feature('male')
    batya.add_feature('mature')
    batya.firstname = u"BATYA"
    batya.surname = u"Сычов"    
    batya.skill('leadership').profession()  
    batya.stance(child).value = 0
    batya.stance(mom).value = 1
    
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
    eot.stance(child).value = 0    
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
    erokhin.stance(child).value = -1
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
    ashot.stance(child).value = 0     
    ashot.firstname = u"Ашот"
    ashot.surname = u"Мудлаев"     
    
    #СВЯЩЕННИК
    pavsykakiy = Person()
    pavsykakiy.skill('leadership').expert()  
    pavsykakiy.stance(child).value = 0 
    pavsykakiy.firstname = u"Павсикакий"
    pavsykakiy.surname = u"Святомудин"      
    
    #ТЕЛЕВЕДУЩИЙ
    kohana = Person()
    kohana.skill('leadership').profession()
    kohana.spirit = 4
    kohana.stance(child).value = 0 
    kohana.firstname = u"Кисель"
    kohana.surname = u"Телеведущев"      
    
    
    
# Игра начинается здесь.
label start:
    call init_events
    define gray = Solid("#ccc")
    show image gray as bg
    #call evn_init
    call label_quiz
    
    return
    
label label_quiz:
    $ child.schedule.add_action('general_accounting')
    $ child.accommodation = "appartment"
    $ child.schedule.add_action('living_appartment')
    $ child.ration['food_type'] = "canned" 
    $ child.ration['amount'] = "unlimited" 
    $ child.schedule.add_action('fap_yes')
    $ child.restrictions.append('alcohol')
    $ child.schedule.add_action('alcohol_no')    
    $ child.restrictions.append('tobacco')
    $ child.schedule.add_action('smoke_no')      
    $ child.restrictions.append('weed')
    $ child.schedule.add_action('weed_no')   
    $ child.appearance = 'normal'
    $ child.schedule.add_action('outfit_normal')    
    
    menu:
        "Ты мальчик или девочка-внутри?"
        "(я не человек уже, я разработчик нахуй)":
            python:
                child.add_feature('male')
                child.add_feature('adolescent')
                child.alignment.orderliness = "conformal"
                child.alignment.activity = "reasonable"
                child.alignment.morality = "selfish"
                child.skill('coding').profession()
                game.set_player(child)
                player = game.player
                mom = game.mother
                mom.alignment.morality = 'evil'
                mom.relations(child)    
                mom.add_feature('female')
                mom.add_feature('mature')
                mom.stance(child).value = 0
                child.ration['food_type'] = "sperm"
                child.ration['target'] = 1
                child.accommodation = "jailed"      
                child.schedule.add_action('living_jailed')
                child.job['name'] = 'chores'
                child.schedule.add_action('job_chores')  
                child.restrictions.append('masturbation')
                child.schedule.add_action('fap_no')        
                child.appearance = 'lame'
                child.schedule.add_action('outfit_lame')
                child.restrictions.append('dates')
                child.restrictions.append('friends')
                child.restrictions.append('pc')
            jump label_new_day
        "(разработчик, игра за маму)":
            python:
                child.add_feature('male')
                child.add_feature('adolescent')
                child.alignment.orderliness = "conformal"
                child.alignment.activity = "reasonable"
                child.alignment.morality = "selfish"
                child.skill('coding').profession()
                mom = game.mother
                game.set_player(mom)
                player = game.player
                mom.alignment.morality = 'selfish'
                mom.relations(child)    
                mom.add_feature('female')
                mom.add_feature('mature')
                child.stance(mom).set_level('rebellious')
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
            $ child.stance(mom).value = 2       
        "Ну что делать? Сяду. А то батя ремня всыпет.":
            $ child.stance(mom).value = 1    
        "Я скажу - женщина, пиздуй на кухню и принеси мне сырных подушечек.":
            $ child.stance(mom).value = 0

            
    $ alignment = child.alignment.description
    "Твой алаймент: [alignment]"

    menu:
        "Кем ты будешь управлять?"
        "Собой":
            $ game.mode = 'son'
            $ game.set_player(child)
            $ player = game.player
            $ player.player_controlled = True
            $ child.relations(mother)
            jump label_new_day
            
        "Своей мамкой":
            $ game.mode = 'mom'
            $ game.set_player(mother)
            $ player = game.player
            $ player.player_controlled = True
            $ child.relations(mother)           
            jump label_new_day

    return

label label_new_day:
    ### ПРОВЕРКА НА ЗАВЕРШЕНИЕ ИГРЫ ###
    if child.feature('dead'):
        jump game_over
    elif len(game.mom_stuff) > 5:
        jump win_wealth
    elif not game.studies:
        jump win_study
        
    
    ### ЕСЛИ ИГРА НЕ ОКОНЧЕНА
    $ study = game.choose_study()
    $ game.child.rest()
    $ game.mother.rest()
    "Неделя номер [game.time]"
       
    $ gt = game.new_turn()
    $ game.evn_skipcheck = False

    $ game.end_turn_event()
    $ game.evn_skipcheck = True
    
    call lbl_universal_menu
    
    # if player == game.child:
    #    call lbl_son_manage
    #else:
    #    call lbl_mom_manage

    return        

label lbl_owl_info:
    python:
        alignment = child.alignment.description()
        job = child.job['name']
        desu = child.description()
        needs_overflow = child.show_needs('overflow')
        needs_tense = child.show_needs('tense')
        needs_relevant = child.show_needs('relevant')
        needs_statisfied = child.show_needs('satisfied')
        # taboos = child.show_taboos()
        features = child.show_features()
        focus = child.show_focus()
        rel = child.relations(mom).description()
        txt = "Настроение: " + str(child.mood()) + " | Подчинение: " + str(child.stance(mother).level)
    "[txt] | Энергия: [child.vigor] \n
    
     Запреты: [child.restrictions] \n 
     Тэнге: [game.tenge] \n
     Условия сна: [child.accommodation]  |  Занятость: [job]       \n
     Характер: [alignment]\n
     Отношение: [rel]\n
     Фокус: [focus]\n
     Напряжения: [needs_tense]\n
     Актуальные нужды: [needs_relevant]\n
     Удовлетворённые: [needs_statisfied]\n          
     Пресыщения: [needs_overflow]\n     
     Особенности: [features]\n
     \n"

    return

label lbl_mom_info:
    python:
        alignment = mom.alignment.description()
        needs_overflow = mom.show_needs('overflow')
        needs_tense = mom.show_needs('tense')
        needs_relevant = mom.show_needs('relevant')
        needs_statisfied = mom.show_needs('satisfied')
        features = mom.show_features()
        rel = child.relations(mom).description()
        txt = "Настроение: " + str(mom.mood()) + " | Благоволение: " + str(mom.stance(player).level)
    "[txt] | Энергия: [mom.vigor] \n
     Тэнге: [game.tenge] \n
     Характер: [alignment]\n
     Отношение: [rel]\n
     Напряжения: [needs_tense]\n
     Актуальные нужды: [needs_relevant]\n
     Удовлетворённые: [needs_statisfied]\n          
     Пресыщения: [needs_overflow]\n     
     Особенности: [features]\n
     \n"

    return
label lbl_skill_check(pros, cons, character, skill=None, name='template_name'):
    python:
        renpy.call_screen('sc_skillcheck', pros, cons, character, skill, name)
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


screen sc_skillcheck(pros, cons, character, skill, name):
    python:
        i = len(pros) - len(cons)
        if i < 0:
            i=0
        if i > 5:
            i=5
        text = [check_results[i]]
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
            def __init__(self, pros, text):
                self.text = text
                self.list = l
            def __call__(self):
                self.list.remove(text)
                renpy.restart_interaction()
        class AddToList(object):
            def __init__(self, l, text, cons=None):
                self.list = l
                self.text = text
                if cons:
                    self.cons = cons
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
            for s in cons:
                text "{color=#f00}[s]{/color}"
        vbox:
            $ CalcResult(pros, cons, text)
            text name
            text "Опции: "
            if not('vigorous' in pros or 'unlucky' in cons or character.vigor < 2):
                textbutton "Работать хорошо" action[AddToList(pros, 'vigorous'), CalcResult(pros, cons, text)] 
            if not('determined' in pros or 'unlucky' in cons or character.determination < 1):
                textbutton "Выложиться полностью" action[AddToList(pros, 'determined'), CalcResult(pros, cons, text)]
            if not('lucky' in pros or 'unlucky' in cons):
                textbutton "Рискнуть" action[AddToList(pros, 'risk', cons), CalcResult(pros, cons, text)]
            vbox:
                text "Результат действия: [text[0]]"
        vbox:
            for s in pros:
                text "{color=#00ff00}[s]{/color}"
    hbox:
        xalign 0.5
        yalign 0.5
        textbutton "Выполнить работу" action[Return()]
        if skill:
            textbutton "Саботировать" action[AddToList(cons, 'sabotage'), Return()]
