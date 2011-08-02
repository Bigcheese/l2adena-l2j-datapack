# Made by Polo
import sys
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "122_OminousNews"

#Npc
MOIRA = 31979
KARUDA = 32017

class Quest (JQuest) :

 def __init__(self,id,name,descr): JQuest.__init__(self,id,name,descr)

 def onAdvEvent (self,event,npc,player) :
   st = player.getQuestState(qn)
   if not st : return
   htmltext = Quest.getNoQuestMsg(player)
   id = st.getState()
   cond = st.getInt("cond")
   if id != State.COMPLETED :
     htmltext = event
     if htmltext == "31979-03.htm" and cond == 0 :
       st.set("cond","1")
       st.setState(State.STARTED)
       st.playSound("ItemSound.quest_accept")
     elif htmltext == "32017-02.htm" :
       if cond == 1 and st.getInt("ok") :
         st.giveItems(57,8923)
         st.addExpAndSp(45151,2310)
         st.unset("cond")
         st.unset("ok")
         st.exitQuest(False)
         st.playSound("ItemSound.quest_finish")
       else :
         htmltext = Quest.getNoQuestMsg(player)
   return htmltext

 def onTalk (self,npc,player):
   npcId = npc.getNpcId()
   htmltext = Quest.getNoQuestMsg(player)
   st = player.getQuestState(qn)
   if not st : return htmltext

   id = st.getState()
   cond = st.getInt("cond")
   if id == State.COMPLETED :
      htmltext="<html><body>This quest have already been State.COMPLETED</body></html>"
   elif npcId == MOIRA :
      if cond == 0 :
         if player.getLevel()>=20 :
            htmltext = "31979-02.htm"
         else :
            htmltext = "31979-01.htm"
            st.exitQuest(1)
      else:
         htmltext = "31979-03.htm"
   elif npcId == KARUDA and cond==1 and id == State.STARTED:
      htmltext = "32017-01.htm"
      st.set("ok","1")
   return htmltext

QUEST       = Quest(122,qn,"Ominous News")


QUEST.addStartNpc(MOIRA)

QUEST.addTalkId(MOIRA)

QUEST.addTalkId(KARUDA)