CREATE TABLE IF NOT EXISTS `character_summon_skills_save` (
  `ownerId` INT NOT NULL default 0,
  `ownerClassIndex` INT(1) NOT NULL DEFAULT 0,
  `summonSkillId` INT NOT NULL default 0,
  `skill_id` INT NOT NULL default 0,
  `skill_level` INT(3) NOT NULL default 1,
  `effect_count` INT NOT NULL default 0,
  `effect_cur_time` INT NOT NULL default 0,
  `buff_index` INT(2) NOT NULL default 0,
  PRIMARY KEY (`ownerId`,`ownerClassIndex`,`summonSkillId`,`skill_id`,`skill_level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;