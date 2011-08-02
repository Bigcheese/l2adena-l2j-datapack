# Created by Gigiikun
import sys
from com.l2jserver import Config
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "688_DefeatTheElrokianRaiders"

#Settings: drop chance in %
DROP_CHANCE = 50
DINOSAUR_FANG_NECKLACE = 8785

class Quest (JQuest) :

 def __init__(self,id,name,descr):
    JQuest.__init__(self,id,name,descr)
    self.questItemIds = [DINOSAUR_FANG_NECKLACE]

 def onEvent (self,event,st) :
    htmltext = event
    count = st.getQuestItemsCount(DINOSAUR_FANG_NECKLACE)
    if event == "None" :
        return
    elif event == "32105-03.htm" :
       st.set("cond","1")
       st.setState(State.STARTED)
       st.playSound("ItemSound.quest_accept")
    elif event == "32105-08.htm" :
       if count > 0 :
          st.takeItems(DINOSAUR_FANG_NECKLACE,-1)
          st.giveItems(57,count*3000)
       st.playSound("ItemSound.quest_finish")
       st.exitQuest(1)
    elif event == "32105-06.htm" :
       st.takeItems(DINOSAUR_FANG_NECKLACE,-1)
       st.giveItems(57,count*3000)
    elif event == "32105-07.htm" :
       if count >= 100 :
          st.takeItems(DINOSAUR_FANG_NECKLACE,100)
          st.giveItems(57,450000)
       else :
          htmltext = "32105-04.htm"
    return htmltext

 def onTalk (self, npc, player):
    st = player.getQuestState(qn)
    htmltext = Quest.getNoQuestMsg(player)
    if st :
       cond = st.getInt("cond")
       count = st.getQuestItemsCount(DINOSAUR_FANG_NECKLACE)
       if cond == 0 :
          if player.getLevel() >= 75 :
             htmltext = "32105-01.htm"
          else :
             htmltext = "32105-00.htm"
             st.exitQuest(1)
       elif st.getState() == State.STARTED :
          if count == 0 :
             htmltext = "32105-04.htm"
          else :
             htmltext = "32105-05.htm"
    return htmltext

 def onKill (self, npc, player,isPet):
    partyMember = self.getRandomPartyMember(player,"1")
    if not partyMember: return
    st = partyMember.getQuestState(qn)
    if st :
       if st.getState() == State.STARTED :
          npcId = npc.getNpcId()
          cond = st.getInt("cond")
          count = st.getQuestItemsCount(DINOSAUR_FANG_NECKLACE)
          if cond == 1 :
             chance = DROP_CHANCE*Config.RATE_QUEST_DROP
             numItems, chance = divmod(chance,100)
             if st.getRandom(100) < chance : 
                numItems += 1
             if numItems :
                if int(count + numItems)/100 > int(count)/100 :
                   st.playSound("ItemSound.quest_middle")
                else :
                   st.playSound("ItemSound.quest_itemget")
                st.giveItems(DINOSAUR_FANG_NECKLACE,int(numItems))
    return

QUEST = Quest(688,qn,"Defeat the Elrokian Raiders")

QUEST.addStartNpc(32105)

QUEST.addTalkId(32105)
QUEST.addKillId(22214)
