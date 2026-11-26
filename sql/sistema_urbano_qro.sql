-- MySQL dump 10.13  Distrib 8.0.46, for Linux (x86_64)
--
-- Host: localhost    Database: sistema_urbano_qro
-- ------------------------------------------------------
-- Server version	8.0.46-0ubuntu0.24.04.5

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
-- Table structure for table `anio`
--

DROP TABLE IF EXISTS `anio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `anio` (
  `id_anio` int NOT NULL AUTO_INCREMENT,
  `anio` int NOT NULL,
  PRIMARY KEY (`id_anio`),
  UNIQUE KEY `anio` (`anio`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anio`
--

LOCK TABLES `anio` WRITE;
/*!40000 ALTER TABLE `anio` DISABLE KEYS */;
INSERT INTO `anio` VALUES (1,2010),(2,2011),(3,2012),(4,2013),(5,2014),(6,2015),(7,2016),(8,2017),(9,2018),(10,2019),(11,2020),(12,2021),(13,2022),(14,2023),(15,2024),(16,2025);
/*!40000 ALTER TABLE `anio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dato_servicio`
--

DROP TABLE IF EXISTS `dato_servicio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dato_servicio` (
  `id_dato` int NOT NULL AUTO_INCREMENT,
  `id_municipio` int NOT NULL,
  `id_anio` int NOT NULL,
  `id_indicador` int NOT NULL,
  `id_fuente` int NOT NULL,
  `valor` decimal(15,2) NOT NULL,
  `observaciones` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id_dato`),
  UNIQUE KEY `uq_dato_mun_anio_ind_fuente` (`id_municipio`,`id_anio`,`id_indicador`,`id_fuente`),
  KEY `id_anio` (`id_anio`),
  KEY `id_indicador` (`id_indicador`),
  KEY `id_fuente` (`id_fuente`),
  CONSTRAINT `dato_servicio_ibfk_1` FOREIGN KEY (`id_municipio`) REFERENCES `municipio` (`id_municipio`),
  CONSTRAINT `dato_servicio_ibfk_2` FOREIGN KEY (`id_anio`) REFERENCES `anio` (`id_anio`),
  CONSTRAINT `dato_servicio_ibfk_3` FOREIGN KEY (`id_indicador`) REFERENCES `indicador_servicio` (`id_indicador`),
  CONSTRAINT `dato_servicio_ibfk_4` FOREIGN KEY (`id_fuente`) REFERENCES `fuente_dato` (`id_fuente`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dato_servicio`
--

LOCK TABLES `dato_servicio` WRITE;
/*!40000 ALTER TABLE `dato_servicio` DISABLE KEYS */;
INSERT INTO `dato_servicio` VALUES (1,1,1,2,9,93.80,'Porcentaje de viviendas con agua de la red publica en 2010'),(2,1,1,4,9,97.70,'Porcentaje de viviendas con energia electrica en 2010'),(3,1,11,2,8,98.60,'Porcentaje de viviendas con agua entubada en 2020'),(4,1,11,11,8,94.10,'Porcentaje de poblacion de 6 a 14 años que asiste a la escuela en 2020'),(5,1,11,14,8,79.80,'Porcentaje de poblacion afiliada a servicios de salud en 2020'),(6,1,12,9,13,306921.00,'Matricula del ciclo escolar 2020-2021 (7 niveles educativos). PMD 2021-2024, pagina 67'),(7,1,16,7,11,169.00,'Flota municipal reportada en 2025'),(8,1,16,8,11,2500000.00,'Ascensos registrados del 1 de enero al 15 de diciembre de 2025'),(9,1,14,17,12,318796.97,'Total anual de residuos recolectados durante 2023'),(10,1,15,17,12,333450.48,'Total anual de residuos recolectados durante 2024');
/*!40000 ALTER TABLE `dato_servicio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fuente_dato`
--

DROP TABLE IF EXISTS `fuente_dato`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fuente_dato` (
  `id_fuente` int NOT NULL AUTO_INCREMENT,
  `institucion` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre_documento` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fecha_consulta` date DEFAULT NULL,
  PRIMARY KEY (`id_fuente`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fuente_dato`
--

LOCK TABLES `fuente_dato` WRITE;
/*!40000 ALTER TABLE `fuente_dato` DISABLE KEYS */;
INSERT INTO `fuente_dato` VALUES (1,'INEGI','Censos de Poblacion y Vivienda','https://www.inegi.org.mx/','2026-11-20'),(2,'CONAPO','Proyecciones de la Poblacion','https://www.gob.mx/conapo','2026-11-20'),(3,'CEA Queretaro','Informacion sobre agua potable','https://www.ceaqueretaro.gob.mx/','2026-11-20'),(4,'SEP','Estadisticas educativas','https://www.gob.mx/sep','2026-11-20'),(5,'Secretaria de Salud','Informacion estadistica de salud','https://www.gob.mx/salud','2026-11-20'),(6,'Municipio de Queretaro','Informacion de servicios urbanos','https://municipiodequeretaro.gob.mx/','2026-11-20'),(7,'INEGI','Principales resultados del Censo de Poblacion 2010 - Queretaro','https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/censos/poblacion/2010/princi_result/qro/22_principales_resultados_cpv2010.pdf','2026-11-20'),(8,'INEGI','Principales resultados del Censo de Poblacion 2020 - Queretaro','https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/702825198282.pdf','2026-11-20'),(9,'INEGI y Municipio de Queretaro','Atlas de Riesgos de Queretaro - datos de vivienda 2010','https://municipiodequeretaro.gob.mx/wp-content/uploads/2019/07/Atlas-de-Riesgos-de-Queretaro.pdf','2026-11-20'),(10,'INEGI','Principales resultados del Censo de Poblacion y Vivienda 2020 - Queretaro','https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/702825198282.pdf','2026-11-20'),(11,'Municipio de Queretaro','Sistema de Transporte del Municipio de Queretaro consolida crecimiento en 2025','https://municipiodequeretaro.gob.mx/sistema-de-transporte-del-municipio-de-queretaro-consolida-crecimiento-en-2025/','2026-11-20'),(12,'Municipio de Queretaro','Anuario Economico Municipal 2025 - Medio Ambiente','https://municipiodequeretaro.gob.mx/anuario-economico-2025/medio-ambiente.php','2026-11-20'),(13,'Municipio de Querétaro','Plan Municipal de Desarrollo 2021-2024','https://municipiodequeretaro.gob.mx/wp-content/uploads/2022/03/PLAN-MUNICIPAL-DE-DESARROLLO-2021-2024.pdf','2026-11-20');
/*!40000 ALTER TABLE `fuente_dato` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `indicador_servicio`
--

DROP TABLE IF EXISTS `indicador_servicio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `indicador_servicio` (
  `id_indicador` int NOT NULL AUTO_INCREMENT,
  `id_servicio` int NOT NULL,
  `nombre` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `unidad` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id_indicador`),
  UNIQUE KEY `uq_servicio_indicador` (`id_servicio`,`nombre`),
  CONSTRAINT `indicador_servicio_ibfk_1` FOREIGN KEY (`id_servicio`) REFERENCES `servicio` (`id_servicio`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `indicador_servicio`
--

LOCK TABLES `indicador_servicio` WRITE;
/*!40000 ALTER TABLE `indicador_servicio` DISABLE KEYS */;
INSERT INTO `indicador_servicio` VALUES (1,1,'Consumo de agua','Litros por habitante al dia','Consumo promedio diario de agua por persona'),(2,1,'Cobertura de agua potable','Porcentaje','Porcentaje de viviendas con acceso al agua potable'),(3,2,'Consumo electrico','kWh','Consumo de energia electrica'),(4,2,'Cobertura electrica','Porcentaje','Porcentaje de viviendas con electricidad'),(5,3,'Pasajeros transportados','Personas','Cantidad de pasajeros transportados'),(6,3,'Unidades de transporte','Unidades','Cantidad de unidades de transporte publico'),(7,3,'Flota del transporte municipal','Vehiculos','Cantidad de vehiculos que integran la flota municipal'),(8,3,'Ascensos del transporte municipal','Ascensos','Cantidad de ascensos registrados en el sistema municipal'),(9,4,'Matricula escolar','Alumnos','Cantidad de alumnos inscritos'),(10,4,'Escuelas','Planteles','Cantidad de escuelas registradas'),(11,4,'Asistencia escolar de 6 a 14 años','Porcentaje','Porcentaje de la poblacion de 6 a 14 años que asiste a la escuela'),(12,5,'Unidades medicas','Unidades','Cantidad de centros de atencion medica'),(13,5,'Poblacion atendida','Personas','Cantidad de personas atendidas'),(14,5,'Afiliacion a servicios de salud','Porcentaje','Porcentaje de la poblacion afiliada a servicios de salud'),(15,6,'Residuos recolectados','Toneladas por dia','Cantidad de residuos recolectados diariamente'),(16,6,'Generacion de residuos','Kg por habitante al dia','Generacion promedio de residuos por persona'),(17,6,'Residuos recolectados anualmente','Toneladas por año','Total anual de residuos recolectados en el municipio');
/*!40000 ALTER TABLE `indicador_servicio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `municipio`
--

DROP TABLE IF EXISTS `municipio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `municipio` (
  `id_municipio` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `estado` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id_municipio`),
  UNIQUE KEY `uq_municipio_estado` (`nombre`,`estado`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `municipio`
--

LOCK TABLES `municipio` WRITE;
/*!40000 ALTER TABLE `municipio` DISABLE KEYS */;
INSERT INTO `municipio` VALUES (1,'Querétaro','Querétaro');
/*!40000 ALTER TABLE `municipio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `poblacion`
--

DROP TABLE IF EXISTS `poblacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `poblacion` (
  `id_poblacion` int NOT NULL AUTO_INCREMENT,
  `id_municipio` int NOT NULL,
  `id_anio` int NOT NULL,
  `id_fuente` int NOT NULL,
  `poblacion_total` int NOT NULL,
  PRIMARY KEY (`id_poblacion`),
  UNIQUE KEY `uq_poblacion_mun_anio_fuente` (`id_municipio`,`id_anio`,`id_fuente`),
  KEY `id_anio` (`id_anio`),
  KEY `id_fuente` (`id_fuente`),
  CONSTRAINT `poblacion_ibfk_1` FOREIGN KEY (`id_municipio`) REFERENCES `municipio` (`id_municipio`),
  CONSTRAINT `poblacion_ibfk_2` FOREIGN KEY (`id_anio`) REFERENCES `anio` (`id_anio`),
  CONSTRAINT `poblacion_ibfk_3` FOREIGN KEY (`id_fuente`) REFERENCES `fuente_dato` (`id_fuente`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `poblacion`
--

LOCK TABLES `poblacion` WRITE;
/*!40000 ALTER TABLE `poblacion` DISABLE KEYS */;
INSERT INTO `poblacion` VALUES (1,1,1,7,801940),(2,1,11,8,1049777);
/*!40000 ALTER TABLE `poblacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proyeccion`
--

DROP TABLE IF EXISTS `proyeccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proyeccion` (
  `id_proyeccion` int NOT NULL AUTO_INCREMENT,
  `id_municipio` int NOT NULL,
  `anio_base` int NOT NULL,
  `anio_proyectado` int NOT NULL,
  `porcentaje_crecimiento` decimal(6,2) NOT NULL,
  `poblacion_estimada` decimal(15,2) NOT NULL,
  `demanda_estimada` decimal(15,2) DEFAULT NULL,
  `unidad_demanda` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_proyeccion`),
  KEY `id_municipio` (`id_municipio`),
  CONSTRAINT `proyeccion_ibfk_1` FOREIGN KEY (`id_municipio`) REFERENCES `municipio` (`id_municipio`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proyeccion`
--

LOCK TABLES `proyeccion` WRITE;
/*!40000 ALTER TABLE `proyeccion` DISABLE KEYS */;
/*!40000 ALTER TABLE `proyeccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servicio`
--

DROP TABLE IF EXISTS `servicio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicio` (
  `id_servicio` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id_servicio`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicio`
--

LOCK TABLES `servicio` WRITE;
/*!40000 ALTER TABLE `servicio` DISABLE KEYS */;
INSERT INTO `servicio` VALUES (1,'Agua potable','Abastecimiento y consumo de agua'),(2,'Energia electrica','Consumo y cobertura de electricidad'),(3,'Transporte publico','Movilidad y transporte de pasajeros'),(4,'Educacion','Escuelas y matricula escolar'),(5,'Salud','Unidades medicas y atencion a la poblacion'),(6,'Residuos','Recoleccion y generacion de residuos');
/*!40000 ALTER TABLE `servicio` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-25 19:33:21
