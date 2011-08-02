# Made by Mr. Have fun! Version 0.2
import sys
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "154_SacrificeToSea"

FOX_FUR_ID = 1032
FOX_FUR_YARN_ID = 1033
MAIDEN_DOLL_ID = 1034
EARING_ID = 113

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [FOX_FUR_ID, FOX_FUR_YARN_ID, MAIDEN_DOLL_ID]

 def onAdvEvent (self,event,npc, player) :
    htmltext = event
    st = player.getQuestState(qn)
    if not st : return
    if event == "1" :
        st.set("id","0")
        htmltext = "30312-04.htm"
        st.set("cond","1")
        st.setState(State.STARTED)
        st.playSound("ItemSound.quest_accept")
    return htmltext


 def onTalk (self,npc,player):
   htmltext = Quest.getNoQuestMsg(player)
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   if npcId == 30312 and st.getInt("cond")==0 and st.getInt("onlyone")==0 :
      if player.getLevel() >= 2 :
        htmltext = "30312-03.htm"
        return htmltext
      else:
        htmltext = "30312-02.htm"
        st.exitQuest(1)
   elif npcId == 30312 and st.getInt("cond")==0 and st.getInt("onlyone")==1 :
        htmltext = Quest.getAlreadyCompletedMsg(player)

   if id == State.STARTED:     
       if npcId == 30312 and st.getInt("cond")>=1 and (st.getQuestItemsCount(FOX_FUR_YARN_ID)==0 and st.getQuestItemsCount(MAIDEN_DOLL_ID)==0) and st.getQuestItemsCount(FOX_FUR_ID)<10 :
            htmltext = "30312-05.htm"
       elif npcId == 30312 and st.getInt("cond")>=1 and st.getQuestItemsCount(FOX_FUR_ID)>=10 :
            htmltext = "30312-08.htm"
       elif npcId == 30051 and st.getInt("cond")>=1 and st.getQuestItemsCount(FOX_FUR_ID)<10 and st.getQuestItemsCount(FOX_FUR_ID)>0 :
            htmltext = "30051-01.htm"
       elif npcId == 30051 and st.getInt("cond")>=1 and st.getQuestItemsCount(FOX_FUR_ID)>=10 and st.getQuestItemsCount(FOX_FUR_YARN_ID)==0 and st.getQuestItemsCount(MAIDEN_DOLL_ID)==0 and st.getQuestItemsCount(MAIDEN_DOLL_ID)<10 :
            htmltext = "30051-02.htm"
            st.giveItems(FOX_FUR_YARN_ID,1)
            st.takeItems(FOX_FUR_ID,st.getQuestItemsCount(FOX_FUR_ID))
            st.set("cond","3")
            st.playSound("ItemSound.quest_middle")
       elif npcId == 30051 and st.getInt("cond")>=1 and st.getQuestItemsCount(FOX_FUR_YARN_ID)>=1 :
            htmltext = "30051-03.htm"
       elif npcId == 30051 and st.getInt("cond")>=1 and st.getQuestItemsCount(MAIDEN_DOLL_ID)==1 :
            htmltext = "30051-04.htm"
       elif npcId == 30312 and st.getInt("cond")>=1 and st.getQuestItemsCount(FOX_FUR_YARN_ID)>=1 :
            htmltext = "30312-06.htm"
       elif npcId == 30055 and st.getInt("cond")>=1 and st.getQuestItemsCount(FOX_FUR_YARN_ID)>=1 :
            htmltext = "30055-01.htm"
            st.giveItems(MAIDEN_DOLL_ID,1)
            st.takeItems(FOX_FUR_YARN_ID,st.getQuestItemsCount(FOX_FUR_YARN_ID))
            st.set("cond","4")
            st.playSound("ItemSound.quest_middle")
       elif npcId == 30055 and st.getInt("cond")>=1 and st.getQuestItemsCount(MAIDEN_DOLL_ID)>=1 :
            htmltext = "30055-02.htm"
       elif npcId == 30055 and st.getInt("cond")>=1 and st.getQuestItemsCount(FOX_FUR_YARN_ID)==0 and st.getQuestItemsCount(MAIDEN_DOLL_ID)==0 :
            htmltext = "30055-03.htm"
       elif npcId == 30312 and st.getInt("cond")>=1 and st.getQuestItemsCount(MAIDEN_DOLL_ID)>=1 and st.getInt("onlyone")==0 :
          if st.getInt("id") != 154 :
            st.set("id","154")
            htmltext = "30312-07.htm"
            st.giveItems(EARING_ID,1)
            st.takeItems(MAIDEN_DOLL_ID,-1)
            st.addExpAndSp(1000,0)
            st.set("cond","0")
            st.exitQuest(False)
            st.playSound("ItemSound.quest_finish")
            st.set("onlyone","1")
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st : return 
   if st.getState() != State.STARTED : return
   
   npcId = npc.getNpcId()
   if npcId == 20481 :
        st.set("id","0")
        if st.getInt("cond") >= 1 and st.getQuestItemsCount(FOX_FUR_ID)<10 and st.getQuestItemsCount(FOX_FUR_YARN_ID) == 0 :
          if st.getRandom(10)<4 :
            st.giveItems(FOX_FUR_ID,1)
            if st.getQuestItemsCount(FOX_FUR_ID) == 10 :
              st.playSound("ItemSound.quest_middle")
              st.set("cond","2")
            else:
              st.playSound("ItemSound.quest_itemget")
   elif npcId == 20545 :
        st.set("id","0")
        if st.getInt("cond") >= 1 and st.getQuestItemsCount(FOX_FUR_ID)<10 and st.getQuestItemsCount(FOX_FUR_YARN_ID) == 0 :
          if st.getRandom(10)<4 :
            st.giveItems(FOX_FUR_ID,1)
            if st.getQuestItemsCount(FOX_FUR_ID) == 10 :
              st.playSound("ItemSound.quest_middle")
              st.set("cond","2")
            else:
              st.playSound("ItemSound.quest_itemget")
   return

QUEST       = Quest(154,qn,"Sacrifice To Sea")

QUEST.addStartNpc(30312)

QUEST.addTalkId(30312)

QUEST.addTalkId(30051)
QUEST.addTalkId(30055)

QUEST.addKillId(20481)
QUEST.addKillId(20545)