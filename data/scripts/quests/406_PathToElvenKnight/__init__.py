# Made by Mr. - Version 0.3 by kmarty and DrLecter
# Shadow Weapon Coupons contributed by BiTi for the Official L2J Datapack Project
# Visit http://www.l2jdp.com/forum/ for more details
import sys
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest
from com.l2jserver.gameserver.network.serverpackets import SocialAction

qn = "406_PathToElvenKnight"

SORIUS_LETTER1 = 1202
KLUTO_BOX = 1203
ELVEN_KNIGHT_BROOCH = 1204
TOPAZ_PIECE = 1205
EMERALD_PIECE = 1206
KLUTO_MEMO = 1276

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [SORIUS_LETTER1, EMERALD_PIECE, TOPAZ_PIECE, KLUTO_MEMO, KLUTO_BOX]

 def onEvent (self,event,st) :
    htmltext = event
    player = st.getPlayer()
    if event == "30327-05.htm" :
       if player.getClassId().getId() != 0x12 :
          if player.getClassId().getId() == 0x13 :
             htmltext = "30327-02a.htm"
          else:
             htmltext = "30327-02.htm"
             st.exitQuest(1)
       else:
          if player.getLevel()<18 :
             htmltext = "30327-03.htm"
             st.exitQuest(1)
          else:
             if st.getQuestItemsCount(ELVEN_KNIGHT_BROOCH) :
                htmltext = "30327-04.htm"
    elif event == "30327-06.htm" :
       st.set("cond","1")
       st.setState(State.STARTED)
       st.playSound("ItemSound.quest_accept")
    elif event == "30317-02.htm" :
       if st.getInt("cond") == 3 :
          st.takeItems(SORIUS_LETTER1,-1)
          if st.getQuestItemsCount(KLUTO_MEMO) == 0 :
             st.giveItems(KLUTO_MEMO,1)
             st.set("cond","4")
          else :
             htmltext = Quest.getNoQuestMsg(player)
       else :
          htmltext = Quest.getNoQuestMsg(player)
    return htmltext

 def onTalk (self,npc,player):
   htmltext = Quest.getNoQuestMsg(player)
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   if npcId != 30327 and id != State.STARTED : return htmltext

   if id == State.CREATED :
     st.set("cond","0")
     cond=0
   else :
     cond=st.getInt("cond")
   if npcId == 30327 :
        if cond == 0 :
            htmltext = "30327-01.htm"
        elif cond == 1 :
            if st.getQuestItemsCount(TOPAZ_PIECE)==0 :
              htmltext = "30327-07.htm"
            else:
              htmltext = "30327-08.htm"
        elif cond == 2 :
            if st.getQuestItemsCount(SORIUS_LETTER1) == 0 :
              st.giveItems(SORIUS_LETTER1,1)
            st.set("cond","3")
            htmltext = "30327-09.htm"
        elif cond in [3, 4, 5] :
            htmltext = "30327-11.htm"
        elif cond == 6 :
            st.takeItems(KLUTO_BOX,-1)
            isFinished = st.getGlobalQuestVar("1ClassQuestFinished")
            if isFinished == "" : 
              if player.getLevel() >= 20 :
                st.addExpAndSp(320534, 23152)
              elif player.getLevel() == 19 :
                st.addExpAndSp(456128, 29850)
              else:
                st.addExpAndSp(591724, 33328)
              st.giveItems(57, 163800)
            player.sendPacket(SocialAction(player,3))
            st.set("cond","0")
            st.exitQuest(False)
            st.playSound("ItemSound.quest_finish")
            st.saveGlobalQuestVar("1ClassQuestFinished","1")
            if st.getQuestItemsCount(ELVEN_KNIGHT_BROOCH) == 0 :
              st.giveItems(ELVEN_KNIGHT_BROOCH,1)
            htmltext = "30327-10.htm"
   elif npcId == 30317 :
        if cond == 3 :
            htmltext = "30317-01.htm"
        elif  cond == 4 :
            if st.getQuestItemsCount(EMERALD_PIECE)==0 :
              htmltext = "30317-03.htm"
            else:
              htmltext = "30317-04.htm"
        elif cond == 5 :
            st.takeItems(EMERALD_PIECE,-1)
            st.takeItems(TOPAZ_PIECE,-1)
            if st.getQuestItemsCount(KLUTO_BOX) == 0 :
              st.giveItems(KLUTO_BOX,1)
            st.takeItems(KLUTO_MEMO,-1)
            st.set("cond","6")
            htmltext = "30317-05.htm"
        elif cond == 6 :
            htmltext = "30317-06.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st : return 
   if st.getState() != State.STARTED : return 
   
   npcId = npc.getNpcId()
   if npcId != 20782 :
        if st.getInt("cond")==1 and st.getQuestItemsCount(TOPAZ_PIECE)<20 and st.getRandom(100)<70 :
            st.giveItems(TOPAZ_PIECE,1)
            if st.getQuestItemsCount(TOPAZ_PIECE) == 20 :
              st.playSound("ItemSound.quest_middle")
              st.set("cond","2")
            else:
              st.playSound("ItemSound.quest_itemget")
   else :
        if st.getInt("cond")==4 and st.getQuestItemsCount(EMERALD_PIECE)<20 and st.getRandom(100)<50 :
            st.giveItems(EMERALD_PIECE,1)
            if st.getQuestItemsCount(EMERALD_PIECE) == 20 :
              st.playSound("ItemSound.quest_middle")
              st.set("cond","5")
            else:
              st.playSound("ItemSound.quest_itemget")
   return

QUEST       = Quest(406,qn,"Path of the Elven Knight")

QUEST.addStartNpc(30327)

QUEST.addTalkId(30327)

QUEST.addTalkId(30317)
QUEST.addTalkId(30327)

QUEST.addKillId(20035)
QUEST.addKillId(20042)
QUEST.addKillId(20045)
QUEST.addKillId(20051)
QUEST.addKillId(20054)
QUEST.addKillId(20060)
QUEST.addKillId(20782)