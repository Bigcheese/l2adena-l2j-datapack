package transformations;

import com.l2jserver.gameserver.datatables.SkillTable;
import com.l2jserver.gameserver.instancemanager.TransformationManager;
import com.l2jserver.gameserver.model.L2Transformation;

public class Kiyachi extends L2Transformation
{
	private static final int[] SKILLS = {733,734,5491,619};
	public Kiyachi()
	{
		// id, colRadius, colHeight
		super(310, 12, 29);
	}
	
	@Override
	public void onTransform()
	{
		if (getPlayer().getTransformationId() != 310 || getPlayer().isCursedWeaponEquipped())
			return;
		
		transformedSkills();
	}
	
	public void transformedSkills()
	{
		// Kechi Double Cutter
		getPlayer().addSkill(SkillTable.getInstance().getInfo(733, 1), false);
		// Kechi Air Blade
		getPlayer().addSkill(SkillTable.getInstance().getInfo(734, 1), false);
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
		// Kechi Double Cutter
		getPlayer().removeSkill(SkillTable.getInstance().getInfo(733, 1), false);
		// Kechi Air Blade
		getPlayer().removeSkill(SkillTable.getInstance().getInfo(734, 1), false);
		// Decrease Bow/Crossbow Attack Speed
		getPlayer().removeSkill(SkillTable.getInstance().getInfo(5491, 1), false);
		// Transform Dispel
		getPlayer().removeSkill(SkillTable.getInstance().getInfo(619, 1), false);
		
		getPlayer().setTransformAllowedSkills(EMPTY_ARRAY);
	}
	
	public static void main(String[] args)
	{
		TransformationManager.getInstance().registerTransformation(new Kiyachi());
	}
}
