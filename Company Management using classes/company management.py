import datetime
import csv

class Employee:
    '''Employee - basic class used for normal employees'''

    listOfWorkers = {}
    
    def __init__(self, ID, firstName, lastName, age, gender, numOfChildren, pay):
        '''
        ID - string with personal identification number
        firstName - string with name
        lastName - string with last name
        age - int with age
        gender - string with "Male" or "Female"
        numOfChildren - int with number of children
        pay - int with current month pay in $
        '''   
        self.ID = ID
        self.firstName = firstName
        self.lastName = lastName
        self.age = age
        self.gender = gender
        self.__numOfChildren = numOfChildren
        self.__pay = pay
        
        Employee.listOfWorkers.setdefault(self.ID ,self.fullName)
        

    @property
    def fullName(self):
        return '{} {}'.format(self.firstName, self.lastName)
    
    @property
    def email(self):
        return '{}.{}@company.com'.format(self.firstName, self.lastName).lower()

    @fullName.setter
    def fullName(self, name):
        '''Setter of fullName from string ex. "John Doe" '''
        firstName, lastName = name.split(' ')
        self.firstName = firstName
        self.lastName = lastName
        Employee.listOfWorkers[self.ID] = self.fullName   # updating list of workers
        print('Setting firstName to: {} and lastName to: {}'.format(self.firstName, self.lastName))
        
    @fullName.deleter
    def fullName(self):
        self.firstName = None
        self.lastName = None
        print('Changing firstName and lastName to "None" value')

    @staticmethod
    def isWorkingDay(year, month, day):
        '''Provide data in order: (year,month,day) as ints to check if day is working day'''
        dayToCheck = datetime.date(year, month, day)
        if dayToCheck.weekday() == 5 or dayToCheck.weekday() == 6:
            return False
        return True

    @property
    def showInfo(self):
        pattern = 'ID: {} ---> {} is {} years old {} with {} children and pay ${}/monthly. Contact: {}'
        print(pattern.format(self.ID, self.fullName, self.age, self.gender, self.__numOfChildren, self.__pay, self.email))
  
    def __str__(self):
        return "Employee: {}".format(self.fullName)
    
    def __add__(self, other):
        '''Allows to check sum pay of two employees'''
        return self.__pay + other.__pay


employee_01 = Employee('E001','Mark','Twain', 27, 'Male', 1, 5000)
employee_02 = Employee('E002','Susan','Smith', 35, 'Female', 0, 7000)
employee_03 = Employee('E003','Diana', 'Lenon', 30, 'Female', 2, 7500)
employee_04 = Employee('E004','John','Johnson',29,'Male', 1, 4000)
employee_05 = Employee('E005','Damian', 'Burris', 27, 'Male', 1, 4800)




# testing field for Employee class
employee_01.showInfo
del employee_01.fullName
print(employee_01)
employee_01.fullName = 'Martin Aston'
employee_01.showInfo
print('Is today a workday? : ', Employee.isWorkingDay(2022, 1, 25))
print("Summary pay of employee_01 and employee_02: ${}".format(employee_01 + employee_02))



class Programmer(Employee):
    
    
    def __init__(self, ID, firstName, lastName, age, gender, numOfChildren, pay, programmingLanguage, experienceYears):
        super().__init__(ID, firstName, lastName, age, gender, numOfChildren, pay)         
        '''
        programmingLanguage - string with main programming language
        experienceYears - int with years or experience in programming
        '''   
        self.programmingLanguage = programmingLanguage
        self.experienceYears = experienceYears
        self.listOfTasks = []
        
    @property
    def showInfo(self):
         super().showInfo
         print('Main programming language: {}, Experience: {} years'.format(self.programmingLanguage, self.experienceYears))
         print('Current tasks: ', self.listOfTasks)
         
    def bonusPayForEfficiency(self, bonusPay):
        '''additional money for most efective programmers, int in $'''
        self._Employee__pay += bonusPay
        print('Bonus ${} was added to Programmer: {}'.format(bonusPay, self.fullName))
        
    @classmethod
    def addProgrammerFromString(cls, ProgrammerStringData):
        '''Mathod allows user to create new instance based on string data'''
        ID,firstName, lastName, age, gender, numOfChildren, pay, programmingLanguage, experienceYears = ProgrammerStringData.split(',')
        age, _Employee__numOfChildren, _Employee__pay, experienceYears = int(age), int(numOfChildren), int(pay), int(experienceYears)
        return cls(ID, firstName, lastName, age, gender, _Employee__numOfChildren, _Employee__pay, programmingLanguage, experienceYears)
        
    def addTaskFromString(self, task):
        '''String with single task for worker'''
        self.listOfTasks.append(task)
        print('Task "{}" added to Programmer:{}'.format(task, self.fullName))
        
    def __str__(self):
        return "Programmer: {}".format(self.fullName)
        

programmer_01 = Programmer('P001','Alice','Smith', 40, 'Female', 3, 9000, 'Java', 1)
programmer_02 = Programmer('P002','Sara','Merson', 43, 'Female', 2, 9500, 'Python', 2)
programmer_03 = Programmer.addProgrammerFromString('P003,Tom,Klinsky,33,Male,0,10000,C++,4')
programmer_04 = Programmer.addProgrammerFromString('P004,Jerry,Fungen,33,Male,1,10500,Python,5')



# testing field of Programmer class
programmer_03.showInfo
programmer_03.bonusPayForEfficiency(777)
programmer_03.addTaskFromString('write documentation to project')
programmer_03.addTaskFromString('clean the windows')
del programmer_03.listOfTasks[-1]
programmer_03.showInfo



class Manager(Employee):
    
    def __init__(self,ID, firstName, lastName, age, gender, numOfChildren, pay, team = None):
        super().__init__(ID, firstName, lastName, age, gender, numOfChildren, pay)     
        if team is None:
            self.team = []
        else:
            self.team = team
    @property       
    def extra500ForBigTeam(self):
        '''additional money for Managers with teams above 4 people, int in $'''  
        teamSize = len(self.team)
        if teamSize >= 4:
            self._Employee__pay += 500
            print('Bonus $500 was added to Manager: {}'.format(self.fullName))
        else:
            print('Sorry, your team has only {} employees. You need at least 4 employees to achieve $500 bonus!'.format(teamSize))
            
    def addEmployeeToTeam(self, employee):
        if employee not in self.team:
            self.team.append(employee)
            print('[{}] added to your team!'.format(employee))
        else:
            print('Sorry, nothing happened... Worker already in team!')
            
    def removeEmployeeFromTeam(self, employee):
        if employee in self.team:
            self.team.remove(employee)
            print('[{}] deleted from your team!'.format(employee))
        else:
            print('Sorry, nothing happened... This employee was not in your team!')         
            
    @property
    def showInfo(self):
         super().showInfo
         print('Current team:')
         for employee in self.team:
             print(employee)

    def __str__(self):
        return "Manager: {}".format(self.fullName)

        
manager_01 = Manager('M001','Doris', 'Punchie', 37, 'Female', 2, 12000, [employee_01, employee_03, programmer_01, programmer_03])
manager_02 = Manager('M002','Sarah', 'Princeton', 39, 'Female', 1, 11500, [employee_02, employee_04, employee_05, programmer_04])
managers = [manager_01, manager_02]

# testing field of Programmer class
manager_01.addEmployeeToTeam(programmer_02)
manager_01.removeEmployeeFromTeam(employee_03)
manager_01.extra500ForBigTeam
manager_01.showInfo



class CEO(Employee):
    
    __possiblePayChange = [employee_02, employee_03, programmer_02, programmer_04, manager_01]
    '''list of worker with possible pay change this year'''
    
    def __init__(self,ID, firstName, lastName, age, gender, numOfChildren, pay):
            super().__init__(ID, firstName, lastName, age, gender, numOfChildren, pay)
    
    def removeEmployeeFromCompany(self, deletedEmployee):
        '''Deletes selected employee from team and listOfWorkers, but does not delete object'''
        print('Employee {} was fired!'.format(deletedEmployee.fullName))
        
        for manager in managers:
            for employee in manager.team:
                if employee.ID == deletedEmployee.ID:
                    manager.team.remove(employee)
  
        del self.listOfWorkers[deletedEmployee.ID]
     
    def changeEmployeePay(self, employee, changePay):
        '''Changes pay of chosen employee when employee is on __possiblePayChange list'''
        if employee in self.__possiblePayChange:
            employee._Employee__pay += changePay
            print('Pay of {} changed: {:^+5.2f}$ ---> Pay now: ${}'.format(employee.fullName, changePay, employee._Employee__pay))
        else:
            print('Changing pay of {} is not possible now!'.format(employee.fullName))
    
    def __str__(self):
        return "CEO: {}".format(self.fullName)


ceo = CEO('!CEO!', ' Harry', 'Tacher', 50, 'Male', 2, 20000)


def exportToFileAllEmployees(path):
    '''outer function to export to csv file'''        
    with open (path, mode = 'w') as file:
        writer = csv.writer(file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        writer.writerow(['ID,fullName'])
        for ID, fullName in Employee.listOfWorkers.items():
            writer.writerow([ID, fullName])

           
ceo.exportToFileAllEmployees_static = exportToFileAllEmployees   # assigning outer function as the static method of instance         

# testing field for Boss class
ceo.removeEmployeeFromCompany(employee_01)
del employee_01
ceo.changeEmployeePay(employee_02, 400)
ceo.changeEmployeePay(programmer_01, 600) 
ceo.exportToFileAllEmployees_static(r'F:\DataScience\sth.csv')  

# printing all workers in company
for person, x in Employee.listOfWorkers.items():  
    print(person, x)







