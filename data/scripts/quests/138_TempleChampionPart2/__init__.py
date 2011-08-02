# Made by Kerberos
# this script is part of the Official L2J Datapack Project.
# Visit http://www.l2jdp.com/forum/ for more details.
import sys
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "138_TempleChampionPart2"

# NPCs
SYLVAIN = 30070
PUPINA = 30118
ANGUS = 30474
SLA = 30666

# ITEMs
MANIFESTO = 10341
RELIC = 10342
ANGUS_REC = 10343
PUPINA_REC = 10344

# MONSTERs
NPC=[20176,20550,20551,20552]

class Quest (JQuest) :

 def __init__(self,id,name,descr):
    JQuest.__init__(self,id,name,descr)
    self.questItemIds = [MANIFESTO,RELIC,ANGUS_REC,PUPINA_REC]

 def onAdvEvent (self,event,npc, player) :
    htmltext = event
    st = player.getQuestState(qn)
    if not st : return
    id = st.getState()
    cond = st.getInt("cond")
    if event == "30070-02.htm" :
       st.set("cond","1")
       st.playSound("ItemSound.quest_accept")
       st.giveItems(MANIFESTO, 1)
    elif event == "30070-05.htm" :
       st.giveItems(57, 84593)
       st.playSound("ItemSound.quest_finish")
       st.exitQuest(False)
       if st.getPlayer().getLevel() >= 36 and st.getPlayer().getLevel() <= 41:
          st.addExpAndSp(187062,11307)
    elif event == "30070-03.htm" :
       st.set("cond","2")
       st.playSound("ItemSound.quest_middle")
    elif event == "30118-06.htm" :
       st.set("cond","3")
       st.playSound("ItemSound.quest_middle")
    elif event == "30118-09.htm" :
       st.set("cond","6")
       st.playSound("ItemSound.quest_middle")
       st.set("talk","0")
       st.giveItems(PUPINA_REC, 1)
    elif event == "30474-02.htm" :
       st.set("cond","4")
       st.playSound("ItemSound.quest_middle")
    elif event == "30666-02.htm" :
       st.set("talk","1")
       st.takeItems(PUPINA_REC, -1)
    elif event == "30666-03.htm" :
       st.set("talk","2")
       st.takeItems(MANIFESTO, -1)
    elif event == "30666-08.htm" :
       st.set("cond","7")
       st.playSound("ItemSound.quest_middle")
       st.unset("talk")
    return htmltext

 def onTalk (self,npc,player):
    htmltext = Quest.getNoQuestMsg(player)
    st = player.getQuestState(qn)
    if not st : return htmltext

    npcId = npc.getNpcId()
    id = st.getState()
    cond = st.getInt("cond")
    if id == State.CREATED : return htmltext
    if id == State.COMPLETED :
       htmltext = Quest.getAlreadyCompletedMsg(player)
    elif npcId == SYLVAIN :
       if cond == 0 :
          if player.getLevel() >= 36:
             htmltext = "30070-01.htm"
          else:
             htmltext = "30070-00.htm"
             st.exitQuest(1)
       elif cond == 1 :
          htmltext = "30070-02.htm"
       elif cond in [2,3,4,5,6] :
          htmltext = "30070-03.htm"
       elif cond == 7 :
          htmltext = "30070-04.htm"
    elif npcId == PUPINA :
       if cond == 2 :
          htmltext = "30118-01.htm"
       elif cond in [3,4] :
          htmltext = "30118-07.htm"
       elif cond == 5 :
          htmltext = "30118-08.htm"
          st.takeItems(ANGUS_REC, -1)
       elif cond == 6 :
          htmltext = "30118-10.htm"
    elif npcId == ANGUS :
       if cond == 3 :
          htmltext = "30474-01.htm"
       elif cond == 4 :
          if st.getQuestItemsCount(RELIC) >= 10:
             htmltext = "30474-04.htm"
             st.takeItems(RELIC, -1)
             st.giveItems(ANGUS_REC, 1)
             st.set("cond","5")
             st.playSound("ItemSound.quest_middle")
          else:
             htmltext = "30474-03.htm"
       elif cond == 5 :
          htmltext = "30474-05.htm"
    elif npcId == SLA :
       if cond == 6 :
          if st.getInt("talk") == 0:
             htmltext = "30666-01.htm"
          elif st.getInt("talk") == 1:
             htmltext = "30666-02.htm"
          elif st.getInt("talk") == 2:
             htmltext = "30666-03.htm"
       elif cond == 7 :
          htmltext = "30666-09.htm"
    return htmltext

 def onKill(self,npc,player,isPet):
    st = player.getQuestState(qn)
    if not st : return
    if st.getState() != State.STARTED : return
    if st.getInt("cond")==4 :
       if st.getQuestItemsCount(RELIC) < 10:
          st.giveItems(RELIC,1)
          if st.getQuestItemsCount(RELIC) >= 10:
             st.playSound("ItemSound.quest_middle")
          else :
             st.playSound("ItemSound.quest_itemget")
    return

 def onFirstTalk (self,npc,player):
   st = player.getQuestState(qn)
   if not st :
      st = self.newQuestState(player)
   qs = st.getPlayer().getQuestState("137_TempleChampionPart1")
   if qs :
      if qs.getState() == State.COMPLETED and st.getState() == State.CREATED :
          st.setState(State.STARTED)
   npc.showChatWindow(player)
   return

QUEST       = Quest(138,qn,"Temple Champion - 2")

QUEST.addFirstTalkId(SYLVAIN) #this quest doesnt have starter npc, quest will appear in list only when u finish quest 137
QUEST.addTalkId(SYLVAIN)
QUEST.addTalkId(PUPINA)
QUEST.addTalkId(ANGUS)
QUEST.addTalkId(SLA)
for mob in NPC :
   QUEST.addKillId(mob)