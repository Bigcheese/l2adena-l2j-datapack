# Made by Mr. Have fun! Version 0.2
# Fixed by Pela Version 0.3 - Enough credits, but DrLecter was here :D
import sys
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "297_GatekeepersFavor"

STARSTONE2_ID = 1573
GATEKEEPER_TOKEN_ID = 1659

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [STARSTONE2_ID]

 def onAdvEvent (self,event,npc, player) :
    htmltext = event
    st = player.getQuestState(qn)
    if not st : return
    if event == "1" :
       if st.getPlayer().getLevel() >= 15 :
          htmltext = "30540-03.htm"
          st.set("cond","1")
          st.setState(State.STARTED)
          st.playSound("ItemSound.quest_accept")
       else:
          htmltext = "30540-01.htm"
    return htmltext

 def onTalk (self,npc,player):
   htmltext = Quest.getNoQuestMsg(player)
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   if id == State.CREATED :
      st.set("cond","0")
   if npcId == 30540 :
      if st.getInt("cond")==0 :
         htmltext = "30540-02.htm"
      elif st.getInt("cond")==1 and st.getQuestItemsCount(STARSTONE2_ID)<20 :
         htmltext = "30540-04.htm"
      elif st.getInt("cond")==2 and st.getQuestItemsCount(STARSTONE2_ID)==20 :
         htmltext = "30540-05.htm"
         st.takeItems(STARSTONE2_ID,-1)
         st.giveItems(GATEKEEPER_TOKEN_ID,2)
         st.exitQuest(1)
         st.playSound("ItemSound.quest_finish")
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st : return 
   if st.getState() != State.STARTED : return 
   
   npcId = npc.getNpcId()
   if npcId == 20521 :
      if st.getInt("cond") == 1 and st.getQuestItemsCount(STARSTONE2_ID) < 20 :
         if st.getRandom(2) == 0 :
            st.giveItems(STARSTONE2_ID,1) 
            if st.getQuestItemsCount(STARSTONE2_ID) == 20 :
               st.playSound("ItemSound.quest_middle")
               st.set("cond","2")
            else:
               st.playSound("ItemSound.quest_itemget")
   return

QUEST       = Quest(297,qn,"Gatekeepers Favor")

QUEST.addStartNpc(30540)
QUEST.addTalkId(30540)

QUEST.addKillId(20521)