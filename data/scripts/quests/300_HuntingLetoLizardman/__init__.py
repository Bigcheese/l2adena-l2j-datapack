# Hunting Leto Lizardman - Version 0.1 by DrLecter
import sys
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "300_HuntingLetoLizardman"

#NPC
RATH=30126
#Items
BRACELET=7139
#BASE CHANCE FOR DROP
CHANCE = 50
#REWARDS
REWARDS=[[57,30000],[1867,50],[1872,50]]

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [BRACELET]

 def onAdvEvent (self,event,npc, player) :
   htmltext = event
   st = player.getQuestState(qn)
   if not st : return
   cond = st.getInt("cond")
   count = st.getQuestItemsCount(BRACELET)
   if event == "30126-03.htm" and cond == 0 :
     st.set("cond","1")
     st.setState(State.STARTED)
     st.playSound("ItemSound.quest_accept")
   elif event == "30126-05.htm" :
     if count == 60 and cond == 2 :
       htmltext = "30126-06.htm"
       st.takeItems(BRACELET,-1)
       item,qty = REWARDS[st.getRandom(len(REWARDS))]
       st.giveItems(item,qty)
       st.playSound("ItemSound.quest_finish")
       st.exitQuest(1)
   return htmltext

 def onTalk (self,npc,player):
   htmltext = Quest.getNoQuestMsg(player)
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   cond=st.getInt("cond")
   if cond == 0 :
     if player.getLevel() >= 34 :
       htmltext = "30126-02.htm"
     else:
       htmltext = "30126-01.htm"
       st.exitQuest(1)
   else :
       htmltext = "30126-04.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st : return 
   if st.getState() != State.STARTED : return 
   
   count = st.getQuestItemsCount(BRACELET)
   cond = st.getInt("cond")
   if st.getRandom(100) < CHANCE + ((npc.getNpcId() - 20579)*5) and count < 60 and cond == 1:
     st.giveItems(BRACELET,1)
     if count == 59 :
        st.playSound("ItemSound.quest_middle")
        st.set("cond","2")
     else :
        st.playSound("ItemSound.quest_itemget")
   return

QUEST       = Quest(300,qn,"Hunting Leto Lizardman")

QUEST.addStartNpc(RATH)

QUEST.addTalkId(RATH)

for mob in range(20577,20581)+[20582] :
    QUEST.addKillId(mob)