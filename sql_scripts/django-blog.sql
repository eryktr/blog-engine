CREATE DATABASE IF NOT EXISTS `django_blog`;

USE `django_blog`;

CREATE TABLE `users` (
  `user_id` INT NOT NULL PRIMARY KEY,
  `nick` VARCHAR(50) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `password` CHAR(50) NOT NULL,
  `join_date` TIMESTAMP NOT NULL
);

CREATE TABLE `posts` (
  `post_id` INT NOT NULL PRIMARY KEY,
  `title` VARCHAR(50) NOT NULL,
  `author` INT NOT NULL,
  `content` TEXT NOT NULL,
  `post_date` TIMESTAMP NOT NULL,
  `last_update` TIMESTAMP NOT NULL,

  FOREIGN KEY (`post_id`) REFERENCES `users`(`user_id`) ON DELETE CASCADE,
  UNIQUE (`title`, `author`)
);

CREATE TABLE `tags` (
  `tag_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(30) NOT NULL,
  `description` TEXT
);

CREATE TABLE `comments` (
  `comment_id` INT NOT NULL PRIMARY KEY,
  `content` TEXT NOT NULL,
  `write_date` TIMESTAMP NOT NULL
);

CREATE TABLE `permissions` (
  `permission_id` INT NOT NULL PRIMARY KEY,
  `name` VARCHAR(30) NOT NULL
);

CREATE TABLE `user_comment` (
  `user` INT NOT NULL,
  `comment` INT NOT NULL,

  FOREIGN KEY (`user`) REFERENCES `users`(`user_id`) ON DELETE CASCADE,
  FOREIGN KEY (`comment`) REFERENCES `comments`(`comment_id`) ON DELETE CASCADE
);

CREATE TABLE `post_tag` (
  `post` INT NOT NULL,
  `tag` INT NOT NULL,

  FOREIGN KEY (`post`) REFERENCES `posts`(`post_id`) ON DELETE CASCADE,
  FOREIGN KEY (`tag`) REFERENCES `tags`(`tag_id`) ON DELETE CASCADE
);

CREATE TABLE `post_comment` (
  `post` INT NOT NULL,
  `comment` INT NOT NULL,

  FOREIGN KEY (`post`) REFERENCES `posts`(`post_id`),
  FOREIGN KEY (`comment`) REFERENCES `comments`(`comment_id`) ON DELETE CASCADE
);

CREATE TABLE `user_permission` (
  `user` INT NOT NULL,
  `permission` INT NOT NULL,

  FOREIGN KEY (`user`) REFERENCES `users`(`user_id`) ON DELETE CASCADE,
  FOREIGN KEY (`permission`) REFERENCES `permissions`(`permission_id`)
);


