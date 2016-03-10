python:
    import sys
    sys.path.append(renpy.loader.transfn("scrypts"))
    from events import *
    
# label evn_init:
#     python:
#         # TODO: Тут надо будет сделать так чтобы список возможных эвентов генеировался динамически
#         for subclass in Event.__subclasses__():

#             game.events_list.append(subclass(game))

#     return


label evn_template:
   "Event №"
   python:
       pass
   
   return
    

label evn_blank:
   $pass   
   return

   
label evn_unic:
   "Event Unic"
   python:
       pass
   
   return

   
label evn_1:
   "Event №1"
   python:
       pass
   
   return   

label evn_do_major:
   $ result = child.use_skill('coding')
   
   python:
       if result < 5:
           txt = "Твёрдо решаешь засесть за курсовую \n @ \n Что-то сложновато  \n @ \n Завтра сделаю  \n @ \n За неделю - два параграфа..."
       else:
           txt = "Берешь себя за задницу покрепче \n @ \n Делаешь курсач как надо  \n @ \n Потом ещё неделю ловишь научрука... "
           game.studies.remove('major')        
   
   '[txt]'
   
   return

label evn_do_gym:
   $ result = child.use_skill('sport')
   
   python:
       if result < 5:
           txt = "Лазаем по канату \n @ \n Ебнулся на копчик  \n @ \n Группа ржёт как стадо гиен"
       else:
           txt = "Четко подтягиваешься \n @ \n Стометровка в нормативе  \n @ \n Фазген-семпай хвалит - ай, братуха-борцуха!"
           game.studies.remove('gym')        
   
   '[txt]'
   
   return

label evn_do_practice_military:
   $ result = child.use_skill('sport')
   
   python:
       if result < 5:
           txt = "В колонну по двое \n @ \n Равнение на знамя \n @ \n Отдавил ноги впереди идущему \n @ \n Из-за тебя вся группа идет на пересдачу"
       else:
           txt = "Вспоминаешь видос про парад в лучшей Корее \n @ \n В голове играет hellmarch \n @ \n Шаг печаетается сам собой "
           game.studies.remove('military')        
   
   '[txt]'
   
   return

label evn_do_practice_military_chat:
   $ result = child.use_skill('communication')
   
   python:
       if result < 5:
           txt = "Пытаешься подружиться с подполканом \n @ \n А он вообще контуженный \n @ \n По итогам разговора - драишь до вечера очки"
       else:
           txt = "Расспрашиваешь старого подполкана про боевой опыт \n @ \n Он пускает скупую слезу по авганским друзьям \n @ \n И рисует тебе зачёт автоматом"
           game.studies.remove('military')        
   
   '[txt]'
   
   return
   
label evn_do_practice_labs:
   $ result = child.use_skill('coding')
   
   python:
       if result < 5:
           txt = "Пытаешься понять как это вообще работает \n @ \n Создаёшь велосипед на костыльной тяге  \n @ \n Но у тебя даже баги не фурычат"
       else:
           txt = "Вспоминаешь чему вас учили \n @ \n Сдаёшь профессору кривое но рабочее решение  \n @ \n А он и не против!"
           game.studies.remove('labs')        
   
   '[txt]'
   
   return

label evn_do_practice_labs_chat:
   $ result = child.use_skill('communication')
   
   python:
       if result < 5:
           txt = "Просишь у ботанов решение \n @ \n Получаешь кукишь с м  \n @ \n Даже ебаные задроты считают что они лучше тебя"
       else:
           txt = "Среди ботанов все свои \n @ \n Один из них такой же некрофил как профессор \n @ \n Можно самому и не напрягаться"
           game.studies.remove('labs')        
   
   '[txt]'
   
   return

label evn_do_practice_programm:
   $ result = child.use_skill('coding')
   
   python:
       if result < 5:
           txt = "Весь день носишь ящики с перфокартами \n @ \n Роняешь один себе на ногу  \n @ \n Ренген показывает трещину \n @ \n  Неделю свободен"
       else:
           txt = "Скармлваешь Эльбрусу ящик перфокарт \n @ \n Понимаешь что это прикольно \n @ \n Как рулон бумаги в унитаз смыть  \n @ \n Руководитель подмахивает зачёт за усидчивость"
           game.studies.remove('practice')        
   
   '[txt]'
   
   return   

label evn_do_practice_programm_chat:
   $ result = child.use_skill('communication')
   
   python:
       if result < 5:
           txt = "Коллектив в перерыве расслабляется \n @ \n Пьют технические жидкости  \n @ \n Сблеванул = слабоват ещё для взрослой работы"
       else:
           txt = "Забухал с коллективом в подсобке \n @ \n Рассказал охуительных историй с учёбы \n @ \n Подписали весь лист практики на год вперёд"
           game.studies.remove('practice')        
   
   '[txt]'
   
   return   
   
   
   