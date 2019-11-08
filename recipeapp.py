from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Init app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipetest.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# Ingredients class/model
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    def __init__(self, name, recipe_id=None):
            self.name = name
            self.recipe_id = recipe_id

# Ingredients Schema
class IngredientSchema(ma.Schema):
	class Meta:
		fields = ['name']
		#fields = ('id', 'name','recipe_id')
		#recipe = ma.Nested(RecipeSchema)


# Init Schema
ingredient_schema = IngredientSchema()
ingredients_schema = IngredientSchema(many=True)


# Recipe class/model
class Recipe(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique = True, nullable=False)	
	ingredient = db.relationship('Ingredient', backref= db.backref('recipe', lazy=True))
	def __init__(self, name, ingredients):
		self.name = name
		self.ingredients = []
		#self.instruction = instruction
		
# Recipe Schema
class RecipeSchema(ma.Schema):
	class Meta:
		fields = ('id', 'name', 'ingredients')
		ingredients = ma.Nested(IngredientSchema, many=True, only=['name'])
		#instruction = ma.Nested(RecipeInstructionSchema)


# Init Schema
recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)



# RecipeInstruction class/model
"""class RecipeInstruction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    recipe = db.relationship('Recipe', lazy = 'select', backref= db.backref('RecipeInstruction', lazy= 'joined'))
    recipe_instruction = db.Column(db.Text, unique=True, nullable=False)

    def __init__(self, recipe_id, recipe_instruction):
            self.recipe_id = recipe_id
            self.recipe_instruction = recipe_instruction
		
# RecipeInstruction Schema
class RecipeInstructionSchema(ma.Schema):
	class Meta:
		fields = ('id', 'recipe_id', 'recipe_instruction', 'recipe')
		recipe=ma.Nested(RecipeSchema)


# Init Schema
instuction_schema = RecipeInstructionSchema()"""



# Create Recipe
@app.route("/recipe/add", methods=['POST'])
def add_recipe():
	name = request.json['name']
	ing = request.json['ing']
	new_recipe = Recipe(name, ing)
	db.session.add(new_recipe)
	db.session.commit()
	return recipes_schema.jsonify(new_recipe)

	# Create Ingredients
@app.route("/recipe/ing/add", methods=['POST'])
def add_ingr():
	name = request.json['name']
	r_id = request.json['r_id']
	ingredient = Ingredient(name, r_id)
	db.session.add(ingredient)
	db.session.commit()
	return ingredient_schema.jsonify(ingredient)

# Get all Recipe
@app.route('/recipe/all', methods=['GET'])
def get_recipes():
	all_recipes = Recipe.query.all()
	result = recipes_schema.dump(all_recipes)
	return jsonify(result)

# Get all Ingredients
@app.route('/recipe/ing/all', methods=['GET'])
def get_ingreds():
	all_ingreds = Ingredient.query.all()
	result = ingredients_schema.dump(all_ingreds, many=True)
	return jsonify(result)

# Get an Ingr
@app.route('/ing/<id>', methods=['GET'])
def get_ing(id):
	ingr = Ingredient.query.get(id)
	return ingredient_schema.jsonify(ingr)

# Get a Recipe and its ingredients
@app.route('/recipe/<id>', methods=['GET'])
def get_recipe(id):
	arecipe = Recipe.query.get(id)
	arecipe_result = recipe_schema.dump(arecipe)
	ingr_result = ingredients_schema.dump(arecipe.ingredient)
	return jsonify({"Recipe": arecipe_result, "Ingredients": ingr_result})
	#return recipe_schema.jsonify(arecipe)


# Run Server
if __name__ == '__main__':
	app.run(debug=True)
