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
package custom.Validators;

import com.l2jserver.Config;
import com.l2jserver.gameserver.datatables.SkillTreesData;
import com.l2jserver.gameserver.model.L2Skill;
import com.l2jserver.gameserver.model.L2SkillLearn;
import com.l2jserver.gameserver.model.actor.instance.L2PcInstance;
import com.l2jserver.gameserver.model.quest.Quest;
import com.l2jserver.gameserver.model.quest.QuestState;
import com.l2jserver.gameserver.util.Util;

/**
 * @author Zoey76
 */
public final class SkillTransferValidator extends Quest
{
	public SkillTransferValidator(int id, String name, String descr)
	{
		super(id, name, descr);
		setOnEnterWorld(true);
	}
	
	private static final String qn = "SkillTransfer";
	
	private static final int[][] PORMANDERS =
	{
		{ 15307, 1 }, // Cardinal (97)
		{ 15308, 1 }, // Eva's Saint (105)
		{ 15309, 4 } // Shillen Saint (112)
	};
	
	@Override
	public String onEnterWorld(L2PcInstance player)
	{
		givePormanders(player);
		return null;
	}
	
	private void givePormanders(L2PcInstance player)
	{
		final int index = getTransferClassIndex(player);
		
		if (index >= 0)
		{
			QuestState st = player.getQuestState(qn);
			if (st == null)
				st = newQuestState(player);
			
			final String name = qn + String.valueOf(player.getClassId().getId());
			if (st.getInt(name) == 0)
			{
				st.setInternal(name, "1");
				if (st.getGlobalQuestVar(name).isEmpty())
				{
					st.saveGlobalQuestVar(name, "1");
					player.addItem(qn, PORMANDERS[index][0], PORMANDERS[index][1], null, true);
				}
			}
			
			if (Config.SKILL_CHECK_ENABLE && (!player.isGM() || Config.SKILL_CHECK_GM))
			{
				int count = PORMANDERS[index][1] - (int)player.getInventory().getInventoryItemCount(PORMANDERS[index][0], -1, false);
				for (L2Skill sk : player.getAllSkills())
				{
					for (L2SkillLearn s : SkillTreesData.getInstance().getTransferSkillTree(player.getClassId()).values())
					{
						if (s.getSkillId() == sk.getId())
						{
							// Holy Weapon allowed for Shilien Saint/Inquisitor stance
							if (sk.getId() == 1043 && index == 2 && player.isInStance())
								continue;
							
							count--;
							if (count < 0)
							{
								Util.handleIllegalPlayerAction(player, "Player " + player.getName() + " has too many transfered skills or items, skill:" + s.getName() + " ("+sk.getId() + "/" + sk.getLevel() + "), class:" + player.getTemplate().className, 1);
								if (Config.SKILL_CHECK_REMOVE)
									player.removeSkill(sk);
							}
						}
					}
				}
			}
		}
	}
	
	private int getTransferClassIndex(L2PcInstance player)
	{
		switch (player.getClassId().getId())
		{
			case 97: // Cardinal
				return 0;
			case 105: // Eva's Saint
				return 1;
			case 112: // Shillien Saint
				return 2;
			default:
				return -1;
		}
	}
	
	public static void main(String[] args)
	{
		new SkillTransferValidator(-1, qn, "custom");
	}
}