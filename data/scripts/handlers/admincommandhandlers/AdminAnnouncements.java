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
package handlers.admincommandhandlers;

import java.util.Collection;
import java.util.List;
import java.util.StringTokenizer;

import javolution.text.TextBuilder;

import com.l2jserver.Config;
import com.l2jserver.gameserver.Announcements;
import com.l2jserver.gameserver.cache.HtmCache;
import com.l2jserver.gameserver.handler.IAdminCommandHandler;
import com.l2jserver.gameserver.model.L2World;
import com.l2jserver.gameserver.model.actor.instance.L2PcInstance;
import com.l2jserver.gameserver.network.serverpackets.NpcHtmlMessage;
import com.l2jserver.gameserver.taskmanager.AutoAnnounceTaskManager;
import com.l2jserver.gameserver.taskmanager.AutoAnnounceTaskManager.AutoAnnouncement;
import com.l2jserver.util.StringUtil;


/**
 * This class handles following admin commands:
 * - announce text = announces text to all players
 * - list_announcements = show menu
 * - reload_announcements = reloads announcements from txt file
 * - announce_announcements = announce all stored announcements to all players
 * - add_announcement text = adds text to startup announcements
 * - del_announcement id = deletes announcement with respective id
 *
 * @version $Revision: 1.4.4.5 $ $Date: 2005/04/11 10:06:06 $
 */
public class AdminAnnouncements implements IAdminCommandHandler
{
	
	private static final String[] ADMIN_COMMANDS =
	{
		"admin_list_announcements",
		"admin_reload_announcements",
		"admin_announce_announcements",
		"admin_add_announcement",
		"admin_del_announcement",
		"admin_announce",
		"admin_announce_menu",
		"admin_list_autoann",
		"admin_reload_autoann",
		"admin_add_autoann",
		"admin_del_autoann"
	};
	
	public boolean useAdminCommand(String command, L2PcInstance activeChar)
	{
		if (command.equals("admin_list_announcements"))
		{
			Announcements.getInstance().listAnnouncements(activeChar);
		}
		else if (command.equals("admin_reload_announcements"))
		{
			Announcements.getInstance().loadAnnouncements();
			Announcements.getInstance().listAnnouncements(activeChar);
		}
		else if (command.startsWith("admin_announce_menu"))
		{
			if (Config.GM_ANNOUNCER_NAME && command.length() > 20)
				command += " ("+activeChar.getName()+")";
			Announcements.getInstance().handleAnnounce(command, 20);
			AdminHelpPage.showHelpPage(activeChar, "gm_menu.htm");
		}
		else if (command.equals("admin_announce_announcements"))
		{
			Collection<L2PcInstance> pls = L2World.getInstance().getAllPlayers().values();
			// synchronized (L2World.getInstance().getAllPlayers())
			{
				for (L2PcInstance player : pls)
					Announcements.getInstance().showAnnouncements(player);
			}
			Announcements.getInstance().listAnnouncements(activeChar);
		}
		else if (command.startsWith("admin_add_announcement"))
		{
			// FIXME the player can send only 16 chars (if you try to send more
			// it sends null), remove this function or not?
			if (!command.equals("admin_add_announcement"))
			{
				try
				{
					String val = command.substring(23);
					Announcements.getInstance().addAnnouncement(val);
					Announcements.getInstance().listAnnouncements(activeChar);
				}
				catch (StringIndexOutOfBoundsException e)
				{
				}// ignore errors
			}
		}
		else if (command.startsWith("admin_del_announcement"))
		{
			try
			{
				int val = Integer.parseInt(command.substring(23));
				Announcements.getInstance().delAnnouncement(val);
				Announcements.getInstance().listAnnouncements(activeChar);
			}
			catch (StringIndexOutOfBoundsException e)
			{
			}
		}
		
		// Command is admin announce
		else if (command.startsWith("admin_announce"))
		{
			if (Config.GM_ANNOUNCER_NAME && command.length() > 15)
				command += " ("+activeChar.getName()+")";
			// Call method from another class
			Announcements.getInstance().handleAnnounce(command, 15);
		}
		else if (command.startsWith("admin_list_autoann"))
		{
			listAutoAnnouncements(activeChar);
		}
		else if (command.startsWith("admin_reload_autoann"))
		{
			AutoAnnounceTaskManager.getInstance().restore();
			activeChar.sendMessage("AutoAnnouncement Reloaded.");
			listAutoAnnouncements(activeChar);
		}
		else if (command.startsWith("admin_add_autoann"))
		{
			StringTokenizer st = new StringTokenizer(command);
			st.nextToken();
			
			if (!st.hasMoreTokens())
			{
				activeChar.sendMessage("Not enough parameters for adding autoannounce!");
				return false;
			}
			long initial = Long.parseLong(st.nextToken());
			if (!st.hasMoreTokens())
			{
				activeChar.sendMessage("Not enough parameters for adding autoannounce!");
				return false;
			}
			long delay = Long.parseLong(st.nextToken());
			if (!st.hasMoreTokens())
			{
				activeChar.sendMessage("Not enough parameters for adding autoannounce!");
				return false;
			}
			int repeat = Integer.parseInt(st.nextToken());
			if (!st.hasMoreTokens())
			{
				activeChar.sendMessage("Not enough parameters for adding autoannounce!");
				return false;
			}
			TextBuilder memo = new TextBuilder();
			while (st.hasMoreTokens())
			{
				memo.append(st.nextToken());
				memo.append(" ");
			}
			
			AutoAnnounceTaskManager.getInstance().addAutoAnnounce(initial*1000, delay*1000, repeat, memo.toString().trim());
			listAutoAnnouncements(activeChar);
		}
		
		else if (command.startsWith("admin_del_autoann"))
		{
			StringTokenizer st = new StringTokenizer(command);
			st.nextToken();
			
			if (!st.hasMoreTokens())
			{
				activeChar.sendMessage("Not enough parameters for deleting autoannounce!");
				return false;
			}
			
			AutoAnnounceTaskManager.getInstance().deleteAutoAnnounce(Integer.parseInt(st.nextToken()));
			listAutoAnnouncements(activeChar);
		}
		return true;
	}
	
	private void listAutoAnnouncements(L2PcInstance activeChar)
	{
		String content = HtmCache.getInstance().getHtmForce(activeChar.getHtmlPrefix(), "data/html/admin/autoannounce.htm");
		NpcHtmlMessage adminReply = new NpcHtmlMessage(5);
		adminReply.setHtml(content);
		
		final StringBuilder replyMSG = StringUtil.startAppend(500, "<br>");
		List<AutoAnnouncement> autoannouncements = AutoAnnounceTaskManager.getInstance().getAutoAnnouncements();
		for (int i = 0; i < autoannouncements.size(); i++)
		{
			AutoAnnouncement autoann = autoannouncements.get(i);
			TextBuilder memo2 = new TextBuilder();
			for (String memo0 : autoann.getMemo())
			{
				memo2.append(memo0);
				memo2.append("/n");
			}
			replyMSG.append("<table width=260><tr><td width=220>");
			replyMSG.append(memo2.toString().trim());
			replyMSG.append("</td><td width=40><button value=\"Delete\" action=\"bypass -h admin_del_autoann ");
			replyMSG.append(i);
			replyMSG.append("\" width=60 height=15 back=\"L2UI_ct1.button_df\" fore=\"L2UI_ct1.button_df\"></td></tr></table>");
		}
		adminReply.replace("%announces%", replyMSG.toString());
		
		activeChar.sendPacket(adminReply);
	}
	
	public String[] getAdminCommandList()
	{
		return ADMIN_COMMANDS;
	}
}
