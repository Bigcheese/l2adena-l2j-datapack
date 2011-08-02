#Guardians of the Holy Grail made by Bloodshed
import sys
from com.l2jserver import Config
from com.l2jserver.gameserver.model.quest        import State
from com.l2jserver.gameserver.model.quest        import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

qn = "639_GuardiansOfTheHolyGrail"

# NPCS
DOMINIC = 31350
GREMORY = 32008
GRAIL = 32028

# Monsters
MONSTERS = range(22122,22136)

# Items
WATER_BOTTLE = 8070
HOLY_WATER_BOTTLE = 8071
SCRIPTURES = 8069

# Drop Chance
DROP_CHANCE = 30

class Quest (JQuest) :

  def __init__(self,id,name,descr):
    JQuest.__init__(self,id,name,descr)
    self.questItemIds = [WATER_BOTTLE,HOLY_WATER_BOTTLE,SCRIPTURES]

  def onAdvEvent (self,event,npc, player) :
    htmltext = event
    st = player.getQuestState(qn)
    if not st : return
    if event == "31350-03.htm" :
      st.set("cond","1")
      st.setState(State.STARTED)
      st.playSound("ItemSound.quest_accept")
    elif event == "31350-07.htm" :
      st.playSound("ItemSound.quest_finish")
      st.exitQuest(1)
    elif event == "31350-08.htm" :
      QI = st.getQuestItemsCount(SCRIPTURES)
      st.takeItems(SCRIPTURES,-1)
      st.rewardItems(57,1625*QI)
    elif event == "32008-05.htm" :
      st.set("cond","2")
      st.playSound("ItemSound.quest_middle")
      st.giveItems(WATER_BOTTLE,1)
    elif event == "32028-02.htm" :
      st.set("cond","3")
      st.playSound("ItemSound.quest_middle")
      st.takeItems(WATER_BOTTLE,-1)
      st.giveItems(HOLY_WATER_BOTTLE,1)
    elif event == "32008-07.htm" :
      st.set("cond","4")
      st.playSound("ItemSound.quest_middle")
      st.takeItems(HOLY_WATER_BOTTLE,-1)
    elif event == "32008-08a.htm" :
      st.takeItems(SCRIPTURES,4000)
      st.rewardItems(959,1)
    elif event == "32008-08b.htm" :
      st.takeItems(SCRIPTURES,400)
      st.rewardItems(960,1)
    return htmltext

  def onTalk (self, npc, player) :
    htmltext = Quest.getNoQuestMsg(player)
    st = player.getQuestState(qn)
    if not st : return htmltext

    npcId = npc.getNpcId()
    cond = st.getInt("cond")
    id = st.getState()
    if npcId == DOMINIC :
      if player.getLevel() >= 73 :
        if id == State.CREATED :
          htmltext = "31350-01.htm"
        elif id == State.STARTED and st.getQuestItemsCount(SCRIPTURES) >= 1 :
          htmltext = "31350-04.htm"
        else :
          htmltext = "31350-05.htm"
      else :
        htmltext = "31350-00.htm"
        st.exitQuest(1)
    elif npcId == GREMORY :
      if cond == 1 :
        htmltext = "32008-01.htm"
      elif cond == 2 :
        htmltext = "32008-05b.htm"
      elif cond == 3 :
        htmltext = "32008-06.htm"
      elif cond == 4 and st.getQuestItemsCount(SCRIPTURES) < 400 :
        htmltext = "32008-08d.htm"
      elif cond == 4 and st.getQuestItemsCount(SCRIPTURES) >= 4000 :
        htmltext = "32008-08c.htm"
      elif cond == 4 and st.getQuestItemsCount(SCRIPTURES) >= 400 and st.getQuestItemsCount(SCRIPTURES) < 4000 :
        htmltext = "32008-08.htm"
    elif npcId == GRAIL :
      if cond == 2 :
        htmltext = "32028-01.htm"
    return htmltext

  def onKill(self, npc, player, isPet) :
    partyMember = self.getRandomPartyMemberState(player, State.STARTED)
    if not partyMember: return
    st = partyMember.getQuestState(qn)
    if not st : return
    numItems, chance = divmod(DROP_CHANCE * Config.RATE_QUEST_DROP,100)
    if st.getRandom(100) < chance :
        numItems += 1
    if numItems :
        st.giveItems(SCRIPTURES,int(numItems))
        st.playSound("ItemSound.quest_itemget")
    return

QUEST       = Quest(639,qn,"Guardians of the Holy Grail")

QUEST.addStartNpc(DOMINIC)
QUEST.addTalkId(DOMINIC)
QUEST.addTalkId(GREMORY)
QUEST.addTalkId(GRAIL)

for i in MONSTERS :
    QUEST.addKillId(i)