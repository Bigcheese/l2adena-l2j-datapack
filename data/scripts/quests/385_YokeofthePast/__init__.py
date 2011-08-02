import sys
from com.l2jserver import Config
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "385_YokeofthePast"

ANCIENT_SCROLL = 5902

CHANCE={
    21208:7, #Hallowed Watchman 
    21209:8, #Hallowed Seer
    21210:11, #Vault Guardian
    21211:11, #Vault Seer 
    #21212 has not spawn
    21213:14, #Hallowed Monk 
    21214:19, #Vault Sentinel 
    21215:19, #Vault Monk 
    #21216 has not spawn
    21217:24, #Hallowed Priest 
    21218:30, #Vault Overlord
    21219:30, #Vault Priest 
    #21220 has not spawn
    21221:37, #Sepulcher Inquisitor 
    21222:46, #Sepulcher Archon 
    21223:45, #Sepulcher Inquisitor
    21224:50, #Sepulcher Guardian 
    21225:54, #Sepulcher Sage 
    21226:66, #Sepulcher Guardian 
    21227:64, #Sepulcher Sage 
    21228:70, #Sepulcher Guard 
    21229:75, #Sepulcher Preacher 
    21230:91, #Sepulcher Guard 
    21231:86, #Sepulcher Preacher 
    #21232 has not spawn
    #21233 has not spawn 
    #21234 has not spawn
    #21235 has not spawn 
    21236:12, #Barrow Sentinel 
    21237:14, #Barrow Monk 
    21238:19, #Grave Sentinel 
    21239:19, #Grave Monk 
    21240:22, #Barrow Overlord 
    21241:24, #Barrow Priest 
    21242:30, #Grave Overlord
    21243:30, #Grave Priest 
    21244:34, #Crypt Archon 
    21245:37, #Crypt Inquisitor
    21246:46, #Tomb Archon 
    21247:45, #Tomb Inquisitor 
    21248:50, #Crypt Guardian 
    21249:54, #Crypt Sage
    21250:99, #Tomb Guardian
    21251:64, #Tomb Sage 	
    21252:70, #Crypt Guard 
    21253:75, #Crypt Preacher 
    21254:91, #Tomb Guard 
    21255:86 #Tomb Preacher 
}
MAX = 100

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = []

 def onEvent (self,event,st) :
    htmltext = event
    if event == "14.htm" :
      st.setState(State.STARTED)
      st.playSound("ItemSound.quest_accept")
      st.set("cond","1")
    elif event == "17.htm" :
      st.playSound("ItemSound.quest_finish")
      st.exitQuest(1)
    return htmltext

 def onTalk (self,npc,player):
   htmltext = Quest.getNoQuestMsg(player)
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   if id == State.CREATED :
     htmltext = "10.htm"
   elif st.getInt("cond") == 1 and st.getQuestItemsCount(ANCIENT_SCROLL) == 0 :
     htmltext = "16.htm"
   elif st.getInt("cond") == 1 and st.getQuestItemsCount(ANCIENT_SCROLL) :
     numancientscrolls = st.getQuestItemsCount(ANCIENT_SCROLL)
     st.giveItems(5965,numancientscrolls)
     st.takeItems(ANCIENT_SCROLL,-1)
     htmltext = "16.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
    partyMember = self.getRandomPartyMemberState(player, State.STARTED)
    if not partyMember : return
    st = partyMember.getQuestState(qn)
    chance = CHANCE[npc.getNpcId()]*Config.RATE_QUEST_DROP
    numItems, chance = divmod(chance,MAX)
    if st.getRandom(MAX)<chance :
      numItems = numItems + 1
    if numItems != 0 :
      st.giveItems(ANCIENT_SCROLL,int(numItems))
      st.playSound("ItemSound.quest_itemget")
    return

QUEST       = Quest(385,qn,"Yoke of the Past")

for npcId in range(31095,31126):
    if npcId in [31111,31112,31113]:
        continue
    QUEST.addTalkId(npcId)
    QUEST.addStartNpc(npcId)

for mobs in range(21208,21256):
    QUEST.addKillId(mobs)