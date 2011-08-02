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
package handlers.usercommandhandlers;

import com.l2jserver.gameserver.handler.IUserCommandHandler;
import com.l2jserver.gameserver.model.L2Object;
import com.l2jserver.gameserver.model.actor.instance.L2PcInstance;
import com.l2jserver.gameserver.model.olympiad.Olympiad;
import com.l2jserver.gameserver.network.SystemMessageId;
import com.l2jserver.gameserver.network.serverpackets.SystemMessage;

/**
 * Support for /olympiadstat command
 * @author kamy, Zoey76
 */
public class OlympiadStat implements IUserCommandHandler
{
	private static final int[] COMMAND_IDS = { 109 };
	
	/**
	 * @see com.l2jserver.gameserver.handler.IUserCommandHandler#useUserCommand(int, com.l2jserver.gameserver.model.actor.instance.L2PcInstance)
	 */
	public boolean useUserCommand(int id, L2PcInstance activeChar)
	{
		if (id != COMMAND_IDS[0])
		{
			return false;
		}
		
		if (!activeChar.isNoble())
		{
			activeChar.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.NOBLESSE_ONLY));
			return false;
		}
		
		int nobleObjId = activeChar.getObjectId();
		final L2Object target = activeChar.getTarget();
		if (target != null)
		{
			if ((target instanceof L2PcInstance) && target.getActingPlayer().isNoble())
			{
				nobleObjId = target.getObjectId();
			}
			else
			{
				activeChar.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.NOBLESSE_ONLY));
				return false;
			}
		}
		
		final SystemMessage sm = SystemMessage.getSystemMessage(SystemMessageId.THE_CURRENT_RECORD_FOR_THIS_OLYMPIAD_SESSION_IS_S1_MATCHES_S2_WINS_S3_DEFEATS_YOU_HAVE_EARNED_S4_OLYMPIAD_POINTS);
		sm.addNumber(Olympiad.getInstance().getCompetitionDone(nobleObjId));
		sm.addNumber(Olympiad.getInstance().getCompetitionWon(nobleObjId));
		sm.addNumber(Olympiad.getInstance().getCompetitionLost(nobleObjId));
		sm.addNumber(Olympiad.getInstance().getNoblePoints(nobleObjId));
		activeChar.sendPacket(sm);
		return true;
	}
	
	/**
	 * @see com.l2jserver.gameserver.handler.IUserCommandHandler#getUserCommandList()
	 */
	public int[] getUserCommandList()
	{
		return COMMAND_IDS;
	}
}
