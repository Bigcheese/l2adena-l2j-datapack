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
import com.l2jserver.gameserver.handler.IVoicedCommandHandler;
import com.l2jserver.gameserver.handler.VoicedCommandHandler;
import com.l2jserver.gameserver.model.actor.L2Character;
import com.l2jserver.gameserver.model.actor.instance.L2PcInstance;

/**
 * 
 * @author DS
 *
 */
public class VoiceCommand implements IBypassHandler
{
	private static final String[] COMMANDS =
	{
		"voice"
	};

	public boolean useBypass(String command, L2PcInstance activeChar, L2Character target)
	{
		// only voice commands allowed
		if (command.length() > 7 && command.charAt(6) == '.')
		{
			final String vc, vparams;
			int endOfCommand = command.indexOf(" ", 7);
			if (endOfCommand > 0)
			{
				vc = command.substring(7, endOfCommand).trim();
				vparams = command.substring(endOfCommand).trim();
			}
			else
			{
				vc = command.substring(7).trim();
				vparams = null;
			}

			if (vc.length() > 0)
			{
				IVoicedCommandHandler vch = VoicedCommandHandler.getInstance().getVoicedCommandHandler(vc);
				if (vch != null)
					return vch.useVoicedCommand(vc, activeChar, vparams);
			}
		}

		return false;
	}

	public String[] getBypassList()
	{
		return COMMANDS;
	}
}