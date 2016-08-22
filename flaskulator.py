from flask import Flask, render_template, request
from decimal import Decimal

app = Flask(__name__)
app.config.from_object(__name__)

# define user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass

class NoNumberError(Error):
    """Raised when one of the number fields is empty"""
    pass

class ZeroDivError(Error):
    """Raised when division by zero is executed"""
    pass

@app.route('/')
def home_page():
    return render_template("index.html")

@app.route('/result', methods=['GET', 'POST'])
def result():
    operator = {
        "+": add,
        "-": subtract,
        "*": mult,
        "/": divide
    }
    form = request.form
    number1 = request.form['number1']
    number2 = request.form['number2']
    operation = request.form['operation']
    try:
        # check if the number fields are not empty
        if len(number1) < 1 or len(number2) < 1:
            raise NoNumberError
        # zero division checking
        if operation == "/" and number2 == "0":
            raise ZeroDivError
        #result calculation
        result = operator[operation](Decimal(number1), Decimal(number2))
        #Result representation.
        if len(str(result)) > 5:
            result = "%.4g" % result # set result precision to 4 digits
        return render_template("result.html", result=result, form=form)
    except ZeroDivError:
        error = "ZeroDivError"
        result = "Infinity (division by zero)"
        return render_template("result.html", result=result, form=form, error=error)
    except NoNumberError:
        error = "NoNumberError"
        return render_template('result.html', error=error)
    except ArithmeticError:
       error = "NotANumberError"
       return render_template('result.html', error=error)
    except Exception:
        error = "AnotherError"
        return render_template("result.html", error=error)

def add(operand1, operand2):
    """ Adds two numbers """
    return operand1 + operand2

def subtract(operand1, operand2):
    """ Subtraction of the given numbers """
    return operand1 - operand2

def mult(operand1, operand2):
    """ Returns the product of two operands """
    return operand1 * operand2

def divide(operand1, operand2):
    """ Returns the result of division operand1 by operand2 """
    return operand1 / operand2


if __name__ == '__main__':
    app.run()
