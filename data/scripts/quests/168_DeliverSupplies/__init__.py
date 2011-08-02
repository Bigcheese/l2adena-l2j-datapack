# Made by Mr. Have fun! Version 0.3
import sys
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "168_DeliverSupplies"

JENNIES_LETTER_ID = 1153
SENTRY_BLADE1_ID = 1154
SENTRY_BLADE2_ID = 1155
SENTRY_BLADE3_ID = 1156
OLD_BRONZE_SWORD_ID = 1157
ADENA_ID = 57

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [SENTRY_BLADE1_ID, OLD_BRONZE_SWORD_ID, JENNIES_LETTER_ID, SENTRY_BLADE2_ID, SENTRY_BLADE3_ID]

 def onAdvEvent (self,event,npc, player) :
    htmltext = event
    st = player.getQuestState(qn)
    if not st : return
    if event == "1" :
      st.set("id","0")
      st.set("cond","1")
      st.setState(State.STARTED)
      st.playSound("ItemSound.quest_accept")
      htmltext = "30349-03.htm"
      st.giveItems(JENNIES_LETTER_ID,1)
    return htmltext

 def onTalk (self,npc,player):
   htmltext = Quest.getNoQuestMsg(player)
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   if npcId == 30349 and st.getInt("cond")==0 and st.getInt("onlyone")==0 :
     if player.getRace().ordinal() != 2 :
       htmltext = "30349-00.htm"
     elif player.getLevel() >= 3 :
       htmltext = "30349-02.htm"
       return htmltext
     else:
       htmltext = "30349-01.htm"
       st.exitQuest(1)
   elif npcId == 30349 and st.getInt("cond")==0 and st.getInt("onlyone")==1 :
      htmltext = Quest.getAlreadyCompletedMsg(player)

   elif npcId == 30349 and st.getInt("cond")==1 and st.getQuestItemsCount(JENNIES_LETTER_ID) :
        htmltext = "30349-04.htm"
   elif npcId == 30349 and st.getInt("cond")==2 and st.getQuestItemsCount(SENTRY_BLADE1_ID)==1 and st.getQuestItemsCount(SENTRY_BLADE2_ID)==1 and st.getQuestItemsCount(SENTRY_BLADE3_ID)==1 :
        htmltext = "30349-05.htm"
        st.takeItems(SENTRY_BLADE1_ID,1)
        st.set("cond","3")
        st.playSound("ItemSound.quest_middle")
   elif npcId == 30349 and st.getInt("cond")==3 and st.getQuestItemsCount(SENTRY_BLADE1_ID)==0 and (st.getQuestItemsCount(SENTRY_BLADE2_ID)==1 or st.getQuestItemsCount(SENTRY_BLADE3_ID)==1) :
        htmltext = "30349-07.htm"
   elif npcId == 30349 and st.getInt("cond")==4 and st.getQuestItemsCount(OLD_BRONZE_SWORD_ID)==2 and st.getInt("onlyone")==0 :
        if st.getInt("id") != 168 :
          st.set("id","168")
          htmltext = "30349-06.htm"
          st.takeItems(OLD_BRONZE_SWORD_ID,2)
          st.set("cond","0")
          st.exitQuest(False)
          st.playSound("ItemSound.quest_finish")
          st.set("onlyone","1")
          st.giveItems(ADENA_ID,820)
   elif id == State.STARTED :       
       if npcId == 30360 and st.getInt("cond")==1 and st.getQuestItemsCount(JENNIES_LETTER_ID)==1 :
            htmltext = "30360-01.htm"
            st.takeItems(JENNIES_LETTER_ID,1)
            st.giveItems(SENTRY_BLADE1_ID,1)
            st.giveItems(SENTRY_BLADE2_ID,1)
            st.giveItems(SENTRY_BLADE3_ID,1)
            st.set("cond","2")
            st.playSound("ItemSound.quest_middle")
       elif npcId == 30360 and st.getInt("cond")==2 and (st.getQuestItemsCount(SENTRY_BLADE1_ID)+st.getQuestItemsCount(SENTRY_BLADE2_ID)+st.getQuestItemsCount(SENTRY_BLADE3_ID))>0 :
            htmltext = "30360-02.htm"
       elif npcId == 30355 and st.getInt("cond")==3 and st.getQuestItemsCount(SENTRY_BLADE2_ID)==1 and st.getQuestItemsCount(SENTRY_BLADE1_ID)==0 :
            htmltext = "30355-01.htm"
            st.takeItems(SENTRY_BLADE2_ID,1)
            st.giveItems(OLD_BRONZE_SWORD_ID,1)
            if st.getQuestItemsCount(OLD_BRONZE_SWORD_ID)==2:
               st.set("cond","4")
               st.playSound("ItemSound.quest_middle")
       elif npcId == 30355 and st.getInt("cond") in [3,4] and st.getQuestItemsCount(SENTRY_BLADE2_ID)==0 :
            htmltext = "30355-02.htm"
       elif npcId == 30357 and st.getInt("cond")==3 and st.getQuestItemsCount(SENTRY_BLADE3_ID)==1 and st.getQuestItemsCount(SENTRY_BLADE1_ID)==0 :
            htmltext = "30357-01.htm"
            st.takeItems(SENTRY_BLADE3_ID,1)
            st.giveItems(OLD_BRONZE_SWORD_ID,1)
            if st.getQuestItemsCount(OLD_BRONZE_SWORD_ID)==2:
               st.set("cond","4")
               st.playSound("ItemSound.quest_middle")
       elif npcId == 30357 and st.getInt("cond") in [3,4] and st.getQuestItemsCount(SENTRY_BLADE3_ID)==0 :
            htmltext = "30357-02.htm"
   return htmltext

QUEST       = Quest(168,qn,"Deliver Supplies")

QUEST.addStartNpc(30349)

QUEST.addTalkId(30349)

QUEST.addTalkId(30355)
QUEST.addTalkId(30357)
QUEST.addTalkId(30360)