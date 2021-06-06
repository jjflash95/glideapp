from flask import Flask
from flask import request
from flask import jsonify
from utils import bad_request, not_found, internal_error
from services.services import Services


app = Flask(__name__)
app.debug = True

DEFAULT_LIMIT = 100
DEFAULT_OFFSET = 0
MAX_LIMIT = 1000

services = Services()

app.register_error_handler(500, internal_error)
app.register_error_handler(400, bad_request)


@app.route("/api/employees")
def list_employees():
    employees = services.get('employee')
    limit = abs(request.args.get('limit', DEFAULT_LIMIT, type=int))
    offset = abs(request.args.get('offset', DEFAULT_OFFSET, type=int))
    expand = request.args.getlist('expand')

    if limit > MAX_LIMIT or limit < 0:
        limit = MAX_LIMIT

    _employees = employees.all(limit, offset)
    _employees = employees.expand(_employees, expand)

    return jsonify(_employees)


@app.route("/api/employees/<employee_id>")
def show_employee(employee_id):
    employee_id = abs(int(employee_id))
    expand = request.args.getlist('expand')
    employees = services.get('employee')
    employee = employees.get(employee_id)
    employee = employees.expand(employee, expand)

    if not employee:
        return not_found('could not find employee: {}'.format(employee_id))

    return jsonify(employee)


if __name__ == "__main__":
    app.run()