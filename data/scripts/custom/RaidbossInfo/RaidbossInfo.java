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
package custom.RaidbossInfo;

import java.util.Map;

import javolution.util.FastMap;

import com.l2jserver.gameserver.datatables.NpcTable;
import com.l2jserver.gameserver.datatables.SpawnTable;
import com.l2jserver.gameserver.model.L2Spawn;
import com.l2jserver.gameserver.model.Location;
import com.l2jserver.gameserver.model.actor.L2Npc;
import com.l2jserver.gameserver.model.actor.instance.L2PcInstance;
import com.l2jserver.gameserver.model.quest.Quest;
import com.l2jserver.gameserver.model.quest.QuestState;
import com.l2jserver.gameserver.templates.chars.L2NpcTemplate;
import com.l2jserver.gameserver.util.Util;

/**
 * @authors: Kerberos (python), Nyaran (java)
 */
public class RaidbossInfo extends Quest
{
	private static final String qn = "RaidbossInfo";

	private static final int[] NPC =
	{
		31729, 31730, 31731, 31732, 31733, 31734, 31735, 31736, 31737, 31738, 31739, 31740, 31741,
		31742, 31743, 31744, 31745, 31746, 31747, 31748, 31749, 31750, 31751, 31752, 31753, 31754,
		31755, 31756, 31757, 31758, 31759, 31760, 31761, 31762, 31763, 31764, 31765, 31766, 31767,
		31768, 31769, 31770, 31771, 31772, 31773, 31774, 31775, 31776, 31777, 31778, 31779, 31780,
		31781, 31782, 31783, 31784, 31785, 31786, 31787, 31788, 31789, 31790, 31791, 31792, 31793,
		31794, 31795, 31796, 31797, 31798, 31799, 31800, 31801, 31802, 31803, 31804, 31805, 31806,
		31807, 31808, 31809, 31810, 31811, 31812, 31813, 31814, 31815, 31816, 31817, 31818, 31819,
		31820, 31821, 31822, 31823, 31824, 31825, 31826, 31827, 31828, 31829, 31830, 31831, 31832,
		31833, 31834, 31835, 31836, 31837, 31838, 31839, 31840, 31841, 32337, 32338, 32339, 32340
	};

	private static final Map<Integer, Location> RADAR = new FastMap<Integer, Location>();

	@Override
	public String onAdvEvent(String event, L2Npc npc, L2PcInstance player)
	{
		String htmltext = event;

		QuestState st = player.getQuestState(qn);

		if (st == null)
			return htmltext;

		if (Util.isDigit(event))
		{
			htmltext = null;
			int rbid = Integer.parseInt(event);

			if (RADAR.containsKey(rbid))
			{
				Location loc = RADAR.get(rbid);
				st.addRadar(loc.getX(), loc.getY(), loc.getZ());
			}
				
			st.exitQuest(true);
		}
		return htmltext;
	}

	@Override
	public String onTalk(L2Npc npc, L2PcInstance player)
	{
		return "info.htm";
	}

	public RaidbossInfo(int id, String name, String descr)
	{
		super(id, name, descr);
		
		for (int i : NPC)
		{
			addStartNpc(i);
			addTalkId(i);
		}
		
		// Add all Raid Bosses to RAIDS list
		for (L2NpcTemplate raid : NpcTable.getInstance().getAllNpcOfClassType("L2RaidBoss"))
		{
			int x = 0, y = 0, z = 0;
			
			for (L2Spawn spawn : SpawnTable.getInstance().getSpawnTable())
			{
				if (spawn.getNpcid() == raid.npcId)
				{
					x = spawn.getLocx();
					y = spawn.getLocy();
					z = spawn.getLocz();
					break;
				}
			}
			RADAR.put(raid.npcId, new Location(x, y, z));
		}
	}

	public static void main(String args[])
	{
		new RaidbossInfo(-1, qn, "custom");
	}
}
