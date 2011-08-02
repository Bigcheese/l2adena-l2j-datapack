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
package ai.individual;


import javolution.util.FastMap;
import javolution.util.FastSet;
import ai.group_template.L2AttackableAIScript;

import com.l2jserver.gameserver.ai.CtrlIntention;
import com.l2jserver.gameserver.datatables.NpcTable;
import com.l2jserver.gameserver.model.actor.L2Attackable;
import com.l2jserver.gameserver.model.actor.L2Character;
import com.l2jserver.gameserver.model.actor.L2Npc;
import com.l2jserver.gameserver.model.actor.instance.L2PcInstance;

public class DarkWaterDragon extends L2AttackableAIScript
{
	private static final int DRAGON = 22267;
	private static final int SHADE1 = 22268;
	private static final int SHADE2 = 22269;
	private static final int FAFURION = 18482;
	private static final int DETRACTOR1 = 22270;
	private static final int DETRACTOR2 = 22271;
	private static FastSet<Integer> secondSpawn = new FastSet<Integer>(); //Used to track if second Shades were already spawned
	private static FastSet<Integer> myTrackingSet = new FastSet<Integer>(); //Used to track instances of npcs
	private static FastMap<Integer, L2PcInstance> _idmap = new FastMap<Integer, L2PcInstance>().shared(); //Used to track instances of npcs
	
	public DarkWaterDragon(int id, String name, String descr)
	{
		super(id,name,descr);
		int[] mobs = {DRAGON, SHADE1, SHADE2, FAFURION, DETRACTOR1, DETRACTOR2};
		this.registerMobs(mobs, QuestEventType.ON_KILL, QuestEventType.ON_SPAWN, QuestEventType.ON_ATTACK);
		myTrackingSet.clear();
		secondSpawn.clear();
	}
	@Override
	public String onAdvEvent (String event, L2Npc npc, L2PcInstance player)
	{
		if (npc != null)
		{
			if (event.equalsIgnoreCase("first_spawn")) //timer to start timer "1"
			{
				this.startQuestTimer("1",40000, npc, null, true); //spawns detractor every 40 seconds
			}
			else if (event.equalsIgnoreCase("second_spawn")) //timer to start timer "2"
			{
				this.startQuestTimer("2",40000, npc, null, true); //spawns detractor every 40 seconds
			}
			else if (event.equalsIgnoreCase("third_spawn")) //timer to start timer "3"
			{
				this.startQuestTimer("3",40000, npc, null, true); //spawns detractor every 40 seconds
			}
			else if (event.equalsIgnoreCase("fourth_spawn")) //timer to start timer "4"
			{
				this.startQuestTimer("4",40000, npc, null, true); //spawns detractor every 40 seconds
			}
			else if (event.equalsIgnoreCase("1")) //spawns a detractor
			{
				this.addSpawn(DETRACTOR1,(npc.getX()+100),(npc.getY()+100),npc.getZ(),0,false,40000);
			}
			else if (event.equalsIgnoreCase("2")) //spawns a detractor
			{
				this.addSpawn(DETRACTOR2,(npc.getX()+100),(npc.getY()-100),npc.getZ(),0,false,40000);
			}
			else if (event.equalsIgnoreCase("3")) //spawns a detractor
			{
				this.addSpawn(DETRACTOR1,(npc.getX()-100),(npc.getY()+100),npc.getZ(),0,false,40000);
			}
			else if (event.equalsIgnoreCase("4")) //spawns a detractor
			{
				this.addSpawn(DETRACTOR2,(npc.getX()-100),(npc.getY()-100),npc.getZ(),0,false,40000);
			}
			else if (event.equalsIgnoreCase("fafurion_despawn"))    //Fafurion Kindred disappears and drops reward
			{
				this.cancelQuestTimer("fafurion_poison", npc, null);
				this.cancelQuestTimer("1", npc, null);
				this.cancelQuestTimer("2", npc, null);
				this.cancelQuestTimer("3", npc, null);
				this.cancelQuestTimer("4", npc, null);
				
				myTrackingSet.remove(npc.getObjectId());
				player = _idmap.remove(npc.getObjectId());
				if(player != null) //You never know ...
					((L2Attackable)npc).doItemDrop(NpcTable.getInstance().getTemplate(18485), player);
				
				npc.deleteMe();
			}
			else if (event.equalsIgnoreCase("fafurion_poison"))    //Reduces Fafurions hp like it is poisoned
			{
				if (npc.getCurrentHp() <= 500)
				{
					this.cancelQuestTimer("fafurion_despawn", npc, null);
					this.cancelQuestTimer("first_spawn", npc, null);
					this.cancelQuestTimer("second_spawn", npc, null);
					this.cancelQuestTimer("third_spawn", npc, null);
					this.cancelQuestTimer("fourth_spawn", npc, null);
					this.cancelQuestTimer("1", npc, null);
					this.cancelQuestTimer("2", npc, null);
					this.cancelQuestTimer("3", npc, null);
					this.cancelQuestTimer("4", npc, null);
					myTrackingSet.remove(npc.getObjectId());
					_idmap.remove(npc.getObjectId());
				}
				npc.reduceCurrentHp(500, npc, null); //poison kills Fafurion if he is not healed
			}
		}
		return super.onAdvEvent(event,npc,player);
	}
	
	@Override
	public String onAttack (L2Npc npc, L2PcInstance attacker, int damage, boolean isPet)
	{
		int npcId = npc.getNpcId();
		int npcObjId = npc.getObjectId();
		if (npcId == DRAGON)
		{
			if (!myTrackingSet.contains(npcObjId)) //this allows to handle multiple instances of npc
			{
				myTrackingSet.add(npcObjId);
				//Spawn first 5 shades on first attack on Dark Water Dragon
				L2Character originalAttacker = isPet? attacker.getPet(): attacker;
				spawnShade(originalAttacker, SHADE1, npc.getX() + 100, npc.getY() + 100, npc.getZ());
				spawnShade(originalAttacker, SHADE2, npc.getX() + 100, npc.getY() - 100, npc.getZ());
				spawnShade(originalAttacker, SHADE1, npc.getX() - 100, npc.getY() + 100, npc.getZ());
				spawnShade(originalAttacker, SHADE2, npc.getX() - 100, npc.getY() - 100, npc.getZ());
				spawnShade(originalAttacker, SHADE1, npc.getX() - 150, npc.getY() + 150, npc.getZ());
			}
			else if (npc.getCurrentHp() < (npc.getMaxHp() / 2.0) && !(secondSpawn.contains(npcObjId)))
			{
				secondSpawn.add(npcObjId);
				//Spawn second 5 shades on half hp of on Dark Water Dragon
				L2Character originalAttacker = isPet? attacker.getPet(): attacker;
				spawnShade(originalAttacker, SHADE2, npc.getX() + 100, npc.getY() + 100, npc.getZ());
				spawnShade(originalAttacker, SHADE1, npc.getX() + 100, npc.getY() - 100, npc.getZ());
				spawnShade(originalAttacker, SHADE2, npc.getX() - 100, npc.getY() + 100, npc.getZ());
				spawnShade(originalAttacker, SHADE1, npc.getX() - 100, npc.getY() - 100, npc.getZ());
				spawnShade(originalAttacker, SHADE2, npc.getX() - 150, npc.getY() + 150, npc.getZ());
			}
		}
		return super.onAttack(npc, attacker, damage, isPet);
	}
	
	@Override
	public String onKill (L2Npc npc, L2PcInstance killer, boolean isPet)
	{
		int npcId = npc.getNpcId();
		int npcObjId = npc.getObjectId();
		if (npcId == DRAGON)
		{
			myTrackingSet.remove(npcObjId);
			secondSpawn.remove(npcObjId);
			L2Attackable faf = (L2Attackable) this.addSpawn(FAFURION,npc.getX(),npc.getY(),npc.getZ(),0,false,0); //spawns Fafurion Kindred when Dard Water Dragon is dead
			_idmap.put(faf.getObjectId(),killer);
		}
		else if (npcId == FAFURION)
		{
			this.cancelQuestTimer("fafurion_poison", npc, null);
			this.cancelQuestTimer("fafurion_despawn", npc, null);
			this.cancelQuestTimer("first_spawn", npc, null);
			this.cancelQuestTimer("second_spawn", npc, null);
			this.cancelQuestTimer("third_spawn", npc, null);
			this.cancelQuestTimer("fourth_spawn", npc, null);
			this.cancelQuestTimer("1", npc, null);
			this.cancelQuestTimer("2", npc, null);
			this.cancelQuestTimer("3", npc, null);
			this.cancelQuestTimer("4", npc, null);
			myTrackingSet.remove(npcObjId);
			_idmap.remove(npcObjId);
		}
		return super.onKill(npc,killer,isPet);
	}
	
	@Override
	public String onSpawn (L2Npc npc)
	{
		int npcId = npc.getNpcId();
		int npcObjId = npc.getObjectId();
		if (npcId == FAFURION)
		{
			if (!myTrackingSet.contains(npcObjId))
			{
				myTrackingSet.add(npcObjId);
				//Spawn 4 Detractors on spawn of Fafurion
				int x = npc.getX();
				int y = npc.getY();
				this.addSpawn(DETRACTOR2,x+100,y+100,npc.getZ(),0,false,40000);
				this.addSpawn(DETRACTOR1,x+100,y-100,npc.getZ(),0,false,40000);
				this.addSpawn(DETRACTOR2,x-100,y+100,npc.getZ(),0,false,40000);
				this.addSpawn(DETRACTOR1,x-100,y-100,npc.getZ(),0,false,40000);
				this.startQuestTimer("first_spawn",2000, npc, null); //timer to delay timer "1"
				this.startQuestTimer("second_spawn",4000, npc, null); //timer to delay timer "2"
				this.startQuestTimer("third_spawn",8000, npc, null); //timer to delay timer "3"
				this.startQuestTimer("fourth_spawn",10000, npc, null); //timer to delay timer "4"
				this.startQuestTimer("fafurion_poison",3000, npc, null, true); //Every three seconds reduces Fafurions hp like it is poisoned
				this.startQuestTimer("fafurion_despawn",120000, npc, null); //Fafurion Kindred disappears after two minutes
			}
		}
		return super.onSpawn(npc);
	}
	
	public void spawnShade(L2Character attacker, int npcId, int x, int y, int z)
	{
		final L2Npc shade = addSpawn(npcId,x,y,z,0,false,0);
		shade.setRunning();
		((L2Attackable)shade).addDamageHate(attacker,0,999);
		shade.getAI().setIntention(CtrlIntention.AI_INTENTION_ATTACK, attacker);
	}
	
	public static void main(String[] args)
	{
		// Quest class and state definition
		new DarkWaterDragon(-1,"DarkWaterDragon","ai");
	}
}