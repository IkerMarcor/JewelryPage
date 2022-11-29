-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: finkies
-- ------------------------------------------------------
-- Server version	5.7.36

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
-- Table structure for table `categoria_producto`
--

DROP TABLE IF EXISTS `categoria_producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categoria_producto` (
  `id_categoria` int(11) NOT NULL AUTO_INCREMENT,
  `categoria` varchar(25) NOT NULL,
  PRIMARY KEY (`id_categoria`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categoria_producto`
--

LOCK TABLES `categoria_producto` WRITE;
/*!40000 ALTER TABLE `categoria_producto` DISABLE KEYS */;
INSERT INTO `categoria_producto` VALUES (1,'Aretes'),(2,'Playeras'),(3,'Collares'),(4,'Stickers'),(5,'Pulseras');
/*!40000 ALTER TABLE `categoria_producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `color`
--

DROP TABLE IF EXISTS `color`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `color` (
  `id_color` int(11) NOT NULL AUTO_INCREMENT,
  `color` varchar(25) NOT NULL,
  PRIMARY KEY (`id_color`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `color`
--

LOCK TABLES `color` WRITE;
/*!40000 ALTER TABLE `color` DISABLE KEYS */;
INSERT INTO `color` VALUES (1,'Verde'),(2,'rojo');
/*!40000 ALTER TABLE `color` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `direccion`
--

DROP TABLE IF EXISTS `direccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `direccion` (
  `id_direccion` int(11) NOT NULL AUTO_INCREMENT,
  `direccion` varchar(255) NOT NULL,
  `ciudad` varchar(255) NOT NULL,
  `estado` varchar(255) NOT NULL,
  `cp` int(10) NOT NULL,
  PRIMARY KEY (`id_direccion`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `direccion`
--

LOCK TABLES `direccion` WRITE;
/*!40000 ALTER TABLE `direccion` DISABLE KEYS */;
/*!40000 ALTER TABLE `direccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empleados`
--

DROP TABLE IF EXISTS `empleados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empleados` (
  `id_empleado` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `contrasena` varchar(100) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `apellido1` varchar(255) NOT NULL,
  `apellido2` varchar(255) DEFAULT NULL,
  `id_permiso` int(11) NOT NULL,
  PRIMARY KEY (`id_empleado`),
  KEY `id_permiso` (`id_permiso`),
  CONSTRAINT `empleados_ibfk_1` FOREIGN KEY (`id_permiso`) REFERENCES `permisos` (`id_permiso`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empleados`
--

LOCK TABLES `empleados` WRITE;
/*!40000 ALTER TABLE `empleados` DISABLE KEYS */;
/*!40000 ALTER TABLE `empleados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historial_visitas`
--

DROP TABLE IF EXISTS `historial_visitas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historial_visitas` (
  `anio` year(4) NOT NULL,
  `id_producto_especifico` int(11) NOT NULL,
  `mes` int(2) NOT NULL,
  `numero_visitas` int(11) NOT NULL,
  PRIMARY KEY (`anio`,`mes`,`id_producto_especifico`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_visitas`
--

LOCK TABLES `historial_visitas` WRITE;
/*!40000 ALTER TABLE `historial_visitas` DISABLE KEYS */;
INSERT INTO `historial_visitas` VALUES (2022,1,11,2),(2022,2,11,1);
/*!40000 ALTER TABLE `historial_visitas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `imagenes_especificas`
--

DROP TABLE IF EXISTS `imagenes_especificas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `imagenes_especificas` (
  `id_imagen_especifica` int(11) NOT NULL AUTO_INCREMENT,
  `id_producto_especifico` int(11) DEFAULT NULL,
  `imagen` varchar(100) NOT NULL,
  PRIMARY KEY (`id_imagen_especifica`),
  KEY `id_producto_especifico` (`id_producto_especifico`),
  CONSTRAINT `imagenes_especificas_ibfk_1` FOREIGN KEY (`id_producto_especifico`) REFERENCES `producto_especifico` (`id_producto_especifico`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imagenes_especificas`
--

LOCK TABLES `imagenes_especificas` WRITE;
/*!40000 ALTER TABLE `imagenes_especificas` DISABLE KEYS */;
INSERT INTO `imagenes_especificas` VALUES (1,1,'20200728184926_1.jpg'),(2,1,'Chipotle_Pepper__Smoked_Dried_Jalapeno.jfif'),(3,1,'chuugun.jpg'),(4,1,'chuuhomo.png'),(5,2,'chuuhomo.png'),(6,3,'317445042_1307802996718221_3746127010734352886_n.jpg'),(7,3,'316949913_193327733270559_1289678874873060459_n.jpg'),(8,3,'WhatsApp Image 2022-11-20 at 14.01.59.jpeg'),(9,4,'WhatsApp Image 2022-11-19 at 21.52.44.jpeg'),(10,4,'316261737_446227671005754_4449940996684684174_n.jpg'),(11,5,'mesa.jpg');
/*!40000 ALTER TABLE `imagenes_especificas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `metodo_pago`
--

DROP TABLE IF EXISTS `metodo_pago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `metodo_pago` (
  `id_metodopago` int(11) NOT NULL AUTO_INCREMENT,
  `id_paypal` varchar(17) NOT NULL,
  PRIMARY KEY (`id_metodopago`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metodo_pago`
--

LOCK TABLES `metodo_pago` WRITE;
/*!40000 ALTER TABLE `metodo_pago` DISABLE KEYS */;
/*!40000 ALTER TABLE `metodo_pago` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos` (
  `idpedidos` int(11) NOT NULL,
  `idproductos` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `idusuario` int(11) DEFAULT NULL,
  `precio` decimal(6,2) DEFAULT NULL,
  PRIMARY KEY (`idpedidos`,`idproductos`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
INSERT INTO `pedidos` VALUES (1,1,1,1,NULL),(2,2,1,1,NULL),(3,1,2,1,NULL),(1,4,2,1,NULL),(1,6,2,1,NULL),(1,2,4,1,0.00),(2,3,4,1,5.00);
/*!40000 ALTER TABLE `pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permisos`
--

DROP TABLE IF EXISTS `permisos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permisos` (
  `id_permiso` int(11) NOT NULL AUTO_INCREMENT,
  `permiso` varchar(50) NOT NULL,
  `descripcion` varchar(500) NOT NULL,
  PRIMARY KEY (`id_permiso`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permisos`
--

LOCK TABLES `permisos` WRITE;
/*!40000 ALTER TABLE `permisos` DISABLE KEYS */;
/*!40000 ALTER TABLE `permisos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto_especifico`
--

DROP TABLE IF EXISTS `producto_especifico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto_especifico` (
  `id_producto_especifico` int(11) NOT NULL AUTO_INCREMENT,
  `id_producto_general` int(11) DEFAULT NULL,
  `id_imagenes_especificas` varchar(5) DEFAULT NULL,
  `nombre` varchar(500) NOT NULL,
  `descripcion` varchar(1000) DEFAULT NULL,
  `precio` decimal(5,2) DEFAULT NULL,
  `detalles` varchar(1000) DEFAULT NULL,
  `cantidad` int(11) NOT NULL,
  `activo` tinyint(1) DEFAULT NULL,
  `id_talla` int(11) DEFAULT NULL,
  `id_color` int(11) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `ultima_modificacion` datetime DEFAULT NULL,
  PRIMARY KEY (`id_producto_especifico`),
  KEY `id_producto_general` (`id_producto_general`),
  KEY `id_talla` (`id_talla`),
  KEY `id_color` (`id_color`),
  CONSTRAINT `producto_especifico_ibfk_1` FOREIGN KEY (`id_producto_general`) REFERENCES `producto_general` (`id_producto_general`),
  CONSTRAINT `producto_especifico_ibfk_2` FOREIGN KEY (`id_talla`) REFERENCES `talla` (`id_talla`),
  CONSTRAINT `producto_especifico_ibfk_3` FOREIGN KEY (`id_color`) REFERENCES `color` (`id_color`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto_especifico`
--

LOCK TABLES `producto_especifico` WRITE;
/*!40000 ALTER TABLE `producto_especifico` DISABLE KEYS */;
INSERT INTO `producto_especifico` VALUES (1,11,NULL,'probando 12','asion',12.00,'sija',12,1,1,1,'2022-11-22 19:01:26',NULL),(2,11,NULL,'totopo','totopeado',14.52,'tata',1,1,1,1,'2022-11-28 18:55:56',NULL),(3,2,NULL,'prueba2','dsfgsf',123.00,'wqr',3214,1,1,2,'2022-11-28 21:25:17',NULL),(4,11,NULL,'prueba124523','asdf',123.00,'1234',2134,1,1,2,'2022-11-28 21:29:25',NULL),(5,11,NULL,'prueba2234','dsf',999.00,'sadg',234,1,1,1,'2022-11-28 21:29:49',NULL);
/*!40000 ALTER TABLE `producto_especifico` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto_general`
--

DROP TABLE IF EXISTS `producto_general`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto_general` (
  `id_producto_general` int(11) NOT NULL AUTO_INCREMENT,
  `id_categoria` int(11) NOT NULL,
  `nombre_general` varchar(500) NOT NULL,
  `descripcion_general` varchar(1000) DEFAULT NULL,
  `imagen` varchar(100) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `ultima_modificacion` datetime DEFAULT NULL,
  PRIMARY KEY (`id_producto_general`),
  KEY `id_categoria` (`id_categoria`),
  CONSTRAINT `producto_general_ibfk_1` FOREIGN KEY (`id_categoria`) REFERENCES `categoria_producto` (`id_categoria`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto_general`
--

LOCK TABLES `producto_general` WRITE;
/*!40000 ALTER TABLE `producto_general` DISABLE KEYS */;
INSERT INTO `producto_general` VALUES (2,1,'asfa','asfasf','cuidados_de_una_capibara_20185_orig.jpg',1,'2022-11-19 17:29:41',NULL),(3,2,'asafasfa','safasfasf','süßkartoffel.jpg',1,'2022-11-19 17:31:30',NULL),(4,3,'sfafgasfqwfqgf ','sadasfgawgawg','218389886_538453937574255_1587615102912411146_n.jpg',1,'2022-11-19 17:32:47',NULL),(5,4,'prueba','me esta','aaaaaaa.png',1,'2022-11-19 17:33:30',NULL),(6,1,'prueba3','probando','4668cde9cd518d8f5eb4869e3a3c02e4 (2).jpg',1,'2022-11-22 18:33:28',NULL),(7,4,'prueba4','asdf','full.Chipotle_Pepper.jpg',1,'2022-11-22 18:39:13',NULL),(8,3,'prueba9','asdfsdf','WhatsApp Image 2021-10-08 at 14.10.54.jpeg',1,'2022-11-22 18:52:40',NULL),(9,3,'prueba90','asdf','5a35bd334d1c24.8884491715134712833159.png',1,'2022-11-22 18:54:29',NULL),(10,2,'prueba166','asdf','2002d200d004a9e19a9bd816ad3c0450.jpg',1,'2022-11-22 18:55:36',NULL),(11,2,'prueba189','dsaf','778082433a4b32f900dd985d8b0f61ad.jpg',1,'2022-11-22 18:57:24',NULL),(12,2,'Angie','Angie','ezgif.com-gif-maker.gif',1,'2022-11-28 01:47:58',NULL);
/*!40000 ALTER TABLE `producto_general` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `talla`
--

DROP TABLE IF EXISTS `talla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `talla` (
  `id_talla` int(11) NOT NULL AUTO_INCREMENT,
  `talla` varchar(5) NOT NULL,
  PRIMARY KEY (`id_talla`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `talla`
--

LOCK TABLES `talla` WRITE;
/*!40000 ALTER TABLE `talla` DISABLE KEYS */;
INSERT INTO `talla` VALUES (1,'S');
/*!40000 ALTER TABLE `talla` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `idusuarios` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `apellido1` varchar(255) NOT NULL,
  `apellido2` varchar(255) DEFAULT NULL,
  `permiso` bit(1) DEFAULT NULL,
  `contrasena` varchar(255) NOT NULL,
  `correo` varchar(255) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  PRIMARY KEY (`idusuarios`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'Jared','Barojas','Alcantar',_binary '','stanloona','jaredbarojas90@gmail.com','indefinido'),(2,'Daniel','Espinoza','Bernal',_binary '','stanloona','daeb2222@gmail.com','indefinido'),(3,'danielespz','Espinoza','Bernal',NULL,'Danielito22','daeb2222@gmail.com','Daniel Antonio');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `venta`
--

DROP TABLE IF EXISTS `venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venta` (
  `id_venta` int(11) NOT NULL AUTO_INCREMENT,
  `costo` decimal(6,2) NOT NULL,
  `tnx_id` varchar(200) NOT NULL,
  `estado` varchar(50) NOT NULL,
  `fecha` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  `id_pedido` int(11) NOT NULL,
  PRIMARY KEY (`id_venta`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venta`
--

LOCK TABLES `venta` WRITE;
/*!40000 ALTER TABLE `venta` DISABLE KEYS */;
/*!40000 ALTER TABLE `venta` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-11-28 23:53:42
