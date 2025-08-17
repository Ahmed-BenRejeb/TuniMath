import os
import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session,jsonify,Response
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helper import *
import time
import matplotlib.pyplot as plt
import io
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import base64
import plotly.graph_objs as go
import plotly.io as pio
import warnings

# Configure application
app = Flask(__name__)







app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    return render_template("index.html")




@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":
        if not request.form.get("mail"):
            return jsonify({
                'title': 'Error',
                'text': 'Must provide mail',
                'icon': 'error'
            })


        elif not request.form.get("password"):
            return jsonify({
                'title': 'Error',
                'text': 'Must provide Password',
                'icon': 'error'
            })


        rows = db.execute("SELECT * FROM users WHERE mail = ?", request.form.get("mail"))

        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return jsonify({
                'title': 'Error',
                'text': 'Wrong password or/and mail',
                'icon': 'error'
            })


        session["user_id"] = rows[0]["id"]

        return jsonify({
            'title': 'Success',
            'text': 'Logged in successfully.',
            'icon': 'success',
            'redirect': '/'
        })


    else:
        return render_template("login.html")
@app.route("/register", methods=["GET", "POST"])
def register():
    """Log user in"""


    session.clear()


    if request.method == "POST":
        if not request.form.get("username"):
            return jsonify({
                'title': 'Error',
                'text': 'Must provide username',
                'icon': 'error'
            }),400

        elif not request.form.get("mail"):
            return jsonify({
                'title': 'Error',
                'text': 'Must provide mail',
                'icon': 'error'
            }),400

        elif not request.form.get("password"):
            return jsonify({
                'title': 'Error',
                'text': 'Must provide Password',
                'icon': 'error'
            }),400
        elif request.form.get("password") != request.form.get("checkpassword"):
            return jsonify({
                'title': 'Error',
                'text': 'Check password must match',
                'icon': 'error'
            }),400
        password = generate_password_hash(request.form.get("password"))
        user = db.execute("select * from users where mail = ? and password = ? ", request.form.get("mail"),password)
        if len(user) != 0:
            return jsonify({
            'title': 'Error',
            'text': 'User exist already',
            'icon': 'error'
        }),400
        username=request.form.get("username")

        now = datetime.datetime.utcnow()
        db.execute("insert into users (mail,password,time,username) values(?,?,?,?)",
                request.form.get("mail"),password,now,username)
        return jsonify({
        'title': 'Success',
        'text': 'Registred with success.',
        'icon': 'success',
        'redirect': '/'
    })
    else:
        return render_template("register.html")
@app.route("/logout")
def logout():
    """Log user out"""

    session.clear()


    return redirect("/")






@app.route("/changepassword", methods=["POST", "GET"])
def changepassword():
    if request.method == "GET":
        return render_template("changepassword.html")
    else:
        mail = request.form.get("mail")
        password = request.form.get("password")
        check_password = request.form.get("checkpassword")
        if password != check_password:
            return jsonify({
                'title': 'Error',
                'text': 'Check password must match',
                'icon': 'error'
            }),400
        user = db.execute("select * from users where mail = ?", mail)
        if len(user) == 0:
            return jsonify({
                'title': 'Error',
                'text': 'user does not exist',
                'icon': 'error'
            }),400
        db.execute("update users set password = ? where mail = ?",
                   generate_password_hash(password), mail)
        return jsonify({
        'title': 'Success',
        'text': 'password changed',
        'icon': 'success',
        'redirect': '/login'
    }),200


@app.route("/calculator", methods=["POST", "GET"])
def calculator():
    return render_template("calculator.html")

@app.route("/systems", methods=["POST", "GET"])
def systems():
    if request.method == 'POST':
        num_variables = int(request.form.get('variables'))
        variables = list(range(1, num_variables + 1))
        return render_template("systems.html", variables=variables)
    return render_template('solve.html')

@app.route("/solve_system", methods=["POST"])
def solve_system_route():
    num_variables = int(request.form.get('numVariables'))
    equations = [request.form.get(f'eq{i}') for i in range(1, num_variables + 1)]
    solution = solve_system(*equations)
    return jsonify(solution)


@app.route("/functions", methods=["POST","GET"])
def functions():

    return render_template("functions.html")

@app.route("/plots", methods=["POST", "GET"])
def plots():
    if request.method == "POST":
        func = request.form.get("function")

        func = change_expression(func)
        f = create_function(func)

        x_values = [i / 50 for i in range(-500, 500)]

        y_values = [f(x) / 10 for x in x_values]


        trace = go.Scatter(
            x=x_values,
            y=y_values,
            mode='lines',
            line=dict(color='cyan', width=1.5),
            name=f'y = {func} / 10'
        )

        layout = go.Layout(
    title='Graph of the Function',
    xaxis=dict(
        title='x',
        showgrid=True,
        gridcolor='rgba(200, 200, 200, 0.3)',
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='rgba(200, 200, 200, 0.5)',
        range=[-10, 10],
        autorange=False,
        fixedrange=False,
        rangeslider=dict(visible=True)
    ),
    yaxis=dict(
        title='y',
        showgrid=True,
        gridcolor='rgba(200, 200, 200, 0.3)',
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='rgba(200, 200, 200, 0.5)',
        range=[-1, 1],
        autorange=False,
        fixedrange=False,
    ),
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    hovermode='closest'
)



        fig = go.Figure(data=[trace], layout=layout)


        config = dict(
            scrollZoom=True,
            displayModeBar=True,
            responsive=True
        )


        plot_div = pio.to_html(fig, full_html=False, config=config)
        l = []
        l.append(func)
        l.append(derivative(func))
        l.append(str(antiderivative(func)))
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        return render_template("plots.html", plot_div=plot_div, l=l)
    else:
        return redirect("/")

@app.route("/polynomials", methods=["POST", "GET"])
def polynomials():
    return render_template('polynomials.html')

@app.route("/solve_poly", methods=["POST"])
def solve_poly():
    p1 = request.form.get("polynome1")
    p1 = change_expression(p1)
    p2 = request.form.get("polynome2")
    operation = request.form.get("operation")


    result = {}
    if operation == 'roots':
        roots = root(p1)
        result['roots'] = str(roots) if roots else 'No roots found'
    elif operation == 'gcd':
        if not p2:
            p2 = "1"
        p2 = str(change_expression(p2))
        gcd_result = gcd(p1, p2)
        result['gcd'] = str(gcd_result)
    elif operation == 'division':
        if not p2:
            p2 = "1"
        quotient, remainder = division(p1, p2)
        result['division'] = f"Quotient: {quotient}, Remainder: {remainder}" if quotient or remainder else "Division operation failed"

    return jsonify(result)

@app.route("/series",methods=["POST","GET"])
def series():
    return render_template("series.html")

