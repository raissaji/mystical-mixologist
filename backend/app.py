from flask import Flask
from routes import routes

# starts the app

app = Flask(__name__, static_folder="../static", template_folder='../templates')
app.register_blueprint(routes)

if __name__ == '__main__':
  app.run(debug=True)