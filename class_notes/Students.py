import datetime 

class Person(object):
    def __init__(self,name):
        '''Create a person'''
        self.name = name 
        try:
            lastBlank = name.rindex(" ")
            self.lastName = name[lastBlank+1:]
        except:
            self.lastName = None 
        self.birthday = None 
        
    def getName(self):
        '''Returns self's full name'''
        return self.name 
    
    def getLastName(self):
        '''Return self's last name'''
        return self.lastName

    def setBirthday(self,birthday):
        '''
        Assumes birthday is of type datetime.date
        sets self's birthday to birthday
        '''
        self.birthday = birthday
        
    def getAge(self):
        '''
        Returns self's current age in days
        '''
        if self.birthday == None:
            raise ValueError
        return (datetime.date.today() - self.birthday).days 
    
    def __lt__(self, other):
        '''
        Returns True if self's name is lexicographically
        less than other's name and false otherwise
        '''
        if self.lastName == other.lastName:
            return self.name < other.name
        return self.lastName < other.lastName

    def __str__(self):
        '''Return self's name'''
        return self.name
    
class IntSet(object):
    '''
    An intset is a set of integers
    '''
    # Information about the implementation (not the abstraction
    # The value of the set is represented by a list of ints, self.vals
    #Each int in the set occurs in self.vals exactly once
    
    def __init__(self):
        '''Create an empty set of integers'''
        self.vals = []
    
    def insert(self,e):
        '''Assumes e is an integer and inserts e into self'''
        if not e in self.vals:
            self.vals.append(e)
        
    def member(self,e):
        '''Assumes e is an integer
        Returns True if e is in self, and False otherwise'''
        return e in self.vals 
    
    def remove(self,e):
        '''
        Assumes e in an integer and removes e from self
        Raises ValueError if e is not in self
        '''
        try:
            self.vals.remove(e)
        except:
            raise ValueError(str(e)+' not found')
        
    def getMembers(self):
        '''
        Returns a list containing the elements of self
        Nothing can be assumed about the order of the elements
        '''
        return self.vals[:]
    
    def __str__(self):
        '''
        Returns a string representation of self
        '''
        self.vals.sort()
        result = ''
        for e in self.vals():
            result += str(e) + ','
        return '{' + result[:-1] + '}'

class MITPerson(Person):
    nextIdNum = 0 
    def __init__(self,name):
        Person.__init__(self,name)
        self.idNum = MITPerson.nextIdNum
        MITPerson.nextIdNum += 1
        
    def getIdNum(self):
        return self.idNum
    
    def __lt__(self,other):
        return self.idNum < other.idNum
    
    def isStudent(self):
        return isinstance(self, Student)
    
class Student(MITPerson):
    pass 

class UG(Student):
    def __init__(self, name, classYear):
        MITPerson.__init__(self,name)
        self.year = classYear
    
    def getClass(self):
        return self.year 
    
class Grad(Student):
    pass

class TransferStudent(Student):
    def __init__(self, name, from_school):
        MITPerson.__init__(self,name)
        self.from_school = from_school
        
    def getOldSchool(self):
        return self.from_school
    
class Grades(object):
    '''A mapping from students to a list of grades'''
    def __init__(self):
        '''Create empty grade book'''
        self.students = []
        self.grades = {}
        self.isSorted = True 
        
    def addStudent(self,student):
        '''
        Assumes: student is of type student
        Add student to the grade book
        '''
        if student in self.students:
            raise ValueError('Duplicate Student')
        self.students.append(student)
        self.grades[student.getIdNum()] = []
        self.isSorted = False 
        
    def addGrade(self, student, grade):
        '''Assumes: grade is a flot
        Add grade to the list of grades for student'''
        try: 
            self.grades[student.getIdNum()].append(grade)
        except:
            raise ValueError('Student not in mapping')
        
    def getGrades(self, student):
        '''Return a list of grades for student'''
        try:
            return self.grades[student.getIdNum()][:]
        except:
            raise ValueError('Student not in mapping')
        
    def getStudents(self):
        '''Return a list of students in the grade book'''
        if not self.isSorted:
            self.students.sort()
            self.isSorted = True
        for s in self.students:
            yield s
    
def gradeReport(course):
    '''Assumes course is of type grades'''
    report = ''
    for s in course.getStudents():
        tot = 0.0
        numGrades = 0
        for g in course.getGrades(s):
            tot += g 
            numGrades +=1 
        try:
            average = tot/numGrades
            report = report + '\n'\
                + str(s) + '\'s mean grade is ' + str(average)
        except ZeroDivisionError:
            report = report + '\n'\
                + str(s) + ' has not grades'
    return report 