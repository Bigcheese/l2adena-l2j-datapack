# Made by Kerberos
# this script is part of the Official L2J Datapack Project.
# Visit http://www.l2jdp.com/forum/ for more details.
import sys
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "137_TempleChampionPart1"

# NPCs
SYLVAIN = 30070

# ITEMs
FRAGMENT = 10340

# MONSTERs
NPC=[20083,20144,20199,20200,20201,20202]

class Quest (JQuest) :

 def __init__(self,id,name,descr):
    JQuest.__init__(self,id,name,descr)
    self.questItemIds = [FRAGMENT]

 def onAdvEvent (self,event,npc, player) :
    htmltext = event
    st = player.getQuestState(qn)
    if not st : return
    id = st.getState()
    cond = st.getInt("cond")
    if event == "30070-02.htm" :
       st.set("cond","1")
       st.setState(State.STARTED)
       st.set("talk","0")
       st.playSound("ItemSound.quest_accept")
    elif event == "30070-05.htm" :
       st.set("talk","1")
    elif event == "30070-06.htm" :
       st.set("talk","2")
    elif event == "30070-08.htm" :
       st.unset("talk")
       st.set("cond","2")
       st.playSound("ItemSound.quest_middle")
    elif event == "30070-16.htm" :
       st.takeItems(10334, -1)
       st.takeItems(10339, -1)
       st.giveItems(57, 69146)
       st.playSound("ItemSound.quest_finish")
       st.unset("talk")
       st.exitQuest(False)
       if st.getPlayer().getLevel() >= 35 and st.getPlayer().getLevel() <= 40:
          st.addExpAndSp(219975,13047)
    return htmltext

 def onTalk (self,npc,player):
    htmltext = Quest.getNoQuestMsg(player)
    st = player.getQuestState(qn)
    if not st : return htmltext

    npcId = npc.getNpcId()
    id = st.getState()
    cond = st.getInt("cond")
    if id == State.COMPLETED :
       htmltext = Quest.getAlreadyCompletedMsg(player)
    elif npcId == SYLVAIN :
       if cond == 0 :
          if player.getLevel() >= 35 and st.getQuestItemsCount(10334) and st.getQuestItemsCount(10339):
             htmltext = "30070-01.htm"
          else:
             htmltext = "30070-00.htm"
             st.exitQuest(1)
       elif cond == 1 :
          if st.getInt("talk") == 0:
             htmltext = "30070-03.htm"
          elif st.getInt("talk") == 1:
             htmltext = "30070-05.htm"
          elif st.getInt("talk") == 2:
             htmltext = "30070-06.htm"
       elif cond == 2 :
          htmltext = "30070-08.htm"
       elif cond == 3 and st.getQuestItemsCount(FRAGMENT) >= 30:
          htmltext = "30070-09.htm"
          st.set("talk","1")
          st.takeItems(FRAGMENT, -1)
       elif cond == 3 and st.getInt("talk") == 1:
          htmltext = "30070-10.htm"
    return htmltext

 def onKill(self,npc,player,isPet):
    st = player.getQuestState(qn)
    if not st : return
    if st.getState() != State.STARTED : return
    if st.getInt("cond")==2 :
       if st.getQuestItemsCount(FRAGMENT) < 30:
          st.giveItems(FRAGMENT,1)
          if st.getQuestItemsCount(FRAGMENT) >= 30:
             st.set("cond","3")
             st.playSound("ItemSound.quest_middle")
          else :
             st.playSound("ItemSound.quest_itemget")
    return

QUEST       = Quest(137,qn,"Temple Champion - 1")

QUEST.addStartNpc(SYLVAIN)
QUEST.addTalkId(SYLVAIN)
for mob in NPC :
   QUEST.addKillId(mob)