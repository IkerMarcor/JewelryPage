USE finkies;
#producto general
CREATE TABLE imagenes_especificas(	
	id_imagen_especifica int not null auto_increment,
    id_producto_especifico int,
    imagen varchar(100) not null,
    primary key(id_imagen_especifica),
    foreign key (id_producto_especifico) references producto_especifico(id_producto_especifico)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE producto_general(
	id_producto_general int not null auto_increment,
	id_categoria int not null,
    nombre_general varchar(500) not null,
    descripcion_general varchar(1000),
    imagen varchar(100) not null,
    activo bool not null,
    fecha_creacion datetime DEFAULT CURRENT_TIMESTAMP,
    ultima_modificacion datetime,
    primary key(id_producto_general),
    foreign key (id_categoria) references categoria_producto(id_categoria)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

#color
CREATE TABLE color(
	id_color int not null auto_increment,
    color varchar(25) not null,
    primary key(id_color)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

#talla
CREATE TABLE talla(
	id_talla int not null auto_increment,
    talla varchar(5) not null,
    primary key(id_talla)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

#producto especifico
CREATE TABLE producto_especifico(
	id_producto_especifico int not null auto_increment,
    id_producto_general int,
    id_imagenes_especificas varchar(5),
    nombre varchar(500) not null,
    descipcion varchar(1000),
    precio decimal(5,2),
    detalles varchar(1000),
    cantidad int not null,
	activo bool,
    id_talla int,
    id_color int,
    fecha_creacion datetime DEFAULT CURRENT_TIMESTAMP,
    ultima_modificacion datetime,
    primary key(id_producto_especifico),
    foreign key (id_producto_general) references producto_general(id_producto_general),
    foreign key (id_talla) references talla(id_talla),
    foreign key (id_color) references color(id_color)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;