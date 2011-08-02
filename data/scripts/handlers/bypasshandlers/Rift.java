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
package handlers.bypasshandlers;

import com.l2jserver.gameserver.handler.IBypassHandler;
import com.l2jserver.gameserver.instancemanager.DimensionalRiftManager;
import com.l2jserver.gameserver.model.actor.L2Character;
import com.l2jserver.gameserver.model.actor.L2Npc;
import com.l2jserver.gameserver.model.actor.instance.L2PcInstance;

public class Rift implements IBypassHandler
{
	private static final String[] COMMANDS =
	{
		"enterrift",
		"changeriftroom",
		"exitrift"
	};
	
	public boolean useBypass(String command, L2PcInstance activeChar, L2Character target)
	{
		if (!(target instanceof L2Npc))
			return false;
		
		if (command.toLowerCase().startsWith(COMMANDS[0])) // EnterRift
		{
			try
			{
				Byte b1 = Byte.parseByte(command.substring(10)); // Selected Area: Recruit, Soldier etc
				DimensionalRiftManager.getInstance().start(activeChar, b1, (L2Npc)target);
				return true;
			}
			catch (Exception e)
			{
				_log.info("Exception in " + getClass().getSimpleName());
			}
		}
		else
		{
			final boolean inRift = activeChar.isInParty() && activeChar.getParty().isInDimensionalRift();
			
			if (command.toLowerCase().startsWith(COMMANDS[1])) //ChangeRiftRoom
			{
				if (inRift)
					activeChar.getParty().getDimensionalRift().manualTeleport(activeChar, (L2Npc)target);
				else
					DimensionalRiftManager.getInstance().handleCheat(activeChar, (L2Npc)target);
				
				return true;
			}
			else if (command.toLowerCase().startsWith(COMMANDS[2])) // ExitRift
			{
				if (inRift)
					activeChar.getParty().getDimensionalRift().manualExitRift(activeChar, (L2Npc)target);
				else
					DimensionalRiftManager.getInstance().handleCheat(activeChar, (L2Npc)target);
				
			}
			return true;
		}
		return false;
	}
	
	public String[] getBypassList()
	{
		return COMMANDS;
	}
}