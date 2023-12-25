--
-- Файл сгенерирован с помощью SQLiteStudio v3.4.4 в Вт ноя 21 23:59:32 2023
--
-- Использованная кодировка текста: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: products_productcategory
CREATE TABLE IF NOT EXISTS "products_productcategory" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(128) NOT NULL UNIQUE, "description" text NULL);
INSERT INTO products_productcategory (id, name, description) VALUES (1, 'Одежда', 'Описание для одежды');
INSERT INTO products_productcategory (id, name, description) VALUES (2, 'Новинки', '');
INSERT INTO products_productcategory (id, name, description) VALUES (3, 'Обувь', '');
INSERT INTO products_productcategory (id, name, description) VALUES (4, 'Аксессуары', '');
INSERT INTO products_productcategory (id, name, description) VALUES (5, 'Подарки', '');

-- Индекс: sqlite_autoindex_products_productcategory_1
CREATE UNIQUE INDEX IF NOT EXISTS sqlite_autoindex_products_productcategory_1 ON products_productcategory (name COLLATE BINARY);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
