CREATE DATABASE wpchannelbot;
USE wpchannelbot;

CREATE TABLE channel (
	id varchar(30),
	nome varchar(300),
	cidade varchar(300),
	bairro varchar(300)
);

CREATE TABLE convs (
	id varchar(30)
);

CREATE TABLE convs_state (
	id varchar(30),
	etapa int
);
