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
package events.TheValentineEvent;

import com.l2jserver.gameserver.instancemanager.QuestManager;
import com.l2jserver.gameserver.model.actor.L2Npc;
import com.l2jserver.gameserver.model.actor.instance.L2PcInstance;
import com.l2jserver.gameserver.model.quest.Quest;
import com.l2jserver.gameserver.model.quest.QuestState;
import com.l2jserver.gameserver.model.quest.State;


/**
 * Event Code for "The Valentine Event"
 * http://www.lineage2.com/archive/2009/01/the_valentine_e.html
 * @author  Gnat
 */
public class TheValentineEvent extends Quest
{
	private static final int _npc		= 4301;
	private static final int _recipe	= 20191;
	
	private static final int[][] _spawns =
	{
		{87792,-142240,-1343,44000},
		{87616,-140688,-1542,16500},
		{114733,-178691,-821,0},
		{115708,-182362,-1449,0},
		{-44337,-113669,-224,0},
		{-44628,-115409,-240,22500},
		{-13073,122801,-3117,0},
		{-13949,121934,-2988,32768},
		{-14822,123708,-3117,8192},
		{-80762,151118,-3043,28672},
		{-84049,150176,-3129,4096},
		{-82623,151666,-3129,49152},
		{-84516,242971,-3730,34000},
		{-86003,243205,-3730,60000},
		{11281,15652,-4584,25000},
		{11303,17732,-4574,57344},
		{47151,49436,-3059,32000},
		{79806,55570,-1560,0},
		{83328,55824,-1525,32768},
		{80986,54504,-1525,32768},
		{18178,145149,-3054,7400},
		{19208,144380,-3097,32768},
		{19508,145775,-3086,48000},
		{17396,170259,-3507,30000},
		{83332,149160,-3405,49152},
		{82277,148598,-3467,0},
		{81621,148725,-3467,32768},
		{81680,145656,-3533,32768},
		{117498,76630,-2695,38000},
		{115914,76449,-2711,59000},
		{119536,76988,-2275,40960},
		{147120,27312,-2192,40960},
		{147920,25664,-2000,16384},
		{111776,221104,-3543,16384},
		{107904,218096,-3675,0},
		{114920,220020,-3632,32768},
		{147888,-58048,-2979,49000},
		{147285,-56461,-2776,11500},
		{44176,-48732,-800,33000},
		{44294,-47642,-792,50000},
		{-116677,46824,360,34828}
	};
	
	public TheValentineEvent(int questId, String name, String descr)
	{
		super(questId, name, descr);
		addStartNpc(_npc);
		addFirstTalkId(_npc);
		addTalkId(_npc);
		for(int[] _spawn : _spawns)
			addSpawn(_npc, _spawn[0], _spawn[1], _spawn[2], _spawn[3], false, 0);
	}
	
	@Override
	public String onAdvEvent(String event, L2Npc npc, L2PcInstance player)
	{
		String htmltext = "";
		QuestState st = player.getQuestState(getName());
		
		htmltext = event;
		if(event.equalsIgnoreCase("4301-3.htm"))
		{
			if(st.getState() == State.COMPLETED)
			{
				htmltext = "4301-4.htm";
			}
			else
			{
				st.giveItems(_recipe, 1);
				st.playSound("Itemsound.quest_itemget");
				st.setState(State.COMPLETED);
			}
		}
		return htmltext;
	}
	
	@Override
	public String onFirstTalk(L2Npc npc, L2PcInstance player)
	{
		String htmltext = "";
		QuestState st = player.getQuestState(getName());
		if (st == null)
		{
			Quest q = QuestManager.getInstance().getQuest(getName());
			st = q.newQuestState(player);
		}
		htmltext = npc.getNpcId() + ".htm";
		return htmltext;
	}
	
	public static void main(String[] args)
	{
		new TheValentineEvent(-1, "TheValentineEvent", "events");
	}
}