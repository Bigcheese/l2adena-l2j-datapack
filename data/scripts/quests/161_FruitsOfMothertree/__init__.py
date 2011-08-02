# Made by Mr. Have fun!
# Version 0.3 by H1GHL4ND3R
import sys
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "161_FruitsOfMothertree"

ANDELLRIAS_LETTER = 1036
MOTHERTREE_FRUIT = 1037
ADENA = 57

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [MOTHERTREE_FRUIT, ANDELLRIAS_LETTER]

 def onAdvEvent (self,event,npc, player) :
    htmltext = event
    st = player.getQuestState(qn)
    if not st : return
    if event == "30362-04.htm" :
      st.set("cond","1")
      st.setState(State.STARTED)
      st.giveItems(ANDELLRIAS_LETTER,1)
      st.playSound("ItemSound.quest_accept")
    return htmltext

 def onTalk (self,npc,player):
   htmltext = Quest.getNoQuestMsg(player)
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   if id == State.CREATED :
     if player.getRace().ordinal() != 1 :
       htmltext = "30362-00.htm"
     elif player.getLevel() >= 3 :
       htmltext = "30362-03.htm"
       st.set("cond","0")
     else:
       htmltext = "30362-02.htm"
       st.exitQuest(1)
   elif id == State.COMPLETED :
     htmltext = Quest.getAlreadyCompletedMsg(player)

   elif id == State.STARTED :
     try :
       cond = st.getInt("cond")
     except :
       cond = None
     if cond == 1 :
       if npcId == 30362 :
         htmltext = "30362-05.htm"
       elif npcId == 30371 and st.getQuestItemsCount(ANDELLRIAS_LETTER) :
         htmltext = "30371-01.htm"
         st.takeItems(ANDELLRIAS_LETTER,1)
         st.giveItems(MOTHERTREE_FRUIT,1)
         st.set("cond", "2")
         st.playSound("ItemSound.quest_middle")
     elif cond == 2 :
       if npcId == 30362 and st.getQuestItemsCount(MOTHERTREE_FRUIT) :
         htmltext = "30362-06.htm"
         st.giveItems(ADENA,1000)
         st.takeItems(MOTHERTREE_FRUIT,1)
         st.addExpAndSp(1000,0)
         st.unset("cond")
         st.exitQuest(False)
         st.playSound("ItemSound.quest_finish")
       elif npcId == 30371 and st.getQuestItemsCount(MOTHERTREE_FRUIT) :
         htmltext = "30371-02.htm"
   return htmltext

QUEST       = Quest(161,qn,"Fruits Of the Mothertree")

QUEST.addStartNpc(30362)

QUEST.addTalkId(30362)

QUEST.addTalkId(30371)