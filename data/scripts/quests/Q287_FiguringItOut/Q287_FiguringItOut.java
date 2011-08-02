package quests.Q287_FiguringItOut;

import com.l2jserver.gameserver.model.actor.L2Npc;
import com.l2jserver.gameserver.model.actor.instance.L2PcInstance;
import com.l2jserver.gameserver.model.quest.Quest;
import com.l2jserver.gameserver.model.quest.QuestState;
import com.l2jserver.gameserver.model.quest.State;
import com.l2jserver.util.Rnd;

/**
 * Figuring It Out! (287)
 * @author malyelfik
 */
public class Q287_FiguringItOut extends Quest
{
	private static final String qn = "287_FiguringItOut";
	//NPC
	private static final int Laki = 32742;
	private static final int[] Monsters = { 22771, 22770, 22774, 22769, 22772, 22768, 22773 };
	// Items
	private static final int VialOfTantaBlood = 15499;
	
	@Override
	public String onAdvEvent(String event, L2Npc npc, L2PcInstance player)
	{
		String htmltext = event;
		QuestState st = player.getQuestState(qn);
		
		if (st == null)
			return htmltext;
		
		if (event.equalsIgnoreCase("32742-03.htm"))
		{
			st.set("cond", "1");
			st.playSound("ItemSound.quest_accept");
			st.setState(State.STARTED);
		}
		else if (event.equalsIgnoreCase("Icarus"))
		{
			if (st.getQuestItemsCount(VialOfTantaBlood) >= 500)
			{
				st.takeItems(VialOfTantaBlood, 500);
				int i0 = Rnd.get(5);
				if (i0 == 0)
					st.giveItems(10381, 1);
				else if (i0 == 1)
					st.giveItems(10405, 1);
				else if (i0 == 2)
					st.giveItems(10405, 4);
				else if (i0 == 3)
					st.giveItems(10405, 4);
				else
					st.giveItems(10405, 6);
				st.playSound("ItemSound.quest_finish");
				htmltext = "32742-06.html";
			}
			else
				htmltext = "32742-07.html";
		}
		else if (event.equalsIgnoreCase("Moirai"))
		{
			if (st.getQuestItemsCount(VialOfTantaBlood) >= 100)
			{
				st.takeItems(VialOfTantaBlood, 100);
				int i0 = Rnd.get(10);
				if (i0 == 0)
					st.giveItems(15776, 1);
				else if (i0 == 1)
					st.giveItems(15779, 1);
				else if (i0 == 2)
					st.giveItems(15782, 1);
				else if (i0 == 3)
				{
					boolean i1 = Rnd.nextBoolean();
					if (!i1)
						st.giveItems(15785, 1);
					else
						st.giveItems(15788, 1);
				}
				else if (i0 == 4)
				{
					int i1 = Rnd.get(10);
					if (i1 < 4)
						st.giveItems(15812, 1);
					else if (i1 < 8)
						st.giveItems(15813, 1);
					else
						st.giveItems(15814, 1);
				}
				else if (i0 == 5)
					st.giveItems(15646, 5);
				else if (i0 == 6)
					st.giveItems(15649, 5);
				else if (i0 == 7)
					st.giveItems(15652, 5);
				else if (i0 == 8)
				{
					boolean i1 = Rnd.nextBoolean();
					if (!i1)
						st.giveItems(15655, 5);
					else
						st.giveItems(15658, 5);
				}
				else
				{
					int i1 = Rnd.get(10);
					if (i1 < 4)
						st.giveItems(15772, 1);
					else if (i1 < 7)
						st.giveItems(15773, 1);
					else
						st.giveItems(15774, 1);
				}
				st.playSound("ItemSound.quest_finish");
				htmltext = "32742-08.html";
			}
			else
				htmltext = "32742-09.html";
		}
		else if (event.equalsIgnoreCase("32742-11.html"))
		{
			if (st.getQuestItemsCount(VialOfTantaBlood) >= 1)
				htmltext = "32742-11.html";
			else
			{
				st.playSound("ItemSound.quest_finish");
				st.exitQuest(true);
				htmltext = "32742-12.html";
			}
		}
		else if (event.equalsIgnoreCase("32742-13.html"))
		{
			st.takeItems(VialOfTantaBlood, -1);
			st.playSound("ItemSound.quest_finish");
			st.exitQuest(true);
			htmltext = "32742-12.html";
		}
		return htmltext;
	}
	
	@Override
	public String onTalk(L2Npc npc, L2PcInstance player)
	{
		String htmltext = getNoQuestMsg(player);
		QuestState st = player.getQuestState(qn);
		QuestState prev = player.getQuestState("250_WatchWhatYouEat");
		
		if (st == null)
			return htmltext;
		
		switch (st.getState())
		{
			case State.CREATED:
				if (player.getLevel() >= 82 && prev != null && prev.getState() == State.COMPLETED)
					htmltext = "32742-01.htm";
				else
					htmltext = "32742-14.htm";
				break;
			case State.STARTED:
				if (st.getQuestItemsCount(VialOfTantaBlood) < 100)
					htmltext = "32742-04.html";
				else
					htmltext = "32742-05.html";
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
		int chance = Rnd.get(1000);
		boolean giveItem = false;
		
		switch (npc.getNpcId())
		{
			case 22771: // Tanta Lizardman Berserker
				if (chance < 159)
					giveItem = true;
				break;
			case 22770: // Tanta Lizardman Soldier
				if (chance < 123)
					giveItem = true;
				break;
			case 22774: // Tanta Lizardman Summoner
				if (chance < 261)
					giveItem = true;
				break;
			case 22769: // Tanta Lizardman Warrior
				if (chance < 689)
					giveItem = true;
				break;
			case 22772: // Tanta Lizardman Archer
				if (chance < 739)
					giveItem = true;
				break;
			case 22768: // Tanta Lizardman Scout
				if (chance < 509)
					giveItem = true;
				break;
			case 22773: // Tanta Lizardman Magician
				if (chance < 737)
					giveItem = true;
				break;
		}
		
		if (giveItem)
		{
			st.giveItems(VialOfTantaBlood, 1);
			st.playSound("ItemSound.quest_itemget");
		}
		return null;
	}
	
	public Q287_FiguringItOut(int questId, String name, String descr)
	{
		super(questId, name, descr);
		addStartNpc(Laki);
		addTalkId(Laki);
		for (int i : Monsters)
		{
			addKillId(i);
		}
		
		questItemIds = new int[] { VialOfTantaBlood };
	}
	
	public static void main(String[] args)
	{
		new Q287_FiguringItOut(287, qn, "Figuring It Out!");
	}
}
