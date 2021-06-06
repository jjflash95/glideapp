from services.employee_service import EmployeeService
from services.department_service import DepartmentService
from services.office_service import OfficeService


class Services:
    def __init__(self):

        eservice = EmployeeService()
        dservice = DepartmentService()
        oservice = OfficeService()

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
