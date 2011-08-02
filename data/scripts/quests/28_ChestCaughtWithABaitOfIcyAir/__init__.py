### ---------------------------------------------------------------------------
###  Create by Skeleton!!!
### ---------------------------------------------------------------------------
import sys
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "28_ChestCaughtWithABaitOfIcyAir"

# NPC List
OFulle=31572
Kiki=31442
# ~~~
# Item List
BigYellowTreasureChest=6503
KikisLetter=7626
ElvenRing=881
# ~~~
class Quest (JQuest) :
    def __init__(self,id,name,descr): JQuest.__init__(self,id,name,descr)
    def onAdvEvent (self,event,npc, player) :
        htmltext = event
        st = player.getQuestState(qn)
        if not st : return
        if event=="31572-04.htm" :
            st.set("cond","1")
            st.playSound("ItemSound.quest_accept")
        elif event=="31572-07.htm" :
            if st.getQuestItemsCount(BigYellowTreasureChest) :
                st.set("cond","2")
                st.takeItems(BigYellowTreasureChest,1)
                st.giveItems(KikisLetter,1)
            else :
                htmltext="31572-08.htm"
        elif event=="31442-02.htm" :
            if st.getQuestItemsCount(KikisLetter)==1 :
                htmltext="31442-02.htm"
                st.takeItems(KikisLetter,-1)
                st.giveItems(ElvenRing,1)
                st.set("cond","0")
                st.exitQuest(False)
                st.playSound("ItemSound.quest_finish")
            else :
                htmltext="31442-03.htm"
        return htmltext

    def onTalk (self,npc,player):
        htmltext = Quest.getNoQuestMsg(player)
        st = player.getQuestState(qn)
        if not st : return htmltext
        npcId = npc.getNpcId()
        id=st.getState()
        if id==State.CREATED :
            st.setState(State.STARTED)
            st.set("cond","0")
        cond=st.getInt("cond")
        id = st.getState()
        if npcId==OFulle :
            if cond==0 and id==State.STARTED:
                PlayerLevel = player.getLevel()
                if PlayerLevel >= 36 :
                    OFullesSpecialBait= player.getQuestState("51_OFullesSpecialBait")
                    if OFullesSpecialBait :
                        if OFullesSpecialBait.getState() == State.COMPLETED :
                            htmltext="31572-01.htm"
                        else :
                            htmltext="31572-02.htm"
                            st.exitQuest(1)
                    else :
                        htmltext="31572-03.htm"
                        st.exitQuest(1)
                else :
                    htmltext="31572-02.htm"
            elif cond==1 :
                htmltext="31572-05.htm"
                if st.getQuestItemsCount(BigYellowTreasureChest)==0 :
                    htmltext="31572-06.htm"
            elif cond==2 :
                htmltext="31572-09.htm"
            elif cond==0 and id==State.COMPLETED :
                htmltext=Quest.getAlreadyCompletedMsg(player)

        elif npcId==Kiki :
            if cond==2 :
                htmltext="31442-01.htm"
        return htmltext

QUEST      = Quest(28,qn,"Chest Caught With A Bait Of Icy Air")


QUEST.addStartNpc(OFulle)
QUEST.addTalkId(OFulle)
QUEST.addTalkId(Kiki)
