# Made by Mr. Have fun! Version 0.2
import sys
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "1_LettersOfLove1"

#NPCs 
DARIN  = 30048 
ROXXY  = 30006 
BAULRO = 30033 

#ITEMS 
DARINGS_LETTER     = 687 
RAPUNZELS_KERCHIEF = 688 
DARINGS_RECEIPT    = 1079 
BAULS_POTION       = 1080 
 
#REWARD 
NECKLACE = 906
 
class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [DARINGS_LETTER, RAPUNZELS_KERCHIEF, DARINGS_RECEIPT, BAULS_POTION]

 def onAdvEvent (self,event,npc, player) :
   htmltext = event
   st = player.getQuestState(qn)
   if not st : return
   if event == "30048-06.htm" : 
     st.set("cond","1") 
     st.setState(State.STARTED) 
     st.playSound("ItemSound.quest_accept") 
     if st.getQuestItemsCount(DARINGS_LETTER) == 0 : 
       st.giveItems(DARINGS_LETTER,1) 
   return htmltext 

 def onTalk (self,npc,player):
   st = player.getQuestState(qn)
   htmltext = Quest.getNoQuestMsg(player) 
   if not st: return htmltext

   npcId = npc.getNpcId()
   id = st.getState()

   cond = st.getInt("cond") 
   ItemsCount_DL = st.getQuestItemsCount(DARINGS_LETTER) 
   ItemsCount_RK = st.getQuestItemsCount(RAPUNZELS_KERCHIEF) 
   ItemsCount_DR = st.getQuestItemsCount(DARINGS_RECEIPT) 
   ItemsCount_BP = st.getQuestItemsCount(BAULS_POTION) 
   if id == State.COMPLETED :
     htmltext = Quest.getAlreadyCompletedMsg(player) 
   elif npcId == DARIN and id == State.CREATED: 
     if player.getLevel() >= 2 : 
       if cond < 15 : 
         htmltext = "30048-02.htm" 
       else: 
         htmltext = "30048-01.htm" 
         st.exitQuest(1) 
     else: 
       htmltext = "<html><body>Quest for characters level 2 and above.</body></html>" 
       st.exitQuest(1) 
   elif id == State.STARTED :
       if npcId == ROXXY and cond: 
         if ItemsCount_RK == 0 and ItemsCount_DL : 
           htmltext = "30006-01.htm" 
           st.takeItems(DARINGS_LETTER,-1) 
           st.giveItems(RAPUNZELS_KERCHIEF,1) 
           st.set("cond","2") 
           st.playSound("ItemSound.quest_middle") 
         elif ItemsCount_BP or ItemsCount_DR : 
           htmltext = "30006-03.htm" 
         elif ItemsCount_RK : 
           htmltext = "30006-02.htm" 
       elif npcId == DARIN and cond and ItemsCount_RK > 0: 
         htmltext = "30048-08.htm" 
         st.takeItems(RAPUNZELS_KERCHIEF,-1) 
         st.giveItems(DARINGS_RECEIPT,1) 
         st.set("cond","3") 
         st.playSound("ItemSound.quest_middle") 
       elif npcId == BAULRO and cond: 
         if ItemsCount_DR > 0 : 
           htmltext = "30033-01.htm" 
           st.takeItems(DARINGS_RECEIPT,-1) 
           st.giveItems(BAULS_POTION,1) 
           st.set("cond","4") 
           st.playSound("ItemSound.quest_middle") 
         elif ItemsCount_BP > 0 : 
           htmltext = "30033-02.htm" 
       elif npcId == DARIN and cond and ItemsCount_RK == 0: 
         if ItemsCount_DR > 0 : 
           htmltext = "30048-09.htm" 
         elif ItemsCount_BP > 0 : 
           htmltext = "30048-10.htm" 
           st.takeItems(BAULS_POTION,-1) 
           st.giveItems(57,2466)
           st.giveItems(NECKLACE,1)
           st.addExpAndSp(5672,446)
           st.unset("cond") 
           st.exitQuest(False)
           st.playSound("ItemSound.quest_finish") 
         else: 
           htmltext = "30048-07.htm" 
   return htmltext

QUEST     = Quest(1,qn,"Letters of Love") 

QUEST.addStartNpc(DARIN) 

QUEST.addTalkId(DARIN) 
QUEST.addTalkId(ROXXY) 
QUEST.addTalkId(BAULRO) 