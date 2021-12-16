"""A simple flask web app"""
from flask import Flask, request, render_template
from app.controllers.index_controller import IndexController
from app.controllers.calculator_controller import CalculatorController
from calc.calculate import Calculator, ReadTable, Pagination

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/", methods=['GET'])
def index_get():
    return render_template('index.html')


@app.route("/calculator", methods=['GET'])
def calculator_get():
    return CalculatorController.get()


@app.route("/calculator", methods=['POST'])
def calculator_post():
    return CalculatorController.post()


@app.route("/do/operation/", methods=['POST'])
def do_operation():
    calc, csv_obj = Calculator(), ReadTable()
    value_1 = int(request.form["value_1"])
    value_2 = int(request.form["value_2"])
    opertion = request.form["opertion"]
    result = calc.opertions.get(opertion)(value_1, value_2)
    csv_obj.write_csv(value_1, value_2, opertion, result)
    return render_template("result.html", value_1=value_1, value_2=value_2, result=result, opertion=opertion)


@app.route("/table/logs")
def read_table():
    page = request.args.get('page')
    per_page = 7
    if page == None or page.strip() == str() or page.strip() == '0':
        page = 1
        start = 0
        end = per_page
    else:
        page = int(page)
        start = (page - 1) * per_page
        end = start + per_page
    csv_obj = ReadTable()
    csv_obj.csv_to_list()
    p = Pagination(len(csv_obj.rows), per_page, page)
    return render_template("table.html", table=csv_obj.rows[start:end], pagination=p)
