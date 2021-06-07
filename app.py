from flask import Flask, jsonify, request
from services.services import Services
from services.expand_service import MissingHookException
from utils import bad_hook, bad_request, internal_error, not_found


app = Flask(__name__)
app.debug = True

services = Services()


@app.route("/api/employees")
def list_employees():
    employees = services.get('employee')
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', type=int)
    expand = request.args.getlist('expand')
    _employees = employees.all(limit, offset)

    limit = limit if limit and limit >= 0 else 0
    offset = offset if offset and offset >= 0 else 0

    try:
        _employees = employees.expand(_employees, expand)
    except MissingHookException as e:
        return bad_hook(e)

    return jsonify(_employees)


@app.route("/api/employees/<employee_id>")
def show_employee(employee_id):
    employee_id = abs(int(employee_id))
    expand = request.args.getlist('expand')
    employees = services.get('employee')
    employee = employees.get(employee_id)

    if not employee:
        return not_found("Employee {} not found".format(employee_id))

    try:
        employee = employees.expand(employee, expand)
    except MissingHookException as e:
        return bad_hook(e)

    return jsonify(employee)


if __name__ == "__main__":
    app.run()
