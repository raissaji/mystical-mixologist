import tkinter as tk
from flask import Blueprint, request, render_template
from user_services import UserServices
import requests
import random

# defines API endpoints

routes = Blueprint('routes', __name__)

user_services = UserServices()

page = random.randint(1, 63)
url = f"https://boozeapi.com/api/v1/cocktails?page={page}"
response = requests.get(url)
response_json = response.json()

@routes.route('/', methods=['GET', 'POST'])
# handle GET: user submitting name, and then POST: displaying the greeting
def get_name():
  if request.method == 'POST':
    name = request.form.get('text')
    return user_services.greet(name)
  return render_template('index.html')

@routes.route('/get_drinks', methods=['POST'])
def get_ingredients():
  user_services.ask_ingredients()

  if request.method == 'POST':
    all_drinks = list()

    for i in response_json['data']:
      all_drinks.append(i['name'])

      return render_template('index.html', cocktails=all_drinks)