# Made by KilKenny & DrLecter
import sys
from com.l2jserver import Config
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "344_1000YearsEndofLamentation"

#Rewards
ADENA = 57

#Quest Items
ARTICLES_DEAD_HEROES,OLD_KEY,OLD_HILT,OLD_TOTEM,CRUCIFIX = range(4269,4274)

#Chances
CHANCE = 36
SPECIAL = int(1+(1000/Config.RATE_QUEST_REWARD))
#NPCs
GILMORE = 30754
RODEMAI = 30756
ORVEN = 30857
KAIEN = 30623
GARVARENTZ = 30704

def rewards(st,npcId):
    state=False
    chance=st.getRandom(100)
    if npcId == ORVEN and st.getQuestItemsCount(CRUCIFIX) :
       st.set("mission","1")
       st.takeItems(CRUCIFIX,-1)
       state=True
       if chance < 50 :
          st.giveItems(1875,19)
       elif chance < 70 :
          st.giveItems(952,5)
       else :
          st.giveItems(2437,1)
    elif npcId == GARVARENTZ and st.getQuestItemsCount(OLD_TOTEM) :
       st.set("mission","2")
       st.takeItems(OLD_TOTEM,-1)
       state=True
       if chance < 45 :
          st.giveItems(1882,70)
       elif chance < 95 :
          st.giveItems(1881,50)
       else :
          st.giveItems(191,1)
    elif npcId == KAIEN and st.getQuestItemsCount(OLD_HILT) :
       st.set("mission","3")
       st.takeItems(OLD_HILT,-1)
       state=True
       if chance < 50 :
          st.giveItems(1874,25)
       elif chance < 75 :
          st.giveItems(1887,10)
       elif chance < 99 :
          st.giveItems(951,1)
       else :
          st.giveItems(133,1)
    elif npcId == RODEMAI and st.getQuestItemsCount(OLD_KEY) :
       st.set("mission","4")
       st.takeItems(OLD_KEY,-1)
       state=True
       if chance < 40 :
          st.giveItems(1879,55)
       elif chance < 90 :
          st.giveItems(951,1)
       else :
          st.giveItems(885,1)
    return state

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = range(4269,4274)

 def onEvent (self,event,st) :
     htmltext = event
     amount = st.getQuestItemsCount(ARTICLES_DEAD_HEROES)
     cond = st.getInt("cond")
     level = st.getPlayer().getLevel()
     if event == "30754-04.htm" :
        if level>=48 and cond == 0 :
          st.setState(State.STARTED)
          st.set("cond","1")
          st.playSound("ItemSound.quest_accept")
        else :
          htmltext = Quest.getNoQuestMsg(player)
          st.exitQuest(1)
     elif event == "30754-08.htm" :     
         st.exitQuest(1)
         st.playSound("ItemSound.quest_finish")
     elif event == "30754-06.htm" and cond == 1 :
       if not amount :
          htmltext = "30754-06a.htm"
       else:
          st.giveItems(ADENA,amount*60)
          st.takeItems(ARTICLES_DEAD_HEROES,-1)
          random = st.getRandom(1000)
          if random < 10 :
             htmltext = "30754-12.htm"
             st.giveItems(OLD_KEY,1)
             st.set("cond","2")
          elif random < 20 :
             htmltext = "30754-13.htm"
             st.giveItems(OLD_HILT,1)
             st.set("cond","2")
          elif random < 30 :
             htmltext = "30754-14.htm"
             st.giveItems(OLD_TOTEM,1)
             st.set("cond","2")
          elif random < 40 :
             htmltext = "30754-15.htm"
             st.giveItems(CRUCIFIX,1)
             st.set("cond","2")
          else :
             htmltext = "30754-16.htm"
             st.set("cond","1")
     return htmltext

 def onTalk (self,npc,player):
     htmltext = Quest.getNoQuestMsg(player)
     st = player.getQuestState(qn)
     if not st : return htmltext

     npcId = npc.getNpcId()
     id = st.getState()
     if npcId != GILMORE and id != State.STARTED : return htmltext
     
     level = player.getLevel()
     cond = st.getInt("cond")
     amount = st.getQuestItemsCount(ARTICLES_DEAD_HEROES)
     if id == State.CREATED : 
        if level>=48 :
           htmltext = "30754-02.htm"
        else :
           htmltext = "30754-01.htm"
           st.exitQuest(1)
     elif npcId == GILMORE and cond==1 :
        if amount :
           htmltext = "30754-05.htm"
        else :
           htmltext = "30754-04.htm"
     elif cond==2 :
        if npcId == GILMORE :
          htmltext="30754-15.htm"
        elif rewards(st,npcId) :
           htmltext=str(npcId)+"-01.htm"
           st.playSound("ItemSound.quest_middle")
           st.set("cond","1")
           st.unset("mission")
     return htmltext

 def onKill(self,npc,player,isPet):
     st = player.getQuestState(qn)
     if not st : return 
     if st.getState() != State.STARTED : return 
   
     npcId = npc.getNpcId()
     chance = (CHANCE+(npcId-20234)*2)*Config.RATE_QUEST_DROP
     bonus = int(divmod(chance,100)[0])
     if st.getInt("cond") == 1 and st.getRandom(100)<chance :
         st.giveItems(ARTICLES_DEAD_HEROES,1+bonus)
         st.playSound("ItemSound.quest_itemget")
     return

QUEST       = Quest(344,qn,"1000 Years, the End of Lamentation")

QUEST.addStartNpc(GILMORE)

QUEST.addTalkId(GILMORE)

QUEST.addTalkId(RODEMAI)
QUEST.addTalkId(ORVEN)
QUEST.addTalkId(GARVARENTZ)
QUEST.addTalkId(KAIEN)

for mob in range(20236,20241):
    QUEST.addKillId(mob)