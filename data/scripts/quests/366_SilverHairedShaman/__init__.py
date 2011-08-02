# Silver Haired Shaman - Version 0.1 by DrLecter
import sys
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "366_SilverHairedShaman"

#NPC
DIETER=30111
#Items
HAIR=5874
ADENA=57
#BASE CHANCE FOR DROP
CHANCE = 55

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [HAIR]

 def onEvent (self,event,st) :
   htmltext = event
   cond = st.getInt("cond")
   if event == "30111-2.htm" and cond == 0 :
     st.set("cond","1")
     st.setState(State.STARTED)
     st.playSound("ItemSound.quest_accept")
   elif event == "30111-6.htm" :
     st.exitQuest(1)
     st.playSound("ItemSound.quest_finish")
   return htmltext

 def onTalk (self,npc,player):
   htmltext = Quest.getNoQuestMsg(player)
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   cond=st.getInt("cond")
   if cond == 0 :
     if player.getLevel() >= 48 :
       htmltext = "30111-1.htm"
     else:
       htmltext = "30111-0.htm"
       st.exitQuest(1)
   else :
     hair=st.getQuestItemsCount(HAIR)
     if not hair :
       htmltext = "30111-3.htm"
     else :
       st.giveItems(ADENA,12070+500*hair)
       st.takeItems(HAIR,-1)
       htmltext = "30111-4.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   partyMember = self.getRandomPartyMemberState(player,State.STARTED)
   if not partyMember : return
   st = partyMember.getQuestState(qn)
   
   if st.getRandom(100) < CHANCE + ((npc.getNpcId() - 20985) * 2) :
     st.giveItems(HAIR,1)
     st.playSound("ItemSound.quest_itemget")
   return

QUEST       = Quest(366,qn,"Silver Haired Shaman")

QUEST.addStartNpc(DIETER)

QUEST.addTalkId(DIETER)

for mob in range(20986,20989) :
    QUEST.addKillId(mob)