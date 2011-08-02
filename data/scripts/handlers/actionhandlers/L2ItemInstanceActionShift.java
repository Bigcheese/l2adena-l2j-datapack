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

import com.l2jserver.gameserver.handler.IActionHandler;
import com.l2jserver.gameserver.model.L2ItemInstance;
import com.l2jserver.gameserver.model.L2Object;
import com.l2jserver.gameserver.model.L2Object.InstanceType;
import com.l2jserver.gameserver.model.actor.instance.L2PcInstance;
import com.l2jserver.gameserver.network.serverpackets.NpcHtmlMessage;
import com.l2jserver.util.StringUtil;

public class L2ItemInstanceActionShift implements IActionHandler
{
	public boolean action(L2PcInstance activeChar, L2Object target, boolean interact)
	{
		if (activeChar.getAccessLevel().isGm())
		{
			NpcHtmlMessage html = new NpcHtmlMessage(target.getObjectId());
			final String html1 = StringUtil.concat(
					"<html><body><center><font color=\"LEVEL\">Item Info</font></center><br><table border=0>",
					"<tr><td>Object ID: </td><td>",
					String.valueOf(target.getObjectId()),
					"</td></tr><tr><td>Item ID: </td><td>",
					String.valueOf(((L2ItemInstance)target).getItemId()),
					"</td></tr><tr><td>Owner ID: </td><td>",
					String.valueOf(((L2ItemInstance)target).getOwnerId()),
					"</td></tr><tr><td>Location: </td><td>",
					String.valueOf(((L2ItemInstance)target).getLocation()),
					"</td></tr><tr><td><br></td></tr><tr><td>Class: </td><td>",
					target.getClass().getSimpleName(),
					"</td></tr></table></body></html>"
			);
			html.setHtml(html1);
			activeChar.sendPacket(html);
		}
		return true;
	}
	
	public InstanceType getInstanceType()
	{
		return InstanceType.L2ItemInstance;
	}
}
