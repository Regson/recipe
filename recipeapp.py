from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

r_app = Flask(__name__)
r_app.Config = SQLALCHEMY_DATABASE_URI = 'sqlite:///recipe.db'
db = SQLAlchemy(r_app)

class Recipe(db.Model):
    r_id = db.Column(db.Integer, primary_key=True)
    r_name = db.Column(db.String(20), unique=True, nullable=False)
    ingredient = db.relationship('Ingredients', backref='recipe', lazy=True)
    r_instruction = db.relationship('RecipeInstruction', backref='recipe', lazy=True)

    def __repr__(self):
        return f"Recipe('{self.r_name}')"


class Ingredients(db.Model):
    ingredient_id = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(db.String(20), unique=True, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.r_id'), nullable=False)
    
    def __repr__(self):
        return f"Ingredients('{self.ingredient_name}')"


class RecipeInstruction(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.r_id'), nullable=False)
    recipe_instruction = db.Column(db.Text, unique=True, nullable=False)
    
    def __repr__(self):
        return f"RecipeInstruction('{self.instruction}')"



recipe = [
    {'id': 0,
     'name': 'fried rice',
     'description': 'cooking of fried rice',
     'instruction': 'boil the rice half way and add blabla.',
     'ingredients': 'rice, green bean, onions, etc'},
    {'id': 1,
     'name': 'boiled egg',
     'description': 'boiling egg',
     'instruction': 'boil the egg in a pot of water for 5mins',
     'ingredients': 'egg, water'},
    {'id': 2,
     'name': 'Beans',
     'description': 'cooking of beans',
     'instruction': 'boil the beans for 45mins, change the water and add blabla.',
     'ingredients': 'rice, green bean, onions, etc'}
]



@r_app.route("/")
def hello():
	return render_template('home.html')


@r_app.route("/about")
def about():
	return render_template('about.html')	


@r_app.route('/recipeapp/v1/recipe/all', methods=['GET'])
def recipe_all():
    return jsonify(recipe)

@r_app.route('/recipeapp/v1/recipe', methods=['GET'])
def recipe_id():
	# Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for r in recipe:
        if r['id'] == id:
            results.append(r)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)


if __name__=='__main__':
	r_app.run(debug=True)