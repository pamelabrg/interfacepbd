CREATE DATABASE trabalho_final;
USE trabalho_final;

create table Modulo (
	codModulo int auto_increment primary key,
	marcaModulo char(15),
    potModulo int,
    modeloModulo char(15)
);

create table Inversor (
	codInversor int auto_increment primary key,
    marcaInversor char(15),
    potInversor int,
    modeloInversor char(25)
);

create table Vendedor (
	idVendedor int not null auto_increment primary key,
    pnomeVendedor char(15) not null,
    mnomeVendedor char(15) not null,
    unomeVendedor char(15)
    );

create table Cliente (
	cpf char(11) primary key,
	pnomeCliente char(15) not null,
    mnomeCliente char(15) not null,
    unomeCliente char(15),
    email varchar(100),
    telefone char(11),
    endereco varchar(100)
);


create table Venda (
	idVenda int not null auto_increment primary key,
    valor float(10,2),
    dataVenda date,
    idVendedor int,
    cpf char(11)
    );
alter table Venda add foreign key (idVendedor) references Vendedor(idVendedor)
	on delete set null
    on update cascade;
    
alter table Venda add foreign key (cpf) references cliente(cpf)
	on delete cascade
    on update cascade;

create table Engenheiro (
	crea char (10) primary key,
    pnomeEng char (15) not null,
    mnomeEng char (15) not null,
    unomeEng char (15),
    telefoneEng char(11)
);

create table Concessionaria (
	idConcessionaria int primary key,
	nome char(100),
    contato char(100)
);

create table projeto (
	idProjeto int not null auto_increment primary key,
    potencia int not null,
    dataInstalacao date,
    idConcessionaria int default '1',
    tipoLigacao char(10),
    ucGeradora char(15) unique,
    idVenda int not null,
    crea char(10)
);

alter table Projeto add foreign key (idConcessionaria) references Concessionaria(idConcessionaria)
	on delete set null
    on update cascade;

alter table Projeto add foreign key (crea) references Engenheiro (crea)
	on delete set null
    on update cascade;

alter table Projeto add foreign key (idVenda) references Venda (idVenda)
	on delete cascade
    on update cascade;

create table registroModulos (
	idProjeto int not null,
    codModulo int not null,
    qtdModulo int,
    constraint primary key(idProjeto, codModulo)
);

alter table registroModulos add foreign key (idProjeto) references Projeto(idProjeto)
	on delete cascade
	on update cascade;
);

alter table registroModulos add foreign key (codModulo) references Modulo(codModulo)
	on delete cascade
	on update cascade;
);

create table registroInversor (
	snInversor char(16) primary key,
    idProjeto int,
    codInversor int,
    qtdInversor int
);

alter table registroInversor add foreign key(idProjeto) references Projeto(idProjeto)
	on delete cascade
	on update cascade;
);
alter table registroInversor add foreign key(codInversor) references Inversor(codInversor)
	on delete cascade
	on update cascade;
);

create table Monitoramento (
	login char(16) primary key,
    senha char(8) default'123456',
    plataforma char(12)
);

alter table Monitoramento add foreign key (login) references registroInversor(snInversor)
	on delete cascade
	on update cascade;
);


