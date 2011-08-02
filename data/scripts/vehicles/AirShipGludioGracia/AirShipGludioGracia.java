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
package vehicles.AirShipGludioGracia;

import com.l2jserver.gameserver.ThreadPoolManager;
import com.l2jserver.gameserver.instancemanager.AirShipManager;
import com.l2jserver.gameserver.model.L2Object;
import com.l2jserver.gameserver.model.L2World;
import com.l2jserver.gameserver.model.Location;
import com.l2jserver.gameserver.model.VehiclePathPoint;
import com.l2jserver.gameserver.model.actor.L2Npc;
import com.l2jserver.gameserver.model.actor.instance.L2AirShipInstance;
import com.l2jserver.gameserver.model.actor.instance.L2PcInstance;
import com.l2jserver.gameserver.model.quest.Quest;
import com.l2jserver.gameserver.network.SystemMessageId;
import com.l2jserver.gameserver.network.clientpackets.Say2;
import com.l2jserver.gameserver.network.serverpackets.NpcSay;

/**
 * 
 * @author DS
 *
 */
public class AirShipGludioGracia extends Quest implements Runnable
{
	private static final int[] CONTROLLERS = {32607, 32609};
	
	private static final int GLUDIO_DOCK_ID = 10;
	private static final int GRACIA_DOCK_ID = 11;
	
	private static final Location OUST_GLUDIO = new Location(-149379, 255246, -80);
	private static final Location OUST_GRACIA = new Location(-186563, 243590, 2608);
	
	private static final VehiclePathPoint[] GLUDIO_TO_WARPGATE =
	{
		new VehiclePathPoint(-151202, 252556, 231),
		new VehiclePathPoint(-160403, 256144, 222),
		new VehiclePathPoint(-167874, 256731, -509, 0, 41035) // teleport: x,y,z,speed=0,heading
	};
	
	private static final VehiclePathPoint[] WARPGATE_TO_GRACIA =
	{
		new VehiclePathPoint(-169763, 254815, 282),
		new VehiclePathPoint(-171822, 250061, 425),
		new VehiclePathPoint(-172595, 247737, 398),
		new VehiclePathPoint(-174538, 246185, 39),
		new VehiclePathPoint(-179440, 243651, 1337),
		new VehiclePathPoint(-182601, 243957, 2739),
		new VehiclePathPoint(-184952, 245122, 2694),
		new VehiclePathPoint(-186936, 244563, 2617)
	};
	
	private static final VehiclePathPoint[] GRACIA_TO_WARPGATE =
	{
		new VehiclePathPoint(-187801, 244997, 2672),
		new VehiclePathPoint(-188520, 245932, 2465),
		new VehiclePathPoint(-189932, 245243, 1682),
		new VehiclePathPoint(-191192, 242969, 1523),
		new VehiclePathPoint(-190408, 239088, 1706),
		new VehiclePathPoint(-187475, 237113, 2768),
		new VehiclePathPoint(-184673, 238433, 2802),
		new VehiclePathPoint(-184524, 241119, 2816),
		new VehiclePathPoint(-182129, 243385, 2733),
		new VehiclePathPoint(-179440, 243651, 1337),
		new VehiclePathPoint(-174538, 246185, 39),
		new VehiclePathPoint(-172595, 247737, 398),
		new VehiclePathPoint(-171822, 250061, 425),
		new VehiclePathPoint(-169763, 254815, 282),
		new VehiclePathPoint(-168067, 256626, 343),
		new VehiclePathPoint(-157261, 255664, 221, 0, 64781) // teleport: x,y,z,speed=0,heading
	};
	
	private static final VehiclePathPoint[] WARPGATE_TO_GLUDIO =
	{
		new VehiclePathPoint(-153414, 255385, 221),
		new VehiclePathPoint(-149548, 258172, 221),
		new VehiclePathPoint(-146884, 257097, 221),
		new VehiclePathPoint(-146672, 254239, 221),
		new VehiclePathPoint(-147855, 252712, 206),
		new VehiclePathPoint(-149378, 252552, 198)
	};
	
	private final L2AirShipInstance _ship;
	private int _cycle = 0;
	
	private boolean _foundAtcGludio = false;
	private L2Npc _atcGludio = null;
	private boolean _foundAtcGracia = false;
	private L2Npc _atcGracia = null;
	
	@Override
	public final String onAdvEvent(String event, L2Npc npc, L2PcInstance player)
	{
		if (player.isTransformed())
		{
			player.sendPacket(SystemMessageId.YOU_CANNOT_BOARD_AN_AIRSHIP_WHILE_TRANSFORMED);
			return null;
		}
		if (player.isParalyzed())
		{
			player.sendPacket(SystemMessageId.YOU_CANNOT_BOARD_AN_AIRSHIP_WHILE_PETRIFIED);
			return null;
		}
		if (player.isDead() || player.isFakeDeath())
		{
			player.sendPacket(SystemMessageId.YOU_CANNOT_BOARD_AN_AIRSHIP_WHILE_DEAD);	
			return null;
		}
		if (player.isFishing())
		{
			player.sendPacket(SystemMessageId.YOU_CANNOT_BOARD_AN_AIRSHIP_WHILE_FISHING);
			return null;
		}
		if (player.isInCombat())
		{
			player.sendPacket(SystemMessageId.YOU_CANNOT_BOARD_AN_AIRSHIP_WHILE_IN_BATTLE);
			return null;
		}
		if (player.isInDuel())
		{
			player.sendPacket(SystemMessageId.YOU_CANNOT_BOARD_AN_AIRSHIP_WHILE_IN_A_DUEL);
			return null;
		}
		if (player.isSitting())
		{
			player.sendPacket(SystemMessageId.YOU_CANNOT_BOARD_AN_AIRSHIP_WHILE_SITTING);
			return null;
		}
		if (player.isCastingNow())
		{
			player.sendPacket(SystemMessageId.YOU_CANNOT_BOARD_AN_AIRSHIP_WHILE_CASTING);
			return null;
		}
		if (player.isCursedWeaponEquipped())
		{
			player.sendPacket(SystemMessageId.YOU_CANNOT_BOARD_AN_AIRSHIP_WHILE_A_CURSED_WEAPON_IS_EQUIPPED);
			return null;
		}
		if (player.isCombatFlagEquipped())
		{
			player.sendPacket(SystemMessageId.YOU_CANNOT_BOARD_AN_AIRSHIP_WHILE_HOLDING_A_FLAG);
			return null;
		}
		if (player.getPet() != null || player.isMounted())
		{
			player.sendPacket(SystemMessageId.YOU_CANNOT_BOARD_AN_AIRSHIP_WHILE_A_PET_OR_A_SERVITOR_IS_SUMMONED);
			return null;
		}
		
		if (_ship.isInDock() && _ship.isInsideRadius(player, 600, true, false))
			_ship.addPassenger(player);
		
		return null;
	}
	
	@Override
	public final String onFirstTalk(L2Npc npc, L2PcInstance player)
	{
		if (player.getQuestState(getName()) == null)
			newQuestState(player);
		
		return npc.getNpcId() + ".htm";
	}
	
	public AirShipGludioGracia(int questId, String name, String descr)
	{
		super(questId, name, descr);
		for (int id : CONTROLLERS)
		{
			addStartNpc(id);
			addFirstTalkId(id);
			addTalkId(id);
		}
		_ship = AirShipManager.getInstance().getNewAirShip(-149378, 252552, 198, 33837);
		_ship.setOustLoc(OUST_GLUDIO);
		_ship.registerEngine(this);
		_ship.runEngine(60000);
	}
	
	public void run()
	{
		try
		{
			switch (_cycle)
			{
				case 0:
					broadcastInGludio(1800223); // The regularly scheduled airship that flies to the Gracia continent has departed.
					_ship.setInDock(0);
					_ship.executePath(GLUDIO_TO_WARPGATE);
					break;
				case 1:
					//_ship.teleToLocation(-167874, 256731, -509, 41035, false);
					_ship.setOustLoc(OUST_GRACIA);
					ThreadPoolManager.getInstance().scheduleGeneral(this, 5000);
					break;
				case 2:
					_ship.executePath(WARPGATE_TO_GRACIA);
					break;
				case 3:
					broadcastInGracia(1800220); // The regularly scheduled airship has arrived. It will depart for the Aden continent in 1 minute.
					_ship.setInDock(GRACIA_DOCK_ID);
					_ship.oustPlayers();
					ThreadPoolManager.getInstance().scheduleGeneral(this, 60000);
					break;
				case 4:
					broadcastInGracia(1800221); // The regularly scheduled airship that flies to the Aden continent has departed.
					_ship.setInDock(0);
					_ship.executePath(GRACIA_TO_WARPGATE);
					break;
				case 5:
					//					_ship.teleToLocation(-157261, 255664, 221, 64781, false);
					_ship.setOustLoc(OUST_GLUDIO);
					ThreadPoolManager.getInstance().scheduleGeneral(this, 5000);
					break;
				case 6:
					_ship.executePath(WARPGATE_TO_GLUDIO);
					break;
				case 7:
					broadcastInGludio(1800222); // The regularly scheduled airship has arrived. It will depart for the Gracia continent in 1 minute.
					_ship.setInDock(GLUDIO_DOCK_ID);
					_ship.oustPlayers();
					ThreadPoolManager.getInstance().scheduleGeneral(this, 60000);
					break;
			}
			_cycle++;
			if (_cycle > 7)
				_cycle = 0;
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
	}
	
	private final void broadcastInGludio(int msg)
	{
		if (!_foundAtcGludio)
		{
			_foundAtcGludio = true;
			_atcGludio = findController();
		}
		if (_atcGludio != null)
			_atcGludio.broadcastPacket(new NpcSay(_atcGludio.getObjectId(), Say2.SHOUT, _atcGludio.getNpcId(), msg));
	}
	
	private final void broadcastInGracia(int msg)
	{
		if (!_foundAtcGracia)
		{
			_foundAtcGracia = true;
			_atcGracia = findController();
		}
		if (_atcGracia != null)
			_atcGracia.broadcastPacket(new NpcSay(_atcGracia.getObjectId(), Say2.SHOUT, _atcGracia.getNpcId(), msg));
	}
	
	private final L2Npc findController()
	{
		// check objects around the ship
		for (L2Object obj : L2World.getInstance().getVisibleObjects(_ship, 600))
		{
			if (obj instanceof L2Npc)
			{
				for (int id : CONTROLLERS)
				{
					if (((L2Npc)obj).getNpcId() == id)
						return (L2Npc)obj;
				}
			}
		}
		return null;
	}
	
	public static void main(String[] args)
	{
		new AirShipGludioGracia(-1, AirShipGludioGracia.class.getSimpleName(), "vehicles");
	}
}
