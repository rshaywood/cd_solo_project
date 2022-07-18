-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema foodie_faves
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema foodie_faves
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `foodie_faves` DEFAULT CHARACTER SET utf8 ;
USE `foodie_faves` ;

-- -----------------------------------------------------
-- Table `foodie_faves`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `foodie_faves`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `foodie_faves`.`restaurants`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `foodie_faves`.`restaurants` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `street_address` VARCHAR(255) NULL,
  `neighborhood` VARCHAR(255) NULL,
  `review` TEXT NULL,
  `has_food` VARCHAR(3) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `foodie_faves`.`faves`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `foodie_faves`.`faves` (
  `restaurant_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`restaurant_id`, `user_id`),
  INDEX `fk_restaurants_has_users_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_restaurants_has_users_restaurants1_idx` (`restaurant_id` ASC) VISIBLE,
  CONSTRAINT `fk_restaurants_has_users_restaurants1`
    FOREIGN KEY (`restaurant_id`)
    REFERENCES `foodie_faves`.`restaurants` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_restaurants_has_users_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `foodie_faves`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `foodie_faves`.`wishlist`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `foodie_faves`.`wishlist` (
  `restaurant_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`restaurant_id`, `user_id`),
  INDEX `fk_restaurants_has_users_users2_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_restaurants_has_users_restaurants2_idx` (`restaurant_id` ASC) VISIBLE,
  CONSTRAINT `fk_restaurants_has_users_restaurants2`
    FOREIGN KEY (`restaurant_id`)
    REFERENCES `foodie_faves`.`restaurants` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_restaurants_has_users_users2`
    FOREIGN KEY (`user_id`)
    REFERENCES `foodie_faves`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
