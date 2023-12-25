--
-- ���� ������������ � ������� SQLiteStudio v3.4.4 � �� ��� 21 23:59:32 2023
--
-- �������������� ��������� ������: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- �������: products_productcategory
CREATE TABLE IF NOT EXISTS "products_productcategory" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(128) NOT NULL UNIQUE, "description" text NULL);
INSERT INTO products_productcategory (id, name, description) VALUES (1, '������', '�������� ��� ������');
INSERT INTO products_productcategory (id, name, description) VALUES (2, '�������', '');
INSERT INTO products_productcategory (id, name, description) VALUES (3, '�����', '');
INSERT INTO products_productcategory (id, name, description) VALUES (4, '����������', '');
INSERT INTO products_productcategory (id, name, description) VALUES (5, '�������', '');

-- ������: sqlite_autoindex_products_productcategory_1
CREATE UNIQUE INDEX IF NOT EXISTS sqlite_autoindex_products_productcategory_1 ON products_productcategory (name COLLATE BINARY);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
