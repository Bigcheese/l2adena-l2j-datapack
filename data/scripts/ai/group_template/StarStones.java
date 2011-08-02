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
package ai.group_template;

import com.l2jserver.gameserver.model.L2Object;
import com.l2jserver.gameserver.model.L2Skill;
import com.l2jserver.gameserver.model.actor.L2Npc;
import com.l2jserver.gameserver.model.actor.instance.L2PcInstance;
import com.l2jserver.gameserver.network.SystemMessageId;
import com.l2jserver.gameserver.network.serverpackets.SystemMessage;
import com.l2jserver.gameserver.util.Util;
import com.l2jserver.util.Rnd;

public class StarStones extends L2AttackableAIScript
{
	private static final int[] mobs = {18684, 18685, 18686, 18687, 18688, 18689, 18690, 18691, 18692};
	private static final int RATE = 1;
	
	public StarStones(int questId, String name, String descr)
	{
		super(questId, name, descr);
		this.registerMobs(mobs, QuestEventType.ON_SKILL_SEE);
	}
	
	@Override
	public String onSkillSee (L2Npc npc, L2PcInstance caster, L2Skill skill, L2Object[] targets, boolean isPet)
	{
		if (Util.contains(targets, npc) && skill.getId() == 932)
		{
			int itemId = 0;
			
			switch(npc.getNpcId())
			{
				case 18684:
				case 18685:
				case 18686:
					// give Red item
					itemId = 14009;
					break;
				case 18687:
				case 18688:
				case 18689:
					// give Blue item
					itemId = 14010;
					break;
				case 18690:
				case 18691:
				case 18692:
					// give Green item
					itemId = 14011;
					break;
				default:
					// unknown npc!
					return super.onSkillSee(npc, caster, skill, targets, isPet);
			}
			if (Rnd.get(100) < 33)
			{
				caster.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.THE_COLLECTION_HAS_SUCCEEDED));
				caster.addItem("StarStone", itemId, Rnd.get(RATE + 1, 2 * RATE), null, true);
			}
			else if ((skill.getLevel() == 1 && Rnd.get(100) < 15) ||
					(skill.getLevel() == 2 && Rnd.get(100) < 50) ||
					(skill.getLevel() == 3 && Rnd.get(100) < 75))
			{
				caster.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.THE_COLLECTION_HAS_SUCCEEDED));
				caster.addItem("StarStone", itemId, Rnd.get(1, RATE), null, true);
			}
			else
				caster.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.THE_COLLECTION_HAS_FAILED));
			npc.deleteMe();
		}
		return super.onSkillSee(npc, caster, skill, targets, isPet);
	}
	
	public static void main(String[] args)
	{
		new StarStones(-1, "starstones", "ai");
	}
}
