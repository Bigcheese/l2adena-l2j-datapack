# Made by Mr. Have fun! Version 0.2
# Shadow Weapon Coupons contributed by BiTi for the Official L2J Datapack Project
# Visit http://www.l2jdp.com/forum/ for more details
import sys
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest
from com.l2jserver.gameserver.network.serverpackets import SocialAction

qn = "410_PathToPalusKnight"

PALLUS_TALISMAN = 1237
LYCANTHROPE_SKULL = 1238
VIRGILS_LETTER = 1239
MORTE_TALISMAN = 1240
PREDATOR_CARAPACE = 1241
TRIMDEN_SILK = 1242
COFFIN_ETERNAL_REST = 1243
GAZE_OF_ABYSS = 1244

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = range(1237,1244)

 def onEvent (self,event,st) :
    htmltext = event
    level = st.getPlayer().getLevel()
    classId = st.getPlayer().getClassId().getId()
    if event == "1" :
        st.set("id","0")
        st.set("cond","1")
        st.setState(State.STARTED)
        st.playSound("ItemSound.quest_accept")
        htmltext = "30329-06.htm"
        st.giveItems(PALLUS_TALISMAN,1)
    elif event == "410_1" :
          if level >= 18 and classId == 0x1f and st.getQuestItemsCount(GAZE_OF_ABYSS) == 0 :
            htmltext = "30329-05.htm"
            return htmltext
          elif classId != 0x1f :
              if classId == 0x20 :
                htmltext = "30329-02a.htm"
              else:
                htmltext = "30329-03.htm"
          elif level<18 and classId == 0x1f :
              htmltext = "30329-02.htm"
          elif level >= 18 and classId == 0x1f and st.getQuestItemsCount(GAZE_OF_ABYSS) == 1 :
              htmltext = "30329-04.htm"
    elif event == "30329_2" :
            htmltext = "30329-10.htm"
            st.takeItems(PALLUS_TALISMAN,1)
            st.takeItems(LYCANTHROPE_SKULL,st.getQuestItemsCount(LYCANTHROPE_SKULL))
            st.giveItems(VIRGILS_LETTER,1)
            st.set("cond","3")
            st.playSound("ItemSound.quest_middle")
    elif event == "30422_1" :
          htmltext = "30422-02.htm"
          st.takeItems(VIRGILS_LETTER,1)
          st.giveItems(MORTE_TALISMAN,1)
          st.set("cond","4")
          st.playSound("ItemSound.quest_middle")
    elif event == "30422_2" :
            htmltext = "30422-06.htm"
            st.takeItems(MORTE_TALISMAN,1)
            st.takeItems(TRIMDEN_SILK,st.getQuestItemsCount(TRIMDEN_SILK))
            st.takeItems(PREDATOR_CARAPACE,st.getQuestItemsCount(PREDATOR_CARAPACE))
            st.giveItems(COFFIN_ETERNAL_REST,1)
            st.set("cond","6")
            st.playSound("ItemSound.quest_middle")
    return htmltext


 def onTalk (self,npc,player):
   htmltext = Quest.getNoQuestMsg(player)
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   if npcId != 30329 and id != State.STARTED : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   if npcId == 30329 and st.getInt("cond")==0 :
        htmltext = "30329-01.htm"
   elif npcId == 30329 and st.getInt("cond") :
        if st.getQuestItemsCount(PALLUS_TALISMAN) == 1 and st.getQuestItemsCount(LYCANTHROPE_SKULL) == 0 :
          htmltext = "30329-07.htm"
        elif st.getQuestItemsCount(PALLUS_TALISMAN) == 1 and st.getQuestItemsCount(LYCANTHROPE_SKULL)>0 and st.getQuestItemsCount(LYCANTHROPE_SKULL)<13 :
            htmltext = "30329-08.htm"
        elif st.getQuestItemsCount(PALLUS_TALISMAN) == 1 and st.getQuestItemsCount(LYCANTHROPE_SKULL) >= 13 :
            htmltext = "30329-09.htm"
        elif st.getQuestItemsCount(COFFIN_ETERNAL_REST) == 1 :
            htmltext = "30329-11.htm"
            st.takeItems(COFFIN_ETERNAL_REST,1)
            st.giveItems(GAZE_OF_ABYSS,1)
            isFinished = st.getGlobalQuestVar("1ClassQuestFinished")
            if isFinished == "" : 
              if player.getLevel() >= 20 :
                st.addExpAndSp(320534, 26212)
              elif player.getLevel() == 19 :
                st.addExpAndSp(456128, 32910)
              else:
                st.addExpAndSp(591724, 39608)
              st.giveItems(57, 163800)
            player.sendPacket(SocialAction(player,3))
            st.set("cond","0")
            st.exitQuest(False)
            st.saveGlobalQuestVar("1ClassQuestFinished","1")
            st.playSound("ItemSound.quest_finish")
        elif st.getQuestItemsCount(MORTE_TALISMAN) or st.getQuestItemsCount(VIRGILS_LETTER) :
            htmltext = "30329-12.htm"
   elif npcId == 30422 and st.getInt("cond") :
        if st.getQuestItemsCount(VIRGILS_LETTER) :
          htmltext = "30422-01.htm"
        elif st.getQuestItemsCount(MORTE_TALISMAN) and st.getQuestItemsCount(TRIMDEN_SILK) == 0 and st.getQuestItemsCount(PREDATOR_CARAPACE) == 0 :
            htmltext = "30422-03.htm"
        elif st.getQuestItemsCount(MORTE_TALISMAN) and st.getQuestItemsCount(TRIMDEN_SILK)>0 and st.getQuestItemsCount(PREDATOR_CARAPACE) == 0 :
            htmltext = "30422-04.htm"
        elif st.getQuestItemsCount(MORTE_TALISMAN) and st.getQuestItemsCount(TRIMDEN_SILK) == 0 and st.getQuestItemsCount(PREDATOR_CARAPACE)>0 :
            htmltext = "30422-04.htm"
        elif st.getQuestItemsCount(MORTE_TALISMAN) and st.getQuestItemsCount(TRIMDEN_SILK) >= 5 and st.getQuestItemsCount(PREDATOR_CARAPACE)>0 :
            htmltext = "30422-05.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st : return 
   if st.getState() != State.STARTED : return 
   
   npcId = npc.getNpcId()
   if npcId == 20049 :
        st.set("id","0")
        if st.getInt("cond") and st.getQuestItemsCount(PALLUS_TALISMAN) == 1 and st.getQuestItemsCount(LYCANTHROPE_SKULL)<13 :
          st.giveItems(LYCANTHROPE_SKULL,1)
          if st.getQuestItemsCount(LYCANTHROPE_SKULL) == 13 :
            st.playSound("ItemSound.quest_middle")
            st.set("cond","2")
          else:
            st.playSound("ItemSound.quest_itemget")
   elif npcId == 20038 :
        st.set("id","0")
        if st.getInt("cond") and st.getQuestItemsCount(MORTE_TALISMAN) == 1 and st.getQuestItemsCount(PREDATOR_CARAPACE)<1 :
          st.giveItems(PREDATOR_CARAPACE,1)
          st.playSound("ItemSound.quest_middle")
          if st.getQuestItemsCount(TRIMDEN_SILK) >= 5 and st.getQuestItemsCount(PREDATOR_CARAPACE)>0 :
            st.set("cond","5")
   elif npcId == 20043 :
        st.set("id","0")
        if st.getInt("cond") and st.getQuestItemsCount(MORTE_TALISMAN) == 1 and st.getQuestItemsCount(TRIMDEN_SILK)<5 :
          st.giveItems(TRIMDEN_SILK,1)
          if st.getQuestItemsCount(TRIMDEN_SILK) == 5 :
            st.playSound("ItemSound.quest_middle")
            if st.getQuestItemsCount(TRIMDEN_SILK) >= 5 and st.getQuestItemsCount(PREDATOR_CARAPACE)>0 :
              st.set("cond","5")
          else:
            st.playSound("ItemSound.quest_itemget")
   return

QUEST       = Quest(410,qn,"Path of the Palus Knight")

QUEST.addStartNpc(30329)

QUEST.addTalkId(30329)

QUEST.addTalkId(30422)

QUEST.addKillId(20038)
QUEST.addKillId(20043)
QUEST.addKillId(20049)