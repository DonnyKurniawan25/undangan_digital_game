-- MySQL dump 10.13  Distrib 8.0.46, for Linux (x86_64)
--
-- Host: localhost    Database: jelajah_db
-- ------------------------------------------------------
-- Server version	8.0.46-0ubuntu0.24.04.4

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add Acara',7,'add_acara'),(26,'Can change Acara',7,'change_acara'),(27,'Can delete Acara',7,'delete_acara'),(28,'Can view Acara',7,'view_acara'),(29,'Can add Foto Galeri',8,'add_fotogaleri'),(30,'Can change Foto Galeri',8,'change_fotogaleri'),(31,'Can delete Foto Galeri',8,'delete_fotogaleri'),(32,'Can view Foto Galeri',8,'view_fotogaleri'),(33,'Can add Mempelai',9,'add_pengantin'),(34,'Can change Mempelai',9,'change_pengantin'),(35,'Can delete Mempelai',9,'delete_pengantin'),(36,'Can view Mempelai',9,'view_pengantin'),(37,'Can add Pengaturan',10,'add_pengaturan'),(38,'Can change Pengaturan',10,'change_pengaturan'),(39,'Can delete Pengaturan',10,'delete_pengaturan'),(40,'Can view Pengaturan',10,'view_pengaturan'),(41,'Can add Rekening Hadiah',11,'add_rekening'),(42,'Can change Rekening Hadiah',11,'change_rekening'),(43,'Can delete Rekening Hadiah',11,'delete_rekening'),(44,'Can view Rekening Hadiah',11,'view_rekening'),(45,'Can add Tamu',12,'add_tamu'),(46,'Can change Tamu',12,'change_tamu'),(47,'Can delete Tamu',12,'delete_tamu'),(48,'Can view Tamu',12,'view_tamu'),(49,'Can add Ucapan & RSVP',13,'add_ucapan'),(50,'Can change Ucapan & RSVP',13,'change_ucapan'),(51,'Can delete Ucapan & RSVP',13,'delete_ucapan'),(52,'Can view Ucapan & RSVP',13,'view_ucapan'),(53,'Can add Undangan',14,'add_undangan'),(54,'Can change Undangan',14,'change_undangan'),(55,'Can delete Undangan',14,'delete_undangan'),(56,'Can view Undangan',14,'view_undangan'),(57,'Can add Pembayaran',15,'add_pembayaran'),(58,'Can change Pembayaran',15,'change_pembayaran'),(59,'Can delete Pembayaran',15,'delete_pembayaran'),(60,'Can view Pembayaran',15,'view_pembayaran'),(61,'Can add Konfigurasi AI',16,'add_konfigurasiai'),(62,'Can change Konfigurasi AI',16,'change_konfigurasiai'),(63,'Can delete Konfigurasi AI',16,'delete_konfigurasiai'),(64,'Can view Konfigurasi AI',16,'view_konfigurasiai'),(65,'Can add Riwayat AI',17,'add_riwayatai'),(66,'Can change Riwayat AI',17,'change_riwayatai'),(67,'Can delete Riwayat AI',17,'delete_riwayatai'),(68,'Can view Riwayat AI',17,'view_riwayatai');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1000000$Lfd4fUKamoG95cifCvtGWk$imgLFOvHO4lr/bpoqTrYgSId6vDr1UMAwdpBzDwbVYY=',NULL,1,'admin','','','',1,1,'2026-10-07 15:46:51.483234'),(2,'pbkdf2_sha256$1000000$xElPxxCLbvvFTLpYV7ho6x$x/nOYfuA/2pgktmNiPL+rYVo2AgsIgXYDuVXpJoKxq4=','2026-10-07 17:03:53.350700',0,'bambang','bambang','','bambang@gmail.com',0,1,'2026-10-07 17:03:52.442068'),(3,'pbkdf2_sha256$1000000$7pZLERpQCNA9EybG67kbEX$rITj5Sbj2wGB718AKJ64BN7k5n4XZOqu/ogEDSYvbGs=','2026-10-08 10:17:28.462919',0,'lilik1997','Lilik Nurhayati, S.Kom','','liliknurhayati1997@gmail.com',0,1,'2026-10-08 10:17:27.548821');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session'),(7,'undangan','acara'),(8,'undangan','fotogaleri'),(16,'undangan','konfigurasiai'),(15,'undangan','pembayaran'),(9,'undangan','pengantin'),(10,'undangan','pengaturan'),(11,'undangan','rekening'),(17,'undangan','riwayatai'),(12,'undangan','tamu'),(13,'undangan','ucapan'),(14,'undangan','undangan');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-10-07 15:46:15.226330'),(2,'auth','0001_initial','2026-10-07 15:46:17.769970'),(3,'admin','0001_initial','2026-10-07 15:46:18.523309'),(4,'admin','0002_logentry_remove_auto_add','2026-10-07 15:46:18.547057'),(5,'admin','0003_logentry_add_action_flag_choices','2026-10-07 15:46:18.577840'),(6,'contenttypes','0002_remove_content_type_name','2026-10-07 15:46:19.138963'),(7,'auth','0002_alter_permission_name_max_length','2026-10-07 15:46:19.449243'),(8,'auth','0003_alter_user_email_max_length','2026-10-07 15:46:19.520181'),(9,'auth','0004_alter_user_username_opts','2026-10-07 15:46:19.546586'),(10,'auth','0005_alter_user_last_login_null','2026-10-07 15:46:19.780651'),(11,'auth','0006_require_contenttypes_0002','2026-10-07 15:46:19.798196'),(12,'auth','0007_alter_validators_add_error_messages','2026-10-07 15:46:19.828616'),(13,'auth','0008_alter_user_username_max_length','2026-10-07 15:46:20.184582'),(14,'auth','0009_alter_user_last_name_max_length','2026-10-07 15:46:20.500574'),(15,'auth','0010_alter_group_name_max_length','2026-10-07 15:46:20.575054'),(16,'auth','0011_update_proxy_permissions','2026-10-07 15:46:20.599565'),(17,'auth','0012_alter_user_first_name_max_length','2026-10-07 15:46:20.935335'),(18,'sessions','0001_initial','2026-10-07 15:46:21.132484'),(19,'undangan','0001_initial','2026-10-07 15:46:22.129641'),(20,'undangan','0002_pengaturan_tema','2026-10-07 15:46:22.380261'),(21,'undangan','0003_alter_pengaturan_tema','2026-10-07 15:46:22.398628'),(22,'undangan','0004_alter_pengaturan_tema','2026-10-07 15:46:22.416558'),(23,'undangan','0005_alter_pengaturan_tema','2026-10-07 15:46:22.439866'),(24,'undangan','0006_fotogaleri_gambar_url_pengantin_foto_url_and_more','2026-10-07 15:46:25.552708'),(25,'undangan','0007_undangan_aktif_berakhir_undangan_status_langganan_and_more','2026-10-07 15:46:26.991785'),(26,'undangan','0008_alter_undangan_aktif_berakhir_and_more','2026-10-07 15:46:27.054263'),(27,'undangan','0009_trial_1_bulan','2026-10-07 15:46:27.105699'),(28,'undangan','0010_konfigurasiai_pengaturan_ai_aktif_and_more','2026-10-07 15:46:29.041441');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('81omierejjhviw8iysvblbmivbtnsncl','.eJxVjMsOgjAQRf-la9PYKS2MS_d8A5kXghpIKKyM_64kLHR7zzn35Tra1qHbii3dqO7iwJ1-NyZ52LQDvdN0m73M07qM7HfFH7T4dlZ7Xg_372CgMnzr2CNEthBRoQlBISBANj5nytZrSMjINZJkjmJJEko02N2GtKpq9_4A2gw31w:1xEV3Z:iNFBuZORuGJCARcjz9RIqiDntHY4ACepIoY3KgMmg30','2026-10-21 17:03:53.370925'),('m0sblm58jzxrlmw4uo3xk1a5yx7f2wz5','.eJxVjDsOwyAQBe9CHSHAmE_K9D4DYtklOIlAMnYV5e6xJRdJOzPvvVmI21rC1mkJM7IrG9jll0FMT6qHwEes98ZTq-syAz8SftrOp4b0up3t30GJvexrnwAMUDJSaqtwIIsuGz1qD5p8djIpI6TIbtxRomyEtxIRlMyAGCP7fAHtMzht:1xElBo:NjauOWwL__nmAS2fB6I6uZzlt0vxlUtbBXdA2MXBKfI','2026-10-22 10:17:28.472496');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `undangan_acara`
--

DROP TABLE IF EXISTS `undangan_acara`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `undangan_acara` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nama` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `waktu_mulai` datetime(6) NOT NULL,
  `waktu_selesai` datetime(6) DEFAULT NULL,
  `nama_tempat` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `alamat` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `url_maps` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `urutan` int unsigned NOT NULL,
  `undangan_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `undangan_acara_undangan_id_b23e30f7_fk_undangan_undangan_id` (`undangan_id`),
  CONSTRAINT `undangan_acara_undangan_id_b23e30f7_fk_undangan_undangan_id` FOREIGN KEY (`undangan_id`) REFERENCES `undangan_undangan` (`id`),
  CONSTRAINT `undangan_acara_chk_1` CHECK ((`urutan` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `undangan_acara`
--

LOCK TABLES `undangan_acara` WRITE;
/*!40000 ALTER TABLE `undangan_acara` DISABLE KEYS */;
INSERT INTO `undangan_acara` VALUES (1,'Akad Nikah','2026-11-21 01:00:00.000000','2026-11-21 03:00:00.000000','Masjid Agung Al-Falah','Jl. Merdeka No. 12, Bandung, Jawa Barat','https://maps.google.com/?q=Masjid+Agung',1,NULL),(2,'Resepsi','2026-11-21 06:00:00.000000','2026-11-21 10:00:00.000000','Gedung Serbaguna Puri Anggrek','Jl. Cendana Raya No. 45, Bandung, Jawa Barat','https://maps.google.com/?q=Puri+Anggrek',2,NULL),(3,'Akad Nikah','2026-11-06 08:00:00.303130','2026-11-06 10:00:00.303130','Masjid Agung / Rumah Mempelai','Jl. Bahagia Selalu No. 1, Kota Impian','',1,1),(4,'Resepsi Pernikahan','2026-11-06 11:00:00.303130','2026-11-06 14:00:00.303130','Gedung Pernikahan Asri','Jl. Bahagia Selalu No. 1, Kota Impian','',2,1),(5,'Akad Nikah','2026-11-07 08:00:00.431965','2026-11-07 10:00:00.431965','Masjid Agung / Rumah Mempelai','Jl. Bahagia Selalu No. 1, Kota Impian','',1,2),(6,'Resepsi Pernikahan','2026-11-07 11:00:00.431965','2026-11-07 14:00:00.431965','Gedung Pernikahan Asri','Jl. Bahagia Selalu No. 1, Kota Impian','',2,2);
/*!40000 ALTER TABLE `undangan_acara` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `undangan_fotogaleri`
--

DROP TABLE IF EXISTS `undangan_fotogaleri`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `undangan_fotogaleri` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `gambar` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `keterangan` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `urutan` int unsigned NOT NULL,
  `gambar_url` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `undangan_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `undangan_fotogaleri_undangan_id_9825a213_fk_undangan_undangan_id` (`undangan_id`),
  CONSTRAINT `undangan_fotogaleri_undangan_id_9825a213_fk_undangan_undangan_id` FOREIGN KEY (`undangan_id`) REFERENCES `undangan_undangan` (`id`),
  CONSTRAINT `undangan_fotogaleri_chk_1` CHECK ((`urutan` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `undangan_fotogaleri`
--

LOCK TABLES `undangan_fotogaleri` WRITE;
/*!40000 ALTER TABLE `undangan_fotogaleri` DISABLE KEYS */;
INSERT INTO `undangan_fotogaleri` VALUES (1,'galeri/galeri-contoh-1.jpg','Momen 1',0,'',NULL),(2,'galeri/galeri-contoh-2.jpg','Momen 2',1,'',NULL),(3,'galeri/galeri-contoh-3.jpg','Momen 3',2,'',NULL),(4,'galeri/galeri-contoh-4.jpg','Momen 4',3,'',NULL),(5,'galeri/galeri-contoh-5.jpg','Momen 5',4,'',NULL),(6,'galeri/galeri-contoh-6.jpg','Momen 6',5,'',NULL);
/*!40000 ALTER TABLE `undangan_fotogaleri` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `undangan_konfigurasiai`
--

DROP TABLE IF EXISTS `undangan_konfigurasiai`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `undangan_konfigurasiai` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nama` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `provider` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `base_url` varchar(300) COLLATE utf8mb4_unicode_ci NOT NULL,
  `api_key` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `temperature` double NOT NULL,
  `max_tokens` int unsigned NOT NULL,
  `timeout_detik` int unsigned NOT NULL,
  `kirim_pdf_langsung` tinyint(1) NOT NULL,
  `is_aktif` tinyint(1) NOT NULL,
  `status_tes` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `pesan_tes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `latensi_tes_ms` int unsigned NOT NULL,
  `terakhir_dites` datetime(6) DEFAULT NULL,
  `dibuat` datetime(6) NOT NULL,
  `diperbarui` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `undangan_konfigurasiai_chk_1` CHECK ((`max_tokens` >= 0)),
  CONSTRAINT `undangan_konfigurasiai_chk_2` CHECK ((`timeout_detik` >= 0)),
  CONSTRAINT `undangan_konfigurasiai_chk_3` CHECK ((`latensi_tes_ms` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `undangan_konfigurasiai`
--

LOCK TABLES `undangan_konfigurasiai` WRITE;
/*!40000 ALTER TABLE `undangan_konfigurasiai` DISABLE KEYS */;
/*!40000 ALTER TABLE `undangan_konfigurasiai` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `undangan_pembayaran`
--

DROP TABLE IF EXISTS `undangan_pembayaran`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `undangan_pembayaran` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nominal` int unsigned NOT NULL,
  `durasi_bulan` int unsigned NOT NULL,
  `metode` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `bukti_bayar` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `catatan` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `dibuat` datetime(6) NOT NULL,
  `diverifikasi_pada` datetime(6) DEFAULT NULL,
  `undangan_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `undangan_pembayaran_undangan_id_4d00376b_fk_undangan_undangan_id` (`undangan_id`),
  KEY `undangan_pembayaran_user_id_f367919b_fk_auth_user_id` (`user_id`),
  CONSTRAINT `undangan_pembayaran_undangan_id_4d00376b_fk_undangan_undangan_id` FOREIGN KEY (`undangan_id`) REFERENCES `undangan_undangan` (`id`),
  CONSTRAINT `undangan_pembayaran_user_id_f367919b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `undangan_pembayaran_chk_1` CHECK ((`nominal` >= 0)),
  CONSTRAINT `undangan_pembayaran_chk_2` CHECK ((`durasi_bulan` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `undangan_pembayaran`
--

LOCK TABLES `undangan_pembayaran` WRITE;
/*!40000 ALTER TABLE `undangan_pembayaran` DISABLE KEYS */;
/*!40000 ALTER TABLE `undangan_pembayaran` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `undangan_pengantin`
--

DROP TABLE IF EXISTS `undangan_pengantin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `undangan_pengantin` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `peran` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nama_lengkap` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nama_panggilan` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `anak_ke` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nama_ayah` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nama_ibu` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `instagram` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `foto` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `foto_url` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `undangan_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `undangan_pengantin_undangan_id_8ca33bb9_fk_undangan_undangan_id` (`undangan_id`),
  CONSTRAINT `undangan_pengantin_undangan_id_8ca33bb9_fk_undangan_undangan_id` FOREIGN KEY (`undangan_id`) REFERENCES `undangan_undangan` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `undangan_pengantin`
--

LOCK TABLES `undangan_pengantin` WRITE;
/*!40000 ALTER TABLE `undangan_pengantin` DISABLE KEYS */;
INSERT INTO `undangan_pengantin` VALUES (1,'pria','Budi Santoso, S.Kom.','Budi','Putra pertama','Hendra Santoso','Sri Wahyuni','budisantoso','pengantin/contoh-pria.jpg','',NULL),(2,'wanita','Rina Kartika Sari, S.Ds.','Rina','Putri kedua','Ahmad Suryana','Dewi Lestari','rinakartika','pengantin/contoh-wanita.jpg','',NULL),(3,'pria','bambang','Mempelai Pria','','','','','','',1),(4,'wanita','Mempelai Wanita','Mempelai Wanita','','','','','','',1),(5,'pria','Lilik Nurhayati, S.Kom','Mempelai Pria','','','','','','',2),(6,'wanita','Mempelai Wanita','Mempelai Wanita','','','','','','',2);
/*!40000 ALTER TABLE `undangan_pengantin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `undangan_pengaturan`
--

DROP TABLE IF EXISTS `undangan_pengaturan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `undangan_pengaturan` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `judul` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `hashtag` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `quote` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `sumber_quote` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `musik` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `catatan_penutup` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `tema` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ai_aktif` tinyint(1) NOT NULL,
  `ai_batas_harian` int unsigned NOT NULL,
  `ai_khusus_berbayar` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `undangan_pengaturan_chk_1` CHECK ((`ai_batas_harian` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `undangan_pengaturan`
--

LOCK TABLES `undangan_pengaturan` WRITE;
/*!40000 ALTER TABLE `undangan_pengaturan` DISABLE KEYS */;
INSERT INTO `undangan_pengaturan` VALUES (1,'Undangan Pernikahan Rina & Budi','#RinaBudiForever','Dan di antara tanda-tanda kekuasaan-Nya diciptakan-Nya untukmu pasangan hidup dari jenismu sendiri, supaya kamu mendapat ketenangan dan dijadikan-Nya di antaramu rasa kasih dan sayang.','QS. Ar-Rum: 21','','Merupakan suatu kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir untuk memberikan doa restu.','klasik',1,5,0);
/*!40000 ALTER TABLE `undangan_pengaturan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `undangan_rekening`
--

DROP TABLE IF EXISTS `undangan_rekening`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `undangan_rekening` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nama_bank` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nomor` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `atas_nama` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `qr` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `urutan` int unsigned NOT NULL,
  `qr_url` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `undangan_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `undangan_rekening_undangan_id_dd3b8910_fk_undangan_undangan_id` (`undangan_id`),
  CONSTRAINT `undangan_rekening_undangan_id_dd3b8910_fk_undangan_undangan_id` FOREIGN KEY (`undangan_id`) REFERENCES `undangan_undangan` (`id`),
  CONSTRAINT `undangan_rekening_chk_1` CHECK ((`urutan` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `undangan_rekening`
--

LOCK TABLES `undangan_rekening` WRITE;
/*!40000 ALTER TABLE `undangan_rekening` DISABLE KEYS */;
INSERT INTO `undangan_rekening` VALUES (1,'BCA','1234567890','Rina Kartika Sari','',1,'',NULL),(2,'Mandiri','0987654321','Budi Santoso','',2,'',NULL);
/*!40000 ALTER TABLE `undangan_rekening` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `undangan_riwayatai`
--

DROP TABLE IF EXISTS `undangan_riwayatai`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `undangan_riwayatai` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nama_file` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ukuran_kb` int unsigned NOT NULL,
  `provider` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mode_baca` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `jumlah_karakter_teks` int unsigned NOT NULL,
  `status` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  `hasil` json NOT NULL,
  `pesan_error` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `durasi_ms` int unsigned NOT NULL,
  `dibuat` datetime(6) NOT NULL,
  `diterapkan_pada` datetime(6) DEFAULT NULL,
  `konfigurasi_id` bigint DEFAULT NULL,
  `undangan_id` bigint DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `undangan_riwayatai_konfigurasi_id_86044532_fk_undangan_` (`konfigurasi_id`),
  KEY `undangan_riwayatai_undangan_id_6dac0bb7_fk_undangan_undangan_id` (`undangan_id`),
  KEY `undangan_riwayatai_user_id_170ead80_fk_auth_user_id` (`user_id`),
  CONSTRAINT `undangan_riwayatai_konfigurasi_id_86044532_fk_undangan_` FOREIGN KEY (`konfigurasi_id`) REFERENCES `undangan_konfigurasiai` (`id`),
  CONSTRAINT `undangan_riwayatai_undangan_id_6dac0bb7_fk_undangan_undangan_id` FOREIGN KEY (`undangan_id`) REFERENCES `undangan_undangan` (`id`),
  CONSTRAINT `undangan_riwayatai_user_id_170ead80_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `undangan_riwayatai_chk_1` CHECK ((`ukuran_kb` >= 0)),
  CONSTRAINT `undangan_riwayatai_chk_2` CHECK ((`jumlah_karakter_teks` >= 0)),
  CONSTRAINT `undangan_riwayatai_chk_3` CHECK ((`durasi_ms` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `undangan_riwayatai`
--

LOCK TABLES `undangan_riwayatai` WRITE;
/*!40000 ALTER TABLE `undangan_riwayatai` DISABLE KEYS */;
/*!40000 ALTER TABLE `undangan_riwayatai` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `undangan_tamu`
--

DROP TABLE IF EXISTS `undangan_tamu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `undangan_tamu` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nama` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(140) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sapaan` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `jumlah_undangan` int unsigned NOT NULL,
  `catatan` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `pertama_dibuka` datetime(6) DEFAULT NULL,
  `jumlah_dibuka` int unsigned NOT NULL,
  `undangan_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `undangan_tamu_slug_e0efba6c` (`slug`),
  KEY `undangan_tamu_undangan_id_515e84c8_fk_undangan_undangan_id` (`undangan_id`),
  CONSTRAINT `undangan_tamu_undangan_id_515e84c8_fk_undangan_undangan_id` FOREIGN KEY (`undangan_id`) REFERENCES `undangan_undangan` (`id`),
  CONSTRAINT `undangan_tamu_chk_1` CHECK ((`jumlah_undangan` >= 0)),
  CONSTRAINT `undangan_tamu_chk_2` CHECK ((`jumlah_dibuka` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `undangan_tamu`
--

LOCK TABLES `undangan_tamu` WRITE;
/*!40000 ALTER TABLE `undangan_tamu` DISABLE KEYS */;
INSERT INTO `undangan_tamu` VALUES (1,'Andi Pratama','andi-pratama','Bapak',2,'','2026-10-07 15:54:38.068931',3,NULL),(2,'Siti Nurhaliza','siti-nurhaliza','Ibu',1,'',NULL,0,NULL),(3,'Keluarga Wijaya','keluarga-wijaya','Bapak/Ibu',4,'',NULL,0,NULL);
/*!40000 ALTER TABLE `undangan_tamu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `undangan_ucapan`
--

DROP TABLE IF EXISTS `undangan_ucapan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `undangan_ucapan` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nama` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `pesan` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `kehadiran` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `jumlah_orang` int unsigned NOT NULL,
  `disetujui` tinyint(1) NOT NULL,
  `dibuat` datetime(6) NOT NULL,
  `tamu_id` bigint DEFAULT NULL,
  `undangan_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `undangan_ucapan_tamu_id_c9308920_fk_undangan_tamu_id` (`tamu_id`),
  KEY `undangan_ucapan_undangan_id_de44bfdd_fk_undangan_undangan_id` (`undangan_id`),
  CONSTRAINT `undangan_ucapan_tamu_id_c9308920_fk_undangan_tamu_id` FOREIGN KEY (`tamu_id`) REFERENCES `undangan_tamu` (`id`),
  CONSTRAINT `undangan_ucapan_undangan_id_de44bfdd_fk_undangan_undangan_id` FOREIGN KEY (`undangan_id`) REFERENCES `undangan_undangan` (`id`),
  CONSTRAINT `undangan_ucapan_chk_1` CHECK ((`jumlah_orang` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `undangan_ucapan`
--

LOCK TABLES `undangan_ucapan` WRITE;
/*!40000 ALTER TABLE `undangan_ucapan` DISABLE KEYS */;
INSERT INTO `undangan_ucapan` VALUES (1,'Andi Pratama','Selamat menempuh hidup baru! Semoga samawa selalu.','hadir',2,1,'2026-10-07 15:46:51.406983',NULL,NULL),(2,'Siti Nurhaliza','Barakallahu lakuma wa baraka alaikuma. Bahagia selalu ya!','hadir',1,1,'2026-10-07 15:46:51.434499',NULL,NULL),(3,'Dimas Arya','Maaf belum bisa hadir, doa terbaik dari jauh untuk kalian berdua.','tidak',1,1,'2026-10-07 15:46:51.459930',NULL,NULL);
/*!40000 ALTER TABLE `undangan_ucapan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `undangan_undangan`
--

DROP TABLE IF EXISTS `undangan_undangan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `undangan_undangan` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `slug` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `judul` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tema` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `hashtag` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `quote` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `sumber_quote` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `musik` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `musik_url` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `catatan_penutup` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `dibuat` datetime(6) NOT NULL,
  `diperbarui` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  `aktif_berakhir` datetime(6) DEFAULT NULL,
  `status_langganan` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `trial_berakhir` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `undangan_undangan_user_id_b0a07882_fk_auth_user_id` (`user_id`),
  CONSTRAINT `undangan_undangan_user_id_b0a07882_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `undangan_undangan`
--

LOCK TABLES `undangan_undangan` WRITE;
/*!40000 ALTER TABLE `undangan_undangan` DISABLE KEYS */;
INSERT INTO `undangan_undangan` VALUES (1,'bambang','Pernikahan bambang','klasik','#BambangWedding','Dan di antara tanda-tanda (kebesaran)-Nya ialah Dia menciptakan pasangan-pasangan untukmu dari jenismu sendiri, agar kamu cenderung dan merasa tenteram kepadanya, dan Dia menjadikan di antaramu rasa kasih dan sayang.','QS. Ar-Rum: 21','','','Merupakan suatu kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir untuk memberikan doa restu.','2026-10-07 17:03:53.300842','2026-10-07 17:03:53.300855',2,NULL,'trial','2026-11-06 17:03:53.300461'),(2,'lilik1997','Pernikahan Lilik Nurhayati, S.Kom','klasik','#Lilik1997Wedding','Dan di antara tanda-tanda (kebesaran)-Nya ialah Dia menciptakan pasangan-pasangan untukmu dari jenismu sendiri, agar kamu cenderung dan merasa tenteram kepadanya, dan Dia menjadikan di antaramu rasa kasih dan sayang.','QS. Ar-Rum: 21','','','Merupakan suatu kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir untuk memberikan doa restu.','2026-10-08 10:17:28.430234','2026-10-08 10:17:28.430246',3,NULL,'trial','2026-11-07 10:17:28.429912');
/*!40000 ALTER TABLE `undangan_undangan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'jelajah_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-07 12:19:42
