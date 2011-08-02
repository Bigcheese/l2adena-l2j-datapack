# Whisper of Dreams, part 2 version 0.1 
# by DrLecter
import sys
from com.l2jserver import Config
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest
 
#Quest info
QUEST_NUMBER,QUEST_NAME,QUEST_DESCRIPTION = 375,"WhisperOfDreams2","Whisper of Dreams, part 2"
qn = "375_WhisperOfDreams2"

#Variables
#Alternative rewards. Set this to a non-zero value and recipes will be 100% instead of 60%
ALT_RP_100=0
 
#Quest items
MSTONE,K_HORN,CH_SKULL=range(5887,5890)
 
#Quest collections
REWARDS = [5348,5350,5352]
 
#NPCs
MANAKIA = 30515
 
#Mobs & Drop
DROPLIST = {20624:[CH_SKULL,"awaitSkull"],20629:[K_HORN,"awaitHorn"]}
 
class Quest (JQuest) :
 
 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [CH_SKULL, K_HORN]
 
 def onEvent (self,event,st) :
    htmltext = event
    if event == "30515-6.htm" :
       if st.getQuestItemsCount(MSTONE):
         ### do not take the item.  Players must remove it manually if they wish.
         ### However, if the players choose not to delete the item, they ARE ALLOWED
         ### to abort the quest and restart it later without having to redo Part 1!
         ### to abort the quest and restart it later without having to redo Part 1!
         #st.takeItems(MSTONE,1)  
         st.setState(State.STARTED)
         st.set("awaitSkull","1")
         st.set("awaitHorn","1")
         st.set("cond","1")
         st.playSound("ItemSound.quest_accept")
       else:
         htmltext = Quest.getNoQuestMsg(player)
    elif event == "30515-7.htm" :
       st.playSound("ItemSound.quest_finish")
       st.exitQuest(1)
    elif event == "30515-8.htm" :
       st.set("awaitSkull","1")
       st.set("awaitHorn","1")
    return htmltext
 
 def onTalk (self,npc,player):
   htmltext = Quest.getNoQuestMsg(player)
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   if id == State.CREATED :
      st.set("cond","0")
      htmltext = "30515-1.htm"
      if player.getLevel() < 60 :
         htmltext = "30515-2.htm"
         st.exitQuest(1)
      elif not st.getQuestItemsCount(MSTONE) :
         htmltext = "30515-3.htm"
         st.exitQuest(1)
   elif id == State.STARTED :
      if st.getQuestItemsCount(CH_SKULL)==st.getQuestItemsCount(K_HORN)==100 :
         st.takeItems(CH_SKULL,-1)
         st.takeItems(K_HORN,-1)
         item=REWARDS[st.getRandom(len(REWARDS))]
         if ALT_RP_100 : item += 1
         st.rewardItems(item,1)
         htmltext="30515-4.htm"
      else :
         htmltext = "30515-5.htm"
   return htmltext
 
 def onKill(self,npc,player,isPet) :
    npcId = npc.getNpcId()
    item, partyCond  = DROPLIST[npcId]
    partyMember = self.getRandomPartyMember(player,"1")
    if not partyMember: return
    st = partyMember.getQuestState(qn)
    if st :
      count = st.getQuestItemsCount(item)
      if st.getInt("cond") == 1 and count < 100 :
        chance = 75 * Config.RATE_QUEST_DROP
        numItems, chance = divmod(chance,100)
        if st.getRandom(100) < chance :
           numItems += 1
        if numItems :
           if count + numItems >= 100 :
              numItems = 100 - count
              st.playSound("ItemSound.quest_middle")
              st.unset(partyCond)
           else:
              st.playSound("ItemSound.quest_itemget")   
           st.giveItems(item,int(numItems))
    return  
 
# Quest class and state definition
QUEST       = Quest(QUEST_NUMBER, str(QUEST_NUMBER)+"_"+QUEST_NAME, QUEST_DESCRIPTION)

# Quest NPC starter initialization
QUEST.addStartNpc(MANAKIA)
# Quest initialization
QUEST.addTalkId(MANAKIA)
 
for i in DROPLIST.keys() :
  QUEST.addKillId(i)