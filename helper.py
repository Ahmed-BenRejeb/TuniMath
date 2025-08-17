import csv
import datetime
import pytz
import requests
import urllib
import uuid

from flask import redirect, render_template, request, session
from functools import wraps
import sympy as sp
import math
import numpy as np


def check_expression(x):
    x=x.replace(" ","")
    if len(x) == 0:
        return True
    if x[0] in ".-*+/^πe" or x[-1 ] in "-.*+/^πe" or check_parantheses(x) ==  False:
        return False
    i=0
    while i < len(x):
        count = i
        l=[]
        while i < len(x) and (x[i] in "xyzt0123456789.πe"):
            i+=1
        if i < len(x):
            l.append(x[i])
        if i+1 < len(x)  and x[i+1] in "-*+/^":
            return False
        i=i+1
    return len(l) == 0

def check_parantheses(x):
    l=[]
    for i in x:
        if i == "(" or i == "[" :
            l.append(i)
        if i==")":
            if len(l) == 0 or l[-1] !="(" :
                return False
            else:
                l.pop()
        if i=="]":
            if  len(l) == 0 or l[-1] !="[":
                return False
            else:
                l.pop()
    return len(l) == 0
def login_required(f):
 

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def change_expression(x):
    i=-0
    while i < len(x)-1 :

        if ("0"<=x[i]<="9" and x[i+1].lower() in "xyzt") or (x[i]=="x" and x[i+1].lower() in "√scae") :
            x=x[0:i+1]+"*"+x[i+1:len(x)]
            i+=1
        i+=1
    x=x.replace("^","**")
    x=x.replace("ln","log")
    return x

def solve_system(*equations):
    variables = sp.symbols('x y z t')
    modified_equations = []
    for eq in equations:
        modified_eq = change_expression(eq)
        modified_equations.append(modified_eq)

    sympy_eqs = [sp.sympify(eq) for eq in modified_equations if eq]
    solution = sp.solve(sympy_eqs, variables[:len(sympy_eqs)])

    return {str(var): str(solution[var]) for var in solution}

def create_function(expr):

    def safe_acos(x):
        return np.arccos(x) if -1 <= x <= 1 else float('nan')

    def safe_asin(x):
        return np.arcsin(x) if -1 <= x <= 1 else float('nan')

    allowed_functions = {
        'sin': np.sin,
        'cos': np.cos,
        'tan': np.tan,
        'acos': safe_acos,
        'asin': safe_asin,
        'atan': np.arctan,
        'exp': np.exp,
        'log': lambda x: np.log(x) if x > 0 else float('nan'),
        'sqrt': lambda x: np.sqrt(x) if x >= 0 else float('nan'),
        'abs': abs,
        'pi': np.pi,
        'e': np.e,
        'pow' : math.pow
    }


    def safe_eval(expression, context):
        return eval(expression, {"__builtins__": {}}, context)

    def f(x):

        expr_with_functions = expr
        for func_name in allowed_functions:
            expr_with_functions = expr_with_functions.replace(func_name + '(', f"{func_name}(")
        return safe_eval(expr_with_functions, {"x": x, **allowed_functions})

    return f
func_map = {
    'sin': sp.sin,
    'cos': sp.cos,
    'tan': sp.tan,
    'acos': sp.acos,
    'asin': sp.asin,
    'atan': sp.atan,
    'exp': sp.exp,
    'log': sp.log,
    'sqrt': sp.sqrt,
    'abs': sp.Abs,
    'pi': sp.pi,
    'e': sp.E,

}

def parse_function(expression):

    x = sp.Symbol('x')

    for func, sympy_func in func_map.items():
        if func == 'pow':
            expression = expression.replace('pow(', 'Pow(')
        else:
            expression = expression.replace(func + '(', func + '(')
    expression = expression.replace('x', 'x')
    expression = expression.replace('Pow', 'sp.Pow')
    return sp.sympify(expression)

def derivative(expression):

    parsed_expression = parse_function(expression)
    x = sp.Symbol('x')
    derivative = sp.diff(parsed_expression, x)
    return derivative
def antiderivative(expression):
    parsed_expression = parse_function(expression)
    x = sp.Symbol('x')
    antiderivative = sp.integrate(parsed_expression, x)

    return antiderivative

def gcd(poly_str1, poly_str2):
    x = sp.symbols('x')
    poly1 = sp.Poly(sp.sympify(poly_str1), x)
    poly2 = sp.Poly(sp.sympify(poly_str2), x)
    gcd_poly = sp.gcd(poly1, poly2)
    gcd_poly = gcd_poly.as_expr().simplify()
    return gcd_poly

def division(poly_str1, poly_str2):
    x = sp.symbols('x')
    try:
        poly1 = sp.Poly(sp.sympify(change_expression(poly_str1)), x)
        poly2 = sp.Poly(sp.sympify(change_expression(poly_str2)), x)
        quotient, remainder = sp.div(poly1, poly2, domain='QQ')

        return str(quotient.as_expr()), str(remainder.as_expr())
    except Exception as e:
        return None, None
def root(poly_str):
    x = sp.symbols('x')
    poly_expr = sp.sympify(poly_str)
    roots = sp.solve(poly_expr, x)
    return roots
def solve_differential_equation(equation):
    y = sp.Function('y')
    x = sp.symbols('x')


    equation = change_expression(equation)


    equation = equation.replace("y''", "sp.Derivative(y(x), x, 2)")
    equation = equation.replace("y'", "sp.Derivative(y(x), x)")

    try:

        lhs, rhs = equation.split('=')
        lhs_expr = sp.sympify(lhs.strip())
        rhs_expr = sp.sympify(rhs.strip())


        diff_eq = sp.Eq(lhs_expr, rhs_expr)


        solution = sp.dsolve(diff_eq, y(x))
        return str(solution)
    except Exception as e:
        return str(e)


