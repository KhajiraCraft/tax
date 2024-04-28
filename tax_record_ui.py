import sqlite3
from flask import Flask, render_template, request, jsonify,Blueprint
from models import *


tax_record_ui = Blueprint('tax_record_ui', __name__)


@tax_record_ui.route('/')
def index():
    return render_template("index.html")

@tax_record_ui.route('/all')
def allrecords():
    return render_template("allrecords.html")