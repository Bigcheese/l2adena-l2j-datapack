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
package quests.SagasScripts;

/**
 *
 * @author Emperorc
 */

public class SagaOfTheDoomcryer extends SagasSuperClass
{
	public static String qn1 = "78_SagaOfTheDoomcryer";
	public static int qnu = 78;
	public static String qna = "Saga of the Doomcryer";
	
	public SagaOfTheDoomcryer()
	{
		super(qnu, qn1, qna);
		NPC = new int[] { 31336, 31624, 31589, 31290, 31642, 31646, 31649, 31650, 31654, 31655, 31657, 31290 };
		Items = new int[] { 7080, 7539, 7081, 7493, 7276, 7307, 7338, 7369, 7400, 7431, 7101, 0 };
		Mob = new int[] { 27295, 27227, 27285 };
		qn = qn1;
		classid = new int[] { 116 };
		prevclass = new int[] { 0x34 };
		X = new int[] { 191046, 46087, 46066 };
		Y = new int[] { -40640, -36372, -36396 };
		Z = new int[] { -3042, -1685, -1685 };
		Text = new String[] {
				"PLAYERNAME! Pursued to here! However, I jumped out of the Banshouren boundaries! You look at the giant as the sign of power!",
				"... Oh ... good! So it was ... let's begin!",
				"I do not have the patience ..! I have been a giant force ...! Cough chatter ah ah ah!",
				"Paying homage to those who disrupt the orderly will be PLAYERNAME's death!",
				"Now, my soul freed from the shackles of the millennium, Halixia, to the back side I come ...",
				"Why do you interfere others' battles?",
				"This is a waste of time.. Say goodbye...!",
				"...That is the enemy",
				"...Goodness! PLAYERNAME you are still looking?",
				"PLAYERNAME ... Not just to whom the victory. Only personnel involved in the fighting are eligible to share in the victory.",
				"Your sword is not an ornament. Don't you think, PLAYERNAME?",
				"Goodness! I no longer sense a battle there now.",
				"let...",
				"Only engaged in the battle to bar their choice. Perhaps you should regret.",
				"The human nation was foolish to try and fight a giant's strength.",
				"Must...Retreat... Too...Strong.",
				"PLAYERNAME. Defeat...by...retaining...and...Mo...Hacker",
				"....! Fight...Defeat...It...Fight...Defeat...It..." };
		registerNPCs();
	}
}
