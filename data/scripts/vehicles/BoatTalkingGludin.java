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
package vehicles;

import java.util.logging.Level;
import java.util.logging.Logger;

import com.l2jserver.gameserver.ThreadPoolManager;
import com.l2jserver.gameserver.instancemanager.BoatManager;
import com.l2jserver.gameserver.model.VehiclePathPoint;
import com.l2jserver.gameserver.model.actor.instance.L2BoatInstance;
import com.l2jserver.gameserver.network.clientpackets.Say2;
import com.l2jserver.gameserver.network.serverpackets.CreatureSay;
import com.l2jserver.gameserver.network.serverpackets.PlaySound;

/**
 * 
 * @author DS
 *
 */
public class BoatTalkingGludin implements Runnable
{
	private static final Logger _log = Logger.getLogger(BoatTalkingGludin.class.getName());
	
	// Time: 919s
	private static final VehiclePathPoint[] TALKING_TO_GLUDIN =
	{
		new VehiclePathPoint(-121385, 261660, -3610, 180, 800),
		new VehiclePathPoint(-127694, 253312, -3610, 200, 800),
		new VehiclePathPoint(-129274, 237060, -3610, 250, 800),
		new VehiclePathPoint(-114688, 139040, -3610, 200, 800),
		new VehiclePathPoint(-109663, 135704, -3610, 180, 800),
		new VehiclePathPoint(-102151, 135704, -3610, 180, 800),
		new VehiclePathPoint(-96686, 140595, -3610, 180, 800),
		new VehiclePathPoint(-95686, 147718, -3610, 180, 800),
		new VehiclePathPoint(-95686, 148718, -3610, 180, 800),
		new VehiclePathPoint(-95686, 149718, -3610, 150, 800)
	};
	
	private static final VehiclePathPoint[] GLUDIN_DOCK =
	{
		new VehiclePathPoint(-95686, 150514, -3610, 150, 800)
	};
	
	// Time: 780s
	private static final VehiclePathPoint[] GLUDIN_TO_TALKING =
	{
		new VehiclePathPoint(-95686, 155514, -3610, 180, 800),
		new VehiclePathPoint(-95686, 185514, -3610, 250, 800),
		new VehiclePathPoint(-60136, 238816, -3610, 200, 800),
		new VehiclePathPoint(-60520, 259609, -3610, 180, 1800),
		new VehiclePathPoint(-65344, 261460, -3610, 180, 1800),
		new VehiclePathPoint(-83344, 261560, -3610, 180, 1800),
		new VehiclePathPoint(-88344, 261660, -3610, 180, 1800),
		new VehiclePathPoint(-92344, 261660, -3610, 150, 1800),
		new VehiclePathPoint(-94242, 261659, -3610, 150, 1800)
	};
	
	private static final VehiclePathPoint[] TALKING_DOCK =
	{
		new VehiclePathPoint(-96622, 261660, -3610, 150, 1800)
	};
	
	private final L2BoatInstance _boat;
	private int _cycle = 0;
	private int _shoutCount = 0;
	
	private final CreatureSay ARRIVED_AT_TALKING;
	private final CreatureSay ARRIVED_AT_TALKING_2;
	private final CreatureSay LEAVE_TALKING5;
	private final CreatureSay LEAVE_TALKING1;
	private final CreatureSay LEAVE_TALKING1_2;
	private final CreatureSay LEAVE_TALKING0;
	private final CreatureSay LEAVING_TALKING;
	private final CreatureSay ARRIVED_AT_GLUDIN;
	private final CreatureSay ARRIVED_AT_GLUDIN_2;
	private final CreatureSay LEAVE_GLUDIN5;
	private final CreatureSay LEAVE_GLUDIN1;
	private final CreatureSay LEAVE_GLUDIN0;
	private final CreatureSay LEAVING_GLUDIN;
	private final CreatureSay BUSY_TALKING;
	private final CreatureSay BUSY_GLUDIN;
	
	private final CreatureSay ARRIVAL_GLUDIN10;
	private final CreatureSay ARRIVAL_GLUDIN5;
	private final CreatureSay ARRIVAL_GLUDIN1;
	private final CreatureSay ARRIVAL_TALKING10;
	private final CreatureSay ARRIVAL_TALKING5;
	private final CreatureSay ARRIVAL_TALKING1;
	
	private final PlaySound TALKING_SOUND;
	private final PlaySound GLUDIN_SOUND;
	
	public BoatTalkingGludin(L2BoatInstance boat)
	{
		_boat = boat;
		_cycle = 0;
		
		ARRIVED_AT_TALKING = new CreatureSay(0, Say2.BOAT, 801, 979);
		ARRIVED_AT_TALKING_2 = new CreatureSay(0, Say2.BOAT, 801, 980);
		LEAVE_TALKING5 = new CreatureSay(0, Say2.BOAT, 801, 981);
		LEAVE_TALKING1 = new CreatureSay(0, Say2.BOAT, 801, 982);
		LEAVE_TALKING1_2 = new CreatureSay(0, Say2.BOAT, 801, 983);
		LEAVE_TALKING0 = new CreatureSay(0, Say2.BOAT, 801, 984);
		LEAVING_TALKING = new CreatureSay(0, Say2.BOAT, 801, 985);
		ARRIVED_AT_GLUDIN = new CreatureSay(0, Say2.BOAT, 801, 986);
		ARRIVED_AT_GLUDIN_2 = new CreatureSay(0, Say2.BOAT, 801, 987);
		LEAVE_GLUDIN5 = new CreatureSay(0, Say2.BOAT, 801, 988);
		LEAVE_GLUDIN1 = new CreatureSay(0, Say2.BOAT, 801, 989);
		LEAVE_GLUDIN0 = new CreatureSay(0, Say2.BOAT, 801, 990);
		LEAVING_GLUDIN = new CreatureSay(0, Say2.BOAT, 801, 991);
		BUSY_TALKING = new CreatureSay(0, Say2.BOAT, 801, 1486);
		BUSY_GLUDIN = new CreatureSay(0, Say2.BOAT, 801, 1485);
		
		ARRIVAL_GLUDIN10 = new CreatureSay(0, Say2.BOAT, 801, 1159);
		ARRIVAL_GLUDIN5 = new CreatureSay(0, Say2.BOAT, 801, 1160);
		ARRIVAL_GLUDIN1 = new CreatureSay(0, Say2.BOAT, 801, 1161);
		ARRIVAL_TALKING10 = new CreatureSay(0, Say2.BOAT, 801, 1191);
		ARRIVAL_TALKING5 = new CreatureSay(0, Say2.BOAT, 801, 1192);
		ARRIVAL_TALKING1 = new CreatureSay(0, Say2.BOAT, 801, 1193);
		
		TALKING_SOUND = new PlaySound(0, "itemsound.ship_arrival_departure", 1, _boat.getObjectId(), TALKING_DOCK[0].x, TALKING_DOCK[0].y, TALKING_DOCK[0].z);
		GLUDIN_SOUND = new PlaySound(0, "itemsound.ship_arrival_departure", 1, _boat.getObjectId(), GLUDIN_DOCK[0].x, GLUDIN_DOCK[0].y, GLUDIN_DOCK[0].z);
	}
	
	public void run()
	{
		try
		{
			switch (_cycle)
			{
				case 0:
					BoatManager.getInstance().broadcastPacket(TALKING_DOCK[0], GLUDIN_DOCK[0], LEAVE_TALKING5);
					ThreadPoolManager.getInstance().scheduleGeneral(this, 240000);
					break;
				case 1:
					BoatManager.getInstance().broadcastPackets(TALKING_DOCK[0], GLUDIN_DOCK[0], LEAVE_TALKING1, LEAVE_TALKING1_2);
					ThreadPoolManager.getInstance().scheduleGeneral(this, 40000);
					break;
				case 2:
					BoatManager.getInstance().broadcastPacket(TALKING_DOCK[0], GLUDIN_DOCK[0], LEAVE_TALKING0);
					ThreadPoolManager.getInstance().scheduleGeneral(this, 20000);
					break;
				case 3:
					BoatManager.getInstance().dockShip(BoatManager.TALKING_ISLAND, false);
					BoatManager.getInstance().broadcastPackets(TALKING_DOCK[0], GLUDIN_DOCK[0], LEAVING_TALKING);
					_boat.broadcastPacket(TALKING_SOUND);
					_boat.payForRide(1074, 1, -96777, 258970, -3623);
					_boat.executePath(TALKING_TO_GLUDIN);
					ThreadPoolManager.getInstance().scheduleGeneral(this, 300000);
					break;
				case 4:
					BoatManager.getInstance().broadcastPacket(GLUDIN_DOCK[0], TALKING_DOCK[0], ARRIVAL_GLUDIN10);
					ThreadPoolManager.getInstance().scheduleGeneral(this, 300000);
					break;
				case 5:
					BoatManager.getInstance().broadcastPacket(GLUDIN_DOCK[0], TALKING_DOCK[0], ARRIVAL_GLUDIN5);
					ThreadPoolManager.getInstance().scheduleGeneral(this, 240000);
					break;
				case 6:
					BoatManager.getInstance().broadcastPacket(GLUDIN_DOCK[0], TALKING_DOCK[0], ARRIVAL_GLUDIN1);
					break;
				case 7:
					if (BoatManager.getInstance().dockBusy(BoatManager.GLUDIN_HARBOR))
					{
						if (_shoutCount == 0)
							BoatManager.getInstance().broadcastPacket(GLUDIN_DOCK[0], TALKING_DOCK[0], BUSY_GLUDIN);
						
						_shoutCount++;
						if (_shoutCount > 35)
							_shoutCount = 0;
						
						ThreadPoolManager.getInstance().scheduleGeneral(this, 5000);
						return;
					}
					_boat.executePath(GLUDIN_DOCK);
					break;
				case 8:
					BoatManager.getInstance().dockShip(BoatManager.GLUDIN_HARBOR, true);
					BoatManager.getInstance().broadcastPackets(GLUDIN_DOCK[0], TALKING_DOCK[0], ARRIVED_AT_GLUDIN, ARRIVED_AT_GLUDIN_2);
					_boat.broadcastPacket(GLUDIN_SOUND);
					ThreadPoolManager.getInstance().scheduleGeneral(this, 300000);
					break;
				case 9:
					BoatManager.getInstance().broadcastPacket(TALKING_DOCK[0], GLUDIN_DOCK[0], LEAVE_GLUDIN5);
					ThreadPoolManager.getInstance().scheduleGeneral(this, 240000);
					break;
				case 10:
					BoatManager.getInstance().broadcastPackets(TALKING_DOCK[0], GLUDIN_DOCK[0], LEAVE_GLUDIN1, LEAVE_TALKING1_2);
					ThreadPoolManager.getInstance().scheduleGeneral(this, 40000);
					break;
				case 11:
					BoatManager.getInstance().broadcastPacket(TALKING_DOCK[0], GLUDIN_DOCK[0], LEAVE_GLUDIN0);
					ThreadPoolManager.getInstance().scheduleGeneral(this, 20000);
					break;
				case 12:
					BoatManager.getInstance().dockShip(BoatManager.GLUDIN_HARBOR, false);
					BoatManager.getInstance().broadcastPackets(TALKING_DOCK[0], GLUDIN_DOCK[0], LEAVING_GLUDIN);
					_boat.broadcastPacket(GLUDIN_SOUND);
					_boat.payForRide(1075, 1, -90015, 150422, -3610);
					_boat.executePath(GLUDIN_TO_TALKING);
					ThreadPoolManager.getInstance().scheduleGeneral(this, 150000);
					break;
				case 13:
					BoatManager.getInstance().broadcastPacket(TALKING_DOCK[0], GLUDIN_DOCK[0], ARRIVAL_TALKING10);
					ThreadPoolManager.getInstance().scheduleGeneral(this, 300000);
					break;
				case 14:
					BoatManager.getInstance().broadcastPacket(TALKING_DOCK[0], GLUDIN_DOCK[0], ARRIVAL_TALKING5);
					ThreadPoolManager.getInstance().scheduleGeneral(this, 240000);
					break;
				case 15:
					BoatManager.getInstance().broadcastPacket(TALKING_DOCK[0], GLUDIN_DOCK[0], ARRIVAL_TALKING1);
					break;
				case 16:
					if (BoatManager.getInstance().dockBusy(BoatManager.TALKING_ISLAND))
					{
						if (_shoutCount == 0)
							BoatManager.getInstance().broadcastPacket(TALKING_DOCK[0], GLUDIN_DOCK[0], BUSY_TALKING);
						
						_shoutCount++;
						if (_shoutCount > 35)
							_shoutCount = 0;
						
						ThreadPoolManager.getInstance().scheduleGeneral(this, 5000);
						return;
					}
					_boat.executePath(TALKING_DOCK);
					break;
				case 17:
					BoatManager.getInstance().dockShip(BoatManager.TALKING_ISLAND, true);
					BoatManager.getInstance().broadcastPackets(TALKING_DOCK[0], GLUDIN_DOCK[0], ARRIVED_AT_TALKING, ARRIVED_AT_TALKING_2);
					_boat.broadcastPacket(TALKING_SOUND);
					ThreadPoolManager.getInstance().scheduleGeneral(this, 300000);
					break;
			}
			_shoutCount = 0;
			_cycle++;
			if (_cycle > 17)
				_cycle = 0;
		}
		catch (Exception e)
		{
			_log.log(Level.WARNING, e.getMessage());
		}
	}
	
	public static void main(String[] args)
	{
		final L2BoatInstance boat = BoatManager.getInstance().getNewBoat(1, -96622, 261660, -3610, 32768);
		if (boat != null)
		{
			boat.registerEngine(new BoatTalkingGludin(boat));
			boat.runEngine(180000);
			BoatManager.getInstance().dockShip(BoatManager.TALKING_ISLAND, true);
		}
	}
}
