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
package quests.Q350_EnhanceYourWeapon;

import java.io.File;
import java.util.StringTokenizer;
import java.util.logging.Level;

import javax.xml.parsers.DocumentBuilderFactory;

import javolution.util.FastList;
import javolution.util.FastMap;

import org.w3c.dom.Document;
import org.w3c.dom.NamedNodeMap;
import org.w3c.dom.Node;

import com.l2jserver.Config;
import com.l2jserver.gameserver.model.L2ItemInstance;
import com.l2jserver.gameserver.model.L2Object;
import com.l2jserver.gameserver.model.L2Skill;
import com.l2jserver.gameserver.model.actor.L2Attackable;
import com.l2jserver.gameserver.model.actor.L2Attackable.AbsorberInfo;
import com.l2jserver.gameserver.model.actor.L2Npc;
import com.l2jserver.gameserver.model.actor.instance.L2PcInstance;
import com.l2jserver.gameserver.model.quest.Quest;
import com.l2jserver.gameserver.model.quest.QuestState;
import com.l2jserver.gameserver.model.quest.State;
import com.l2jserver.gameserver.network.SystemMessageId;
import com.l2jserver.gameserver.network.serverpackets.InventoryUpdate;
import com.l2jserver.gameserver.network.serverpackets.SystemMessage;
import com.l2jserver.util.Rnd;

public class Q350_EnhanceYourWeapon extends Quest
{
	private static final String qn = "350_EnhanceYourWeapon";
	private static final int[] STARTING_NPCS = { 30115, 30856, 30194 };
	private static final int RED_SOUL_CRYSTAL0_ID = 4629;
	private static final int GREEN_SOUL_CRYSTAL0_ID = 4640;
	private static final int BLUE_SOUL_CRYSTAL0_ID = 4651;
	
	private final FastMap<Integer, SoulCrystal> _soulCrystals = new FastMap<Integer, SoulCrystal>();
	// <npcid, <level, LevelingInfo>>
	private final FastMap<Integer, FastMap<Integer, LevelingInfo>> _npcLevelingInfos = new FastMap<Integer, FastMap<Integer, LevelingInfo>>();
	
	private static enum AbsorbCrystalType
	{
		LAST_HIT,
		FULL_PARTY,
		PARTY_ONE_RANDOM,
		PARTY_RANDOM
	}
	
	private static final class SoulCrystal
	{
		private final int _level;
		private final int _itemId;
		private final int _leveledItemId;
		
		public SoulCrystal(int level, int itemId, int leveledItemId)
		{
			_level = level;
			_itemId = itemId;
			_leveledItemId = leveledItemId;
		}
		
		public final int getLevel()
		{
			return _level;
		}
		
		public final int getItemId()
		{
			return _itemId;
		}
		
		public final int getLeveledItemId()
		{
			return _leveledItemId;
		}
	}
	
	private static final class LevelingInfo
	{
		private final AbsorbCrystalType _absorbCrystalType;
		private final boolean _isSkillNeeded;
		private final int _chance;
		
		public LevelingInfo(AbsorbCrystalType absorbCrystalType, boolean isSkillNeeded, int chance)
		{
			_absorbCrystalType = absorbCrystalType;
			_isSkillNeeded = isSkillNeeded;
			_chance = chance;
		}
		
		public final AbsorbCrystalType getAbsorbCrystalType()
		{
			return _absorbCrystalType;
		}
		
		public final boolean isSkillNeeded()
		{
			return _isSkillNeeded;
		}
		
		public final int getChance()
		{
			return _chance;
		}
	}
	
	private boolean check(QuestState st)
	{
		for (int i = 4629; i < 4665; i++)
			if (st.getQuestItemsCount(i) > 0)
				return true;
		return false;
	}
	
	private void load()
	{
		try
		{
			DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
			factory.setValidating(false);
			factory.setIgnoringComments(true);
			
			File file = new File(Config.DATAPACK_ROOT + "/data/scripts/quests/Q350_EnhanceYourWeapon/data.xml");
			if (!file.exists())
			{
				_log.severe("[EnhanceYourWeapon] Missing data.xml. The quest wont work without it!");
				return;
			}
			
			Document doc = factory.newDocumentBuilder().parse(file);
			Node first = doc.getFirstChild();
			if (first != null && "list".equalsIgnoreCase(first.getNodeName()))
			{
				for (Node n = first.getFirstChild(); n != null; n = n.getNextSibling())
				{
					if ("crystal".equalsIgnoreCase(n.getNodeName()))
					{
						for (Node d = n.getFirstChild(); d != null; d = d.getNextSibling())
						{
							if ("item".equalsIgnoreCase(d.getNodeName()))
							{
								NamedNodeMap attrs = d.getAttributes();
								Node att = attrs.getNamedItem("itemId");
								if (att == null)
								{
									_log.severe("[EnhanceYourWeapon] Missing itemId in Crystal List, skipping");
									continue;
								}
								int itemId = Integer.parseInt(attrs.getNamedItem("itemId").getNodeValue());
								
								att = attrs.getNamedItem("level");
								if (att == null)
								{
									_log.severe("[EnhanceYourWeapon] Missing level in Crystal List itemId: "+itemId+", skipping");
									continue;
								}
								int level = Integer.parseInt(attrs.getNamedItem("level").getNodeValue());
								
								att = attrs.getNamedItem("leveledItemId");
								if (att == null)
								{
									_log.severe("[EnhanceYourWeapon] Missing leveledItemId in Crystal List itemId: "+itemId+", skipping");
									continue;
								}
								int leveledItemId = Integer.parseInt(attrs.getNamedItem("leveledItemId").getNodeValue());
								
								_soulCrystals.put(itemId, new SoulCrystal(level, itemId, leveledItemId));
							}
						}
					}
					else if ("npc".equalsIgnoreCase(n.getNodeName()))
					{
						for (Node d = n.getFirstChild(); d != null; d = d.getNextSibling())
						{
							if ("item".equalsIgnoreCase(d.getNodeName()))
							{
								NamedNodeMap attrs = d.getAttributes();
								Node att = attrs.getNamedItem("npcId");
								if (att == null)
								{
									_log.severe("[EnhanceYourWeapon] Missing npcId in NPC List, skipping");
									continue;
								}
								int npcId = Integer.parseInt(att.getNodeValue());
								
								FastMap<Integer, LevelingInfo> temp = new FastMap<Integer, LevelingInfo>();
								
								for (Node cd = d.getFirstChild(); cd != null; cd = cd.getNextSibling())
								{
									boolean isSkillNeeded = false;
									int chance = 5;
									AbsorbCrystalType absorbType = AbsorbCrystalType.LAST_HIT;
									
									if ("detail".equalsIgnoreCase(cd.getNodeName()))
									{
										attrs = cd.getAttributes();
										
										att = attrs.getNamedItem("absorbType");
										if (att != null)
											absorbType = Enum.valueOf(AbsorbCrystalType.class, att.getNodeValue());
										
										att = attrs.getNamedItem("chance");
										if (att != null)
											chance = Integer.parseInt(att.getNodeValue());
										
										att = attrs.getNamedItem("skill");
										if (att != null)
											isSkillNeeded = Boolean.parseBoolean(att.getNodeValue());
										
										Node att1 = attrs.getNamedItem("maxLevel");
										Node att2 = attrs.getNamedItem("levelList");
										if (att1 == null && att2 == null)
										{
											_log.severe("[EnhanceYourWeapon] Missing maxlevel/levelList in NPC List npcId: "+npcId+", skipping");
											continue;
										}
										LevelingInfo info = new LevelingInfo(absorbType, isSkillNeeded, chance);
										if (att1 != null)
										{
											int maxLevel = Integer.parseInt(att1.getNodeValue());
											for(int i = 0; i <= maxLevel; i++)
												temp.put(i, info);
										}
										else
										{
											StringTokenizer st = new StringTokenizer(att2.getNodeValue(), ",");
											int tokenCount = st.countTokens();
											for (int i=0; i < tokenCount; i++)
											{
												Integer value = Integer.decode(st.nextToken().trim());
												if (value == null)
												{
													_log.severe("[EnhanceYourWeapon] Bad Level value!! npcId: "+npcId+ " token: "+ i);
													value = 0;
												}
												temp.put(value, info);
											}
										}
									}
								}
								
								if (temp.isEmpty())
								{
									_log.severe("[EnhanceYourWeapon] No leveling info for npcId: "+npcId+", skipping");
									continue;
								}
								_npcLevelingInfos.put(npcId, temp);
							}
						}
					}
				}
			}
		}
		catch(Exception e)
		{
			_log.log(Level.WARNING, "[EnhanceYourWeapon] Could not parse data.xml file: " + e.getMessage(), e);
		}
		_log.info("[EnhanceYourWeapon] Loaded " + _soulCrystals.size() + " Soul Crystal data.");
		_log.info("[EnhanceYourWeapon] Loaded " + _npcLevelingInfos.size() + " npc Leveling info data.");
	}
	
	public Q350_EnhanceYourWeapon(int questId, String name, String descr)
	{
		super(questId, name, descr);
		
		for(int npcId : STARTING_NPCS)
		{
			addStartNpc(npcId);
			addTalkId(npcId);
		}
		
		load();
		for(int npcId : _npcLevelingInfos.keySet())
		{
			addSkillSeeId(npcId);
			addKillId(npcId);
		}
	}
	
	@Override
	public String onSkillSee (L2Npc npc, L2PcInstance caster, L2Skill skill, L2Object[] targets, boolean isPet)
	{
		super.onSkillSee(npc, caster, skill, targets, isPet);
		
		if (skill == null || skill.getId() != 2096)
			return null;
		else if (caster == null || caster.isDead())
			return null;
		if (!(npc instanceof L2Attackable) || npc.isDead() || !_npcLevelingInfos.containsKey(npc.getNpcId()))
			return null;
		
		try
		{
			((L2Attackable)npc).addAbsorber(caster);
		}
		catch (Exception e)
		{
			_log.log(Level.SEVERE, "", e);
		}
		return null;
	}
	
	@Override
	public String onKill (L2Npc npc, L2PcInstance killer, boolean isPet)
	{
		if (npc instanceof L2Attackable && _npcLevelingInfos.containsKey(npc.getNpcId()))
			levelSoulCrystals((L2Attackable)npc, killer);
		
		return null;
	}
	
	@Override
	public String onAdvEvent (String event, L2Npc npc, L2PcInstance player)
	{
		String htmltext = event;
		QuestState st = player.getQuestState(qn);
		if (event.endsWith("-04.htm"))
		{
			st.set("cond","1");
			st.setState(State.STARTED);
			st.playSound("ItemSound.quest_accept");
		}
		else if (event.endsWith("-09.htm"))
			st.giveItems(RED_SOUL_CRYSTAL0_ID,1);
		else if (event.endsWith("-10.htm"))
			st.giveItems(GREEN_SOUL_CRYSTAL0_ID,1);
		else if (event.endsWith("-11.htm"))
			st.giveItems(BLUE_SOUL_CRYSTAL0_ID,1);
		else if (event.equalsIgnoreCase("exit.htm"))
			st.exitQuest(true);
		return htmltext;
	}
	
	@Override
	public String onTalk(L2Npc npc,L2PcInstance player)
	{
		String htmltext = getNoQuestMsg(player);
		QuestState st = player.getQuestState(qn);
		if (st == null)
			return htmltext;
		
		if (st.getState() == State.CREATED)
			st.set("cond","0");
		if (st.getInt("cond") == 0)
			htmltext = npc.getNpcId() + "-01.htm";
		else if (check(st))
			htmltext = npc.getNpcId() + "-03.htm";
		else if (st.getQuestItemsCount(RED_SOUL_CRYSTAL0_ID) == 0
				&& st.getQuestItemsCount(GREEN_SOUL_CRYSTAL0_ID) == 0
				&& st.getQuestItemsCount(BLUE_SOUL_CRYSTAL0_ID) == 0)
			htmltext = npc.getNpcId() + "-21.htm";
		return htmltext;
	}
	
	public static void main(String[] args)
	{
		new Q350_EnhanceYourWeapon(350, qn, "Enhance Your Weapon");
	}
	
	/**
	 * Calculate the leveling chance of Soul Crystals based on the attacker that killed this L2Attackable
	 *
	 * @param attacker The player that last killed this L2Attackable
	 * $ Rewrite 06.12.06 - Yesod
	 * $ Rewrite 08.01.10 - Gigiikun
	 */
	public void levelSoulCrystals(L2Attackable mob, L2PcInstance killer)
	{
		// Only L2PcInstance can absorb a soul
		if (killer == null)
		{
			mob.resetAbsorbList();
			return;
		}
		
		FastMap<L2PcInstance, SoulCrystal> players = FastMap.newInstance();
		int maxSCLevel = 0;
		
		//TODO: what if mob support last_hit + party?
		if (isPartyLevelingMonster(mob.getNpcId()) && killer.getParty() != null)
		{
			// firts get the list of players who has one Soul Cry and the quest
			for (L2PcInstance pl : killer.getParty().getPartyMembers())
			{
				if (pl == null)
					continue;
				
				SoulCrystal sc = getSCForPlayer(pl);
				if (sc == null)
					continue;
				
				players.put(pl, sc);
				if (maxSCLevel < sc.getLevel() && _npcLevelingInfos.get(mob.getNpcId()).containsKey(sc.getLevel()))
					maxSCLevel = sc.getLevel();
			}
		}
		else
		{
			SoulCrystal sc = getSCForPlayer(killer);
			if (sc != null)
			{
				players.put(killer, sc);
				if (maxSCLevel < sc.getLevel()
						&& _npcLevelingInfos.get(mob.getNpcId()).containsKey(sc.getLevel()))
					maxSCLevel = sc.getLevel();
			}
		}
		//Init some useful vars
		LevelingInfo mainlvlInfo = _npcLevelingInfos.get(mob.getNpcId()).get(maxSCLevel);
		
		if (mainlvlInfo == null)
			/*throw new NullPointerException("Target: "+mob+ " player: "+killer+" level: "+maxSCLevel);*/
			return;
		
		// If this mob is not require skill, then skip some checkings
		if (mainlvlInfo.isSkillNeeded())
		{
			// Fail if this L2Attackable isn't absorbed or there's no one in its _absorbersList
			if (!mob.isAbsorbed() /*|| _absorbersList == null*/)
			{
				mob.resetAbsorbList();
				return;
			}
			
			// Fail if the killer isn't in the _absorbersList of this L2Attackable and mob is not boss
			AbsorberInfo ai = mob.getAbsorbersList().get(killer.getObjectId());
			boolean isSuccess = true;
			if (ai == null || ai._objId != killer.getObjectId())
				isSuccess = false;
			
			// Check if the soul crystal was used when HP of this L2Attackable wasn't higher than half of it
			if (ai != null && ai._absorbedHP > (mob.getMaxHp()/2.0))
				isSuccess = false;
			
			if (!isSuccess)
			{
				mob.resetAbsorbList();
				return;
			}
		}
		
		switch (mainlvlInfo.getAbsorbCrystalType())
		{
			case PARTY_ONE_RANDOM:
				// This is a naive method for selecting a random member.	It gets any random party member and
				// then checks if the member has a valid crystal.	It does not select the random party member
				// among those who have crystals, only.	However, this might actually be correct (same as retail).
				if (killer.getParty() != null)
				{
					L2PcInstance lucky = killer.getParty().getPartyMembers().get(Rnd.get(killer.getParty().getMemberCount()));
					tryToLevelCrystal(lucky, players.get(lucky), mob);
				}
				else
					tryToLevelCrystal(killer, players.get(killer), mob);
				break;
			case PARTY_RANDOM:
				if (killer.getParty() != null)
				{
					FastList<L2PcInstance> luckyParty = FastList.newInstance();
					luckyParty.addAll(killer.getParty().getPartyMembers());
					while (Rnd.get(100) < 33 && !luckyParty.isEmpty())
					{
						L2PcInstance lucky = luckyParty.remove(Rnd.get(luckyParty.size()));
						if (players.containsKey(lucky))
							tryToLevelCrystal(lucky, players.get(lucky), mob);
					}
					FastList.recycle(luckyParty);
				}
				else if (Rnd.get(100) < 33)
					tryToLevelCrystal(killer, players.get(killer), mob);
				break;
			case FULL_PARTY:
				if (killer.getParty() != null)
					for(L2PcInstance pl : killer.getParty().getPartyMembers())
						tryToLevelCrystal(pl, players.get(pl), mob);
				else
					tryToLevelCrystal(killer, players.get(killer), mob);
				break;
			case LAST_HIT:
				tryToLevelCrystal(killer, players.get(killer), mob);
				break;
		}
		FastMap.recycle(players);
	}
	
	private boolean isPartyLevelingMonster(int npcId)
	{
		for (LevelingInfo li : _npcLevelingInfos.get(npcId).values())
		{
			if (li.getAbsorbCrystalType() != AbsorbCrystalType.LAST_HIT)
				return true;
		}
		return false;
	}
	
	private SoulCrystal getSCForPlayer(L2PcInstance player)
	{
		QuestState st = player.getQuestState(qn);
		if (st == null || st.getState() != State.STARTED)
			return null;
		
		L2ItemInstance[] inv = player.getInventory().getItems();
		SoulCrystal ret = null;
		for (L2ItemInstance item : inv)
		{
			int itemId = item.getItemId();
			if (!_soulCrystals.containsKey(itemId))
				continue;
			
			if (ret != null)
				return null;
			else
				ret = _soulCrystals.get(itemId);
		}
		return ret;
	}
	
	private void tryToLevelCrystal(L2PcInstance player, SoulCrystal sc, L2Attackable mob)
	{
		if (sc == null || !_npcLevelingInfos.containsKey(mob.getNpcId()))
			return;
		
		// If the crystal level is way too high for this mob, say that we can't increase it
		if (!_npcLevelingInfos.get(mob.getNpcId()).containsKey(sc.getLevel()))
		{
			player.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.SOUL_CRYSTAL_ABSORBING_REFUSED));
			return;
		}
		
		if (Rnd.get(100) <= _npcLevelingInfos.get(mob.getNpcId()).get(sc.getLevel()).getChance())
			exchangeCrystal(player, mob, sc.getItemId(), sc.getLeveledItemId(), false);
		else
			player.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.SOUL_CRYSTAL_ABSORBING_FAILED));
	}
	
	private void exchangeCrystal(L2PcInstance player, L2Attackable mob, int takeid, int giveid, boolean broke)
	{
		L2ItemInstance Item = player.getInventory().destroyItemByItemId("SoulCrystal", takeid, 1, player, mob);
		
		if (Item != null)
		{
			// Prepare inventory update packet
			InventoryUpdate playerIU = new InventoryUpdate();
			playerIU.addRemovedItem(Item);
			
			// Add new crystal to the killer's inventory
			Item = player.getInventory().addItem("SoulCrystal", giveid, 1, player, mob);
			playerIU.addItem(Item);
			
			// Send a sound event and text message to the player
			if (broke)
				player.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.SOUL_CRYSTAL_BROKE));
			
			else
				player.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.SOUL_CRYSTAL_ABSORBING_SUCCEEDED));
			
			// Send system message
			SystemMessage sms = SystemMessage.getSystemMessage(SystemMessageId.EARNED_ITEM_S1);
			sms.addItemName(giveid);
			player.sendPacket(sms);
			
			// Send inventory update packet
			player.sendPacket(playerIU);
		}
	}
}