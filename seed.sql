

-- -----------------------------------------------------
-- Table `participants`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `participants` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  `age` INTEGER NULL,
  `gender` VARCHAR(45) NULL,
  `handedness` TINYINT NULL,
  `arthritis` VARCHAR(45) NULL,
  `vision` VARCHAR(45) NULL,
  `avg_weekly_computer_usage` VARCHAR(45) NULL,
  `plays_fps_pc_games` TINYINT NULL,
  `mouse_or_trackpad_user` VARCHAR(45) NULL,
  `dpi_feeling` VARCHAR(45) NULL,
  `avg_weekly_exercise` VARCHAR(45) NULL);


-- -----------------------------------------------------
-- Table `blocks`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `blocks` (
  `id` INTEGER primary key AUTOINCREMENT NOT NULL,
  `participant_id` INTEGER NOT NULL,
  `started_at` TIMESTAMP NULL,
  `finished_at` TIMESTAMP NULL,
  CONSTRAINT `fk_blocks_participants`
    FOREIGN KEY (`participant_id`)
    REFERENCES `participants` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `tasks`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tasks` (
  `id` INTEGER AUTOINCREMENT NOT NULL,
  `diameter` INTEGER NULL,
  `distance` INTEGER NULL,
  `direction` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `trials`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `trials` (
  `id` INTEGER AUTOINCREMENT NOT NULL,
  `block_id` INTEGER NOT NULL,
  `task_id` INTEGER NOT NULL,
  `started_at` TIMESTAMP NULL,
  `finished_at` TIMESTAMP NULL,
  `distance_travelled` INTEGER NULL,
  `errors` INTEGER NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_trials_blocks1`
    FOREIGN KEY (`block_id`)
    REFERENCES `blocks` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_trials_tasks1`
    FOREIGN KEY (`task_id`)
    REFERENCES `tasks` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

INSERT INTO `tasks` (`diameter`,`distance`,`direction`) VALUES ('20','100','left');
INSERT INTO `tasks` (`diameter`,`distance`,`direction`) VALUES ('40','100','left');
INSERT INTO `tasks` (`diameter`,`distance`,`direction`) VALUES ('80','100','left');
INSERT INTO `tasks` (`diameter`,`distance`,`direction`) VALUES ('20','100','right');
INSERT INTO `tasks` (`diameter`,`distance`,`direction`) VALUES ('40','100','right');
INSERT INTO `tasks` (`diameter`,`distance`,`direction`) VALUES ('80','100','right');
INSERT INTO `tasks` (`diameter`,`distance`,`direction`) VALUES ('20','300','left');
INSERT INTO `tasks` (`diameter`,`distance`,`direction`) VALUES ('40','300','left');
INSERT INTO `tasks` (`diameter`,`distance`,`direction`) VALUES ('80','300','left');
INSERT INTO `tasks` (`diameter`,`distance`,`direction`) VALUES ('20','300','right');
INSERT INTO `tasks` (`diameter`,`distance`,`direction`) VALUES ('40','300','right');
INSERT INTO `tasks` (`diameter`,`distance`,`direction`) VALUES ('80','300','right');
