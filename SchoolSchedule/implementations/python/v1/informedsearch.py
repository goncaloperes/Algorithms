'''

High school timetabling using Genetic Algorithm

Algorithm Overview
----------------------
    initialize()
    While improvement:
        // Try to change all lesson
        for L1 in lesson_list for L2 in lesson_list
            try_to_change_lessons(L1, L2)
            if there are improvement:
                improvement = true
    
        // Try to change lessons of one teacher
        for t in teacher_list for L1 in lesson_list for l2 in lesson_list
            try_to_change_teacher_lesson(t, L1, L2)
            if there are improvement:
                improvement = true
    
        // Try to change lessons of one class
        for c in class_list for L1 in lesson_list for l2 in lesson_list
            try_to_change_class_lesson(t, L1, L2)
            if there are improvement:
                improvement = true
        
    print result
-------------------------

In the algorithm, the panelty of the state is calculated by the following:
    (the number of over-lessons where the teacher has more than 4 lessons + 
    the number of over-lessons where the class has more than 4 lessons + 
    the number of same pair Class/Teacher in one day) * 100 + 
    the number of holes
    
So if there are improvement, this panelty is smaller than before

'''

import numpy as np
from copy import deepcopy

""" check if this day is hole """
def holes(v, flag):
    s = 0
    cnt = 0
    for i in range(6):
        if v[i] >= 0:
            cnt = cnt + 1
        if i > 0 and v[i] >= 0 and v[i-1] == -1:
            s = s + 1
    if cnt == 1:
        s = s + 1
    if flag:
        return s > 0
    else:
        return s

""" get the number of holes of this class or teacher """
def getholes(v, flag):
    s = 0
    for i in range(5):
        s = s + holes(v[i], flag)
    return s
    

class state:
    
    """ init class """
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.T = np.zeros((n, 5, 6), int) - 1
        self.C = np.zeros((m, 5, 6), int) - 1
        
    """ get copy of this class """
    def copy(self):
        a = state(self.n, self.m)
        a.n = self.n
        a.m = self.m
        a.T = self.T.copy()
        a.C = self.C.copy()
        return a
        
    """ set lesson to the state 
        c is class
        t is teacher
        d is day
        l is lesson on the day
    """
    def setLesson(self, c, t, d, l):
        if self.T[t][d][l] >= 0:
            return False
        if self.C[c][d][l] >= 0:
            return False
        self.T[t][d][l] = c
        self.C[c][d][l] = t
        return True
        
    """ try to change all lessons """ 
    
    def tryToChangeLesson(self, d1, l1, d2, l2):
        #print(d1, l1, d2, l2)
        for i in range(m):
            self.C[i][d1][l1], self.C[i][d2][l2] = self.C[i][d2][l2], self.C[i][d1][l1]
        for i in range(n):
            self.T[i][d1][l1], self.T[i][d2][l2] = self.T[i][d2][l2], self.T[i][d1][l1]
        return True
    
    """ try to change two lessons of the teacher
        t is teacher
        d1, l1 is the first lesson
        d2, l2 is the second lesson
    """ 
    def tryToChangeTeacher(self, t, d1, l1, d2, l2):
        c1 = self.T[t][d1][l1]
        c2 = self.T[t][d2][l2]
        
        
        if c2 >= 0 and self.C[c2][d1][l1] >= 0: # we can't change this pair if lesson because there are some lessons for the class c1
            return False
        if c1 >= 0 and self.C[c1][d2][l2] >= 0: # we can't change this pair if lesson because there are some lessons for the class c2
            return False
        
        if c1 >= 0:
            self.C[c1][d1][l1] = -1
        if c2 >= 0:
            self.C[c2][d2][l2] = -1
        self.T[t][d1][l1], self.T[t][d2][l2] = self.T[t][d2][l2], self.T[t][d1][l1]
        
        if c1 >= 0:
            self.C[c1][d2][l2] = t
        if c2 >= 0:
            self.C[c2][d1][l1] = t
        return True
        
    def tryToChangeClass(self, c, d1, l1, d2, l2):
        t1 = self.C[c][d1][l1]
        t2 = self.C[c][d2][l2]
        if t2 >= 0 and self.T[t2][d1][l1] >= 0:
            return False
        if t1 >= 0 and self.T[t1][d2][l2] >= 0:
            return False
        
        if t1 >= 0:
            self.T[t1][d1][l1] = -1
        if t2 >= 0:
            self.T[t2][d2][l2] = -1
        self.C[c][d1][l1], self.C[c][d2][l2] = self.C[c][d2][l2], self.C[c][d1][l1]
        
        if t1 >= 0:
            self.T[t1][d2][l2] = c
        if t2 >= 0:
            self.T[t2][d1][l1] = c
        return True
            
    def panelty(self, flag = False):
        
        paneltyA = 0
        paneltyB = 0
        T = self.T
        C = self.C
        paneltyA = ((T >= 0).sum(axis = 2) - 4).clip(min=0).sum() + ((C >= 0).sum(axis = 2) - 4).clip(min=0).sum()
        for t in range(n):
            for d in range(5):
                for i in range(5):
                    for j in range(i + 1, 6):
                        if T[t][d][i] >= 0 and T[t][d][i] == T[t][d][j]:
                            paneltyB = paneltyB + 1
        
        for c in range(m):
            for d in range(5):
                for i in range(5):
                    for j in range(i + 1, 6):
                        if C[c][d][i] >= 0 and C[c][d][i] == C[c][d][j]:
                            paneltyB = paneltyB + 1
                            
        panelty = (paneltyA + paneltyB) * 100 + self.holes(flag)
        
        return panelty
    
    def holes(self, flag):
        s = 0
        for i in range(n):
            s = s + getholes(self.T[i], flag)
        for i in range(m):
            s = s + getholes(self.C[i], flag)
        return s
    
    def __copy__(self):
        self.normalizeArgs()
        return state()
        

    def print(self):
        print("Classes:")
        for i in range(m):
            s = "T" + chr(ord('A') + i)
            for j in range(5):
                s = s + " | "
                for k in range(6):
                    c = '.' if self.C[i][j][k] == -1 else chr(ord('A') + self.C[i][j][k])
                    s = s + c
            print(s)
        print("Teachers:")
        for i in range(n):
            s = "P" + chr(ord('A') + i)
            for j in range(5):
                s = s + " | "
                for k in range(6):
                    c = '.' if self.T[i][j][k] == -1 else chr(ord('A') + self.T[i][j][k])
                    s = s + c
            print(s)
            
                    
            
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--data', metavar = ': input file', type = str,help = 'input file for this problem', default='he12t9p2a20s.txt')
args = parser.parse_args()

input_file = open(args.data, 'r')  


m, n = map(int, input_file.readline().split(","));
l = np.zeros((m, n), int)
for line in input_file:
    p, q, r = map(int, line.split(","))
    l[p][q] = r
    
S = state(n, m)
for i in range(m):
    for j in range(n):
        c = l[i][j]
        for p in range(5):
            for q in range(6):
                if c > 0 and S.setLesson(i, j, p, q):
                    c = c - 1
        if c != 0:
            print("Error initialize:", i, j, c)

panelty = S.panelty()

while True:
    improved = False
    minS = S.copy()
    for l in range(30):
        for l1 in range(l + 1, 30):
            S1 = S.copy()
            if S1.tryToChangeLesson(int(l / 6), l % 6, int(l1 / 6), l1 % 6):
                if S1.panelty() < panelty:
                    panelty = S1.panelty()
                    improved = True
                    minS = S1.copy()
    
    for c in range(m):
        for l in range(30):
            for l1 in range(l + 1, 30):
                S1 = S.copy()
                if S1.tryToChangeClass(c, int(l / 6), l % 6, int(l1 / 6), l1 % 6) and S1.panelty() < panelty:
                    panelty = S1.panelty()
                    improved = True
                    minS = S1.copy()
    for t in range(n):                    
        for l in range(30):
            for l1 in range(l + 1, 30):
                S1 = S.copy()
                if S1.tryToChangeTeacher(t, int(l / 6), l % 6, int(l1 / 6), l1 % 6) and S1.panelty() < panelty:
                    panelty = S1.panelty()
                    improved = True
                    minS = S1.copy()
                
    S = minS
    if improved == False:
        break
   
S.print()
print(S.panelty(True))