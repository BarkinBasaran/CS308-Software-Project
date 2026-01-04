-- MySQL dump 10.13  Distrib 8.0.42, for Linux (aarch64)
--
-- Host: localhost    Database: store_db
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `addresses`
--

DROP TABLE IF EXISTS `addresses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `addresses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `address_type` varchar(20) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `street_address` varchar(255) NOT NULL,
  `city` varchar(100) NOT NULL,
  `state` varchar(100) NOT NULL,
  `postal_code` varchar(20) NOT NULL,
  `country` varchar(100) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `addresses_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `addresses`
--

LOCK TABLES `addresses` WRITE;
/*!40000 ALTER TABLE `addresses` DISABLE KEYS */;
INSERT INTO `addresses` VALUES (3,1,'shipping','oguz baba','ankara','istanbul','trabzon','32100','Turkey','2025-04-13 19:00:10','2025-04-13 19:00:10'),(5,3,'shipping','asdasd','asd','asd','asd','asd','Turkey','2025-04-18 16:02:00','2025-04-18 16:02:00'),(6,4,'shipping','Toprak Aktepe','okul','ist','tr','36900','Turkey','2025-04-24 11:00:15','2025-04-24 11:00:15'),(7,4,'shipping','Toprak Aktepe','okul','ist','tr','sa234','Turkey','2025-04-27 17:26:04','2025-04-27 17:26:04'),(8,6,'shipping','asd','asd','asdasd','asd','23412','Turkey','2025-05-19 15:18:22','2025-05-19 15:18:22');
/*!40000 ALTER TABLE `addresses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('8b6b989077b2');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart_items`
--

DROP TABLE IF EXISTS `cart_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `session_id` varchar(255) DEFAULT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `added_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `cart_items_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `cart_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart_items`
--

LOCK TABLES `cart_items` WRITE;
/*!40000 ALTER TABLE `cart_items` DISABLE KEYS */;
INSERT INTO `cart_items` VALUES (8,2,NULL,4,1,'2025-04-13 17:59:43'),(9,2,NULL,3,1,'2025-04-13 17:59:45'),(19,1,NULL,2,1,'2025-04-18 15:55:19'),(20,3,NULL,4,1,'2025-04-18 16:01:48');
/*!40000 ALTER TABLE `cart_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'CPU','Processors','2025-04-13 17:47:51','2025-04-13 17:47:51'),(2,'GPU','Graphics Cards','2025-04-13 18:02:02','2025-04-13 18:02:02'),(3,'RAM','Memory Modules','2025-04-13 18:02:02','2025-04-13 18:02:02'),(4,'SSD','Solid State Drives','2025-04-13 18:02:02','2025-04-13 18:02:02'),(5,'Motherboard','Motherboards','2025-04-13 18:02:02','2025-04-13 18:02:02'),(8,'Demo','Demo product category','2025-05-22 04:23:05','2025-05-22 04:23:05');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `product_id` int NOT NULL,
  `comment` text NOT NULL,
  `approved` tinyint(1) DEFAULT NULL,
  `comment_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
INSERT INTO `comments` VALUES (1,4,2,'zuppaaa',1,'2025-04-25 21:03:51'),(2,4,4,'.',1,'2025-04-25 21:04:24'),(3,4,9,'yeesss',1,'2025-05-18 12:57:11'),(4,4,6,'allllessguttee',0,'2025-05-18 13:16:13');
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `credit_cards`
--

DROP TABLE IF EXISTS `credit_cards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `credit_cards` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `card_holder` varchar(100) NOT NULL,
  `card_number` varchar(16) DEFAULT NULL,
  `expiry_month` int NOT NULL,
  `expiry_year` int NOT NULL,
  `card_type` varchar(50) NOT NULL,
  `last_four` varchar(4) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `credit_cards_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `credit_cards`
--

LOCK TABLES `credit_cards` WRITE;
/*!40000 ALTER TABLE `credit_cards` DISABLE KEYS */;
INSERT INTO `credit_cards` VALUES (1,1,'oguz baba','323245456767',12,2026,'MasterCard','6767','2025-04-13 19:02:44','2025-04-13 19:02:44'),(2,3,'asdasd','asdasd',1,2024,'visa','dasd','2025-04-18 16:02:10','2025-04-18 16:02:10'),(3,3,'dggx','fhfgh',3,2024,'amex','hfgh','2025-04-18 16:04:08','2025-04-18 16:04:08'),(4,4,'toprak','123123',12,2024,'visa','3123','2025-04-24 11:02:38','2025-04-24 11:02:38'),(5,6,'asdsad','12312451',3,2024,'mastercard','2451','2025-05-19 15:18:35','2025-05-19 15:18:35');
/*!40000 ALTER TABLE `credit_cards` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deliveries`
--

DROP TABLE IF EXISTS `deliveries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deliveries` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `status` varchar(50) NOT NULL,
  `delivered_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `deliveries_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
  CONSTRAINT `deliveries_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deliveries`
--

LOCK TABLES `deliveries` WRITE;
/*!40000 ALTER TABLE `deliveries` DISABLE KEYS */;
/*!40000 ALTER TABLE `deliveries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_items`
--

DROP TABLE IF EXISTS `order_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `unit_price` decimal(10,2) NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
  CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_items`
--

LOCK TABLES `order_items` WRITE;
/*!40000 ALTER TABLE `order_items` DISABLE KEYS */;
INSERT INTO `order_items` VALUES (1,1,2,1,699.99,699.99),(2,2,6,1,999.99,999.99),(3,3,4,1,449.99,449.99),(4,4,6,1,999.99,999.99),(5,4,4,1,449.99,449.99),(6,5,1,1,599.99,599.99),(7,6,13,1,589.99,589.99),(8,7,9,1,219.99,219.99),(9,8,2,1,699.99,699.99),(10,9,4,1,449.99,449.99),(11,10,4,1,449.99,449.99),(12,11,4,1,449.99,449.99),(13,11,2,1,699.99,699.99),(14,12,4,1,449.99,449.99),(15,13,4,1,449.99,449.99),(16,14,2,1,699.99,699.99),(17,15,4,1,449.99,449.99),(18,16,2,1,699.99,699.99),(19,16,6,1,999.99,999.99),(20,17,2,1,699.99,699.99),(21,18,4,1,449.99,449.99),(22,19,4,1,449.99,449.99),(23,20,2,2,699.99,1399.98),(24,21,4,1,449.99,449.99),(25,22,4,1,449.99,449.99),(26,23,4,1,449.99,449.99),(27,24,6,1,999.99,999.99),(28,24,3,1,419.99,419.99),(29,24,1,1,599.99,599.99),(30,24,5,1,1599.99,1599.99),(31,24,12,1,699.99,699.99),(32,25,6,1,999.99,999.99),(33,26,6,1,999.99,999.99),(34,27,9,1,219.99,219.99),(35,28,9,1,219.99,219.99),(36,29,6,1,999.99,999.99),(37,30,15,1,50.00,50.00),(38,31,15,1,25.00,25.00),(39,32,15,1,25.00,25.00),(40,33,15,1,25.00,25.00),(41,34,15,1,50.00,50.00),(42,35,19,1,140.00,140.00),(43,36,20,1,150.00,150.00),(44,37,21,1,160.00,160.00),(45,38,22,1,170.00,170.00),(46,39,18,1,120.00,120.00);
/*!40000 ALTER TABLE `order_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `order_date` datetime DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `total_price` decimal(10,2) DEFAULT NULL,
  `payment_status` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `subtotal` decimal(10,2) DEFAULT NULL,
  `shipping_cost` decimal(10,2) DEFAULT NULL,
  `tax` decimal(10,2) DEFAULT NULL,
  `shipping_address` varchar(255) DEFAULT NULL,
  `payment_method` varchar(100) DEFAULT NULL,
  `delivery_address` varchar(255) DEFAULT NULL,
  `billing_address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,1,'2025-04-13 19:07:41','processing',699.99,'completed','2025-04-13 19:07:41','2025-04-13 19:07:41',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,4,'2025-04-24 11:37:51','processing',1179.99,'completed','2025-04-24 11:37:51','2025-04-24 11:37:51',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(3,4,'2025-04-24 11:38:03','processing',530.99,'completed','2025-04-24 11:38:03','2025-04-24 11:38:03',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(4,4,'2025-04-24 11:38:35','processing',1710.98,'completed','2025-04-24 11:38:35','2025-04-24 11:38:35',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(5,4,'2025-04-24 11:42:54','processing',707.99,'completed','2025-04-24 11:42:54','2025-04-24 11:42:54',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(6,4,'2025-04-24 11:43:18','processing',696.19,'completed','2025-04-24 11:43:18','2025-04-24 11:43:18',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(7,4,'2025-04-24 11:46:17','processing',259.59,'completed','2025-04-24 11:46:17','2025-04-24 11:46:17',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(8,4,'2025-04-24 11:50:58','processing',825.99,'completed','2025-04-24 11:50:58','2025-04-24 11:50:58',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(9,4,'2025-04-24 12:11:39','processing',530.99,'completed','2025-04-24 12:11:39','2025-04-24 12:11:39',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(10,4,'2025-04-24 12:19:07','processing',530.99,'completed','2025-04-24 12:19:07','2025-04-24 12:19:07',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(11,4,'2025-04-24 12:22:19','processing',1356.98,'completed','2025-04-24 12:22:19','2025-04-24 12:22:19',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(12,4,'2025-04-24 12:25:46','processing',530.99,'completed','2025-04-24 12:25:46','2025-04-24 12:25:46',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(13,4,'2025-04-24 12:41:12','processing',530.99,'completed','2025-04-24 12:41:12','2025-04-24 12:41:12',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(14,4,'2025-04-24 13:26:17','processing',825.99,'completed','2025-04-24 13:26:17','2025-04-24 13:26:17',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(15,4,'2025-04-24 14:16:44','processing',530.99,'completed','2025-04-24 14:16:44','2025-04-24 14:16:44',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(16,4,'2025-04-24 16:03:13','processing',2005.98,'completed','2025-04-24 16:03:13','2025-04-24 16:03:13',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(17,4,'2025-04-25 21:03:40','processing',825.99,'completed','2025-04-25 21:03:40','2025-04-25 21:03:40',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(18,4,'2025-04-25 21:04:20','processing',530.99,'completed','2025-04-25 21:04:20','2025-04-25 21:04:20',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(19,4,'2025-04-27 16:40:08','processing',530.99,'completed','2025-04-27 16:40:08','2025-04-27 16:40:08',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(20,4,'2025-04-27 16:42:15','processing',1651.98,'completed','2025-04-27 16:42:15','2025-04-27 16:42:15',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(21,4,'2025-04-27 16:57:22','processing',530.99,'completed','2025-04-27 16:57:22','2025-04-27 16:57:22',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(22,4,'2025-04-27 16:57:22','processing',530.99,'completed','2025-04-27 16:57:22','2025-04-27 16:57:22',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(23,4,'2025-04-27 17:06:43','processing',530.99,'completed','2025-04-27 17:06:43','2025-04-27 17:06:43',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(24,4,'2025-04-27 17:46:30','delivered',5097.54,'completed','2025-04-27 17:46:30','2025-04-27 17:46:30',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr sa234','Toprak Aktepe, okul, ist, tr sa234'),(25,4,'2025-04-27 19:15:17','delivered',1179.99,'completed','2025-04-27 19:15:17','2025-05-18 13:15:49',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(26,4,'2025-04-27 19:28:22','delivered',1179.99,'completed','2025-04-27 19:28:22','2025-05-18 13:15:47',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(27,4,'2025-05-18 12:50:23','refunded',259.59,'completed','2025-05-18 12:50:23','2025-05-19 01:02:30',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(28,4,'2025-05-18 12:50:49','refunded',259.59,'completed','2025-05-18 12:50:49','2025-05-19 01:02:24',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(29,6,'2025-05-19 15:18:39','refunded',1179.99,'completed','2025-05-19 15:18:39','2025-05-19 15:33:27',NULL,NULL,NULL,NULL,'mastercard ending in 2451','asd, asd, asdasd, asd 23412','asd, asd, asdasd, asd 23412'),(30,4,'2025-05-19 16:09:48','refunded',69.00,'completed','2025-05-19 16:09:48','2025-05-19 16:23:40',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(31,4,'2025-05-19 16:24:24','refunded',69.00,'completed','2025-05-19 16:24:24','2025-05-19 16:26:19',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(32,4,'2025-05-19 16:26:47','delivered',39.50,'completed','2025-05-19 16:26:47','2025-05-21 21:09:08',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(33,4,'2025-05-19 16:35:11','refunded',39.50,'completed','2025-05-19 16:35:11','2025-05-19 16:36:27',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(34,4,'2025-05-19 16:41:22','cancelled',69.00,'completed','2025-05-19 16:41:22','2025-05-19 16:46:01',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(35,9,'2025-04-12 04:23:05','delivered',140.00,'completed','2025-04-12 04:23:05','2025-04-17 04:23:05',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(36,9,'2025-05-07 04:23:05','delivered',150.00,'completed','2025-05-07 04:23:05','2025-05-12 04:23:05',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(37,9,'2025-05-22 04:23:05','processing',160.00,'completed','2025-05-22 04:23:05','2025-05-22 04:23:05',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(38,9,'2025-05-22 04:23:05','in_transit',170.00,'completed','2025-05-22 04:23:05','2025-05-22 04:23:05',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(39,9,'2025-05-02 04:23:05','delivered',120.00,'completed','2025-05-02 04:23:05','2025-05-03 04:23:05',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category_id` int DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `model` varchar(50) DEFAULT NULL,
  `serial_number` varchar(100) DEFAULT NULL,
  `description` text,
  `quantity_in_stock` int NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `warranty_status` varchar(50) DEFAULT NULL,
  `distributor_info` varchar(255) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `average_rating` float DEFAULT '0',
  `total_reviews` int DEFAULT '0',
  `sales_count` int DEFAULT '0',
  `discounted_price` decimal(10,2) DEFAULT NULL,
  `discount_rate` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `serial_number` (`serial_number`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,1,'Intel Core i9-13900K','13900K','INTL-13900K-001','24 cores, up to 5.8GHz',8,599.99,'2 Years','Intel Official','/static/product_images/1.jpg','2025-04-13 17:47:51','2025-04-27 17:46:30',0,0,0,NULL,NULL),(2,1,'AMD Ryzen 9 7950X','7950X','AMD-7950X-001','16 cores, up to 5.7GHz',0,699.99,'3 Years','AMD Official','/static/product_images/22.jpg','2025-04-13 17:47:51','2025-04-27 16:42:15',4,1,0,NULL,NULL),(3,1,'Intel Core i7-13700K','13700K','INTL-13700K-001','16 cores, up to 5.4GHz',14,419.99,'2 Years','Intel Official','/static/product_images/33.jpg','2025-04-13 17:47:51','2025-04-27 17:46:30',0,0,0,NULL,NULL),(4,1,'AMD Ryzen 7 7800X3D','7800X3D','AMD-7800X3D-001','8 cores, up to 5.0GHz',31,449.99,'3 Years','AMD Official','/static/product_images/44.jpg','2025-04-13 17:47:51','2025-05-18 12:39:44',3,1,0,NULL,NULL),(5,2,'NVIDIA RTX 4090','RTX4090','NV-4090-001','24GB GDDR6X, Ray Tracing',4,1599.99,'3 Years','NVIDIA Official','/static/product_images/55.jpg','2025-04-13 18:02:02','2025-04-27 17:46:30',0,0,0,NULL,NULL),(6,2,'AMD RX 7900 XTX','RX7900XTX','AMD-7900XTX-001','24GB GDDR6, RDNA 3',2,999.99,'3 Years','AMD Official','/static/product_images/66.jpg','2025-04-13 18:02:02','2025-05-19 15:33:27',5,1,3,NULL,NULL),(7,3,'Corsair Vengeance 32GB','CMK32GX5M2B6000C30','COR-32GB-001','DDR5-6000MHz CL30',20,189.99,'Lifetime','Corsair','/static/product_images/77.jpg','2025-04-13 18:02:02','2025-04-24 14:32:00',0,0,0,NULL,NULL),(8,3,'G.Skill Trident Z5 64GB','F5-7200J3445G32GX2-TZ5RK','GSK-64GB-001','DDR5-7200MHz CL34',15,389.99,'Lifetime','G.Skill','/static/product_images/88.jpg','2025-04-13 18:02:02','2025-04-24 14:32:00',0,0,0,NULL,NULL),(9,4,'Samsung 990 PRO 2TB','MZ-V9P2T0BW','SAM-990P-001','PCIe 4.0 NVMe SSD',24,219.99,'5 Years','Samsung','/static/product_images/99.jpg','2025-04-13 18:02:02','2025-05-19 01:02:30',4,1,2,NULL,NULL),(10,4,'WD Black SN850X 4TB','WDS400T2X0E','WD-850X-001','PCIe 4.0 NVMe SSD',12,429.99,'5 Years','Western Digital','/static/product_images/10.jpg','2025-04-13 18:02:02','2025-04-24 14:32:00',0,0,0,NULL,NULL),(11,5,'ASUS ROG Maximus Z790 Hero','ROG-MAX-Z790-HERO','ASU-Z790H-001','Intel Z790 Chipset',7,629.99,'3 Years','ASUS','/static/product_images/11.jpg','2025-04-13 18:02:02','2025-04-24 14:32:00',0,0,0,NULL,NULL),(12,5,'MSI MEG X670E ACE','MEG-X670E-ACE','MSI-X670E-001','AMD X670E Chipset',5,699.99,'3 Years','MSI','/static/product_images/12.jpg','2025-04-13 18:02:02','2025-04-27 17:46:30',0,0,0,NULL,NULL),(13,4,'Crucial T700 4TB','CT4000T700SSD5','CRU-T700-001','PCIe 5.0 NVMe SSD',9,589.99,'5 Years','Crucial','/static/product_images/13.jpg','2025-04-13 18:02:02','2025-04-24 14:32:00',0,0,0,NULL,NULL),(14,3,'Kingston Fury Beast 64GB','KF560C32BBK2-64','KNG-64GB-001','DDR5-6000MHz CL32',18,299.99,'Lifetime','Kingston','/static/product_images/14.jpg','2025-04-13 18:02:02','2025-04-24 14:32:00',0,0,0,NULL,NULL),(15,1,'görkem',NULL,NULL,'subaş',1,50.00,NULL,NULL,NULL,'2025-05-18 13:25:30','2025-05-19 16:46:01',0,0,5,NULL,NULL),(16,8,'Product A','ModelA','SN-A-001','Demo product A',0,100.00,'2 Years','Demo Distributor',NULL,'2025-05-22 04:23:05','2025-05-22 04:23:05',0,0,0,NULL,NULL),(17,8,'Product B','ModelB','SN-B-001','Demo product B',1,110.00,'2 Years','Demo Distributor',NULL,'2025-05-22 04:23:05','2025-05-22 04:23:05',0,0,0,NULL,NULL),(18,8,'Product C','ModelC','SN-C-001','Demo product C',3,120.00,'2 Years','Demo Distributor',NULL,'2025-05-22 04:23:05','2025-05-22 04:23:05',0,0,0,NULL,NULL),(19,8,'Product E','ModelE','SN-E-001','Demo product E',1,140.00,'2 Years','Demo Distributor',NULL,'2025-05-22 04:23:05','2025-05-22 04:23:05',0,0,0,NULL,NULL),(20,8,'Product F','ModelF','SN-F-001','Demo product F',1,150.00,'2 Years','Demo Distributor',NULL,'2025-05-22 04:23:05','2025-05-22 04:23:05',0,0,0,NULL,NULL),(21,8,'Product G','ModelG','SN-G-001','Demo product G',1,160.00,'2 Years','Demo Distributor',NULL,'2025-05-22 04:23:05','2025-05-22 04:23:05',0,0,0,NULL,NULL),(22,8,'Product H','ModelH','SN-H-001','Demo product H',1,170.00,'2 Years','Demo Distributor',NULL,'2025-05-22 04:23:05','2025-05-22 04:23:05',0,0,0,NULL,NULL);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ratings`
--

DROP TABLE IF EXISTS `ratings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ratings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `product_id` int NOT NULL,
  `rating` int NOT NULL,
  `rating_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `ratings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `ratings_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ratings`
--

LOCK TABLES `ratings` WRITE;
/*!40000 ALTER TABLE `ratings` DISABLE KEYS */;
INSERT INTO `ratings` VALUES (1,4,2,4,'2025-04-25 21:03:51'),(2,4,4,3,'2025-04-25 21:04:24'),(3,4,9,4,'2025-05-18 12:57:11'),(4,4,6,5,'2025-05-18 13:16:13');
/*!40000 ALTER TABLE `ratings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `returns`
--

DROP TABLE IF EXISTS `returns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `returns` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `user_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `reason` text NOT NULL,
  `status` enum('pending','approved','rejected','completed') DEFAULT NULL,
  `refund_amount` decimal(10,2) DEFAULT NULL,
  `refund_method` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  KEY `user_id` (`user_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `returns_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
  CONSTRAINT `returns_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `returns_ibfk_3` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `returns`
--

LOCK TABLES `returns` WRITE;
/*!40000 ALTER TABLE `returns` DISABLE KEYS */;
INSERT INTO `returns` VALUES (1,29,6,6,1,'ıdk','approved',1179.99,'credit','2025-05-19 15:28:37','2025-05-19 15:33:27'),(2,30,4,15,1,'ıdk','approved',69.00,'credit','2025-05-19 16:23:27','2025-05-19 16:23:40'),(3,31,4,15,1,'ıdk','approved',69.00,'credit','2025-05-19 16:26:05','2025-05-19 16:26:19'),(4,32,4,15,1,'ıdk','approved',39.50,'credit','2025-05-19 16:28:10','2025-05-19 16:28:20'),(5,33,4,15,1,'ıdk','approved',39.50,'credit','2025-05-19 16:36:10','2025-05-19 16:36:27');
/*!40000 ALTER TABLE `returns` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(20) NOT NULL DEFAULT 'customer',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'o','o@o.com','scrypt:32768:8:1$50qUwmXcbbDw54jd$3e109ec354c1d3935df04166d7f3ec4953080457053f03bcbf1edcd1d9da6edb10c2f04443dd467212c6391a57f0acf8a65895c028108298e99713eb20321ee9','product_manager','2025-04-13 17:44:55','2025-04-13 17:44:55'),(2,'a','a@a.com','scrypt:32768:8:1$KC45M5jvAGEYsXtu$321795a7dedee294874677880af793d09dbf83093fd9c2b42576e5c6043e35c00ab600e2349362989f1b7542f7c5745ddad738b014d7429dd682630002a040a7','customer','2025-04-13 17:51:20','2025-04-13 17:51:20'),(3,'asd','asd@asd.com','scrypt:32768:8:1$odi9LmeTqkrRhtpv$e176ddbbe5a3d9ecd5e961c2592b7c02ff3edfb6c8204cf8bdbc475d7a85aaa721667f6d9ca912d28f9c4d7be65e26ead385f4aa78423f82ab817b729bf20851','customer','2025-04-18 16:01:16','2025-04-18 16:01:16'),(4,'Toprak','taktepe07@gmail.com','scrypt:32768:8:1$jMz3uRTluSLr65fx$095e2d638c2673af0e3df361b8311b9246f306c99ff63ae3b058820bd688ef289990f2da85032318379a3c2affc342411258e2c56f9eec636b0d190e65641abb','customer','2025-04-24 10:59:32','2025-04-27 19:51:15'),(5,'toprakak','taktepe007@gmail.com','scrypt:32768:8:1$ZXc5upxORgAmxKEb$cfd1fa7e213a8154d07b18b1bf0010a1ab9835e9ffe39e5c7498bd9a6f29baba67499de1df5319b948034591308e16abcfc9fcbc2f9065581427db4ecc275814','customer','2025-05-18 12:29:43','2025-05-18 12:29:43'),(6,'1','1@hotmail.com','scrypt:32768:8:1$Ajfpl7D7XHvJMYPJ$c000db144e33f792a5597749aa58defb7662136f32c41664657427b83e1615a0e69e3a9665d5e41d4bbdca5f0cc87f2f456463f57d3654c218f1b8760c597d9c','customer','2025-05-19 15:17:53','2025-05-19 15:17:53'),(7,'pm','pm@hotmail.com','scrypt:32768:8:1$DsgYgMxaxw3Dx0Eu$1163588db3174a2d98f01793078cf7f1622b69a42581863973454637d3c06b55456f937320a996c12c663063562210822821c6a4c90441251a81a3154164266f','product_manager','2025-05-19 15:19:20','2025-05-19 15:19:20'),(8,'sm','sm@gmail.com','scrypt:32768:8:1$l4T7P7rkLSr6c3W9$100721c67671cf9e6d73cadd0cd8b24b42338e411a63916d88a4a7d6800e936c220be88ade4cd5ca3b03f2c63d47bc86c736dd816f61bee029c9f4d35f83b7a4','sales_manager','2025-05-19 15:34:56','2025-05-19 15:34:56'),(9,'oguz','oguz.temelli@sabanciuniv.edu','scrypt:32768:8:1$SB786yehBk2gIdra$0a7803f14f5a52208f15e3720c3d939fcc47befad1c9be0adfa8452a8656576a38dadbea269870331da947847f9bf9768ab359bfa53caf33fdc88871e09f2426','customer','2025-05-22 01:51:17','2025-05-22 01:51:17');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wishlists`
--

DROP TABLE IF EXISTS `wishlists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wishlists` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `product_id` int NOT NULL,
  `added_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `wishlists_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `wishlists_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wishlists`
--

LOCK TABLES `wishlists` WRITE;
/*!40000 ALTER TABLE `wishlists` DISABLE KEYS */;
INSERT INTO `wishlists` VALUES (1,1,4,'2025-04-18 15:13:41'),(18,4,15,'2025-05-19 15:36:34');
/*!40000 ALTER TABLE `wishlists` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-22  4:43:59
