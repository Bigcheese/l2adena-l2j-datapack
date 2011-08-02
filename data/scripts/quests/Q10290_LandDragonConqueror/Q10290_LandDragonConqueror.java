package quests.Q10290_LandDragonConqueror;

import com.l2jserver.gameserver.model.actor.L2Npc;
import com.l2jserver.gameserver.model.actor.instance.L2PcInstance;
import com.l2jserver.gameserver.model.quest.Quest;
import com.l2jserver.gameserver.model.quest.QuestState;
import com.l2jserver.gameserver.model.quest.State;

/**
 * Land Dragon Conqueror (10290)
 * @author malyelfik
 */
public class Q10290_LandDragonConqueror extends Quest
{
	private static final String qn = "Q10290_LandDragonConqueror";
	// NPC
	private static final int Theodoric = 30755;
	private static final int[] Antharas = { 29019, 29066, 29067, 29068 }; //Old, Weak, Normal, Strong
	// Item
	private static final int PortalStone = 3865;
	private static final int ShabbyNecklace = 15522;
	private static final int MiracleNecklace = 15523;
	private static final int AntharaSlayerCirclet = 8568;
	
	@Override
	public String onAdvEvent(String event, L2Npc npc, L2PcInstance player)
	{
		String htmltext = event;
		QuestState st = player.getQuestState(qn);
		
		if (st == null)
			return htmltext;
		
		if (event.equalsIgnoreCase("30755-07.htm"))
		{
			st.setState(State.STARTED);
			st.set("cond", "1");
			st.giveItems(ShabbyNecklace, 1);
			st.playSound("ItemSound.quest_accept");
		}
		return htmltext;
	}
	
	@Override
	public String onTalk(L2Npc npc, L2PcInstance player)
	{
		String htmltext = getNoQuestMsg(player);
		QuestState st = player.getQuestState(qn);
		
		if (st == null)
			return htmltext;
		
		switch (st.getState())
		{
			case State.CREATED:
			{
				if (player.getLevel() >= 83 && st.getQuestItemsCount(PortalStone) >= 1)
					htmltext = "30755-01.htm";
				else if (player.getLevel() < 83)
					htmltext = "30755-02.htm";
				else
					htmltext = "30755-04.htm";
				break;
			}
			case State.STARTED:
			{
				if (st.getInt("cond") == 1 && st.getQuestItemsCount(ShabbyNecklace) >= 1)
					htmltext = "30755-08.htm";
				else if (st.getInt("cond") == 1 && st.getQuestItemsCount(ShabbyNecklace) == 0)
				{
					st.giveItems(ShabbyNecklace, 1);
					htmltext = "30755-09.htm";
				}
				else if (st.getInt("cond") == 2)
				{
					st.takeItems(MiracleNecklace, 1);
					st.giveItems(57, 131236);
					st.addExpAndSp(702557, 76334);
					st.giveItems(AntharaSlayerCirclet, 1);
					st.unset("cond");
					st.exitQuest(false);
					st.playSound("ItemSound.quest_finish");
					htmltext = "30755-10.htm";
				}
				break;
			}
			case State.COMPLETED:
			{
				htmltext = "30755-03.htm";
				break;
			}
		}
		
		return htmltext;
	}
	
	@Override
	public String onKill(L2Npc npc, L2PcInstance player, boolean isPet)
	{
		if (player.getParty() != null)
		{
			for (L2PcInstance partyMember : player.getParty().getPartyMembers())
				rewardPlayer(partyMember);
		}
		else
			rewardPlayer(player);
		return null;
	}
	
	private void rewardPlayer(L2PcInstance player)
	{
		QuestState st = player.getQuestState(qn);
		
		if (st != null && st.getInt("cond") == 1)
		{
			st.takeItems(ShabbyNecklace, 1);
			st.giveItems(MiracleNecklace, 1);
			st.playSound("ItemSound.quest_middle");
			st.set("cond", "2");
		}
	}
	
	public Q10290_LandDragonConqueror(int questId, String name, String descr)
	{
		super(questId, name, descr);
		addStartNpc(Theodoric);
		addTalkId(Theodoric);
		for (int i : Antharas)
			addKillId(i);
		
		questItemIds = new int[] { MiracleNecklace, ShabbyNecklace };
	}
	
	public static void main(String[] args)
	{
		new Q10290_LandDragonConqueror(10290, qn, "Land Dragon Conqueror");
	}
}