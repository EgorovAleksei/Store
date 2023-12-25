--
-- Файл сгенерирован с помощью SQLiteStudio v3.4.4 в Ср ноя 22 00:01:55 2023
--
-- Использованная кодировка текста: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: products_product
CREATE TABLE IF NOT EXISTS "products_product" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(256) NOT NULL, "description" text NOT NULL, "price" decimal NOT NULL, "quantity" integer unsigned NOT NULL CHECK ("quantity" >= 0), "image" varchar(100) NOT NULL, "category_id" bigint NOT NULL REFERENCES "products_productcategory" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO products_product (id, name, description, price, quantity, image, category_id) VALUES (1, 'Худи черного цвета с монограммами adidas Originals', 'Мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни.', 6090, 10, 'products_images/Adidas-hoodie.png', 1);
INSERT INTO products_product (id, name, description, price, quantity, image, category_id) VALUES (2, 'Синяя куртка The North Face', 'Гладкая ткань. Водонепроницаемое покрытие. Легкий и теплый пуховый наполнитель.', 23725, 15, 'products_images/Blue-jacket-The-North-Face.png', 2);
INSERT INTO products_product (id, name, description, price, quantity, image, category_id) VALUES (3, 'Коричневый спортивный oversized-топ ASOS DESIGN', 'Материал с плюшевой текстурой. Удобный и мягкий.', 3390, 20, 'products_images/Brown-sports-oversized-top-ASOS-DESIGN.png', 1);
INSERT INTO products_product (id, name, description, price, quantity, image, category_id) VALUES (4, 'Черный рюкзак Nike Heritage', 'Плотная ткань. Легкий материал.', 2340, 5, 'products_images/Black-Nike-Heritage-backpack.png', 4);
INSERT INTO products_product (id, name, description, price, quantity, image, category_id) VALUES (5, 'Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex', 'Гладкий кожаный верх. Натуральный материал.', 13590, 12, 'products_images/Black-Dr-Martens-shoes.png', 3);
INSERT INTO products_product (id, name, description, price, quantity, image, category_id) VALUES (6, 'Темно-синие широкие строгие брюки ASOS DESIGN', 'Легкая эластичная ткань сирсакер Фактурная ткань.', 2890, 25, 'products_images/Dark-blue-wide-leg-ASOs-DESIGN-trousers.png', 2);

-- Индекс: products_product_category_id_9b594869
CREATE INDEX IF NOT EXISTS "products_product_category_id_9b594869" ON "products_product" ("category_id");

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
