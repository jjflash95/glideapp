import os
from services.employee_service import EmployeeService
from services.department_service import DepartmentService
from services.office_service import OfficeService


class Singleton(object):
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance


class Services(Singleton):
    def __init__(self):
        eservice = EmployeeService(os.getenv('EMPLOYEES_API'))
        dservice = DepartmentService(os.getenv('DEPARTMENTS_FILE'))
        oservice = OfficeService(os.getenv('OFFICES_FILE'))

        eservice.registerhook('manager', eservice.get)
        eservice.registerhook('department', dservice.get)
        eservice.registerhook('superdepartment', dservice.get)
        eservice.registerhook('office', oservice.get)

        self.services = {
            'employee': eservice,
            'department': dservice,
            'office': oservice,
        }

    def get(self, servicename):
        return self.services.get(servicename)
