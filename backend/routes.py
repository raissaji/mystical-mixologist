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
             ingredients.append(i.get("name", ""))
             
          return ', '.join(ingredients)

def get_instructions(response_json, drink):
   for d in response_json['data']:
    if d.get("name", "").lower() == drink.lower():
        return d.get("instructions")

@routes.route('/', methods = ['GET', 'POST'])
def index():
  return render_template('start.html')

@routes.route('/chat', methods=['GET', 'POST'])
def chat():
  if request.method == 'GET':
     return render_template('chat.html')
  else:

    data = request.get_json()
    user_input = data.get("message", "")
    state = data.get("state", {"step": 0, "name": None, "drink_data": None, "drink": None, "drinks_list": None})

    step = state.get("step", 0)
    name = state.get("name", None)
    drink = state.get("drink", None)

    if step == 0:
        response = "Before we start... what's your name?"
        state["step"] = 1

    elif step == 1:
        name = user_input.capitalize()
        state["name"] = name
        state["step"] = 2

        drink_data = get_drinks_json()

        all_drinks = list()
        for i in drink_data['data']:
          all_drinks.append(i['name'].title())
          drinks_list = ', '.join(all_drinks)

        state["drink_data"] = drink_data
        state["drinks_list"] = drinks_list

        response = f'''<i>poof</i><br><br>
        Ah, greetings to you, noble soul, {name} the bold!<br>
        I’m Mike the Mixer, with potions of old.<br>
        From goblets and glasses, enchantments shall flow,<br> 
        With these mighty elixirs to soften your woe.<br>
        Behold my fine brews: <br><br><b>{drinks_list}</b>.<br><br>
        Oh so divine, each one a spell in a shimmering wine.<br>
        So tell me, dear traveler, don’t be so shy—<br>
        Which magical mixture has caught your keen eye?'''

    elif step == 2:
        drink = user_input.title()

        if drink not in state["drinks_list"]:
          response = f'''Alas, <b>{drink}</b> is not among my enchanted brews.<br><br>
          Might you try another drink from the spellbook? Name one from the list, dear traveler.'''
        else:
          state["drink"] = drink
          state["step"] = 3

          ingredients = get_ingredients(state["drink_data"], drink)
          instructions = get_instructions(state["drink_data"], drink)

          response = f'''Ahh, to brew the {drink}, a most curious feat,<br>  
          You’ll need these ingredients—a magical treat: <br><br><b>{ingredients}.</b><br><br>
          Now heed these instructions, both clever and wise,<br>  
          To summon a potion that dazzles the eyes:<br><br>  
          <b>{instructions}</b><br><br>  
          So stir it with care, let no step go astray,<br>  
          And your elixir shall brighten the rest of your day!'''

    elif step == 3:
      state["step"] = 4

      response = '''Oh, where did the time go! I muust bid thee farewell.<br><br>
        <i>poof</i>'''

    else:
        response = "<i>Mike has disappeared...</i>"

    return jsonify({"response": response, "state": state})