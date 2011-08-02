# Made by disKret
import sys
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "14_WhereaboutsOfTheArchaeologist"

#NPC
LIESEL = 31263
GHOST_OF_ADVENTURER = 31538

#QUEST ITEM
LETTER = 7253

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [LETTER]

 def onAdvEvent (self,event,npc, player) :
   htmltext = event
   st = player.getQuestState(qn)
   if not st : return
   cond = st.getInt("cond")
   if event == "31263-2.htm" and cond == 0 :
     st.set("cond","1")
     st.setState(State.STARTED)
     st.giveItems(LETTER,1)
     st.playSound("ItemSound.quest_accept")
   elif event == "31538-1.htm" :
     if cond == 1 and st.getQuestItemsCount(LETTER) == 1 :
       st.takeItems(LETTER,1)
       st.giveItems(57,136928)
       st.addExpAndSp(325881,32524)
       st.exitQuest(False)
       st.set("cond","0")
       st.playSound("ItemSound.quest_finish")
     else :
       htmltext = "You don't have required items"
   return htmltext

 def onTalk (self,npc,player):
   htmltext = Quest.getNoQuestMsg(player)
   st = player.getQuestState(qn)
   if not st : return htmltext
   npcId = npc.getNpcId()
   id = st.getState()
   cond = st.getInt("cond")
   if npcId == LIESEL and cond == 0 :
     if id == State.COMPLETED :
       htmltext = Quest.getAlreadyCompletedMsg(player)
     elif player.getLevel() < 74 : 
       htmltext = "31263-1.htm"
       st.exitQuest(1)
     elif player.getLevel() >= 74 : 
       htmltext = "31263-0.htm"
   elif npcId == LIESEL and cond == 1 :
     htmltext = "31263-2.htm"
   elif npcId == GHOST_OF_ADVENTURER and cond == 1 and id == State.STARTED:
     htmltext = "31538-0.htm"
   return htmltext

QUEST       = Quest(14,qn,"Whereabouts Of The Archaeologist")

QUEST.addStartNpc(LIESEL)
QUEST.addTalkId(LIESEL)
QUEST.addTalkId(GHOST_OF_ADVENTURER)