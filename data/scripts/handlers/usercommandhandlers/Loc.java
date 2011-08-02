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
import com.l2jserver.gameserver.instancemanager.MapRegionManager;
import com.l2jserver.gameserver.instancemanager.ZoneManager;
import com.l2jserver.gameserver.model.actor.instance.L2PcInstance;
import com.l2jserver.gameserver.model.base.Race;
import com.l2jserver.gameserver.model.zone.type.L2RespawnZone;
import com.l2jserver.gameserver.network.serverpackets.SystemMessage;

public class Loc implements IUserCommandHandler
{
	private static final int[] COMMAND_IDS =
	{
		0
	};
	
	/**
	 * 
	 * @see com.l2jserver.gameserver.handler.IUserCommandHandler#useUserCommand(int, com.l2jserver.gameserver.model.actor.instance.L2PcInstance)
	 */
	public boolean useUserCommand(int id, L2PcInstance activeChar)
	{
		int region;
		L2RespawnZone zone = ZoneManager.getInstance().getZone(activeChar, L2RespawnZone.class);
		
		if (zone != null)
			region = MapRegionManager.getInstance().getRestartRegion(activeChar, zone.getAllRespawnPoints().get(Race.Human)).getLocId();
		else
			region = MapRegionManager.getInstance().getMapRegionLocId(activeChar);
		
		SystemMessage sm = SystemMessage.getSystemMessage(region);
		if(sm.getSystemMessageId().getParamCount() == 3)
		{
			sm.addNumber(activeChar.getX());
			sm.addNumber(activeChar.getY());
			sm.addNumber(activeChar.getZ());
		}
		activeChar.sendPacket(sm);
		return true;
	}
	
	/**
	 * 
	 * @see com.l2jserver.gameserver.handler.IUserCommandHandler#getUserCommandList()
	 */
	public int[] getUserCommandList()
	{
		return COMMAND_IDS;
	}
}
