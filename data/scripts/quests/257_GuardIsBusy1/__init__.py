# Made by Mr. Have fun! - Version 0.3 by DrLecter
import sys
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "257_GuardIsBusy1"

GLUDIO_LORDS_MARK = 1084
ORC_AMULET = 752
ORC_NECKLACE = 1085
WEREWOLF_FANG = 1086
ADENA = 57
#Newbie/one time rewards section
#Any quest should rely on a unique bit, but
#it could be shared among quest that were mutually
#exclusive or race restricted.
#Bit #1 isn't used for backwards compatibility.
NEWBIE_REWARD = 4
SPIRITSHOT_FOR_BEGINNERS = 5790
SOULSHOT_FOR_BEGINNERS = 5789

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [ORC_AMULET, ORC_NECKLACE, WEREWOLF_FANG, GLUDIO_LORDS_MARK]

 def onAdvEvent (self,event,npc, player) :
    htmltext = event
    st = player.getQuestState(qn)
    if not st : return
    if event == "30039-03.htm" :
      st.set("cond","1")
      st.setState(State.STARTED)
      st.playSound("ItemSound.quest_accept")
      st.giveItems(GLUDIO_LORDS_MARK,1)
    elif event == "30039-05.htm" :
      st.takeItems(GLUDIO_LORDS_MARK,1)
      st.exitQuest(1)
      st.playSound("ItemSound.quest_finish")
    return htmltext

 def onTalk (self,npc,player):
   htmltext = Quest.getNoQuestMsg(player)
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   if id == State.CREATED :
     st.set("cond","0")
   if st.getInt("cond")==0 :
     if player.getLevel() >= 6 :
       htmltext = "30039-02.htm"
     else:
       htmltext = "30039-01.htm"
       st.exitQuest(1)
   else :
     orc_a=st.getQuestItemsCount(ORC_AMULET)
     orc_n=st.getQuestItemsCount(ORC_NECKLACE)
     wer_f=st.getQuestItemsCount(WEREWOLF_FANG)
     if orc_a==orc_n==wer_f==0 :
       htmltext = "30039-04.htm"
     else :
       # check the player state against this quest newbie rewarding mark.
       newbie = player.getNewbie()
       if newbie | NEWBIE_REWARD != newbie :
          player.setNewbie(newbie|NEWBIE_REWARD)
          st.showQuestionMark(26)
          if player.getClassId().isMage() :
             st.playTutorialVoice("tutorial_voice_027")
             st.giveItems(SPIRITSHOT_FOR_BEGINNERS,3000)
          else :
             st.playTutorialVoice("tutorial_voice_026")
             st.giveItems(SOULSHOT_FOR_BEGINNERS,6000)
       st.giveItems(ADENA,5*orc_a+15*orc_n+10*wer_f)
       st.takeItems(ORC_AMULET,-1)
       st.takeItems(ORC_NECKLACE,-1)
       st.takeItems(WEREWOLF_FANG,-1)
       htmltext = "30039-07.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st : return 
   if st.getState() != State.STARTED : return 
   
   npcId = npc.getNpcId()
   chance=5
   if npcId in [20130,20131,20006] :
     item = ORC_AMULET
   elif npcId in [20093,20096,20098] :
     item = ORC_NECKLACE
   else :
     item = WEREWOLF_FANG
     if npcId == 20343 : chance = 4
     elif npcId == 20342 : chance = 2
   if st.getQuestItemsCount(GLUDIO_LORDS_MARK) :
     if st.getRandom(10)<chance :
       st.giveItems(item,1)
       st.playSound("ItemSound.quest_itemget")
   return

QUEST       = Quest(257,qn,"Guard Is Busy1")

QUEST.addStartNpc(30039)

QUEST.addTalkId(30039)

QUEST.addKillId(20130)
QUEST.addKillId(20131)
QUEST.addKillId(20132)
QUEST.addKillId(20342)
QUEST.addKillId(20343)
QUEST.addKillId(20006)
QUEST.addKillId(20093)
QUEST.addKillId(20096)
QUEST.addKillId(20098)
