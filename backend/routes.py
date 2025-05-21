import tkinter as tk
from flask import Blueprint, request, render_template
from user_services import UserServices

# defines API endpoints

routes = Blueprint('routes', __name__)

user_services = UserServices()

# @routes.route("/")
# def intro():
#   return render_template('index.html')

  # message = user_services.greet()
  # return Response(message, mimetype="text/plain")

@routes.route('/', methods=['GET', 'POST']) # handle GET: user submitting name, and then POST: displaying the greeting
def intro():
  if request.method == 'POST':
    name = request.form.get('text')
    return user_services.greet(name)
  return render_template('index.html')

# url = "https://boozeapi.com/api/v1/cocktails"
# response = requests.get(url)
# print(response.json())