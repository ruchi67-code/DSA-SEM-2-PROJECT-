from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample Data (acts like database)
products = [
    {"id": 1, "name": "Laptop", "price": 50000},
    {"id": 2, "name": "Phone", "price": 20000},
]

users = [
    {"id": 1, "name": "Ruchika"}
]

carts = {}  # user_id -> list of products


# ---------------- PRODUCT APIs ----------------

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)


@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    new_product = {
        "id": len(products) + 1,
        "name": data["name"],
        "price": data["price"]
    }
    products.append(new_product)
    return jsonify({"message": "Product added", "product": new_product})


# ---------------- USER APIs ----------------

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)


@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    new_user = {
        "id": len(users) + 1,
        "name": data["name"]
    }
    users.append(new_user)
    return jsonify({"message": "User added", "user": new_user})


# ---------------- CART APIs ----------------

@app.route('/cart/<int:user_id>', methods=['GET'])
def view_cart(user_id):
    cart = carts.get(user_id, [])
    return jsonify(cart)


@app.route('/cart/<int:user_id>/add', methods=['POST'])
def add_to_cart(user_id):
    data = request.json
    product_id = data["product_id"]

    product = next((p for p in products if p["id"] == product_id), None)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    if user_id not in carts:
        carts[user_id] = []

    carts[user_id].append(product)

    return jsonify({"message": "Product added to cart"})


@app.route('/cart/<int:user_id>/remove', methods=['POST'])
def remove_from_cart(user_id):
    data = request.json
    product_id = data["product_id"]

    if user_id not in carts:
        return jsonify({"error": "Cart not found"}), 404

    carts[user_id] = [p for p in carts[user_id] if p["id"] != product_id]

    return jsonify({"message": "Product removed"})


# ---------------- RUN SERVER ----------------

if __name__ == '__main__':
    app.run(debug=True)
