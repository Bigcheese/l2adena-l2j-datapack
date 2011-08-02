# Made by Mr. Have fun! - Version 0.3 by DrLecter
import sys
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "265_ChainsOfSlavery"

IMP_SHACKLES = 1368
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
     self.questItemIds = [IMP_SHACKLES]

 def onAdvEvent (self,event,npc, player) :
    htmltext = event
    st = player.getQuestState(qn)
    if not st : return
    if event == "30357-03.htm" :
      st.set("cond","1")
      st.setState(State.STARTED)
      st.playSound("ItemSound.quest_accept")
    elif event == "30357-06.htm" :
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
     if player.getRace().ordinal() != 2 :
       htmltext = "30357-00.htm"
       st.exitQuest(1)
     else :
       if player.getLevel()<6 :
          htmltext = "30357-01.htm"
          st.exitQuest(1)
       else:
          htmltext = "30357-02.htm"
   else :
     count=st.getQuestItemsCount(IMP_SHACKLES)
     if count :
       if count >= 10:
          st.giveItems(ADENA,12*count+500)
       else :
          st.giveItems(ADENA,12*count)
       st.takeItems(IMP_SHACKLES,-1)
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
       htmltext = "30357-05.htm"
     else:
       htmltext = "30357-04.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st : return 
   if st.getState() != State.STARTED : return 
   
   if st.getRandom(10) < (5+((npc.getNpcId()-20000)^4)) :
     st.giveItems(IMP_SHACKLES,1)
     st.playSound("ItemSound.quest_itemget")
   return

QUEST       = Quest(265,qn,"Chains Of Slavery")

QUEST.addStartNpc(30357)

QUEST.addTalkId(30357)

QUEST.addKillId(20004)
QUEST.addKillId(20005)
