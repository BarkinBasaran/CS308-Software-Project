-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: store_db
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `addresses`
--

LOCK TABLES `addresses` WRITE;
/*!40000 ALTER TABLE `addresses` DISABLE KEYS */;
INSERT INTO `addresses` VALUES (3,1,'shipping','oguz baba','ankara','istanbul','trabzon','32100','Turkey','2025-04-13 19:00:10','2025-04-13 19:00:10'),(5,3,'shipping','asdasd','asd','asd','asd','asd','Turkey','2025-04-18 16:02:00','2025-04-18 16:02:00'),(6,4,'shipping','Toprak Aktepe','okul','ist','tr','36900','Turkey','2025-04-24 11:00:15','2025-04-24 11:00:15');
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
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'CPU','Processors','2025-04-13 17:47:51','2025-04-13 17:47:51'),(2,'GPU','Graphics Cards','2025-04-13 18:02:02','2025-04-13 18:02:02'),(3,'RAM','Memory Modules','2025-04-13 18:02:02','2025-04-13 18:02:02'),(4,'SSD','Solid State Drives','2025-04-13 18:02:02','2025-04-13 18:02:02'),(5,'Motherboard','Motherboards','2025-04-13 18:02:02','2025-04-13 18:02:02');
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `credit_cards`
--

LOCK TABLES `credit_cards` WRITE;
/*!40000 ALTER TABLE `credit_cards` DISABLE KEYS */;
INSERT INTO `credit_cards` VALUES (1,1,'oguz baba','323245456767',12,2026,'MasterCard','6767','2025-04-13 19:02:44','2025-04-13 19:02:44'),(2,3,'asdasd','asdasd',1,2024,'visa','dasd','2025-04-18 16:02:10','2025-04-18 16:02:10'),(3,3,'dggx','fhfgh',3,2024,'amex','hfgh','2025-04-18 16:04:08','2025-04-18 16:04:08'),(4,4,'toprak','123123',12,2024,'visa','3123','2025-04-24 11:02:38','2025-04-24 11:02:38');
/*!40000 ALTER TABLE `credit_cards` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_items`
--

LOCK TABLES `order_items` WRITE;
/*!40000 ALTER TABLE `order_items` DISABLE KEYS */;
INSERT INTO `order_items` VALUES (1,1,2,1,699.99,699.99),(2,2,6,1,999.99,999.99),(3,3,4,1,449.99,449.99),(4,4,6,1,999.99,999.99),(5,4,4,1,449.99,449.99),(6,5,1,1,599.99,599.99),(7,6,13,1,589.99,589.99),(8,7,9,1,219.99,219.99),(9,8,2,1,699.99,699.99),(10,9,4,1,449.99,449.99),(11,10,4,1,449.99,449.99),(12,11,4,1,449.99,449.99),(13,11,2,1,699.99,699.99),(14,12,4,1,449.99,449.99),(15,13,4,1,449.99,449.99),(16,14,2,1,699.99,699.99),(17,15,4,1,449.99,449.99),(18,16,2,1,699.99,699.99),(19,16,6,1,999.99,999.99);
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
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,1,'2025-04-13 19:07:41','processing',699.99,'completed','2025-04-13 19:07:41','2025-04-13 19:07:41',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,4,'2025-04-24 11:37:51','processing',1179.99,'completed','2025-04-24 11:37:51','2025-04-24 11:37:51',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(3,4,'2025-04-24 11:38:03','processing',530.99,'completed','2025-04-24 11:38:03','2025-04-24 11:38:03',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(4,4,'2025-04-24 11:38:35','processing',1710.98,'completed','2025-04-24 11:38:35','2025-04-24 11:38:35',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(5,4,'2025-04-24 11:42:54','processing',707.99,'completed','2025-04-24 11:42:54','2025-04-24 11:42:54',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(6,4,'2025-04-24 11:43:18','processing',696.19,'completed','2025-04-24 11:43:18','2025-04-24 11:43:18',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(7,4,'2025-04-24 11:46:17','processing',259.59,'completed','2025-04-24 11:46:17','2025-04-24 11:46:17',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(8,4,'2025-04-24 11:50:58','processing',825.99,'completed','2025-04-24 11:50:58','2025-04-24 11:50:58',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(9,4,'2025-04-24 12:11:39','processing',530.99,'completed','2025-04-24 12:11:39','2025-04-24 12:11:39',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(10,4,'2025-04-24 12:19:07','processing',530.99,'completed','2025-04-24 12:19:07','2025-04-24 12:19:07',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(11,4,'2025-04-24 12:22:19','processing',1356.98,'completed','2025-04-24 12:22:19','2025-04-24 12:22:19',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(12,4,'2025-04-24 12:25:46','processing',530.99,'completed','2025-04-24 12:25:46','2025-04-24 12:25:46',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(13,4,'2025-04-24 12:41:12','processing',530.99,'completed','2025-04-24 12:41:12','2025-04-24 12:41:12',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(14,4,'2025-04-24 13:26:17','processing',825.99,'completed','2025-04-24 13:26:17','2025-04-24 13:26:17',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(15,4,'2025-04-24 14:16:44','processing',530.99,'completed','2025-04-24 14:16:44','2025-04-24 14:16:44',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900'),(16,4,'2025-04-24 16:03:13','processing',2005.98,'completed','2025-04-24 16:03:13','2025-04-24 16:03:13',NULL,NULL,NULL,NULL,'visa ending in 3123','Toprak Aktepe, okul, ist, tr 36900','Toprak Aktepe, okul, ist, tr 36900');
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `serial_number` (`serial_number`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,1,'Intel Core i9-13900K','13900K','INTL-13900K-001','24 cores, up to 5.8GHz',9,599.99,'2 Years','Intel Official','/static/product_images/1.jpg','2025-04-13 17:47:51','2025-04-24 23:23:23'),(2,1,'AMD Ryzen 9 7950X','7950X','AMD-7950X-001','16 cores, up to 5.7GHz',3,699.99,'3 Years','AMD Official','/static/product_images/22.jpg','2025-04-13 17:47:51','2025-04-24 16:03:13'),(3,1,'Intel Core i7-13700K','13700K','INTL-13700K-001','16 cores, up to 5.4GHz',15,419.99,'2 Years','Intel Official','/static/product_images/33.jpg','2025-04-13 17:47:51','2025-04-24 14:32:00'),(4,1,'AMD Ryzen 7 7800X3D','7800X3D','AMD-7800X3D-001','8 cores, up to 5.0GHz',4,449.99,'3 Years','AMD Official','/static/product_images/44.jpg','2025-04-13 17:47:51','2025-04-24 14:32:00'),(5,2,'NVIDIA RTX 4090','RTX4090','NV-4090-001','24GB GDDR6X, Ray Tracing',5,1599.99,'3 Years','NVIDIA Official','/static/product_images/55.jpg','2025-04-13 18:02:02','2025-04-24 14:32:00'),(6,2,'AMD RX 7900 XTX','RX7900XTX','AMD-7900XTX-001','24GB GDDR6, RDNA 3',5,999.99,'3 Years','AMD Official','/static/product_images/66.jpg','2025-04-13 18:02:02','2025-04-24 16:03:13'),(7,3,'Corsair Vengeance 32GB','CMK32GX5M2B6000C30','COR-32GB-001','DDR5-6000MHz CL30',20,189.99,'Lifetime','Corsair','/static/product_images/77.jpg','2025-04-13 18:02:02','2025-04-24 14:32:00'),(8,3,'G.Skill Trident Z5 64GB','F5-7200J3445G32GX2-TZ5RK','GSK-64GB-001','DDR5-7200MHz CL34',15,389.99,'Lifetime','G.Skill','/static/product_images/88.jpg','2025-04-13 18:02:02','2025-04-24 14:32:00'),(9,4,'Samsung 990 PRO 2TB','MZ-V9P2T0BW','SAM-990P-001','PCIe 4.0 NVMe SSD',24,219.99,'5 Years','Samsung','/static/product_images/99.jpg','2025-04-13 18:02:02','2025-04-24 14:32:00'),(10,4,'WD Black SN850X 4TB','WDS400T2X0E','WD-850X-001','PCIe 4.0 NVMe SSD',12,429.99,'5 Years','Western Digital','/static/product_images/10.jpg','2025-04-13 18:02:02','2025-04-24 14:32:00'),(11,5,'ASUS ROG Maximus Z790 Hero','ROG-MAX-Z790-HERO','ASU-Z790H-001','Intel Z790 Chipset',7,629.99,'3 Years','ASUS','/static/product_images/11.jpg','2025-04-13 18:02:02','2025-04-24 14:32:00'),(12,5,'MSI MEG X670E ACE','MEG-X670E-ACE','MSI-X670E-001','AMD X670E Chipset',6,699.99,'3 Years','MSI','/static/product_images/12.jpg','2025-04-13 18:02:02','2025-04-24 14:32:00'),(13,4,'Crucial T700 4TB','CT4000T700SSD5','CRU-T700-001','PCIe 5.0 NVMe SSD',9,589.99,'5 Years','Crucial','/static/product_images/13.jpg','2025-04-13 18:02:02','2025-04-24 14:32:00'),(14,3,'Kingston Fury Beast 64GB','KF560C32BBK2-64','KNG-64GB-001','DDR5-6000MHz CL32',18,299.99,'Lifetime','Kingston','/static/product_images/14.jpg','2025-04-13 18:02:02','2025-04-24 14:32:00');
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ratings`
--

LOCK TABLES `ratings` WRITE;
/*!40000 ALTER TABLE `ratings` DISABLE KEYS */;
/*!40000 ALTER TABLE `ratings` ENABLE KEYS */;
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
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'o','o@o.com','scrypt:32768:8:1$50qUwmXcbbDw54jd$3e109ec354c1d3935df04166d7f3ec4953080457053f03bcbf1edcd1d9da6edb10c2f04443dd467212c6391a57f0acf8a65895c028108298e99713eb20321ee9','2025-04-13 17:44:55','2025-04-13 17:44:55'),(2,'a','a@a.com','scrypt:32768:8:1$KC45M5jvAGEYsXtu$321795a7dedee294874677880af793d09dbf83093fd9c2b42576e5c6043e35c00ab600e2349362989f1b7542f7c5745ddad738b014d7429dd682630002a040a7','2025-04-13 17:51:20','2025-04-13 17:51:20'),(3,'asd','asd@asd.com','scrypt:32768:8:1$odi9LmeTqkrRhtpv$e176ddbbe5a3d9ecd5e961c2592b7c02ff3edfb6c8204cf8bdbc475d7a85aaa721667f6d9ca912d28f9c4d7be65e26ead385f4aa78423f82ab817b729bf20851','2025-04-18 16:01:16','2025-04-18 16:01:16'),(4,'Toprak','taktepe07@gmail.com','scrypt:32768:8:1$14uUfdd9xUKe6fFo$2b47de98f2f91ce2456e57c4775a42c66781915be2bb6a4d05c8b8ff1cb32c45504042ddaa3612b9216f7a48e9ce95d46a719aea500e60249a587cf6a217d2e0','2025-04-24 10:59:32','2025-04-24 10:59:32');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wishlists`
--

LOCK TABLES `wishlists` WRITE;
/*!40000 ALTER TABLE `wishlists` DISABLE KEYS */;
INSERT INTO `wishlists` VALUES (1,1,4,'2025-04-18 15:13:41');
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

-- Dump completed on 2025-04-25 20:43:48
