# Made by Vice - cleanup by DrLecter
# this script is part of the Official L2J Datapack Project.
# Visit http://www.l2jdp.com/forum/ for more details.
import sys
from com.l2jserver import Config
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "618_IntoTheFlame"
#NPCs
KLEIN = 31540
HILDA = 31271

#QUEST ITEMS
VACUALITE_ORE,VACUALITE,FLOATING_STONE = range(7265,7268)

#CHANCE
CHANCE_FOR_QUEST_ITEMS = 50

class Quest (JQuest) :
   def __init__(self,id,name,descr):
      JQuest.__init__(self,id,name,descr)
      self.questItemIds = range(7265,7267)

   def onEvent (self,event,st) :
      htmltext = event
      cond = st.getInt("cond")
      if event == "31540-03.htm" and cond == 0 :
         st.setState(State.STARTED)
         st.set("cond","1")
         st.playSound("ItemSound.quest_accept")
      elif event == "31540-05.htm" :
         if st.getQuestItemsCount(VACUALITE) and cond == 4 :
            st.takeItems(VACUALITE,1)
            st.giveItems(FLOATING_STONE,1)
            st.playSound("ItemSound.quest_finish")
            st.exitQuest(1)
         else :
            htmltext = "31540-03.htm"
      elif event == "31271-02.htm" and cond == 1 :
         st.set("cond","2")
         st.playSound("ItemSound.quest_middle")
      elif event == "31271-05.htm" :
         if cond == 3 and st.getQuestItemsCount(VACUALITE_ORE) == 50 :
            st.takeItems(VACUALITE_ORE,-1)
            st.giveItems(VACUALITE,1)
            st.set("cond","4")
            st.playSound("ItemSound.quest_middle")
         else :
            htmltext = "31271-03.htm"
      return htmltext

   def onTalk (self,npc,player) :
      htmltext = Quest.getNoQuestMsg(player)
      st = player.getQuestState(qn)
      if not st : return htmltext
      npcId = npc.getNpcId()
      cond = st.getInt("cond")
      id = st.getState()
      if npcId == KLEIN :
         if cond == 0 :
            if player.getLevel() < 60 :
               htmltext = "31540-01.htm"
               st.exitQuest(1)
            else :
               htmltext = "31540-02.htm"
         elif cond == 4 and st.getQuestItemsCount(VACUALITE) :
            htmltext = "31540-04.htm"
         else :
            htmltext = "31540-03.htm"
      elif npcId == HILDA :
         if cond == 1 :
            htmltext = "31271-01.htm"
         elif cond == 3 and st.getQuestItemsCount(VACUALITE_ORE) == 50 :
            htmltext = "31271-04.htm"
         elif cond == 4 :
            htmltext = "31271-06.htm"
         else :
            htmltext = "31271-03.htm"
      return htmltext

   def onKill(self,npc,player,isPet) :
      partyMember = self.getRandomPartyMember(player,"2")
      if not partyMember : return
      st = partyMember.getQuestState(qn) 
      if not st : return
      count = st.getQuestItemsCount(VACUALITE_ORE)
      if st.getInt("cond") == 2 and count < 50 :
         chance = CHANCE_FOR_QUEST_ITEMS * Config.RATE_QUEST_DROP
         numItems, chance = divmod(chance,100)
         if st.getRandom(100) < chance : 
            numItems += 1
         if numItems :
            if count + numItems >= 50 :
               numItems = 50 - count
               st.playSound("ItemSound.quest_middle")
               st.set("cond","3")
            else:
               st.playSound("ItemSound.quest_itemget")   
            st.giveItems(VACUALITE_ORE,int(numItems)) 
      return

QUEST       = Quest(618,qn,"Into the Flame")

QUEST.addStartNpc(KLEIN)
QUEST.addTalkId(KLEIN)
QUEST.addTalkId(HILDA)

for mob in range(21274,21278)+range(21282,21286)+range(21290,21294) :
    QUEST.addKillId(mob)