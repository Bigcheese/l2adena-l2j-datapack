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
package teleports.StrongholdsTeleports;

import com.l2jserver.gameserver.model.actor.L2Npc;
import com.l2jserver.gameserver.model.actor.instance.L2PcInstance;
import com.l2jserver.gameserver.model.quest.Quest;

/**
 * @author Plim
 * Original python script by Kerberos
 */
public class StrongholdsTeleports extends Quest
{
	private final static int[] NPCs = {32163,32181,32184,32186};
	
	@Override
	public String onFirstTalk(L2Npc npc, L2PcInstance player)
	{
		String htmltext = "";

	    if (player.getLevel() < 20)
	       htmltext = String.valueOf(npc.getNpcId()) + ".htm";
	    else
	       htmltext = String.valueOf(npc.getNpcId()) + "-no.htm";
	    
	    return htmltext;
	}

	public StrongholdsTeleports(int questId, String name, String descr)
	{
		super(questId, name, descr);
		
		for (int npcId : NPCs)
			addFirstTalkId(npcId);
	}
	
	public static void main(String[] args)
	{
		new StrongholdsTeleports(-1, StrongholdsTeleports.class.getSimpleName(), "teleports");
	}
}
