# Made by Kerberos v1.0 on 2009/23/02
# this script is part of the Official L2J Datapack Project.
# Visit http://www.l2jdp.com/forum for more details.

import sys

from com.l2jserver.gameserver.model.quest			import State
from com.l2jserver.gameserver.model.quest			import QuestState
from com.l2jserver.gameserver.model.quest.jython		import QuestJython as JQuest

qn = "187_Nikolas_Heart"

#NPCs
Kusto = 30512
Nikola = 30621
Lorain = 30673

#Items
Certificate = 10362
Metal = 10368

class Quest (JQuest) :
    def __init__(self,id,name,descr):
        JQuest.__init__(self,id,name,descr)
        self.questItemIds = [Certificate,Metal]

    def onAdvEvent (self,event,npc, player) :
        st = player.getQuestState(qn)
        if not st: return
        htmltext = event
        if event == "30673-02.htm" :
            st.playSound("ItemSound.quest_accept")
            st.set("cond","1")
            st.takeItems(Certificate,-1)
            st.giveItems(Metal,1)
        elif event == "30621-03.htm":
            st.set("cond","2")
            st.playSound("ItemSound.quest_middle")
        elif event == "30512-03.htm":
            if player.getLevel() < 50 :
               st.addExpAndSp(285935,18711)
            st.giveItems(57,93383)
            st.exitQuest(False)
            st.playSound("ItemSound.quest_finish")
        return htmltext

    def onTalk (self,npc,player):
        htmltext = Quest.getNoQuestMsg(player)
        st = player.getQuestState(qn)
        if not st : return htmltext
        npcId = npc.getNpcId()
        id = st.getState()
        cond = st.getInt("cond")
        if id == State.COMPLETED:
            htmltext = Quest.getAlreadyCompletedMsg(player)
        elif id == State.STARTED:
            if npcId == Lorain:
                if not cond :
                    if player.getLevel() < 41 :
                        htmltext = "30673-00.htm"
                    else :
                        htmltext = "30673-01.htm"
                elif cond == 1 :
                    htmltext = "30673-03.htm"
            elif npcId == Nikola :
                if cond == 1 :
                    htmltext = "30621-01.htm"
                elif cond == 2 :
                    htmltext = "30621-04.htm"
            elif npcId == Kusto :
                if cond == 2 :
                    htmltext = "30512-01.htm"
        return htmltext

QUEST       = Quest(187,qn,"Nikola's Heart")

QUEST.addTalkId(Nikola)
QUEST.addTalkId(Lorain)
QUEST.addTalkId(Kusto)