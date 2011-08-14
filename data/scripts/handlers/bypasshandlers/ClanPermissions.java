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

import java.util.StringTokenizer;

import com.l2jserver.gameserver.handler.IBypassHandler;
import com.l2jserver.gameserver.model.L2Clan;
import com.l2jserver.gameserver.model.actor.L2Character;
import com.l2jserver.gameserver.model.actor.L2Npc;
import com.l2jserver.gameserver.model.actor.instance.L2NpcInstance;
import com.l2jserver.gameserver.model.actor.instance.L2PcInstance;
import com.l2jserver.gameserver.network.serverpackets.NpcHtmlMessage;

public class ClanPermissions implements IBypassHandler
{
	private static final String[] COMMANDS =
	{
		"ViewClanPermissions",
		"SetClanPermission"
	};
	
	private static final String[] RANKS =
	{
		"1st",
		"2nd",
		"3rd",
		"4th",
		"5th"
	};
	
	public void viewPerms(L2Character target, L2PcInstance activeChar, L2Clan clan)
	{
		NpcHtmlMessage msg = new NpcHtmlMessage(((L2Npc)target).getObjectId());
		String message = "<html>";
		for (int i = 0; i < RANKS.length; ++i)
		{
			String value = "";
			String action = "true";
			if ((clan.getRankPrivs(i + 1) & L2Clan.CP_CL_WITHDRAWL) == L2Clan.CP_CL_WITHDRAWL)
			{
				value = "X";
				action = "false";
			}
			message += RANKS[i] + " Level<br>"
				       + "Withdraw From Warehouse: <button action=\"bypass -h npc_" + ((L2Npc)target).getObjectId() + "_SetClanPermission " + (i + 1) + " withdraw " + action + "\" value=\"" + value + "\" width=14 height=14 back=\"L2UI_CT1.Button_DF_Down\" fore=\"L2UI_CT1.Button_DF\"><br>";
		}
		message += "</html>";
		msg.setHtml(message);
		activeChar.sendPacket(msg);
	}

	public boolean useBypass(String command, L2PcInstance activeChar, L2Character target)
	{
		if (!(target instanceof L2NpcInstance) || !activeChar.isClanLeader())
			return false;

		L2Clan clan = activeChar.getClan();

		if (command.startsWith(COMMANDS[0])) {
			viewPerms(target, activeChar, clan);
		} else if (command.startsWith(COMMANDS[1]))
		{
			StringTokenizer st = new StringTokenizer(command);
			st.nextToken(); // bypass "SetClanPermission"
			if (!st.hasMoreTokens())
				return false;

			String rankS = st.nextToken();
			int rank = Integer.parseInt(rankS);
			String perm = st.nextToken();
			String value = st.nextToken();

			if (perm.equals("withdraw"))
			{
				if (value.equals("true"))
				{
					clan.setRankPrivs(rank, clan.getRankPrivs(rank) | L2Clan.CP_CL_WITHDRAWL | L2Clan.CP_CL_VIEW_WAREHOUSE);
				}else
				{
					clan.setRankPrivs(rank, clan.getRankPrivs(rank) & ~L2Clan.CP_CL_WITHDRAWL);
				}
			}

			viewPerms(target, activeChar, clan);
		}

		return true;
	}

	public String[] getBypassList()
	{
		return COMMANDS;
	}
}
