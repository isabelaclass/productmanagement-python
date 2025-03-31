from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# HTTP status codes for responses
SUCCESS = 200
CREATED = 201
BAD_REQUEST = 400
NOT_FOUND = 404
INTERNAL_ERROR = 500
NOT_IMPLEMENTED = 501
EXTERNAL_ERROR = 502

# Create a Flask application instance
app = Flask(__name__)

# Configuring the database URI and disabling modification tracking for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:your_passsword@localhost/products'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creae an instance of SQLAlchemy to interact with the database
db = SQLAlchemy(app)

# Define the Product model (table) in the database
class Product(db.Model):
    __tablename__ = 'products' 

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    vend = db.Column(db.String(255), nullable=False)
    vend_address= db.Column(db.String(255))
    quantity = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(255))
    price_unit = db.Column(db.Float, nullable=False)

# Route to handle GET requests and retrieve all products 
@app.route("/products", methods=["GET"])
def get_product():
    try: 
        products = Product.query.all()

        if not products:
            return jsonify({"message": "No products found"}), NOT_FOUND
        
        return jsonify({
            "products": [
                {
                    "id": product.id,
                    "name": product.name,
                    "vend:": product.vend,
                    "vend_address": product.vend_address,
                    "quantity": product.quantity,
                    "address": product.address,
                    "price_unit": product.price_unit
                }
                for product in products
            ]
        }), SUCCESS
    except Exception as e:
        return jsonify({"message": "Internal server error", "error": str(e)}), INTERNAL_ERROR

# Route to handle POST requests and create a new product
@app.route("/products", methods=["POST"])
def post_product():
    try: 
        data = request.get_json()

        if not all(key in data for key in ["name", "vend", "quantity", "price_unit"]):
            return jsonify({"message": "Missing required fields"}), BAD_REQUEST

        new_product = Product(
            name=data['name'],
            vend=data['vend'],
            vend_address=['vend_address'],
            quantity=data['quantity'],
            address=data['address'],
            price_unit=data['price_unit']
        )

        db.session.add(new_product)
        db.session.commit()

        return jsonify({
            "id": new_product.id,
            "name": new_product.name,
            "vend": new_product.vend,
            "vend_address": new_product.vend_address,
            "quantity": new_product.quantity,
            "address": new_product.address,
            "price_unit": new_product.price_unit
        }), CREATED
    
    except Exception as e:
        return jsonify({"message": "Internal server error", "error": str(e)}), INTERNAL_ERROR

# Route to handle PUT requests and update an existing product
@app.route("/products", methods=["PUT"])
def update_product():
    try:
        product_id = request.args.get("id")

        if not product_id:
            return jsonify({"message": "Product ID is required"}), BAD_REQUEST

        data = request.get_json()

        if not all(key in data for key in ["name", "vend", "quantity", "price_unit"]):
            return jsonify({"message": "Missing required fields"}), BAD_REQUEST
        
        product = Product.query.get(product_id)

        if not product:
            return jsonify({"message": "Product not found"}), NOT_FOUND

        product.name = data['name']
        product.vend = data['vend']
        product.vend_address = data['vend_address']
        product.quantity = data['quantity']
        product.price_unit = data['price_unit']

        db.session.commit()

        return jsonify({
            "id": product.id,
            "name": product.name,
            "vend": product.vend,
            "vend_address": product.vend_address,
            "quantity": product.quantity,
            "address": product.address,
            "price_unit": product.price_unit
        }), SUCCESS
    
    except Exception as e:
        return jsonify({"message": "Internal server error", "error": str(e)}), INTERNAL_ERROR

# Route to handke DELETE requests and delete a product
@app.route("/products", methods=["DELETE"])
def delete_product():
    try: 
        product_id = int(request.args.get("id"))

        if not product_id:
            return jsonify({"message": "Product ID is required"}), BAD_REQUEST
        
        product = Product.query.get(product_id)

        if not product:
            return jsonify({"message": "Product not found"}), NOT_FOUND

        db.session.delete(product)
        db.session.commit()

        return jsonify({"message": "Product deleted successfully"}), SUCCESS
    
    except Exception as e:
        return jsonify({"message": "Internal server error", "error": str(e)}), INTERNAL_ERROR

# Start the Flask application in debug mode
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)