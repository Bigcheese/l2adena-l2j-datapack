# Made by disKret
import sys
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "621_EggDelivery"

#NPC
JEREMY = 31521
PULIN = 31543
NAFF = 31544
CROCUS = 31545
KUBER = 31546
BEORIN = 31547
VALENTINE = 31584

#QUEST ITEMS
BOILED_EGGS = 7195
FEE_OF_EGGS = 7196

#REWARDS
ADENA = 57
HASTE_POTION = 734

#Chance to get an S-grade random recipe instead of just adena and haste potion
RPCHANCE=10
#Change this value to 1 if you wish 100% recipes, default 70%
ALT_RP100=0

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [BOILED_EGGS, FEE_OF_EGGS]

 def onEvent (self,event,st) :
   htmltext = event
   cond=st.getInt("cond")
   if event == "31521-1.htm" :
     if cond==0:
       st.set("cond","1")
       st.setState(State.STARTED)
       st.giveItems(BOILED_EGGS,5)
       st.playSound("ItemSound.quest_accept")
     else:
       htmltext = Quest.getNoQuestMsg(player)
   elif event == "31543-1.htm" :
     if st.getQuestItemsCount(BOILED_EGGS):
       if cond==1:
         st.takeItems(BOILED_EGGS,1)
         st.giveItems(FEE_OF_EGGS,1)
         st.set("cond","2")
       else:
         htmltext = Quest.getNoQuestMsg(player)
     else:
       htmltext="LMFAO!"
       st.exitQuest(1)
   elif event == "31544-1.htm" :
     if st.getQuestItemsCount(BOILED_EGGS):
       if cond==2:
         st.takeItems(BOILED_EGGS,1)
         st.giveItems(FEE_OF_EGGS,1)
         st.set("cond","3")
       else:
         htmltext = Quest.getNoQuestMsg(player)
     else:
       htmltext="LMFAO!"
       st.exitQuest(1)
   elif event == "31545-1.htm" :
     if st.getQuestItemsCount(BOILED_EGGS):
       if cond==3:
         st.takeItems(BOILED_EGGS,1)
         st.giveItems(FEE_OF_EGGS,1)
         st.set("cond","4")
       else:
         htmltext = Quest.getNoQuestMsg(player)
     else:
       htmltext="LMFAO!"
       st.exitQuest(1)
   elif event == "31546-1.htm" :
     if st.getQuestItemsCount(BOILED_EGGS):
       if cond==4:
         st.takeItems(BOILED_EGGS,1)
         st.giveItems(FEE_OF_EGGS,1)
         st.set("cond","5")
       else:
         htmltext = Quest.getNoQuestMsg(player)
     else:
       htmltext="LMFAO!"
       st.extiQuest(1)
   elif event == "31547-1.htm" :
     if st.getQuestItemsCount(BOILED_EGGS):
       if cond==5:
         st.takeItems(BOILED_EGGS,1)
         st.giveItems(FEE_OF_EGGS,1)
         st.set("cond","6")
       else:
         htmltext = Quest.getNoQuestMsg(player)
     else:
       htmltext="LMFAO!"
       st.extiQuest(1)
   elif event == "31521-3.htm" :
     st.set("cond","7")
   elif event == "31584-2.htm" :
     if st.getQuestItemsCount(FEE_OF_EGGS) == 5:
        st.takeItems(FEE_OF_EGGS,5)
        if st.getRandom(100) < RPCHANCE :
          st.giveItems(range(6847+ALT_RP100,6853,2)[st.getRandom(3)],1)
        else:
          st.giveItems(ADENA,18800)
          st.giveItems(HASTE_POTION,1)
        st.playSound("ItemSound.quest_finish")
        st.exitQuest(1)
     else:
        htmltext = Quest.getNoQuestMsg(player)
   return htmltext

 def onTalk (self,npc,player):
   htmltext = Quest.getNoQuestMsg(player)
   st = player.getQuestState(qn)
   if st :
     npcId = npc.getNpcId()
     id = st.getState()
     if id == State.CREATED :
       st.set("cond","0")
     cond = st.getInt("cond")
     if npcId == 31521 and cond == 0 :
       if player.getLevel() >= 68 :
         htmltext = "31521-0.htm"
       else :
         st.exitQuest(1)
     elif id == State.STARTED :
       if npcId == 31543 and cond == 1 and st.getQuestItemsCount(BOILED_EGGS) :
         htmltext = "31543-0.htm"
       elif npcId == 31544 and cond == 2 and st.getQuestItemsCount(BOILED_EGGS) :
         htmltext = "31544-0.htm"
       elif npcId == 31545 and cond == 3 and st.getQuestItemsCount(BOILED_EGGS) :
         htmltext = "31545-0.htm"
       elif npcId == 31546 and cond == 4 and st.getQuestItemsCount(BOILED_EGGS) :
         htmltext = "31546-0.htm"
       elif npcId == 31547 and cond == 5 and st.getQuestItemsCount(BOILED_EGGS) :
         htmltext = "31547-0.htm"
       elif npcId == 31521 and cond == 6 and st.getQuestItemsCount(FEE_OF_EGGS) == 5 :
         htmltext = "31521-2.htm"
       elif npcId == 31521 and cond == 7 and st.getQuestItemsCount(FEE_OF_EGGS) == 5 :
         htmltext = "31521-4.htm"
       elif npcId == 31584 and cond == 7 and st.getQuestItemsCount(FEE_OF_EGGS) == 5 :
         htmltext = "31584-1.htm"
   return htmltext

QUEST       = Quest(621,qn,"Egg Delivery")

QUEST.addStartNpc(31521)

for i in range(31543,31548)+[31521,31584]:
    QUEST.addTalkId(i)