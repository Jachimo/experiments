#!/usr/bin/env python

# TriTek programming test implemented in Python 2.x

class Employee:
    """A simple employee class."""

    # used at class level only not on instances
    empCount = 0 

    # Constructor method
    def __init__(self, firstName, lastName):
        self.firstName = firstName
        self.lastName = lastName
        self.id = Employee.empCount
        Employee.empCount += 1
        self.sub = []
        self.mgr = []

    # setters
    def setmanager(self, manager):
        self.mgr.append(manager)
        manager.sub.append(self)
    
    def setsub(self, subordinate):
        self.sub.append(subordinate)
        subordinate.mgr.append(self)

    # print methods (getters)
    def printsubs(self):
        if self.sub:
            for s in self.sub:
                print s.firstName, s.lastName
    
    def printallsubs(self):
        if self.sub:
            for s in self.sub:
                print s.firstName, s.lastName
                s.printallsubs() # recurse

    def printmgrs(self):
        if self.mgr:
            for m in self.mgr:
                print m.firstName, m.lastName
                


# Test w/ 4 employees
joe = Employee("Joe", "Cool")
sam = Employee("Sam", "Smith")
frank = Employee("Frank", "Daboss")
lisa = Employee("Lisa", "Noob")

# Frank manages Joe and Sam; Joe manages Lisa
frank.setsub(joe)
frank.setsub(sam)
joe.setsub(lisa)

