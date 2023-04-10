-- Syed Faquaruddin Quadri(24379388)

-- creating a database named MY_CUATOM_BOT
CREATE DATABASE MY_CUSTOM_BOT;
COMMIT;

-- stating which database to use
USE MY_CUSTOM_BOT;

-- creating a table named bing
-- columns:
-- search_id: unique id for every seacrh
-- search_query: query given by the user
-- link: url extracted from the search
-- raw_text: extracted text below the url
CREATE table bing (
	search_id int not null primary key auto_increment,
    search_query varchar(255),
    link varchar(300) null,
    title varchar(5000) null,
    raw_text varchar(10000) null
    );
commit;

-- creating a table named yahoo
-- columns:
-- search_id: unique id for every seacrh
-- search_query: query given by the user
-- link: url extracted from the search
-- raw_text: extracted text below the url
CREATE table yahoo (
	search_id int not null primary key auto_increment,
    search_query varchar(255),
    link varchar(300) null,
    title varchar(5000) null,
    raw_text varchar(10000) null
    );
commit;

-- creating a table named google
-- columns:
-- search_id: unique id for every seacrh
-- search_query: query given by the user
-- link: url extracted from the search
-- raw_text: extracted text below the url
CREATE table google (
	search_id int not null primary key auto_increment,
    search_query varchar(255),
    link varchar(300) null,
    title varchar(5000) null,
    raw_text varchar(10000) null
    );
commit;

-- creating a table named duckduckgo
-- columns:
-- search_id: unique id for every seacrh
-- search_query: query given by the user
-- link: url extracted from the search
-- raw_text: extracted text below the url
CREATE table duckduckgo (
	search_id int not null primary key auto_increment,
    search_query varchar(255),
    link varchar(300) null,
    title varchar(5000) null,
    raw_text varchar(10000) null
    );
commit;