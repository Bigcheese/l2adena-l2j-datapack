#  Created by Kerberos
import sys
from com.l2jserver.gameserver import GameTimeController
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest
from com.l2jserver.gameserver.network.serverpackets import NpcSay

qn = "24_InhabitantsOfTheForrestOfTheDead"

# Npcs
Dorian = 31389
Wizard = 31522
Tombstone = 31531
MaidOfLidia = 31532

#Items
Letter = 7065
Hairpin = 7148
Totem = 7151
Flower = 7152
SilverCross = 7153
BrokenSilverCross = 7154
SuspiciousTotem = 7156

def FindTemplate (npcId) :
    npcinstance = 0
    for spawn in SpawnTable.getInstance().getSpawnTable().values():
        if spawn :
            if spawn.getNpcid() == npcId:
                npcinstance=spawn.getLastSpawn()
                break
    return npcinstance

def AutoChat(npc,text) :
    chars = npc.getKnownList().getKnownPlayers().values().toArray()
    if chars != None:
       for pc in chars :
          sm = NpcSay(npc.getObjectId(), 0, npc.getNpcId(), text)
          pc.sendPacket(sm)

class Quest (JQuest) : 

    def __init__(self,id,name,descr):  
       JQuest.__init__(self,id,name,descr)
       self.questItemIds = [Flower,SilverCross,BrokenSilverCross,Letter,Hairpin,Totem]

    def onAdvEvent (self,event,npc,player) :
        st = player.getQuestState(qn)
        if not st: return
        htmltext = event
        if event == "31389-02.htm":
            st.giveItems(Flower,1)
            st.set("cond","1")
            st.playSound("ItemSound.quest_accept")
            st.setState(State.STARTED)
        elif event == "31389-11.htm":
            st.set("cond","3")
            st.playSound("ItemSound.quest_middle")
            st.giveItems(SilverCross,1)
        elif event == "31389-16.htm":
            st.playSound("InterfaceSound.charstat_open_01")
        elif event == "31389-17.htm":
            st.takeItems(BrokenSilverCross,-1)
            st.giveItems(Hairpin,1)
            st.set("cond","5")
        elif event == "31522-03.htm":
            st.takeItems(Totem,-1)
        elif event == "31522-07.htm":
            st.set("cond","11")
        elif event == "31522-19.htm":
            st.giveItems(SuspiciousTotem,1)
            st.addExpAndSp(242105,22529)
            st.exitQuest(False)
            st.playSound("ItemSound.quest_finish")
        elif event == "31531-02.htm":
            st.playSound("ItemSound.quest_middle")
            st.set("cond","2")
            st.takeItems(Flower,-1)
        elif event == "31532-04.htm":
            st.playSound("ItemSound.quest_middle")
            st.giveItems(Letter,1)
            st.set("cond","6")
        elif event == "31532-06.htm":
            st.takeItems(Hairpin,-1)
            st.takeItems(Letter,-1)
        elif event == "31532-16.htm":
            st.playSound("ItemSound.quest_middle")
            st.set("cond","9")
        return htmltext

    def onTalk (self,npc,player):
        htmltext = Quest.getNoQuestMsg(player)
        st = player.getQuestState(qn)
        if not st : return htmltext
        npcId = npc.getNpcId()
        state = st.getState()
        if state == State.COMPLETED :
            if npcId == Wizard :
                htmltext = "31522-20.htm"
            else:
                htmltext = Quest.getAlreadyCompletedMsg(player)
        cond = st.getInt("cond")
        if npcId == Dorian :
            if state == State.CREATED :
                st2 = st.getPlayer().getQuestState("23_LidiasHeart")
                if st2 :
                    if st2.getState() == State.COMPLETED and player.getLevel() >= 65 :
                        htmltext = "31389-01.htm"
                    else:
                        htmltext = "31389-00.htm"
                else:
                    htmltext = "31389-00.htm"
            elif cond == 1 :
                htmltext = "31389-03.htm"
            elif cond == 2 :
                htmltext = "31389-04.htm"
            elif cond == 3 :
                htmltext = "31389-12.htm"
            elif cond == 4 :
                htmltext = "31389-13.htm"
            elif cond == 5 :
                htmltext = "31389-18.htm"
        elif npcId == Tombstone :
            if cond == 1 :
                st.playSound("AmdSound.d_wind_loot_02")
                htmltext = "31531-01.htm"
            elif cond == 2 :
                htmltext = "31531-03.htm"
        elif npcId == MaidOfLidia :
            if cond == 5 :
                htmltext = "31532-01.htm"
            elif cond == 6 :
                if st.getQuestItemsCount(Letter) and st.getQuestItemsCount(Hairpin) :
                    htmltext = "31532-05.htm"
                else:
                    htmltext = "31532-07.htm"
            elif cond == 9 :
                htmltext = "31532-16.htm"
        elif npcId == Wizard :
            if cond == 10 :
                htmltext = "31522-01.htm"
            elif cond == 11 :
                htmltext = "31522-08.htm"
        return htmltext

    def onKill(self,npc,player,isPet):
        st = player.getQuestState(qn)
        if not st : return 
        if st.getState() != State.STARTED : return 
        npcId = npc.getNpcId()
        if not st.getQuestItemsCount(Totem) and st.getInt("cond") == 9:
            if npcId in [21557,21558,21560,21563,21564,21565,21566,21567] and st.getRandom(100) <=30:
                st.giveItems(Totem,1)
                st.set("cond","10")
                st.playSound("ItemSound.quest_middle")
        return

    def onAggroRangeEnter(self, npc, player, isPet) : 
       if npc.getNpcId() == 25332:
         if isPet: npc.getAggroList().remove(player.getPet())
         else :
          npc.getAggroList().remove(player)
          st = player.getQuestState(qn) 
          if st and st.getQuestItemsCount(SilverCross):
             st.takeItems(SilverCross,-1)
             st.giveItems(BrokenSilverCross,1)
             st.set("cond","4")
             AutoChat(npc,"That sign!")
       return

QUEST     = Quest(24,qn,"Inhabitants Of The Forrest Of The Dead")

QUEST.addStartNpc(Dorian)

QUEST.addTalkId(Dorian)
QUEST.addTalkId(Tombstone)
QUEST.addTalkId(MaidOfLidia)
QUEST.addTalkId(Wizard)
QUEST.addAggroRangeEnterId(25332)

for mob in [21557,21558,21560,21563,21564,21565,21566,21567]:
    QUEST.addKillId(mob)