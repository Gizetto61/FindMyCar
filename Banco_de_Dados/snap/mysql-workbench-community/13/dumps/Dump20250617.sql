-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: FindMyCar2
-- ------------------------------------------------------
-- Server version	8.0.41-3+b1

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
-- Table structure for table `Anuncio`
--

DROP TABLE IF EXISTS `Anuncio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Anuncio` (
  `id_Anuncio` int NOT NULL AUTO_INCREMENT,
  `Descricao` varchar(255) DEFAULT NULL,
  `data_Anun` varchar(10) DEFAULT NULL,
  `Status` varchar(20) DEFAULT NULL,
  `fk_Carro_id_Carro` int DEFAULT NULL,
  `fk_Usuario_id_Usuario` int DEFAULT NULL,
  PRIMARY KEY (`id_Anuncio`),
  KEY `FK_Anuncio_2` (`fk_Carro_id_Carro`),
  KEY `FK_Anuncio_3` (`fk_Usuario_id_Usuario`),
  CONSTRAINT `FK_Anuncio_2` FOREIGN KEY (`fk_Carro_id_Carro`) REFERENCES `Carro` (`id_Carro`) ON DELETE CASCADE,
  CONSTRAINT `FK_Anuncio_3` FOREIGN KEY (`fk_Usuario_id_Usuario`) REFERENCES `Usuario` (`id_Usuario`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Anuncio`
--

LOCK TABLES `Anuncio` WRITE;
/*!40000 ALTER TABLE `Anuncio` DISABLE KEYS */;
/*!40000 ALTER TABLE `Anuncio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Carro`
--

DROP TABLE IF EXISTS `Carro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Carro` (
  `id_Carro` int NOT NULL AUTO_INCREMENT,
  `Modelo` varchar(50) DEFAULT NULL,
  `Ano` char(1) DEFAULT NULL,
  `Preco` varchar(15) DEFAULT NULL,
  `Consumo` varchar(6) DEFAULT NULL,
  `Manutencao` varchar(15) DEFAULT NULL,
  `Origem` varchar(5) DEFAULT NULL,
  `Espaco` varchar(12) DEFAULT NULL,
  `Marca` varchar(20) DEFAULT NULL,
  `Desempenho` varchar(12) DEFAULT NULL,
  `Conforto` varchar(9) DEFAULT NULL,
  `Imagem_F` varchar(255) DEFAULT NULL,
  `Imagem_L` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_Carro`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Carro`
--

LOCK TABLES `Carro` WRITE;
/*!40000 ALTER TABLE `Carro` DISABLE KEYS */;
/*!40000 ALTER TABLE `Carro` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Formulario_Usuario_NL`
--

DROP TABLE IF EXISTS `Formulario_Usuario_NL`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Formulario_Usuario_NL` (
  `id_Formulario` int NOT NULL,
  `data_Resp` varchar(10) DEFAULT NULL,
  `Tipo` char(1) DEFAULT NULL,
  `fk_Usuario_id_Usuario` int DEFAULT NULL,
  `id_Anonimo` int NOT NULL,
  `data_Acesso` varchar(10) DEFAULT NULL,
  `fk_Resposta_id_Resposta` int DEFAULT NULL,
  PRIMARY KEY (`id_Formulario`,`id_Anonimo`),
  KEY `FK_Formulario_Usuario_NL_2` (`fk_Usuario_id_Usuario`),
  KEY `FK_Formulario_Usuario_NL_3` (`fk_Resposta_id_Resposta`),
  CONSTRAINT `FK_Formulario_Usuario_NL_2` FOREIGN KEY (`fk_Usuario_id_Usuario`) REFERENCES `Usuario` (`id_Usuario`) ON DELETE RESTRICT,
  CONSTRAINT `FK_Formulario_Usuario_NL_3` FOREIGN KEY (`fk_Resposta_id_Resposta`) REFERENCES `Resposta` (`id_Resposta`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Formulario_Usuario_NL`
--

LOCK TABLES `Formulario_Usuario_NL` WRITE;
/*!40000 ALTER TABLE `Formulario_Usuario_NL` DISABLE KEYS */;
/*!40000 ALTER TABLE `Formulario_Usuario_NL` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Login`
--

DROP TABLE IF EXISTS `Login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Login` (
  `id_Login` int NOT NULL AUTO_INCREMENT,
  `data_Login` varchar(10) DEFAULT NULL,
  `IP` varchar(15) DEFAULT NULL,
  `Tipo` varchar(10) DEFAULT NULL,
  `fk_Usuario_id_Usuario` int DEFAULT NULL,
  PRIMARY KEY (`id_Login`),
  KEY `FK_Login_2` (`fk_Usuario_id_Usuario`),
  CONSTRAINT `FK_Login_2` FOREIGN KEY (`fk_Usuario_id_Usuario`) REFERENCES `Usuario` (`id_Usuario`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Login`
--

LOCK TABLES `Login` WRITE;
/*!40000 ALTER TABLE `Login` DISABLE KEYS */;
/*!40000 ALTER TABLE `Login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Recomendacao`
--

DROP TABLE IF EXISTS `Recomendacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Recomendacao` (
  `data_Rec` varchar(10) DEFAULT NULL,
  `id_Recomendacao` int NOT NULL AUTO_INCREMENT,
  `fk_Carro_id_Carro` int DEFAULT NULL,
  PRIMARY KEY (`id_Recomendacao`),
  KEY `FK_Recomendacao_2` (`fk_Carro_id_Carro`),
  CONSTRAINT `FK_Recomendacao_2` FOREIGN KEY (`fk_Carro_id_Carro`) REFERENCES `Carro` (`id_Carro`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Recomendacao`
--

LOCK TABLES `Recomendacao` WRITE;
/*!40000 ALTER TABLE `Recomendacao` DISABLE KEYS */;
/*!40000 ALTER TABLE `Recomendacao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Resposta`
--

DROP TABLE IF EXISTS `Resposta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Resposta` (
  `id_Resposta` int NOT NULL AUTO_INCREMENT,
  `Pergunta` int DEFAULT NULL,
  `Resposta` int DEFAULT NULL,
  PRIMARY KEY (`id_Resposta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Resposta`
--

LOCK TABLES `Resposta` WRITE;
/*!40000 ALTER TABLE `Resposta` DISABLE KEYS */;
/*!40000 ALTER TABLE `Resposta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Usuario`
--

DROP TABLE IF EXISTS `Usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Usuario` (
  `Nome` varchar(100) DEFAULT NULL,
  `Email` varchar(50) DEFAULT NULL,
  `Senha` varchar(50) DEFAULT NULL,
  `data_Nasc` varchar(10) DEFAULT NULL,
  `foto_Perfil` varchar(255) DEFAULT NULL,
  `Telefone` varchar(14) DEFAULT NULL,
  `aut_2_fac` tinyint(1) DEFAULT NULL,
  `id_Usuario` int NOT NULL AUTO_INCREMENT,
  `fk_Recomendacao_id_Recomendacao` int DEFAULT NULL,
  PRIMARY KEY (`id_Usuario`),
  KEY `FK_Usuario_2` (`fk_Recomendacao_id_Recomendacao`),
  CONSTRAINT `FK_Usuario_2` FOREIGN KEY (`fk_Recomendacao_id_Recomendacao`) REFERENCES `Recomendacao` (`id_Recomendacao`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Usuario`
--

LOCK TABLES `Usuario` WRITE;
/*!40000 ALTER TABLE `Usuario` DISABLE KEYS */;
/*!40000 ALTER TABLE `Usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'FindMyCar2'
--

--
-- Dumping routines for database 'FindMyCar2'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-17 14:58:13
