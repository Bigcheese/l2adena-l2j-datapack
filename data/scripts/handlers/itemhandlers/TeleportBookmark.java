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
package handlers.itemhandlers;

import com.l2jserver.gameserver.handler.IItemHandler;
import com.l2jserver.gameserver.model.L2ItemInstance;
import com.l2jserver.gameserver.model.actor.L2Playable;
import com.l2jserver.gameserver.model.actor.instance.L2PcInstance;
import com.l2jserver.gameserver.network.SystemMessageId;
import com.l2jserver.gameserver.network.serverpackets.SystemMessage;

/**
 * Teleport Bookmark Slot Handler
 *
 * @author ShanSoft
 */
public class TeleportBookmark implements IItemHandler
{
	
	public void useItem(L2Playable playable, L2ItemInstance item, boolean forceUse)
	{
		if (playable == null || item == null || !(playable instanceof L2PcInstance))
			return;
		
		L2PcInstance player = (L2PcInstance) playable;
		
		if(player.getBookMarkSlot() >= 9)
		{
			player.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.YOUR_NUMBER_OF_MY_TELEPORTS_SLOTS_HAS_REACHED_ITS_MAXIMUM_LIMIT));
			return;
		}
		
		player.destroyItem("Consume", item.getObjectId(), 1, null, false);
		
		player.setBookMarkSlot(player.getBookMarkSlot()+3);
		player.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.THE_NUMBER_OF_MY_TELEPORTS_SLOTS_HAS_BEEN_INCREASED));
		
		SystemMessage sm = SystemMessage.getSystemMessage(SystemMessageId.S1_DISAPPEARED);
		sm.addItemName(item.getItemId());
		player.sendPacket(sm);
	}
}
