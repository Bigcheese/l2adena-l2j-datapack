# Made by Mr. - Version 0.3 by DrLecter
import sys
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "293_HiddenVein"

CHRYSOLITE_ORE = 1488
TORN_MAP_FRAGMENT = 1489
HIDDEN_VEIN_MAP = 1490
ADENA = 57

#Newbie/one time rewards section
#Any quest should rely on a unique bit, but
#it could be shared among quest that were mutually
#exclusive or race restricted.
#Bit #1 isn't used for backwards compatibility.
NEWBIE_REWARD = 4
SOULSHOT_FOR_BEGINNERS = 5789

def newbie_rewards(st) :
  # check the player state against this quest newbie rewarding mark.
  player=st.getPlayer()
  newbie = player.getNewbie()
  if newbie | NEWBIE_REWARD != newbie :
     player.setNewbie(newbie|NEWBIE_REWARD)
     st.giveItems(SOULSHOT_FOR_BEGINNERS,6000)
     st.playTutorialVoice("tutorial_voice_026")
  

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [HIDDEN_VEIN_MAP, CHRYSOLITE_ORE, TORN_MAP_FRAGMENT]

 def onAdvEvent (self,event,npc, player) :
    htmltext = event
    st = player.getQuestState(qn)
    if not st : return
    if event == "30535-03.htm" :
      st.set("cond","1")
      st.setState(State.STARTED)
      st.playSound("ItemSound.quest_accept")
    elif event == "30535-06.htm" :
      st.takeItems(TORN_MAP_FRAGMENT,-1)
      st.exitQuest(1)
      st.playSound("ItemSound.quest_finish")
    elif event == "30539-02.htm" :
      if st.getQuestItemsCount(TORN_MAP_FRAGMENT) >=4 :
        htmltext = "30539-03.htm"
        st.giveItems(HIDDEN_VEIN_MAP,1)
        st.takeItems(TORN_MAP_FRAGMENT,4)
    return htmltext

 def onTalk (self,npc,player):
   htmltext = Quest.getNoQuestMsg(player)
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   if npcId != 30535 and id != State.STARTED : return htmltext
   
   if id == State.CREATED :
     st.set("cond","0")
   if npcId == 30535 :
     if st.getInt("cond")==0 :
       if player.getRace().ordinal() != 4 :
         htmltext = "30535-00.htm"
         st.exitQuest(1)
       elif player.getLevel() >= 6 :
         htmltext = "30535-02.htm"
         return htmltext
       else:
         htmltext = "30535-01.htm"
         st.exitQuest(1)
     else :
       if st.getQuestItemsCount(CHRYSOLITE_ORE)==0 :
         if st.getQuestItemsCount(HIDDEN_VEIN_MAP)==0 :
           htmltext = "30535-04.htm"
         else :
           newbie_rewards(st)
           htmltext = "30535-08.htm"
           st.giveItems(ADENA,st.getQuestItemsCount(HIDDEN_VEIN_MAP)*1000)
           st.takeItems(HIDDEN_VEIN_MAP,-1)
       else :
         if st.getQuestItemsCount(HIDDEN_VEIN_MAP)==0 :
           newbie_rewards(st)
           htmltext = "30535-05.htm"
           st.giveItems(ADENA,st.getQuestItemsCount(CHRYSOLITE_ORE)*10)
           st.takeItems(CHRYSOLITE_ORE,-1)
         else :
           newbie_rewards(st)
           htmltext = "30535-09.htm"
           st.giveItems(ADENA,st.getQuestItemsCount(CHRYSOLITE_ORE)*10+st.getQuestItemsCount(HIDDEN_VEIN_MAP)*1000)
           st.takeItems(HIDDEN_VEIN_MAP,-1)
           st.takeItems(CHRYSOLITE_ORE,-1)
   elif npcId == 30539 :
      htmltext = "30539-01.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st : return 
   if st.getState() != State.STARTED : return 
   
   n = st.getRandom(100)
   if n > 50 :
     st.giveItems(CHRYSOLITE_ORE,1)
     st.playSound("ItemSound.quest_itemget")
   elif n < 5 :
     st.giveItems(TORN_MAP_FRAGMENT,1)
     st.playSound("ItemSound.quest_itemget")
   return

QUEST       = Quest(293,qn,"The Hidden Veins")

QUEST.addStartNpc(30535)

QUEST.addTalkId(30535)

QUEST.addTalkId(30539)

QUEST.addKillId(20446)
QUEST.addKillId(20447)
QUEST.addKillId(20448)
