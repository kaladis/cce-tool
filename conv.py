##
## conv.py
## Author: "kaladis"<kaladis@inf.in>
## Started on  Sat Apr 17 12:14:48 2010 kaladis
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



def grade(m):
    
    g = None
    if m >= 91.000000000000000 and m <=100.000000000000000: g = 'A1'
    if m >= 81.000000000000000 and m <=90.999999999999999: g = 'A2'

    if m >= 71.000000000000000 and m <=80.999999999999999: g = 'B1'
    if m >= 61.000000000000000 and m <=70.999999999999999: g = 'B2'

    if m >= 51.000000000000000 and m <=60.999999999999999: g = 'C1'
    if m >= 41.000000000000000 and m <=50.999999999999999: g = 'C2'
    if m >= 33.000000000000000 and m <=40.999999999999999: g = 'D'
    
    if m >= 21.000000000000000 and m <=32.999999999999999: g = 'E1'
    
    if m >= 0.0000000000000000 and m <=20.999999999999999: g = 'E2'
    
    return g

def tocent(m,o):
    return round((100.0*m)/o)

def toten(m,o): 
    return tocent(m,o)/10

contri = {}
contri['fa1'] = 10.0
contri['fa2'] = 10.0
contri['fa3'] = 10.0
contri['fa4'] = 10.0
contri['sa1'] = 20.0
contri['sa2'] = 40.0

def getContri(asmt,forten):
    return (contri[asmt]*forten)/10




#     if m >= 9.1 and m <=10.0: g = 'A1'
#     if m >= 8.1 and m <=9.0: g = 'A2'

#     if m >= 7.1 and m <=8.0: g = 'B1'
#     if m >= 6.1 and m <=7.0: g = 'B2'
    
#     if m >= 5.1 and m <=6.0: g = 'C1'
#     if m >= 4.1 and m <=5.0: g = 'C2'
#     if m >= 3.3 and m <=4.0: g = 'D'
#     if m >= 2.1 and m <=3.2: g = 'E1'
#     if m >= 0.0 and m <=2.0: g = 'E2
