# Made by Mr. Have fun! Version 0.2
# Version 0.3 by H1GHL4ND3R
import sys
from com.l2jserver import Config 
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "106_ForgottenTruth"

ONYX_TALISMAN1,      ONYX_TALISMAN2,     ANCIENT_SCROLL,  \
ANCIENT_CLAY_TABLET, KARTAS_TRANSLATION, ELDRITCH_DAGGER  \
= range(984,990)

ORC = 27070
#Newbie/one time rewards section
#Any quest should rely on a unique bit, but
#it could be shared among quest that were mutually
#exclusive or race restricted.
#Bit #1 isn't used for backwards compatibility.
NEWBIE_REWARD = 2
SPIRITSHOT_FOR_BEGINNERS = 5790
SOULSHOT_FOR_BEGINNERS = 5789

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [KARTAS_TRANSLATION, ONYX_TALISMAN1, ONYX_TALISMAN2, ANCIENT_SCROLL, ANCIENT_CLAY_TABLET]

 def onAdvEvent (self,event,npc, player) :
    htmltext = event
    st = player.getQuestState(qn)
    if not st : return
    if event == "30358-05.htm" :
        st.giveItems(ONYX_TALISMAN1,1)
        st.set("cond","1")
        st.setState(State.STARTED)
        st.playSound("ItemSound.quest_accept")
    return htmltext

 def onTalk (self,npc,player):
   npcId = npc.getNpcId()
   htmltext = Quest.getNoQuestMsg(player)
   st = player.getQuestState(qn)
   if not st : return htmltext

   id = st.getState()
   if id == State.COMPLETED :                                  # Check if the quest is already made
     htmltext = Quest.getAlreadyCompletedMsg(player)
   elif id == State.CREATED :                                      # Check if is starting the quest
     if player.getRace().ordinal() == 2 :
       if player.getLevel() >= 10 :
         htmltext = "30358-03.htm"
       else:
         htmltext = "30358-02.htm"
         st.exitQuest(1)
     else :
       htmltext = "30358-00.htm"
       st.exitQuest(1)
   else :                                                  # The quest itself
     cond = st.getInt("cond")
     if cond == 1 :
       if npcId == 30358 :
         htmltext = "30358-06.htm"
       elif npcId == 30133 and st.getQuestItemsCount(ONYX_TALISMAN1) : 
         htmltext = "30133-01.htm"
         st.takeItems(ONYX_TALISMAN1,1)
         st.giveItems(ONYX_TALISMAN2,1)
         st.set("cond","2")
         st.playSound("ItemSound.quest_middle") 
     elif cond == 2 :
       if npcId == 30358 :
         htmltext = "30358-06.htm"
       elif npcId == 30133 :
         htmltext = "30133-02.htm"
     elif cond == 3 :
       if npcId == 30358 :
         htmltext = "30358-06.htm"
       elif npcId == 30133 and st.getQuestItemsCount(ANCIENT_SCROLL) and st.getQuestItemsCount(ANCIENT_CLAY_TABLET):
         htmltext = "30133-03.htm"
         st.takeItems(ONYX_TALISMAN2,1)
         st.takeItems(ANCIENT_SCROLL,1)
         st.takeItems(ANCIENT_CLAY_TABLET,1)
         st.giveItems(KARTAS_TRANSLATION,1)
         st.set("cond","4")
         st.playSound("ItemSound.quest_middle") 
     elif cond == 4 :
       if npcId == 30358 and st.getQuestItemsCount(KARTAS_TRANSLATION) :
         htmltext = "30358-07.htm"
         st.takeItems(KARTAS_TRANSLATION,1)
         st.giveItems(57,10266)
         st.addExpAndSp(24195,2074)
         st.giveItems(ELDRITCH_DAGGER,1)
         for item in range(4412,4417) :
               st.rewardItems(item,10)
         st.rewardItems(1060,100)
         if player.getClassId().isMage() :
            st.giveItems(2509,500)
         else :
            st.giveItems(1835,1000)
         # check the player state against this quest newbie rewarding mark.
         newbie = player.getNewbie()
         if newbie | NEWBIE_REWARD != newbie :
            player.setNewbie(newbie|NEWBIE_REWARD)
            if player.getClassId().isMage() :
               st.giveItems(SPIRITSHOT_FOR_BEGINNERS,3000)
               st.playTutorialVoice("tutorial_voice_027")
         st.unset("cond")
         st.exitQuest(False)
         st.playSound("ItemSound.quest_finish")
       elif npcId == 30133 :
         htmltext = "30133-04.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st : return
   if st.getState() != State.STARTED : return
   
   if st.getInt("cond") == 2 :
     if st.getRandom(100) < 20 :
       if st.getQuestItemsCount(ANCIENT_SCROLL) == 0 :
         st.giveItems(ANCIENT_SCROLL,1)
         st.playSound("Itemsound.quest_itemget")
       elif st.getQuestItemsCount(ANCIENT_CLAY_TABLET) == 0 :
         st.giveItems(ANCIENT_CLAY_TABLET,1)
         st.playSound("ItemSound.quest_middle")
         st.set("cond","3")
   return

QUEST       = Quest(106,qn,"Forgotten Truth")

QUEST.addStartNpc(30358)

QUEST.addTalkId(30358)

QUEST.addTalkId(30133)

QUEST.addKillId(27070)
