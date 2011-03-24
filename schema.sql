CREATE TABLE students (
       id integer PRIMARY KEY AUTOINCREMENT,
       admission_num character(5),
       name character(255)
       );

CREATE TABLE subjects (
             id integer PRIMARY KEY AUTOINCREMENT,
             name character(100)
       );
       
create table sections (
             id integer PRIMARY KEY AUTOINCREMENT,
             name character(2)
       );

CREATE TABLE marks (
       id integer PRIMARY KEY AUTOINCREMENT,
       student_id integer,
       subject character(20),
       ac_year character(10),
       std character(2),
       section character(2),
       
       fa1_m real,
       fa1_o real,
       fa1_g character(5),
       fa1_p real,
             
       fa2_m real,
       fa2_o real,
       fa2_g character(5),
       fa2_p real,
       
       fa12_p real,
       
       sa1_m real,
       sa1_o real,
       sa1_g character(5),
       sa1_p real,
       
       t1_p real,
              
       fa3_m real,
       fa3_o real,
       fa3_g character(5),
       fa3_p real,
       
       fa4_m real,
       fa4_o real,
       fa4_g character(5),
       fa4_p real,
       fa34_p real,
       
       sa2_m real,
       sa2_o real,
       sa2_g character(5),
       sa2_p real,
       
       t2_p real
       );