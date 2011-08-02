# Linnaeus Special Bait - a seamless merge from Next and DooMita contributions
import sys
from com.l2jserver import Config
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "53_LinnaeusSpecialBait"

LINNAEUS = 31577
CRIMSON_DRAKE = 20670
CRIMSON_DRAKE_HEART = 7624
FLAMING_FISHING_LURE = 7613
#Drop chance
CHANCE = 50
#Custom setting: wether or not to check for fishing skill level?
#default False to require fishing skill level, any other value to ignore fishing
#and evaluate char level only.
ALT_IGNORE_FISHING=False

def fishing_level(player):
    if ALT_IGNORE_FISHING :
       level=20
    else :
       level = player.getSkillLevel(1315)
       effect = player.getFirstEffect(2274)
       if effect:
            level = int(effect.getSkill().getPower())
    return level

class Quest (JQuest):

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [CRIMSON_DRAKE_HEART]

 def onEvent (self,event,st):
     htmltext = event
     if event == "31577-1.htm":
        st.setState(State.STARTED)
        st.set("cond","1")
        st.playSound("ItemSound.quest_accept")
     elif event == "31577-3.htm":
        cond = st.getInt("cond")
        if cond == 2 and st.getQuestItemsCount(CRIMSON_DRAKE_HEART) == 100:
           st.giveItems(FLAMING_FISHING_LURE, 4)
           st.takeItems(CRIMSON_DRAKE_HEART, 100)                
           st.exitQuest(False)
           st.unset("cond") # we dont need it in db if quest is already State.COMPLETED
           st.playSound("ItemSound.quest_finish")
        else :
           htmltext = "31577-5.htm"
     return htmltext

 def onTalk (self,npc,player):
     st = player.getQuestState(qn)
     htmltext = Quest.getNoQuestMsg(player)
     if not st: return htmltext
     id = st.getState()
     if id == State.COMPLETED:
        htmltext = Quest.getAlreadyCompletedMsg(player)
           
     elif id == State.CREATED :
        if player.getLevel() > 59 and fishing_level(player) > 19 :
           htmltext= "31577-0.htm"
        else:
           st.exitQuest(1)
           htmltext= "31577-0a.htm"
     elif id == State.STARTED:
        if st.getInt("cond") == 1:
            htmltext = "31577-4.htm"
        else :
            htmltext = "31577-2.htm"
     return htmltext

 def onKill(self,npc,player,isPet):
     partyMember = self.getRandomPartyMember(player,"1")
     if not partyMember : return
     st = partyMember.getQuestState(qn)
     if st :
        count = st.getQuestItemsCount(CRIMSON_DRAKE_HEART)
        if st.getInt("cond") == 1 and count < 100 :
           chance = 33 * Config.RATE_QUEST_DROP
           numItems, chance = divmod(chance,100)
           if st.getRandom(100) < chance : 
              numItems += 1
           if numItems :
              if count + numItems >= 100 :
                 numItems = 100 - count
                 st.playSound("ItemSound.quest_middle")
                 st.set("cond","2")
              else:
                 st.playSound("ItemSound.quest_itemget")
              st.giveItems(CRIMSON_DRAKE_HEART,int(numItems))
     return

QUEST       = Quest(53, qn, "Linnaeus Special Bait")

QUEST.addStartNpc(LINNAEUS)
QUEST.addTalkId(LINNAEUS)

QUEST.addKillId(CRIMSON_DRAKE)