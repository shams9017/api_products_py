from flask import request, jsonify, Blueprint,send_file,Response
import sys
import os

from db import Product,db

current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)

# importing
product_route = Blueprint('product_route', __name__,url_prefix="/")

@product_route.route('/search/all', methods=['GET'])
def get_all_products():
  products = Product.query.all()
    
  data = []

  for prod in products:
    data.append({
      "id": prod.id,
      'name': prod.name,
      'description': prod.description,
      'price': prod.price,
      'qty': prod.qty
    })

  return jsonify({'data': data})

@product_route.route('/product/search', methods=['GET'])
def get_products():
  name = request.args.get('name')
  description = request.args.get('description')
  price = request.args.get('price')
  qty = request.args.get('qty')
  
  if name:
    products = db.session.query(Product).filter(Product.name == name).all()
  if description:
    products = db.session.query(Product).filter(Product.description == description).all()
  if price:
    products = db.session.query(Product).filter(Product.price == price).all()
  if qty:
    products = db.session.query(Product).filter(Product.qty == qty).all()
    
  data = []

  for prod in products:

    data.append({
      "id": prod.id,
      'name': prod.name,
      'description': prod.description,
      'price': prod.price,
      'qty': prod.qty
    })

  meta = {
      "id": Product.id,
      'name': Product.name,
      'description': Product.description,
      'price': Product.price,
      'qty': Product.qty

  }
  
  return jsonify({'data': data})

# Create the product route
@product_route.route('/product/add', methods=['POST'])
def add_product():
  name = request.json['name']
  description = request.json['description']
  price = request.json['price']
  qty = request.json['qty']
  
  new_product = Product(name, description, price, qty)
  try:
    db.session.add(new_product)
    db.session.commit()
  except:
    raise Exception("error while adding new product")

  return jsonify({
    'id': new_product.id,
    'name': new_product.name,
    'description': new_product.description,
    'price': new_product.price,
    'qty': new_product.qty
})

@product_route.route('/product/update', methods=['PUT'])
def update_product():
  id = request.args.get('id')
  
  if id:
    product = db.session.query(Product).filter(Product.id == id).first()
  if not product:
      return jsonify({'message': 'Item not found'})
  
  
  body = request.get_json()

  product.from_json(body)

  try:
    db.session.commit()
  except:
    raise Exception("error updating product")

  return jsonify({
    'id': product.id,
    'name': product.name,
    'description': product.description,
    'price': product.price,
    'qty': product.qty
})


@product_route.route('/product/delete', methods=['DELETE'])
def delete_product():
  id = request.args.get('id')
  
  if id:
    product = db.session.query(Product).filter(Product.id == id).first()

  if not product:
      return jsonify({'message': 'Item not found'})
  

  try:
    db.session.delete(product)
    db.session.commit()
  except:
    raise Exception("error deleting product")

  return jsonify({
    'id': product.id,
    'name': product.name,
    'description': product.description,
    'price': product.price,
    'qty': product.qty
})







