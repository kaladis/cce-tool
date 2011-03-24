##
## model.py
## Author: "Kaladis"<kaladis@inf.in>
## Started on  Sun Aug 15 14:13:52 2010 kaladis
## $Id$
## 
## Copyright (C) 2010 INFORMEDIA
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
## 
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##
import web,re
db = web.database(dbn='sqlite',db='db.sqlite')

asmts={}
asmts['fa1'] = {'fields': ('fa1_m','fa1_o','fa1_g','fa1_p'),
                'names': ('FA1 MARKS','FA1 MAX','FA1 GRADE','FA1 PER')}

asmts['fa2'] = {'fields': ('fa2_m','fa2_o','fa2_g','fa2_p'),
                'names' : ('FA2 MARKS','FA2 MAX','FA2 GRADE','FA2 PER')}

asmts['fa3'] = {'fields': ('fa3_m','fa3_o','fa3_g','fa3_p'),
                'names' : ('FA3 MARKS','FA3 MAX','FA3 GRADE','FA3 PER')}

asmts['fa4'] = {'fields': ('fa4_m','fa4_o','fa4_g','fa4_p'),
                'names' : ('FA4 MARKS','FA4 MAX','FA4 GRADE','FA4 PER')}

asmts['sa1'] = {'fields': ('sa1_m','sa1_o','sa1_g','sa1_p'),
                'names' : ('SA1 MARKS','SA1 MAX','SA1 GRADE','SA1 PER')}

asmts['sa2'] = {'fields': ('sa2_m','sa2_o','sa2_g','sa2_p'),
                'names' : ('SA2 MARKS','SA2 MAX','SA2 GRADE','SA2 PER')}

asmts['t1'] = {'fields': (asmts['fa1']['fields'] + asmts['fa2']['fields'] + asmts['sa1']['fields']) ,
               'names':(asmts['fa1']['names'] + asmts['fa2']['names'] + asmts['sa1']['names']) }

asmts['t2'] = {'fields':(asmts['fa3']['fields'] + asmts['fa4']['fields'] + asmts['sa2']['fields']) ,
               'names':(asmts['fa3']['names'] + asmts['fa4']['names'] + asmts['sa1']['names']) }

asmts['all'] = {'fields':(asmts['t1']['fields'] + asmts['t2']['fields']),
                'names':(asmts['t1']['names'] + asmts['t2']['names'])}

def getStudentId(year,std,section,adnum,name):
    sql = "select count(*) as count from students where admission_num ='%s' "
    count = db.query(sql % adnum)
    if count[0]['count'] == 0:
        return addStudent(adnum,name)
    else:
        sql = "select id from students where admission_num = '%s'"
        return db.query(sql % adnum)[0]['id']
    
def addStudent(adnum,name):
    sql = "insert into students(admission_num,name) values ('%s','%s')"
    db.query(sql % (adnum,name))
    sql = "select last_insert_rowid() as id"
    res = db.query(sql)
    return res[0]['id']

def getMarkId(studentid,sub,year,std,section):
    sql = """select count(*) as count from marks 
             where student_id = %d and subject = '%s' and ac_year = '%s'
             and std = '%s' and section = '%s' """
    count = db.query(sql % (studentid,sub,year,std,section))
    if count[0]['count'] == 0:
        return addMark(studentid,sub,year,std,section)
    else:
        sql = """select id from marks 
                 where student_id = %d and subject = '%s' and ac_year = '%s'
                 and std = '%s' and section = '%s'"""
        return db.query(sql % (studentid,sub,year,std,section))[0]['id']
    
def addMark(studentid,sub,year,std,section):
    sql = "insert into marks(student_id,subject,ac_year,std,section) values(%d,'%s','%s','%s','%s')" 
    db.query(sql % (studentid,sub,year,std,section))
    sql = "select last_insert_rowid() as id"
    res = db.query(sql)
    return res[0]['id']

def updateMark(markid,fields,data):
    sql = "update marks set "
    c = len(fields)
    count = 1
    for f in fields:
        if f.split('_')[1] == 'g':
            sql += f+" = '%s' "
        else:
            sql += f+' = %0.1f '
        if count < c:
            sql +=', '
        count = count+1
    sql += " where id = %d"
    db.query(sql %(data[0],data[1],data[2],data[3],markid))
    return True

def isMarkThere(sub,year,std,sec):
    sql = """ select count(*) as count from marks 
              where subject = '%s'
              and ac_year = '%s'
              and std = '%s'
              and section = '%s' """
    count = db.query(sql % (sub,year,std,sec))
    if count[0]['count'] > 0:
        return True
    else:
        return False
              
def getMarks(sub,year,std,sec,astm):
    fields = asmts[astm]['fields']
    sql = """ select marks.id as markid,marks.subject, marks.ac_year as year, marks.std, marks.section,students.name,students.id, %s 
              from marks,students
              where subject = '%s'
              and ac_year = '%s'
              and std = '%s'
              and section = '%s' 
              and marks.student_id = students.id"""
    
    res = db.query(sql % ( ','.join(fields),sub,year,std,sec))
    return res

def getMarksByMarkId(id):
    sql = "select * from marks where id = %d"
    res = db.query(sql % id)
    return res[0]

def getReports():
    sql = """select subject,ac_year as year,std,section from marks group by subject,ac_year,std,section """
    res = db.query(sql)
    return res

def getAsmtMarksById(id):
    sql = """select marks.id, marks.student_id, marks.subject,marks.ac_year as year, marks.std, marks.section, marks.fa1_m,marks.fa1_o, marks.fa2_m,marks.fa2_o, marks.sa1_m,marks.sa1_o, marks.fa3_m, marks.fa3_o,marks.fa4_m, marks.fa4_o, marks.sa2_m, marks.sa2_o,students.name from marks,students where marks.id = %d and marks.student_id = students.id"""
    res = db.query(sql % id)
    return res

def getAllReports():
    sql = """ select ac_year as year, section, subject from marks group by ac_year, section, subject """
    res = db.query(sql)
    return res

def delMarks(year,sec,sub):
    sql = """ delete from marks where ac_year ='%s' and section = '%s' and subject = '%s' """
    count = db.query(sql % (year,sec,sub))
    return count

def getStudents(year,std,sec):
    sql = """ select marks.student_id,students.name from marks,students where marks.ac_year = '%s' and marks.std = '%s' and marks.section = '%s' group by marks.student_id order by students.name;"""
    res = db.query(sql % (year,std,sec))
    return res

def getStudentMarks(id,sub):
    sql = """ select marks.id,students.name,%s from marks,students where students.id = %d and marks.subject ='%s' and students.id = marks.student_id """
    fields = asmts['all']['fields']
    res = db.query(sql % (','.join(fields),int(id),sub))
    return res
