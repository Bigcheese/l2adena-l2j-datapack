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
package handlers.actionhandlers;

import com.l2jserver.gameserver.ai.CtrlIntention;
import com.l2jserver.gameserver.handler.IActionHandler;
import com.l2jserver.gameserver.instancemanager.MercTicketManager;
import com.l2jserver.gameserver.model.L2ItemInstance;
import com.l2jserver.gameserver.model.L2Object;
import com.l2jserver.gameserver.model.L2Object.InstanceType;
import com.l2jserver.gameserver.model.actor.instance.L2PcInstance;

public class L2ItemInstanceAction implements IActionHandler
{
	public boolean action(L2PcInstance activeChar, L2Object target, boolean interact)
	{
		// this causes the validate position handler to do the pickup if the location is reached.
		// mercenary tickets can only be picked up by the castle owner.
		final int castleId = MercTicketManager.getInstance().getTicketCastleId(((L2ItemInstance)target).getItemId());
		
		if (castleId > 0 &&  (!activeChar.isCastleLord(castleId) || activeChar.isInParty()))
		{
			if (activeChar.isInParty())    //do not allow owner who is in party to pick tickets up
				activeChar.sendMessage("You cannot pickup mercenaries while in a party.");
			else
				activeChar.sendMessage("Only the castle lord can pickup mercenaries.");
			
			activeChar.setTarget(target);
			activeChar.getAI().setIntention(CtrlIntention.AI_INTENTION_IDLE);
		}
		else if (!activeChar.isFlying()) // cannot pickup
			activeChar.getAI().setIntention(CtrlIntention.AI_INTENTION_PICK_UP, target);
		
		return true;
	}
	
	public InstanceType getInstanceType()
	{
		return InstanceType.L2ItemInstance;
	}
}