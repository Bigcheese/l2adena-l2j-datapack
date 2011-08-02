package quests.Q278_HomeSecurity;

import com.l2jserver.gameserver.model.actor.L2Npc;
import com.l2jserver.gameserver.model.actor.instance.L2PcInstance;
import com.l2jserver.gameserver.model.quest.Quest;
import com.l2jserver.gameserver.model.quest.QuestState;
import com.l2jserver.gameserver.model.quest.State;
import com.l2jserver.util.Rnd;

/**
 * Home Security (278)
 * @author malyelfik
 */
public class Q278_HomeSecurity extends Quest
{
	private static final String qn = "278_HomeSecurity";
	// NPC
	private static final int Tunatun = 31537;
	private static final int[] Monster = { 18905, 18906, 18907 };
	// Item
	private static final int SelMahumMane = 15531;
	
	@Override
	public String onAdvEvent(String event, L2Npc npc, L2PcInstance player)
	{
		String htmltext = event;
		QuestState st = player.getQuestState(qn);
		
		if (st == null)
			return htmltext;
		
		if (event.equalsIgnoreCase("31537-02.htm"))
		{
			if (player.getLevel() >= 82)
				htmltext = "31537-02.htm";
			else
				htmltext = "31537-03.html";
		}
		else if (event.equalsIgnoreCase("31537-04.htm"))
		{
			st.set("cond", "1");
			st.playSound("ItemSound.quest_accept");
			st.setState(State.STARTED);
		}
		else if (event.equalsIgnoreCase("31537-07.html"))
		{
			int i0 = Rnd.get(100);
			
			if (i0 < 10)
				st.giveItems(960, 1);
			else if (i0 < 19)
				st.giveItems(960, 2);
			else if (i0 < 27)
				st.giveItems(960, 3);
			else if (i0 < 34)
				st.giveItems(960, 4);
			else if (i0 < 40)
				st.giveItems(960, 5);
			else if (i0 < 45)
				st.giveItems(960, 6);
			else if (i0 < 49)
				st.giveItems(960, 7);
			else if (i0 < 52)
				st.giveItems(960, 8);
			else if (i0 < 54)
				st.giveItems(960, 9);
			else if (i0 < 55)
				st.giveItems(960, 10);
			else if (i0 < 75)
				st.giveItems(9553, 1);
			else if (i0 < 90)
				st.giveItems(9553, 2);
			else
				st.giveItems(959, 1);
			
			st.takeItems(SelMahumMane, st.getQuestItemsCount(SelMahumMane));
			st.unset("cond");
			st.playSound("ItemSound.quest_finish");
			st.exitQuest(true);
			htmltext = "31537-07.html";
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
				htmltext = "31537-01.htm";
				break;
			case State.STARTED:
				if (st.getInt("cond") == 1 || st.getQuestItemsCount(SelMahumMane) < 300)
					htmltext = "31537-06.html";
				else if (st.getInt("cond") == 2 && st.getQuestItemsCount(SelMahumMane) >= 300)
					htmltext = "31537-05.html";
				break;
		}
		return htmltext;
	}
	
	@Override
	public String onKill(L2Npc npc, L2PcInstance player, boolean isPet)
	{
		L2PcInstance partyMember = getRandomPartyMember(player, "1");
		if (partyMember == null)
			return null;
		final QuestState st = partyMember.getQuestState(qn);
		
		int chance, i1;
		if (st.getInt("cond") == 1)
		{
			switch (npc.getNpcId())
			{
				case 18907: // Beast Devourer
				case 18906: // Farm Bandit
					chance = Rnd.get(1000);
					if (chance < 85)
					{
						st.giveItems(SelMahumMane, 1);
						if (st.getQuestItemsCount(SelMahumMane) >= 300)
						{
							st.set("cond", "2");
							st.playSound("ItemSound.quest_middle");
						}
						else
							st.playSound("ItemSound.quest_itemget");
					}
					break;
				case 18905: // Farm Ravager (Crazy)
					chance = Rnd.get(1000);
					if (chance < 486)
					{
						i1 = Rnd.get(6) + 1;
						if ((i1 + st.getQuestItemsCount(SelMahumMane)) >= 300)
						{
							st.set("cond", "2");
							st.playSound("ItemSound.quest_middle");
							st.giveItems(SelMahumMane, (300 - st.getQuestItemsCount(SelMahumMane)));
						}
						else
						{
							st.giveItems(SelMahumMane, i1);
							st.playSound("ItemSound.quest_itemget");
						}
					}
					else
					{
						i1 = (Rnd.get(5) + 1);
						if ((i1 + st.getQuestItemsCount(SelMahumMane)) >= 300)
						{
							st.set("cond", "2");
							st.playSound("ItemSound.quest_middle");
							st.giveItems(SelMahumMane, (300 - st.getQuestItemsCount(SelMahumMane)));
						}
						else
						{
							st.giveItems(SelMahumMane, i1);
							st.playSound("ItemSound.quest_itemget");
						}
					}
					break;
			}
		}
		return null;
	}
	
	public Q278_HomeSecurity(int questId, String name, String descr)
	{
		super(questId, name, descr);
		addStartNpc(Tunatun);
		addTalkId(Tunatun);
		for (int i : Monster)
			addKillId(i);
		
		questItemIds = new int[] { SelMahumMane };
	}
	
	public static void main(String[] args)
	{
		new Q278_HomeSecurity(278, qn, "Home Security");
	}
}
