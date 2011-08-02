#####################################################################
#                                                                   #
#   "The Clan's Reputation"                                         #
#   "Raise the Clan's Reputation"                                   #
#   "Sir Eric Rodemai in Aden Castle Town is looking                #
#   for a brave adventurer to raise the clan's reputation."         #
#   "Clan Leader, Clan Level 5 and above"                           #
#                                                                   #
#   Start NPC: Sir Eric Rodemai[30868]                              #
#                                                                   #
#   fixed and State.COMPLETED by chris_00 @katmai and DrLecter      #
#                                                                   #
#####################################################################
import sys
from com.l2jserver.gameserver.model.quest        			import State
from com.l2jserver.gameserver.model.quest        			import QuestState
from com.l2jserver.gameserver.model.quest.jython 			import QuestJython as JQuest
from com.l2jserver.gameserver.network.serverpackets      	import PledgeShowInfoUpdate
from com.l2jserver.gameserver.network.serverpackets      	import SystemMessage
from com.l2jserver.util 									import Rnd

qn="508_TheClansReputation"
qd="The Clans Reputation"

# Quest NPC
SIR_ERIC_RODEMAI = 30868

# Quest Items
NUCLEUS_OF_FLAMESTONE_GIANT = 8494 # Nucleus of Flamestone Giant : Nucleus obtained by defeating Flamestone Giant
THEMIS_SCALE                = 8277 # Themis' Scale : Obtain this scale by defeating Palibati Queen Themis.
NUCLEUS_OF_HEKATON_PRIME    = 8279 # Nucleus of Hekaton Prime : Nucleus obtained by defeating Hekaton Prime
TIPHON_SHARD                = 8280 # Tiphon Shard : Debris obtained by defeating Tiphon, Gargoyle Lord.
GLAKIS_NUCLEUS              = 8281 # Glaki's Necleus : Nucleus obtained by defeating Glaki, the last lesser Giant.
RAHHAS_FANG                 = 8282 # Rahha's Fang : Fangs obtained by defeating Rahha.

#Quest Raid Bosses
FLAMESTONE_GIANT        = 25524
PALIBATI_QUEEN_THEMIS   = 25252
HEKATON_PRIME           = 25140
GARGOYLE_LORD_TIPHON    = 25255
LAST_LESSER_GIANT_GLAKI = 25245
RAHHA                   = 25051

# id:[RaidBossNpcId,questItemId,minClanPoints,maxClanPoints]
REWARDS_LIST={
    1:[PALIBATI_QUEEN_THEMIS,  THEMIS_SCALE,130,200],
    2:[HEKATON_PRIME,          NUCLEUS_OF_HEKATON_PRIME,80,150],
    3:[GARGOYLE_LORD_TIPHON,   TIPHON_SHARD,60,130],
    4:[LAST_LESSER_GIANT_GLAKI,GLAKIS_NUCLEUS,210,280],
    5:[RAHHA,                  RAHHAS_FANG,80,150],
    6:[FLAMESTONE_GIANT,       NUCLEUS_OF_FLAMESTONE_GIANT,120,190]
    }

RADAR={
    1:[192346,21528,-3648],
    2:[191979,54902,-7658],
    3:[170038,-26236,-3824],
    4:[171762,55028,-5992],
    5:[117232,-9476,-3320],
    6:[144218,-5816,-4722],
    }

class Quest (JQuest) :

 def __init__(self,id,name,descr) :
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [THEMIS_SCALE, NUCLEUS_OF_HEKATON_PRIME, TIPHON_SHARD, GLAKIS_NUCLEUS, RAHHAS_FANG, NUCLEUS_OF_FLAMESTONE_GIANT]

 def onAdvEvent (self,event,npc,player) :
  st = player.getQuestState(qn)
  if not st: return
  cond = st.getInt("cond")
  htmltext=event
  if event == "30868-0.htm" :
    if cond == 0 :
      st.set("cond","1")
      st.setState(State.STARTED)
  elif event.isdigit() :
    if int(event) in REWARDS_LIST.keys():
      st.set("raid",event)
      htmltext="30868-"+event+".htm"
      x,y,z=RADAR[int(event)]
      if x+y+z:
        st.addRadar(x, y, z)
      st.playSound("ItemSound.quest_accept")
  elif event == "30868-7.htm" :
    st.playSound("ItemSound.quest_finish")
    st.exitQuest(1)
  return htmltext

 def onTalk (self,npc,player) :
  htmltext = Quest.getNoQuestMsg(player)
  st = player.getQuestState(qn)
  if not st : return htmltext
  clan = player.getClan()
  npcId = npc.getNpcId()
  if player.getClan() == None or player.isClanLeader() == 0 :
     st.exitQuest(1)
     htmltext = "30868-0a.htm"
  elif player.getClan().getLevel() < 5 :
     st.exitQuest(1)
     htmltext =  "30868-0b.htm"
  else :
     cond = st.getInt("cond")
     raid = st.getInt("raid")
     id = st.getState()
     if id == State.CREATED and cond == 0 :
        htmltext =  "30868-0c.htm"
     elif id == State.STARTED and cond == 1 and raid in REWARDS_LIST.keys() :
        npc,item,min,max=REWARDS_LIST[raid]
        count = st.getQuestItemsCount(item)
        CLAN_POINTS_REWARD = Rnd.get(min, max)
        if not count :
           htmltext = "30868-"+str(raid)+"a.htm"
        elif count == 1 :
           htmltext = "30868-"+str(raid)+"b.htm"
           st.takeItems(item,1)
           clan.addReputationScore(CLAN_POINTS_REWARD,True)
           player.sendPacket(SystemMessage.getSystemMessage(1777).addNumber(CLAN_POINTS_REWARD))
           clan.broadcastToOnlineMembers(PledgeShowInfoUpdate(clan))
  return htmltext

 def onKill(self,npc,player,isPet) :
  st = 0
  if player.isClanLeader() :
   st = player.getQuestState(qn)
  else:
   clan = player.getClan()
   if clan:
    leader=clan.getLeader()
    if leader :
     pleader= leader.getPlayerInstance()
     if pleader :
      if player.isInsideRadius(pleader, 1600, 1, 0) :
       st = pleader.getQuestState(qn)
  if not st : return
  option=st.getInt("raid")
  if st.getInt("cond") == 1 and st.getState() == State.STARTED and option in REWARDS_LIST.keys():
   raid,item,min,max = REWARDS_LIST[option]
   npcId=npc.getNpcId()
   if npcId == raid and not st.getQuestItemsCount(item) :
      st.giveItems(item,1)
      st.playSound("ItemSound.quest_middle")
  return


# Quest class and state definition
QUEST       = Quest(508,qn,qd)

QUEST.addStartNpc(SIR_ERIC_RODEMAI)
QUEST.addTalkId(SIR_ERIC_RODEMAI)

for npc,item,min,max in REWARDS_LIST.values():
    QUEST.addKillId(npc)