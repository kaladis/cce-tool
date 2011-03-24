##
## code.py
## Author: "Kaladis"<kaladis@inf.in>
## Started on  Fri Aug  6 16:51:41 2010 kaladis
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

import web,math,os,xlrd,conv,model,simplejson

from web import form

urls = (
    '/','index',
    '/upload', 'upload',
    '/marks','marks',
    '/markedit','markedit',
    '/reports', 'reports',
    '/delmarks', 'delmarks',
    '/stu', 'stu',
    '/stuview','stuview',
    )

app=web.application(urls,globals())

uploadform = form.Form (
    form.File('datafile'),
    # form.Dropdown('asmt',[('FA1','FA1'),('FA2','FA2'),('SA1','SA1'),('FA3','FA3'), ('FA4','FA4'), ('SA2','SA2')]),
    # form.Dropdown('year',[('2010-11','2010-11'),('2011-12','2011-12')]),
    # form.Dropdown('std',[('9','9'),('10','10')]),
    # form.Dropdown('section',[('A','A'),('B','B'),('C','C')]),
    # form.Dropdown('subject',[('Kannada','Kannada'),('Maths','Maths')]),
    # form.Textbox('per'),
    form.Button('Upload')
    )

marksform = form.Form(
    form.Dropdown('asmt',[('FA1','FA1'),('FA2','FA2'),('SA1','SA1'),('FA3','FA3'), ('FA4','FA4'), ('SA2','SA2'),('All','All')]),
    form.Dropdown('year',[('2010-11','2010-11'),('2011-12','2011-12')]),
    form.Dropdown('std',[('9','9'),('10','10')]),
    form.Dropdown('section',[('A','A'),('B','B'),('C','C')]),
    form.Dropdown('subject',[('Kannada','Kannada'),('Maths','Maths')]),
    form.Button('Submit')
    )

stuform = form.Form(
    form.Dropdown('year',[('2010-11','2010-11'),('2011-12','2011-12')]),
    form.Dropdown('std',[('9','9'),('10','10')]),
    form.Dropdown('section',[('A','A'),('B','B'),('C','C')]),
    form.Button('Submit')
    )

session=web.session.Session(app,web.session.DiskStore('sessions'),initializer={'logged':False})

render = web.template.render('templates/',
                             base="layout",
                             globals={'context':session},
                             )

class index:
    def __init__(self):
        pass
    def GET(self):
        return render.index()
    def POST(self):
        pass
    
class upload:
    def __init__(self): pass
    
    def GET(self):
        upform = uploadform()
        message = ''
        reports = model.getReports()
        return render.upload(message,upform,reports)
    def POST(self):
        disdir = os.path.join(os.getcwd(),'files')
        x= web.input(datafile={})
        
        # asmt = x.asmt.lower()
        # year = x.year
        # std = x.std
        # section = x.section
        # sub = x.subject
        # max = int(x.max)
        a = ('year','section','assessment','percent')

        if 'datafile' in x:
            filename = x.datafile.filename
            f = open(os.path.join(disdir,filename),'w')
            f.write(x.datafile.file.read())
            f.close()
            book = xlrd.open_workbook(os.path.join(disdir,filename))
            sheet = book.sheet_by_index(0)
            # print sheet
            for rownum in range(sheet.nrows):
                # if rownum == 0: continue
                row = sheet.row_values(rownum)
                if row[0].lower() == 'year':
                    year = row[0].lower()
                    continue
                if row[0].lower() == 'standard':
                    std = row[0].lower()
                    continue
                if row[0].lower() == 'section':
                    section = row[0].lower()
                    continue
                if row[0].lower() == 'assessment':
                    asmt = row[0].lower()
                    continue
                if row[0].lower() == 'percent':
                    per = row[0].lower()
                    continue
                if row[0].lower() == 'marks': continue
                if row[0].lower() == 'sl': continue
                name = row[1]
                adnum = row[2]
                english = float(row[3])
                seclang = float(row[4])
                maths = float(row[5])
                science = float(row[6])
                social = float(row[7])
                studentid = model.getStudentId(year,std,section,adnum,name)
                
                fields =  model.asmts[asmt]['fields']
                forten = conv.toten(mark,max)
                grade = conv.grade(conv.tocent(mark,max))
                per = conv.getContri(asmt,forten)
                data = [mark,max,grade,per]
                markid = model.getMarkId(studentid,sub,year,std,section)
                
                model.updateMark(markid,fields,data)
                
        raise web.seeother('/upload')

class marks:
    def __init__(self):
        pass
    
    def GET(self):
        mform= marksform()
        message = ''
        return render.marks(message,mform)
    
    def POST(self):
        form = marksform()
        q = web.input()
        render = web.template.render('templates/', base=None,globals={'context':session})
        if model.isMarkThere(q.subject,q.year,q.std,q.section) == False:
            return render.marksajax(None,None,None,None,None)

        marks = model.getMarks(q.subject,q.year,q.std,q.section,q.asmt.lower())
        field_names = model.asmts[q.asmt.lower()]['names']
        fields = model.asmts[q.asmt.lower()]['fields']
        asmt = q.asmt.lower()
        return render.marksajax(fields,field_names,marks,asmt)

class markedit:
    def __init__(self):
        pass
    def GET(self):
        q = web.input()
        render = web.template.render('templates/', base=None,globals={'context':session})
        mark = model.getAsmtMarksById(int(q.id))
        mark = mark[0]
        active= model.asmts[q.a]['fields'][0]
        return render.markedit(mark,active)
    
    def POST(self):
        q = web.input()
        markid = int(q.markid)
        marks = model.getMarksByMarkId(markid)
        ret = {}
        ret = {'fields':{},'id':0, 'status': False}
        render = web.template.render('templates/', base=None,globals={'context':session})
        
        if 'fa1_m' in q:
            fa1_m = float(q.fa1_m)
            forten = conv.toten(fa1_m,marks['fa1_o'])
            grade = conv.grade(conv.tocent(fa1_m,marks['fa1_o']))
            per = conv.getContri('fa1',forten)
            fields = model.asmts['fa1']['fields']
            data= [fa1_m,marks['fa1_o'],grade,per]
            model.updateMark(markid,fields,data)
            ret['fields'] = {'fa1_m':fa1_m,'fa1_g':grade,'fa1_p': per}
            ret['id'] = markid
            ret['status'] = True
            
        if 'fa2_m' in q:
            fa2_m = float(q.fa2_m)
            forten = conv.toten(fa2_m,marks['fa2_o'])
            grade = conv.grade(forten)
            per = conv.getContri('fa2',forten)
            fields = model.asmts['fa2']['fields']
            data = [fa2_m,marks['fa2_o'],grade,per]
            model.updateMark(markid,fields,data)
            ret['fields'] = {'fa2_m':fa2_m,'fa2_g':grade,'fa2_p': per}
            ret['id'] = markid
            ret['status'] = True
            
        if 'sa1_m' in q:
            sa1_m = float(q.sa1_m)
            forten = conv.toten(sa1_m,marks['sa1_o'])
            grade = conv.grade(forten)
            per = conv.getContri('sa1_m',forten)
            fields = model.asmts['sa1']['fields']
            data= [sa1_m,marks['sa1_o'],grade,per]
            model.updateMark(markid,fields,data)
            ret['fields'] = {'sa1_m':sa1_m,'sa1_g':grade,'sa1_p': per}
            ret['id'] = markid
            ret['status'] = True

        if 'fa3_m' in q:
            fa3_m = float(q.fa3_m)
            forten = conv.toten(fa3_m,marks['fa3_o'])
            grade = conv.grade(forten)
            per = conv.getContri('fa3_m',forten)
            fields = model.asmts['fa3']['fields']
            data= [fa3_m,marks['fa3_o'],grade,per]
            model.updateMark(markid,fields,data)
            ret['fields'] = {'fa3_m':fa3_m,'fa3_g':grade,'fa3_p': per}
            ret['id'] = markid
            ret['status'] = True
            
        if 'fa4_m' in q:
            fa4_m = float(q.fa4_m)
            forten = conv.toten(fa4_m,marks['fa4_o'])
            grade = conv.grade(forten)
            per = conv.getContri('fa4_m',forten)
            fields = model.asmts['fa4']['fields']
            data=[fa4_m,marks['fa4_o'],grade,per]
            model.updateMark(markid,fields,data)
            ret['fields'] = {'fa4_m':fa4_m,'fa4_g':grade,'fa3_p': per}
            ret['id'] = markid
            ret['status'] = True
            
        if 'sa2_m' in q:
            sa2_m = float(q.sa2_m)
            forten = conv.toten(sa2_m,marks['sa2_o'])
            grade = conv.grade(forten)
            per = conv.getContri('sa2_m',forten)
            fields = model.asmts['sa2']['fields']
            data= [sa2_m,marks['sa2_o'],grade,per]
            model.updateMark(markid,fields,data)
            ret['fields'] = {'sa2_m':fa4_m,'sa2_g':grade,'sa23_p': per}
            ret['id'] = markid
            ret['status'] = True
            
        web.header("Content-Type","text/json;charset=utf-8")
        return render.savemark(simplejson.dumps(ret))

class reports:
    def __init__(self):
        pass
    def GET(self):
        reports = model.getAllReports()
        return render.reports(reports)
    
class delmarks:
    def __init__(self):
        pass
    def GET(self):
        q = web.input()
        ret = {}
        ret['done'] = False
        count = model.delMarks(q.year,q.sec,q.sub)
        if count > 0:
            ret['done'] = True
            ret['count'] = count
            
        render = web.template.render('templates/', base=None,globals={'context':session})
        web.header("Content-Type","text/json;charset=utf-8")
        return render.delmarks(simplejson.dumps(ret))
    
class stu:
    def __init__(self):
        pass
    def GET(self):
        sform = stuform()
        return render.stu(sform)
    def POST(self):
        q = web.input()
        students = model.getStudents(q.year,q.std,q.section)
        render = web.template.render('templates/', base=None,globals={'context':session})
        return render.stuajax(students)
    
class stuview:
    def __init__(self):
        pass
    def GET(self):
        q = web.input()
        marks = model.getStudentMarks(q.id,q.sub)
        return render.stuviewajax(marks[0])
    def POST(self):
        pass
    
if __name__=='__main__': app.run()
