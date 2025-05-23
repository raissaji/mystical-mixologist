import tkinter as tk

# methods for interacting with user

class UserServices:
  def greet(self, name):
    return f'Hi, {name}! \nI am Mike, the Mystical Mixologist, here to help you concoct any drink you desire. 🍸'
  
  def ask_ingredients(self):
    return 'List out the ingredients you have, separated by commas. If you don\'t have any, enter \'None\'.'