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
package handlers.skillhandlers;

import com.l2jserver.gameserver.handler.ISkillHandler;
import com.l2jserver.gameserver.model.L2Object;
import com.l2jserver.gameserver.model.L2Skill;
import com.l2jserver.gameserver.model.actor.L2Character;
import com.l2jserver.gameserver.model.actor.L2Trap;
import com.l2jserver.gameserver.model.actor.instance.L2PcInstance;
import com.l2jserver.gameserver.model.quest.Quest;
import com.l2jserver.gameserver.model.quest.Quest.TrapAction;
import com.l2jserver.gameserver.network.SystemMessageId;
import com.l2jserver.gameserver.network.serverpackets.SystemMessage;
import com.l2jserver.gameserver.templates.skills.L2SkillType;

public class Trap implements ISkillHandler
{
	private static final L2SkillType[] SKILL_IDS =
	{
		L2SkillType.DETECT_TRAP,
		L2SkillType.REMOVE_TRAP
	};
	
	/**
	 * 
	 * @see com.l2jserver.gameserver.handler.ISkillHandler#useSkill(com.l2jserver.gameserver.model.actor.L2Character, com.l2jserver.gameserver.model.L2Skill, com.l2jserver.gameserver.model.L2Object[])
	 */
	public void useSkill(L2Character activeChar, L2Skill skill, L2Object[] targets)
	{
		if (activeChar == null || skill == null)
			return;
		
		switch (skill.getSkillType())
		{
			case DETECT_TRAP:
			{
				for (L2Character target: activeChar.getKnownList().getKnownCharactersInRadius(skill.getSkillRadius()))
				{
					if (!(target instanceof L2Trap))
						continue;
					
					if (target.isAlikeDead())
						continue;
					
					final L2Trap trap = (L2Trap)target;
					
					if (trap.getLevel() <= skill.getPower())
						trap.setDetected(activeChar);
				}
				break;
			}
			case REMOVE_TRAP:
			{
				for (L2Character target: (L2Character[]) targets)
				{
					if (!(target instanceof L2Trap))
						continue;
					
					if (target.isAlikeDead())
						continue;
					
					final L2Trap trap = (L2Trap)target;
					
					if (!trap.canSee(activeChar))
					{
						if (activeChar instanceof L2PcInstance)
							((L2PcInstance) activeChar).sendPacket(SystemMessage.getSystemMessage(SystemMessageId.INCORRECT_TARGET));
						continue;
					}
					
					if (trap.getLevel() > skill.getPower())
						continue;
					
					if (trap.getTemplate().getEventQuests(Quest.QuestEventType.ON_TRAP_ACTION) != null)
						for (Quest quest : trap.getTemplate().getEventQuests(Quest.QuestEventType.ON_TRAP_ACTION))
							quest.notifyTrapAction(trap, activeChar, TrapAction.TRAP_DISARMED);
					
					trap.unSummon();
					if (activeChar instanceof L2PcInstance)
						((L2PcInstance) activeChar).sendPacket(SystemMessage.getSystemMessage(SystemMessageId.A_TRAP_DEVICE_HAS_BEEN_STOPPED));
				}
			}
		}
	}
	
	/**
	 * 
	 * @see com.l2jserver.gameserver.handler.ISkillHandler#getSkillIds()
	 */
	public L2SkillType[] getSkillIds()
	{
		return SKILL_IDS;
	}
}
