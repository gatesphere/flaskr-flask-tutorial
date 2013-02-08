--@+leo-ver=5-thin
--@+node:peckj.20130208092851.1376: * @file schema.sql
--@@language plsql
drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title string not null,
  text string not null
);

--@-leo
