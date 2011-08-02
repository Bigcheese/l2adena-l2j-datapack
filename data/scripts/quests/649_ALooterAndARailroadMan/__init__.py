# Made by Kilkenny
import sys
from com.l2jserver import Config
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "649_ALooterAndARailroadMan"

#NPC
OBI = 32052

#ITEMS
THIEF_GUILD_MARK = 8099

#REWARDS
ADENA = 57

#Chances
DROP_CHANCE = 50

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [THIEF_GUILD_MARK]

 def onEvent (self,event,st) :
   htmltext = event
   count = st.getQuestItemsCount(THIEF_GUILD_MARK)
   if event == "32052-1.htm" :
     st.set("cond","1")
     st.setState(State.STARTED)
     st.playSound("ItemSound.quest_accept")
   elif event == "32052-3.htm" :
     if count < 200 :
        htmltext = "32052-3a.htm"
     else :
        st.giveItems(ADENA,21698)
        st.takeItems(THIEF_GUILD_MARK,-1)
        st.playSound("ItemSound.quest_finish")
        st.exitQuest(1)
   return htmltext

 def onTalk(self, npc, player):
   st = player.getQuestState(qn)
   htmltext = Quest.getNoQuestMsg(player)
   if st :
     npcId = npc.getNpcId()
     id = st.getState()
     cond = st.getInt("cond")
     if cond == 0 :
       if player.getLevel() >= 30 :
         htmltext = "32052-0.htm"
       else:
         htmltext = "32052-0a.htm"
         st.exitQuest(1)
     elif id == State.STARTED :
       if st.getQuestItemsCount(THIEF_GUILD_MARK) == 200 :
         htmltext = "32052-2.htm"
       else :
         htmltext = "32052-2a.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if st :
     if st.getState() == State.STARTED :
       count = st.getQuestItemsCount(THIEF_GUILD_MARK)
       numItems, chance = divmod(DROP_CHANCE * Config.RATE_QUEST_DROP,100)
       if st.getInt("cond") == 1 and count < 200 :
         if st.getRandom(100) < chance :
           numItems += 1
         if numItems :
           st.giveItems(THIEF_GUILD_MARK,int(numItems))
         if count == 199 :  
           st.playSound("ItemSound.quest_middle")  
           st.set("cond","2")  
         else:  
           st.playSound("ItemSound.quest_itemget") 
   return

QUEST       = Quest(649,qn,"A Looter and a Railroad Man")

QUEST.addStartNpc(OBI)
QUEST.addTalkId(OBI)

for BANDITS in [22017,22018,22019,22021,22022,22023,22024,22026]:
  QUEST.addKillId(BANDITS)