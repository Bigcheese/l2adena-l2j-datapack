# Made by Mr. - Version 0.3 by DrLecter
import sys
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "261_DreamOfMoneylender1"

GIANT_SPIDER_LEG = 1087
ADENA = 57

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [GIANT_SPIDER_LEG]

 def onAdvEvent (self,event,npc, player) :
    htmltext = event
    st = player.getQuestState(qn)
    if not st : return
    if event == "30222-03.htm" :
      st.set("cond","1")
      st.setState(State.STARTED)
      st.playSound("ItemSound.quest_accept")
    return htmltext

 def onTalk (self,npc,player):
   htmltext = Quest.getNoQuestMsg(player)
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()

   if id == State.CREATED :
     st.set("cond","0")
   if st.getInt("cond")==0 :
     if player.getLevel() >= 15 :
       htmltext = "30222-02.htm"
     else:
       htmltext = "30222-01.htm"
       st.exitQuest(1)
   else :
     if st.getQuestItemsCount(GIANT_SPIDER_LEG) >= 8 :
       st.giveItems(ADENA,1000)
       st.takeItems(GIANT_SPIDER_LEG,-1)
       st.addExpAndSp(2000,0)
       htmltext = "30222-05.htm"
       st.exitQuest(1)
       st.playSound("ItemSound.quest_finish")
     else:
       htmltext = "30222-04.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st : return 
   if st.getState() != State.STARTED : return 
   
   count = st.getQuestItemsCount(GIANT_SPIDER_LEG)
   if count < 8 :
     st.giveItems(GIANT_SPIDER_LEG,1)
     if count == 7 :
       st.playSound("ItemSound.quest_middle")
       st.set("cond","2")
     else:
       st.playSound("ItemSound.quest_itemget")
   return

QUEST       = Quest(261,qn,"Collector's Dream")

QUEST.addStartNpc(30222)

QUEST.addTalkId(30222)

QUEST.addKillId(20308)
QUEST.addKillId(20460)
QUEST.addKillId(20466)