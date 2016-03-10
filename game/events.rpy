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
   'Оценка: [result]'
   python:
       pass
   
   return
   
   