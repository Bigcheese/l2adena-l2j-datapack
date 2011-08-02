/*
 * This program is free software: you can redistribute it and/or modify it under
 * the terms of the GNU General Public License as published by the Free Software
 * Foundation, either version 3 of the License, or (at your option) any later
 * version.
 * 
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
 * details.
 * 
 * You should have received a copy of the GNU General Public License along with
 * this program. If not, see <http://www.gnu.org/licenses/>.
 */
package teleports.TeleportWithCharm;

import com.l2jserver.gameserver.model.actor.L2Npc;
import com.l2jserver.gameserver.model.actor.instance.L2PcInstance;
import com.l2jserver.gameserver.model.quest.Quest;
import com.l2jserver.gameserver.model.quest.QuestState;

/**
 * @author Plim
 * Original python script by DraX
 */
public class TeleportWithCharm extends Quest
{
	//NPCs
	private final static int WHIRPY = 30540;
	private final static int TAMIL = 30576;
	
	//ITEMS
	private final static int ORC_GATEKEEPER_CHARM = 1658;
	private final static int DWARF_GATEKEEPER_TOKEN = 1659;
	
	@Override
	public String onTalk(L2Npc npc, L2PcInstance player)
	{
		String htmltext = "";
		QuestState st = player.getQuestState(getName());
		
		if (st == null)
			return null;
		
		switch (npc.getNpcId())
		{
			case WHIRPY:
				if (st.hasQuestItems(DWARF_GATEKEEPER_TOKEN))
				{
					st.takeItems(DWARF_GATEKEEPER_TOKEN,1);
					st.getPlayer().teleToLocation(-80826,149775,-3043);
					st.exitQuest(true);
				}
				else
				{
					st.exitQuest(true);
					htmltext = "30576-01.htm";
				}
				break;
			case TAMIL:
				if (st.hasQuestItems(ORC_GATEKEEPER_CHARM))
				{
					st.takeItems(ORC_GATEKEEPER_CHARM,1);
					st.getPlayer().teleToLocation(-80826,149775,-3043);
					st.exitQuest(true);
				}
				else
				{
					st.exitQuest(true);
					htmltext = "30540-01.htm";
				}
				break;
		}
		
		return htmltext;
	}

	public TeleportWithCharm(int questId, String name, String descr)
	{
		super(questId, name, descr);
		addStartNpc(WHIRPY);
		addStartNpc(TAMIL);
		addTalkId(WHIRPY);
		addTalkId(TAMIL);
	}
	
	public static void main(String[] args)
	{
		new TeleportWithCharm(-1, TeleportWithCharm.class.getSimpleName(), "teleports");
	}
}
