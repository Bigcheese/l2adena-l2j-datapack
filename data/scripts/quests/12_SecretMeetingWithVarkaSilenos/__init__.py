#made by Emperorc
import sys
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "12_SecretMeetingWithVarkaSilenos"

#NPCs
Cadmon = 31296
Helmut = 31258
Naran = 31378

#Item
Box = 7232

class Quest (JQuest) :

 def __init__(self,id,name,descr): JQuest.__init__(self,id,name,descr)

 def onAdvEvent (self,event,npc, player) :
     htmltext = event
     st = player.getQuestState(qn)
     if not st : return
     if event == "31296-03.htm" :
         st.set("cond","1")
         st.setState(State.STARTED)
         st.playSound("ItemSound.quest_accept")
         htmltext = "31296-03.htm"
     elif event == "31258-02.htm" :
         st.set("cond","2")
         htmltext = "31258-02.htm"
         st.giveItems(Box,1)
     elif event == "31378-02.htm" :
         htmltext = "31378-02.htm"
         st.takeItems(Box,-1)
         st.addExpAndSp(233125,18142)
         st.set("cond","0")
         st.exitQuest(False)
         st.playSound("ItemSound.quest_finish")
     return htmltext

 def onTalk (self,npc,player):
     npcId = npc.getNpcId()
     htmltext = Quest.getNoQuestMsg(player)
     st = player.getQuestState(qn)
     if not st : return htmltext

     cond = st.getInt("cond")
     id = st.getState()
     if id == State.COMPLETED :
        htmltext = Quest.getAlreadyCompletedMsg(player)
     elif id == State.CREATED :
         if st.getPlayer().getLevel() >= 74 :
             htmltext = "31296-01.htm"
         else :
             htmltext = "31296-02.htm"
             st.exitQuest(1)
     elif id == State.STARTED :
         if npcId == Cadmon :
             if cond == 1 :
                 htmltext = "31296-04.htm"
         elif npcId == Helmut :
             if cond == 1 :
                 htmltext = "31258-01.htm"
             elif cond == 2 :
                 htmltext = "31258-03.htm"
         elif npcId == Naran and cond == 2 :
             htmltext = "31378-01.htm"
     return htmltext
     
QUEST       = Quest(12, qn, "Secret Meeting With Varka Silenos")


QUEST.addStartNpc(Cadmon)

QUEST.addTalkId(Cadmon)

QUEST.addTalkId(Helmut)
QUEST.addTalkId(Naran)