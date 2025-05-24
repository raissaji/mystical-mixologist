from flask import Blueprint, request, render_template, jsonify
import requests
import random

# defines API endpoints

routes = Blueprint('routes', __name__)

def get_drinks_json():
  page = random.randint(1, 63)
  url = f"https://boozeapi.com/api/v1/cocktails?page={page}"
  
  response = requests.get(url)
  response_json = response.json()

  return response_json

def get_ingredients(response_json, drink):
   ingredients = list()
   for d in response_json['data']:
      if d.get("name", "").lower() == drink.lower():
         for i in d.get("ingredients"):
            ingredients.append(i['name'])
      return ', '.join(ingredients)

def get_instructions(response_json, drink):
   for d in response_json['data']:
    if d.get("name", "").lower() == drink.lower():
        return d.get("instructions")

@routes.route('/')
def index():
  return render_template('chat.html')

@routes.route('/chat', methods=['POST'])
def chat():
  data = request.get_json()
  user_input = data.get("message", "")
  state = data.get("state", {"step": 0, "name": None, "drink_data": None, "drink": None})

  step = state.get("step", 0)
  name = state.get("name", None)
  drink = state.get("drink", None)

  if step == 0:
      response = "Before we start... what's your name?"
      state["step"] = 1

  elif step == 1:
      name = user_input
      state["name"] = name
      state["step"] = 2

      drink_data = get_drinks_json()
      # print(response_json)

      all_drinks = list()
      for i in drink_data['data']:
        all_drinks.append(i['name'])
        drinks_list = ', '.join(all_drinks)

      state["drink_data"] = drink_data

      response = f'''Ah, greetings to you, noble soul, {name} the bold!
      I’m Mike the Mixer, with potions of old.
      From goblets and glasses, enchantments shall flow, 
      With these mighty elixirs to soften your woe.
      Behold my fine brews: {drinks_list}.
      Oh so divine—each one a spell in a shimmering wine.
      So tell me, dear traveler, don’t be so shy—
      Which magical mixture has caught your keen eye?'''

  elif step == 2:
      drink = user_input
      state["drink"] = drink
      state["step"] = 3

      ingredients = get_ingredients(state["drink_data"], drink)
      instructions = get_instructions(state["drink_data"], drink)

      response = f'''Ahh, to brew the {drink}, a most curious feat,  
      You’ll need these ingredients—a magical treat: {ingredients}.  
      Now heed these instructions, both clever and wise,  
      To summon a potion that dazzles the eyes:  
      {instructions}  
      So stir it with care, let no step go astray,  
      And your elixir shall brighten the rest of your day!'''

  else:
      response = "Bye bitch!"

  return jsonify({"response": response, "state": state})