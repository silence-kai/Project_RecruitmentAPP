-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: recruitment
-- ------------------------------------------------------
-- Server version	8.0.19

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
-- Table structure for table `applicant`
--

DROP TABLE IF EXISTS `applicant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `applicant` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  `account` varchar(30) DEFAULT NULL,
  `wanted_position` varchar(30) DEFAULT NULL,
  `wanted_salary` decimal(8,2) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL,
  `resume_path` varchar(32) DEFAULT NULL,
  `login_time` datetime DEFAULT NULL,
  `logout_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `applicant`
--

LOCK TABLES `applicant` WRITE;
/*!40000 ALTER TABLE `applicant` DISABLE KEYS */;
INSERT INTO `applicant` VALUES (1,'张晓','111@163.com','测试',5000.00,'1234561',NULL,'2020-01-18 23:06:19','2020-01-18 23:06:19'),(2,'刘强','222@163.com','程序员',6000.00,'234567',NULL,'2020-01-18 23:06:19','2020-01-18 23:06:19'),(3,'付超','333@qq.com','测试',5000.00,'345678',NULL,'2020-01-18 23:06:19','2020-01-18 23:06:19'),(4,'尹婷','444@qq.com','架构师',5000.00,'456789',NULL,'2020-01-18 23:06:19','2020-01-18 23:06:19'),(5,'何丽','555@qq.com','秘书',5000.00,'567891',NULL,'2020-01-18 23:06:19','2020-01-18 23:06:19'),(6,'严蓉','666@qq.com','测试',5000.00,'678911',NULL,'2020-01-18 23:06:19','2020-01-18 23:06:19'),(7,'王俊文','777@163.com','程序员',5000.00,'789112',NULL,'2020-01-18 23:06:19','2020-01-18 23:06:19'),(23,'zhangkai','911077046@qq.com','开发工程师',15000.00,'QWEasd123','../FTP_store/911077046@qq.com',NULL,NULL);
/*!40000 ALTER TABLE `applicant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat`
--

DROP TABLE IF EXISTS `chat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat` (
  `id` int NOT NULL AUTO_INCREMENT,
  `position_id` int DEFAULT NULL,
  `applicant_id` int DEFAULT NULL,
  `hr_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat`
--

LOCK TABLES `chat` WRITE;
/*!40000 ALTER TABLE `chat` DISABLE KEYS */;
/*!40000 ALTER TABLE `chat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_record`
--

DROP TABLE IF EXISTS `chat_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_record` (
  `id` int NOT NULL AUTO_INCREMENT,
  `content` text COMMENT '消息内容',
  `isofflinemsg` tinyint(1) DEFAULT NULL COMMENT '是否为离线消息 0:离线 1:在线',
  `from_account` varchar(20) DEFAULT NULL COMMENT '消息发送者',
  `to_account` varchar(20) DEFAULT NULL COMMENT '消息接收者',
  `send_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '消息接收者',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=141 DEFAULT CHARSET=utf8 COMMENT='聊天记录';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_record`
--

LOCK TABLES `chat_record` WRITE;
/*!40000 ALTER TABLE `chat_record` DISABLE KEYS */;
INSERT INTO `chat_record` VALUES (135,'你好啊',0,'911077046@qq.com','123@qq.com','2020-02-21 19:31:04'),(136,'我爱你',0,'911077046@qq.com','123@qq.com','2020-02-21 19:32:04'),(137,'我爱你',0,'123@qq.com','911077046@qq.com','2020-02-21 19:34:04'),(138,'你吃了吗',0,'123@qq.com','911077046@qq.com','2020-02-21 19:35:04'),(139,'how are you',0,'123@qq.com','911077046@qq.com','2020-02-21 19:35:04'),(140,'hello world',0,'123@qq.com','911077046@qq.com','2020-02-21 19:40:04');
/*!40000 ALTER TABLE `chat_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enterprise`
--

DROP TABLE IF EXISTS `enterprise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `enterprise` (
  `id` int NOT NULL AUTO_INCREMENT,
  `enterprise_name` varchar(128) DEFAULT NULL,
  `address` varchar(256) DEFAULT NULL,
  `introduction` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enterprise`
--

LOCK TABLES `enterprise` WRITE;
/*!40000 ALTER TABLE `enterprise` DISABLE KEYS */;
INSERT INTO `enterprise` VALUES (1,'阿里巴巴（中国）有限公司','杭州余杭区阿里巴巴西溪园区','牛逼的公司'),(2,'腾讯科技（深圳）有限公司','深圳南山区腾讯大厦','牛逼的公司'),(3,'百度在线网络技术（北京）有限公司','北京海淀区百度科技园','牛逼的公司'),(4,'北京滴滴无限科技发展有限公司','北京市海淀区未名视通研发楼','牛逼的公司'),(5,'华为技术有限公司','杭州滨江区华为科技有限公司杭州研究所','牛逼的公司'),(6,'北京小米移动软件有限公司','北京海淀区小米移动互联网产业园','牛逼的公司');
/*!40000 ALTER TABLE `enterprise` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hr`
--

DROP TABLE IF EXISTS `hr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hr` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  `enterprise_id` int DEFAULT NULL,
  `hr_password` varchar(20) DEFAULT NULL,
  `hr_account` varchar(30) DEFAULT NULL,
  `login_time` datetime DEFAULT NULL,
  `logout_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hr`
--

LOCK TABLES `hr` WRITE;
/*!40000 ALTER TABLE `hr` DISABLE KEYS */;
INSERT INTO `hr` VALUES (1,'张三',1,'123456','123@qq.com','2020-01-18 17:04:42','2020-01-18 17:04:42'),(2,'李四',2,'234567','456@qq.com','2020-01-18 17:04:42','2020-01-18 17:04:42'),(3,'王五',3,'345678','789@qq.com','2020-01-18 17:04:42','2020-01-18 17:04:42'),(4,'孙六',4,'456789','asv@qq.com','2020-01-18 17:04:42','2020-01-18 17:04:42'),(5,'赵七',5,'567891','rfv@qq.com','2020-01-18 17:04:42','2020-01-18 17:04:42'),(6,'吴八',6,'678911','fds@qq.com','2020-01-18 17:04:42','2020-01-18 17:04:42'),(7,'Lily',1,'123456','478@qq.com','2020-01-18 17:04:42','2020-01-18 17:04:42'),(8,'Martin',1,'123456','asdqew@qq.com','2020-01-18 17:04:42','2020-01-18 17:04:42'),(9,'Gaga',2,'123456','123543@qq.com','2020-01-18 17:04:42','2020-01-18 17:04:42'),(10,'Tom',2,'123456','545rfdrg@qq.com','2020-01-18 17:04:42','2020-01-18 17:04:42'),(11,'Lucy',3,'123456','zxcrt345@qq.com','2020-01-18 17:04:42','2020-01-18 17:04:42'),(12,'Julia',3,'123456','12315df8@qq.com','2020-01-18 17:04:42','2020-01-18 17:04:42'),(13,'Nancy',4,'123456','6687fg@qq.com','2020-01-18 17:04:42','2020-01-18 17:04:42'),(14,'Daisy',5,'123456','zxchgty1@qq.com','2020-01-18 17:04:42','2020-01-18 17:04:42'),(15,'Bob',6,'123456','qweasdzz@qq.com','2020-01-18 17:04:42','2020-01-18 17:04:42');
/*!40000 ALTER TABLE `hr` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `position`
--

DROP TABLE IF EXISTS `position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `position` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  `month_pay` decimal(8,2) DEFAULT NULL,
  `content` text,
  `hr_id` int DEFAULT NULL,
  `enterprise_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `position`
--

LOCK TABLES `position` WRITE;
/*!40000 ALTER TABLE `position` DISABLE KEYS */;
INSERT INTO `position` VALUES (1,'程序员',12000.00,'好好工作,天天向上',1,1),(2,'架构师',20000.00,'好好工作,天天向上',11,3),(3,'秘书',8000.00,'好好工作,天天向上',11,3),(4,'测试员',6000.00,'好好工作,天天向上',1,1),(5,'开发工程师',9000.00,'无忧无虑',7,1),(6,'开发工程师',13000.00,'吃喝玩乐',10,2),(7,'开发工程师',13000.00,'吃喝玩乐',10,2),(8,'测试工程师',15000.00,'你来我往',11,3),(9,'秘书',10000.00,'玩命干',12,3),(10,'架构师',11000.00,'拼命加班',13,4),(11,'开发工程师',14000.00,'你死我活',15,6),(12,'测试工程师',8000.00,'打王者荣耀',2,2),(13,'开发工程师',9000.00,'看月亮',3,3),(14,'开发工程师',20000.00,'看星星',4,4),(15,'秘书',6000.00,'喝咖啡',5,5),(16,'测试工程师',7000.00,'打豆豆',1,1),(17,'开发工程师',10000.00,'砸键盘',2,2),(18,'开发工程师',12000.00,'吃鼠标',3,3),(22,'保安',5000.00,'打架',10,2);
/*!40000 ALTER TABLE `position` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-02-23  9:45:29
