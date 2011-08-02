# Made by Mr. Have fun! Version 0.2
import sys
from com.l2jserver import Config 
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "102_FungusFever"

ALBERRYUS_LETTER_ID = 964
EVERGREEN_AMULET_ID = 965
DRYAD_TEARS_ID = 966
ALBERRYUS_LIST_ID = 746
COBS_MEDICINE1_ID = 1130
COBS_MEDICINE2_ID = 1131
COBS_MEDICINE3_ID = 1132
COBS_MEDICINE4_ID = 1133
COBS_MEDICINE5_ID = 1134
SWORD_OF_SENTINEL_ID = 743
STAFF_OF_SENTINEL_ID = 744

def check(st) :
   if (st.getQuestItemsCount(COBS_MEDICINE1_ID)==\
       st.getQuestItemsCount(COBS_MEDICINE2_ID)==\
       st.getQuestItemsCount(COBS_MEDICINE3_ID)==\
       st.getQuestItemsCount(COBS_MEDICINE4_ID)==\
       st.getQuestItemsCount(COBS_MEDICINE5_ID)==0) :
       st.set("cond","6")
       st.playSound("ItemSound.quest_middle")


class Quest (JQuest) :

 def __init__(self,id,name,descr):
    JQuest.__init__(self,id,name,descr)
    self.questItemIds = [ALBERRYUS_LETTER_ID, EVERGREEN_AMULET_ID, DRYAD_TEARS_ID, COBS_MEDICINE1_ID, COBS_MEDICINE2_ID, COBS_MEDICINE3_ID, COBS_MEDICINE4_ID, COBS_MEDICINE5_ID, ALBERRYUS_LIST_ID]

 def onAdvEvent (self,event,npc, player) :
    htmltext = event
    st = player.getQuestState(qn)
    if not st : return
    if event == "1" :
        htmltext = "30284-02.htm"
        st.giveItems(ALBERRYUS_LETTER_ID,1)
        st.set("cond","1")
        st.setState(State.STARTED)
        st.playSound("ItemSound.quest_accept")
    return htmltext


 def onTalk (self,npc,player):
   npcId = npc.getNpcId()
   htmltext = Quest.getNoQuestMsg(player)
   st = player.getQuestState(qn)
   if not st: return htmltext

   id = st.getState()
   if id == State.COMPLETED :
        htmltext = Quest.getAlreadyCompletedMsg(player)
   elif npcId == 30284 and id == State.CREATED :
      if player.getRace().ordinal() != 1 :
         htmltext = "30284-00.htm"
         st.exitQuest(1)
      elif player.getLevel() >= 12 :
         htmltext = "30284-07.htm"
         return htmltext
      else:
         htmltext = "30284-08.htm"
         st.exitQuest(1)
   elif id == State.STARTED :
      if npcId == 30284 and st.getInt("cond")==1 and st.getQuestItemsCount(ALBERRYUS_LETTER_ID)==1 :
           htmltext = "30284-03.htm"
      elif npcId == 30284 and st.getInt("cond")==1 and st.getQuestItemsCount(EVERGREEN_AMULET_ID)==1 :
           htmltext = "30284-09.htm"
      elif npcId == 30156 and st.getInt("cond")==1 and st.getQuestItemsCount(ALBERRYUS_LETTER_ID)==1 :
           st.giveItems(EVERGREEN_AMULET_ID,1)
           st.takeItems(ALBERRYUS_LETTER_ID,1)
           st.set("cond","2")
           st.playSound("ItemSound.quest_middle")
           htmltext = "30156-03.htm"
      elif npcId == 30156 and st.getInt("cond")==2 and st.getQuestItemsCount(EVERGREEN_AMULET_ID)>0 and st.getQuestItemsCount(DRYAD_TEARS_ID)<10 :
           htmltext = "30156-04.htm"
      elif npcId == 30156 and st.getInt("cond")==5 and st.getQuestItemsCount(ALBERRYUS_LIST_ID)>0 :
           htmltext = "30156-07.htm"
      elif npcId == 30156 and st.getInt("cond")==3 and st.getQuestItemsCount(EVERGREEN_AMULET_ID)>0 and st.getQuestItemsCount(DRYAD_TEARS_ID)>=10 :
           st.takeItems(EVERGREEN_AMULET_ID,1)
           st.takeItems(DRYAD_TEARS_ID,-1)
           st.giveItems(COBS_MEDICINE1_ID,1)
           st.giveItems(COBS_MEDICINE2_ID,1)
           st.giveItems(COBS_MEDICINE3_ID,1)
           st.giveItems(COBS_MEDICINE4_ID,1)
           st.giveItems(COBS_MEDICINE5_ID,1)
           st.set("cond","4")
           st.playSound("ItemSound.quest_middle")
           htmltext = "30156-05.htm"
      elif npcId == 30156 and st.getInt("cond")==4 and st.getQuestItemsCount(ALBERRYUS_LIST_ID)==0 and (st.getQuestItemsCount(COBS_MEDICINE1_ID)==1 or st.getQuestItemsCount(COBS_MEDICINE2_ID)==1 or st.getQuestItemsCount(COBS_MEDICINE3_ID)==1 or st.getQuestItemsCount(COBS_MEDICINE4_ID)==1 or st.getQuestItemsCount(COBS_MEDICINE5_ID)==1) :
           htmltext = "30156-06.htm"
      elif npcId == 30284 and st.getInt("cond")==4 and st.getQuestItemsCount(ALBERRYUS_LIST_ID)==0 and st.getQuestItemsCount(COBS_MEDICINE1_ID)==1 :
           st.takeItems(COBS_MEDICINE1_ID,1)
           st.giveItems(ALBERRYUS_LIST_ID,1)
           st.set("cond","5")
           st.playSound("ItemSound.quest_middle")
           htmltext = "30284-04.htm"
      elif npcId == 30284 and st.getInt("cond")==5 and st.getQuestItemsCount(ALBERRYUS_LIST_ID)==1 and (st.getQuestItemsCount(COBS_MEDICINE1_ID)==1 or st.getQuestItemsCount(COBS_MEDICINE2_ID)==1 or st.getQuestItemsCount(COBS_MEDICINE3_ID)==1 or st.getQuestItemsCount(COBS_MEDICINE4_ID)==1 or st.getQuestItemsCount(COBS_MEDICINE5_ID)==1) :
           htmltext = "30284-05.htm"
      elif npcId == 30217 and st.getInt("cond")==5 and st.getQuestItemsCount(ALBERRYUS_LIST_ID)==1 and st.getQuestItemsCount(COBS_MEDICINE2_ID)==1 :
           st.takeItems(COBS_MEDICINE2_ID,1)
           check(st)
           htmltext = "30217-01.htm"
      elif npcId == 30219 and st.getInt("cond")==5 and st.getQuestItemsCount(ALBERRYUS_LIST_ID)==1 and st.getQuestItemsCount(COBS_MEDICINE3_ID)==1 :
           st.takeItems(COBS_MEDICINE3_ID,1)
           check(st)
           htmltext = "30219-01.htm"
      elif npcId == 30221 and st.getInt("cond")==5 and st.getQuestItemsCount(ALBERRYUS_LIST_ID)==1 and st.getQuestItemsCount(COBS_MEDICINE4_ID)==1 :
           st.takeItems(COBS_MEDICINE4_ID,1)
           check(st)
           htmltext = "30221-01.htm"
      elif npcId == 30285 and st.getInt("cond")==5 and st.getQuestItemsCount(ALBERRYUS_LIST_ID)==1 and st.getQuestItemsCount(COBS_MEDICINE5_ID)==1 :
           st.takeItems(COBS_MEDICINE5_ID,1)
           check(st)
           htmltext = "30285-01.htm"
      elif npcId == 30284 and st.getInt("cond")==6 and st.getQuestItemsCount(ALBERRYUS_LIST_ID)==1 :
           st.takeItems(ALBERRYUS_LIST_ID,1)
           st.set("cond","0")
           st.exitQuest(False)
           st.playSound("ItemSound.quest_finish")
           htmltext = "30284-06.htm"
           st.giveItems(57,6331)
           if player.getClassId().getId() in range(18,25) :
             st.giveItems(SWORD_OF_SENTINEL_ID,1)
             st.rewardItems(1835,1000)
           else:
             st.giveItems(STAFF_OF_SENTINEL_ID,1)
             st.rewardItems(2509,1000)
           for item in range(4412,4417) :
             st.rewardItems(item,10)
           st.rewardItems(1060,100)
           st.addExpAndSp(30202,1339)
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st: return 

   if st.getState() == State.STARTED :       
      npcId = npc.getNpcId()
      if npcId in [20013,20019] :
         if st.getQuestItemsCount(EVERGREEN_AMULET_ID)>0 and st.getQuestItemsCount(DRYAD_TEARS_ID)<10 :
            if st.getRandom(10)<3 :
               st.giveItems(DRYAD_TEARS_ID,1)
               if st.getQuestItemsCount(DRYAD_TEARS_ID) == 10 :
                 st.playSound("ItemSound.quest_middle")
                 st.set("cond","3")
               else:
                 st.playSound("ItemSound.quest_itemget")
   return

QUEST       = Quest(102,"102_FungusFever","Sea of Spores Fever")

QUEST.addStartNpc(30284)
QUEST.addTalkId(30284)

QUEST.addTalkId(30156)
QUEST.addTalkId(30217)
QUEST.addTalkId(30219)
QUEST.addTalkId(30221)
QUEST.addTalkId(30285)

QUEST.addKillId(20013)
QUEST.addKillId(20019)