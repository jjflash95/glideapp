from flask import Flask, jsonify, request
from services.services import Services
from utils import bad_request, internal_error, not_found


app = Flask(__name__)
app.debug = True

app.register_error_handler(500, internal_error)
app.register_error_handler(400, bad_request)

services = Services()


@app.route("/api/employees")
def list_employees():
    employees = services.get('employee')
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', type=int)
    expand = request.args.getlist('expand')

    if limit < 0:
        limit = 0
    if offset < 0:
        offset = 0

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
        return not_found()

    return jsonify(employee)


if __name__ == "__main__":
    app.run()
