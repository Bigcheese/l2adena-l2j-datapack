# Made by Kerberos v1.0 on 2009/23/02
# this script is part of the Official L2J Datapack Project.
# Visit http://www.l2jdp.com/forum for more details.

import sys

from com.l2jserver.gameserver.model.quest			import State
from com.l2jserver.gameserver.model.quest			import QuestState
from com.l2jserver.gameserver.model.quest.jython		import QuestJython as JQuest

qn = "191_Vain_Conclusion"

#NPCs
Kusto = 30512
Dorothy = 30970
Lorain = 30673
Shegfield = 30068

#Items
Metal = 10371

class Quest (JQuest) :
    def __init__(self,id,name,descr):
        JQuest.__init__(self,id,name,descr)
        self.questItemIds = [Metal]

    def onAdvEvent (self,event,npc, player) :
        st = player.getQuestState(qn)
        if not st: return
        htmltext = event
        if event == "30970-03.htm" :
            st.playSound("ItemSound.quest_accept")
            st.set("cond","1")
            st.giveItems(Metal,1)
        elif event == "30673-02.htm":
            st.set("cond","2")
            st.playSound("ItemSound.quest_middle")
            st.takeItems(Metal,-1)
        elif event == "30068-03.htm":
            st.set("cond","3")
            st.playSound("ItemSound.quest_middle")
        elif event == "30512-02.htm":
            if player.getLevel() < 50 :
               st.addExpAndSp(309467,20614)
            st.giveItems(57,117327)
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
            if npcId == Dorothy:
                if not cond :
                    if player.getLevel() < 42 :
                        htmltext = "30970-00.htm"
                    else :
                        htmltext = "30970-01.htm"
                elif cond  == 1:
                    htmltext = "30970-04.htm"
            elif npcId == Lorain:
                if cond == 1 :
                    htmltext = "30673-01.htm"
                elif cond == 2 :
                    htmltext = "30673-03.htm"
                elif cond == 3 :
                    htmltext = "30673-04.htm"
                    st.set("cond","4")
                    st.playSound("ItemSound.quest_middle")
                elif cond == 4 :
                    htmltext = "30673-05.htm"
            elif npcId == Shegfield:
                if cond == 2 :
                    htmltext = "30068-01.htm"
                elif cond == 3 :
                    htmltext = "30068-04.htm"
            elif npcId == Kusto:
                if cond == 4 :
                    htmltext = "30512-01.htm"
        return htmltext

    def onFirstTalk (self,npc,player):
       st = player.getQuestState(qn)
       qs = player.getQuestState("188_Seal_Removal")
       if not st and qs and qs.getState() == State.COMPLETED:
           st = self.newQuestState(player)
           st.setState(State.STARTED)
       npc.showChatWindow(player)
       return None

QUEST       = Quest(191,qn,"Vain Conclusion")

QUEST.addTalkId(Kusto)
QUEST.addTalkId(Lorain)
QUEST.addTalkId(Dorothy)
QUEST.addTalkId(Shegfield)
QUEST.addFirstTalkId(Dorothy)