from flask import render_template
from . import main

@main.route("/", methods = ['GET'])
def home():
  return render_template('home.html')

@main.route("/contacts", methods = ['GET'])
def contacts():
  return render_template('contacts.html')

@main.route("/about", methods = ['GET'])
def about():
  return render_template('about.html')