CREATE SCHEMA IF NOT EXISTS "content";
ALTER ROLE admin SET search_path TO content,public;
SET search_path TO content,public;


ALTER TABLE IF EXISTS "content".direction
    DROP CONSTRAINT curator_fk;

DROP TABLE IF EXISTS "content".direction_discipline;
DROP TABLE IF EXISTS "content".student;
DROP TABLE IF EXISTS "content".discipline;
DROP TABLE IF EXISTS "content".class;
DROP TABLE IF EXISTS "content".direction;



-- EDUCATION

CREATE TABLE "content".direction (
    id uuid PRIMARY KEY,
    name varchar(100) NOT NULL,
    description text NOT NULL,
    curator_fk int NOT NULL
);

CREATE TABLE "content".discipline(
    id uuid PRIMARY KEY,
    name varchar(100) NOT NULL,
    description text NOT NULL
);

CREATE TABLE "content".direction_discipline(
    id uuid PRIMARY KEY,
    direction_fk uuid NOT NULL,
    discipline_fk uuid NOT NULL
);

-- STUDENT

CREATE TABLE "content".class (
    id uuid PRIMARY KEY,
    number serial NOT NULL,
    direction_fk  uuid NOT NULL
);

CREATE TABLE "content".student (
    id uuid PRIMARY KEY,
    first_name varchar(30) NOT NULL,
    last_name varchar(30) NOT NULL,
    patronymic varchar(30) NOT NULL,
    email varchar(30) UNIQUE NOT NULL,
    tel_number varchar(30) UNIQUE NOT NULL,
    class_fk uuid NOT NULL
);

ALTER TABLE direction
    ADD CONSTRAINT curator_fk FOREIGN KEY (curator_fk)
        REFERENCES auth_user(id);

ALTER TABLE direction_discipline
    ADD CONSTRAINT direction_fk FOREIGN KEY (direction_fk)
        REFERENCES direction(id) ON DELETE CASCADE;
ALTER TABLE direction_discipline
    ADD CONSTRAINT discipline_fk FOREIGN KEY (discipline_fk)
        REFERENCES discipline(id) ON DELETE CASCADE;
ALTER TABLE direction_discipline
    ADD CONSTRAINT category_feature_uk UNIQUE (direction_fk, discipline_fk);


ALTER TABLE class
    ADD CONSTRAINT direction_fk FOREIGN KEY (direction_fk)
        REFERENCES direction(id) ON DELETE CASCADE;

ALTER TABLE student
    ADD CONSTRAINT class_fk FOREIGN KEY (class_fk)
        REFERENCES class(id) ON DELETE CASCADE;
-- todo: подумать как сделать ограничение на группу (не более 20 студентов в группе)
