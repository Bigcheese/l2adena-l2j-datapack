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

import com.l2jserver.gameserver.SevenSigns;
import com.l2jserver.gameserver.handler.IItemHandler;
import com.l2jserver.gameserver.instancemanager.CastleManager;
import com.l2jserver.gameserver.instancemanager.MercTicketManager;
import com.l2jserver.gameserver.model.L2ItemInstance;
import com.l2jserver.gameserver.model.actor.L2Playable;
import com.l2jserver.gameserver.model.actor.instance.L2PcInstance;
import com.l2jserver.gameserver.model.entity.Castle;
import com.l2jserver.gameserver.network.SystemMessageId;
import com.l2jserver.gameserver.network.serverpackets.SystemMessage;

public class MercTicket implements IItemHandler
{
	/**
	 * handler for using mercenary tickets.  Things to do:
	 * 1) Check constraints:
	 * 1.a) Tickets may only be used in a castle
	 * 1.b) Only specific tickets may be used in each castle (different tickets for each castle)
	 * 1.c) only the owner of that castle may use them
	 * 1.d) tickets cannot be used during siege
	 * 1.e) Check if max number of tickets has been reached
	 * 1.f) Check if max number of tickets from this ticket's TYPE has been reached
	 * 2) If allowed, call the MercTicketManager to add the item and spawn in the world
	 * 3) Remove the item from the person's inventory
	 */
	public void useItem(L2Playable playable, L2ItemInstance item, boolean forceUse)
	{
		int itemId = item.getItemId();
		L2PcInstance activeChar = (L2PcInstance) playable;
		Castle castle = CastleManager.getInstance().getCastle(activeChar);
		int castleId = -1;
		if (castle != null)
			castleId = castle.getCastleId();
		
		//add check that certain tickets can only be placed in certain castles
		if (MercTicketManager.getInstance().getTicketCastleId(itemId) != castleId)
		{
			activeChar.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.MERCENARIES_CANNOT_BE_POSITIONED_HERE));
			return;
		}
		
		if (!activeChar.isCastleLord(castleId))
		{
			activeChar.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.YOU_DO_NOT_HAVE_AUTHORITY_TO_POSITION_MERCENARIES));
			return;
		}
		
		if (castle.getSiege().getIsInProgress())
		{
			activeChar.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.THIS_MERCENARY_CANNOT_BE_POSITIONED_ANYMORE));
			return;
		}
		
		//Checking Seven Signs Quest Period
		if (SevenSigns.getInstance().getCurrentPeriod() != SevenSigns.PERIOD_SEAL_VALIDATION)
		{
			//_log.warning("Someone has tried to spawn a guardian during Quest Event Period of The Seven Signs.");
			activeChar.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.THIS_MERCENARY_CANNOT_BE_POSITIONED_ANYMORE));
			return;
		}
		//Checking the Seal of Strife status
		switch (SevenSigns.getInstance().getSealOwner(SevenSigns.SEAL_STRIFE))
		{
			case SevenSigns.CABAL_NULL:
				if (SevenSigns.getInstance().checkIsDawnPostingTicket(itemId))
				{
					//_log.warning("Someone has tried to spawn a Dawn Mercenary though the Seal of Strife is not controlled by anyone.");
					activeChar.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.THIS_MERCENARY_CANNOT_BE_POSITIONED_ANYMORE));
					return;
				}
				break;
			case SevenSigns.CABAL_DUSK:
				if (!SevenSigns.getInstance().checkIsRookiePostingTicket(itemId))
				{
					//_log.warning("Someone has tried to spawn a non-Rookie Mercenary though the Seal of Strife is controlled by Revolutionaries of Dusk.");
					activeChar.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.THIS_MERCENARY_CANNOT_BE_POSITIONED_ANYMORE));
					return;
				}
				break;
			case SevenSigns.CABAL_DAWN:
				break;
		}
		
		if(MercTicketManager.getInstance().isAtCasleLimit(item.getItemId()))
		{
			activeChar.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.THIS_MERCENARY_CANNOT_BE_POSITIONED_ANYMORE));
			return;
		}
		
		if (MercTicketManager.getInstance().isAtTypeLimit(item.getItemId()))
		{
			activeChar.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.THIS_MERCENARY_CANNOT_BE_POSITIONED_ANYMORE));
			return;
		}
		if (MercTicketManager.getInstance().isTooCloseToAnotherTicket(activeChar.getX(), activeChar.getY(), activeChar.getZ()))
		{
			activeChar.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.POSITIONING_CANNOT_BE_DONE_BECAUSE_DISTANCE_BETWEEN_MERCENARIES_TOO_SHORT));
			return;
		}
		
		MercTicketManager.getInstance().addTicket(item.getItemId(), activeChar, null);
		activeChar.destroyItem("Consume", item.getObjectId(), 1, null, false); // Remove item from char's inventory
		activeChar.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.PLACE_CURRENT_LOCATION_DIRECTION).addItemName(item));
	}
}
