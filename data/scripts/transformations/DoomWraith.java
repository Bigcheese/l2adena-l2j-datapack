package transformations;

import com.l2jserver.gameserver.datatables.SkillTable;
import com.l2jserver.gameserver.instancemanager.TransformationManager;
import com.l2jserver.gameserver.model.L2Transformation;

public class DoomWraith extends L2Transformation
{
	private static final int[] SKILLS = {586,587,588,589,5491,619};
	public DoomWraith()
	{
		// id, colRadius, colHeight
		super(2, 13, 25);
	}
	
	@Override
	public void onTransform()
	{
		if (getPlayer().getTransformationId() != 2 || getPlayer().isCursedWeaponEquipped())
			return;
		
		transformedSkills();
	}
	
	public void transformedSkills()
	{
		// Rolling Attack (up to 2 levels)
		getPlayer().addSkill(SkillTable.getInstance().getInfo(586, 2), false);
		// Earth Storm (up to 2 levels)
		getPlayer().addSkill(SkillTable.getInstance().getInfo(587, 2), false);
		// Curse of Darkness (up to 2 levels)
		getPlayer().addSkill(SkillTable.getInstance().getInfo(588, 2), false);
		// Darkness Energy Drain (up to 2 levels)
		getPlayer().addSkill(SkillTable.getInstance().getInfo(589, 2), false);
		// Decrease Bow/Crossbow Attack Speed
		getPlayer().addSkill(SkillTable.getInstance().getInfo(5491, 1), false);
		// Transform Dispel
		getPlayer().addSkill(SkillTable.getInstance().getInfo(619, 1), false);
		
		getPlayer().setTransformAllowedSkills(SKILLS);
	}
	
	@Override
	public void onUntransform()
	{
		removeSkills();
	}
	
	public void removeSkills()
	{
		// Rolling Attack (up to 2 levels)
		getPlayer().removeSkill(SkillTable.getInstance().getInfo(586, 2), false);
		// Earth Storm (up to 2 levels)
		getPlayer().removeSkill(SkillTable.getInstance().getInfo(587, 2), false);
		// Curse of Darkness (up to 2 levels)
		getPlayer().removeSkill(SkillTable.getInstance().getInfo(588, 2), false);
		// Darkness Energy Drain (up to 2 levels)
		getPlayer().removeSkill(SkillTable.getInstance().getInfo(589, 2), false);
		// Decrease Bow/Crossbow Attack Speed
		getPlayer().removeSkill(SkillTable.getInstance().getInfo(5491, 1), false);
		// Transform Dispel
		getPlayer().removeSkill(SkillTable.getInstance().getInfo(619, 1), false);
		
		getPlayer().setTransformAllowedSkills(EMPTY_ARRAY);
	}
	
	public static void main(String[] args)
	{
		TransformationManager.getInstance().registerTransformation(new DoomWraith());
	}
}
