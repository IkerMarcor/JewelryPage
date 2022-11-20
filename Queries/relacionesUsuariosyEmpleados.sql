CREATE TABLE empleados(
	id_empleado int not null auto_increment,
    username varchar(100) not null,
    contrasena varchar(100) not null,
    correo varchar(100) not null,
    nombre varchar(255) not null,
    apellido1 varchar(255) not null,
    apellido2 varchar(255) null,
    id_permiso tinyint(1) not null,
    primary key(id_empleado),
    FOREIGN KEY (id_permiso) REFERENCES permisos(id_permiso)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE permisos(
	id_permiso int not null auto_increment,
    permiso varchar(50) not null,
    descripcion varchar(500) not null
)ENGINE= InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE empleados 