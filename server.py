import os
import peeweedbevolve
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Store, Warehouse , Product
app = Flask(__name__)
app.secret_key=os.getenv("SECRETKEY")

@app.before_request 
def before_request():
   db.connect()

@app.after_request 
def after_request(response):
   db.close()
   return response

@app.cli.command() 
def migrate():  
   db.evolve(ignore_tables={'base_model'})

@app.route("/")
def index():
   return render_template('index.html')


@app.route("/store/new", methods = ['GET'])
def store_new():
    return render_template('addstore.html')
    
@app.route("/store/", methods =['POST'])
def store_created() :
    
    store_name = request.form.get("store_name")
    store = Store(name=store_name)
    if store.save():
        flash("Successfully added","success")
    else :
        flash("Duplicate Entry!!","danger")
    return redirect(url_for("store_new"))

@app.route("/store/", methods = ['GET'])
def store_index():
    stores = Store.select()
    return render_template('store_index.html',stores=stores)
    
    

@app.route("/store/<store_id>", methods = ['GET'])
def store_show(store_id):
    store = Store.get_by_id(store_id)
    return render_template('store_show.html', store=store) 

@app.route("/store/<store_id>", methods = ['POST'])
def store_update(store_id):
    store = Store.get_by_id(store_id)
    store.name = request.form.get("store_name")
    if store.save():
        flash("Store name successfully updated.", "success")
    else :
        flash("The name entered is same as the previous", "danger")
    return redirect(url_for('store_show', store_id = store.id))


@app.route("/store/<store_id>/delete", methods = ['POST'])
def store_delete(store_id):
    store = Store.get_by_id(store_id)
    if store.delete_instance():
        flash("Store successfull deleted.", "success")
    return redirect(url_for('store_index'))


@app.route("/warehouse/new", methods = ['GET'])
def warehouse_new() :
    stores = Store.select()
    return render_template("warehouse_new.html", stores=stores)

@app.route("/warehouse/", methods = ['POST'])
def warehouse_created() :
    store = request.form.get("store_id")
    location = request.form.get("location")
    w = Warehouse(store=store , location = location)
    if w.save() :
        flash("Warehouse Created!","success")
    else :
        flash("Warehouse Duplicated","danger")
    return redirect(url_for('warehouse_new'))


@app.route("/product/new", methods = ['GET'])
def product_new() :
    warehouses = Warehouse.select()
    return render_template("product_new.html", warehouses=warehouses)

@app.route("/product/", methods = ['POST'])
def product_created() :
    warehouse = request.form.get("warehouse_id")
    product_name = request.form.get("product_name")
    product_description = request.form.get("product_description")
    product_color = request.form.get("product_color")
    p = Product(warehouse=warehouse ,  name= product_name, description = product_description, color = product_color)
    if p.save() :
        flash("Product Created!","success")
    else :
        flash("Product Duplicated","danger")
    return redirect(url_for('product_new'))

@app.route("/warehouse/", methods = ['GET'])
def warehouse_index():
    warehouses = Warehouse.select()
    return render_template('warehouse_index.html',warehouses=warehouses)

@app.route("/warehouse/<warehouse_id>", methods = ['GET'])
def warehouse_show(warehouse_id):
    warehouse = Warehouse.get_by_id(warehouse_id)
    return render_template('warehouse_show.html', warehouse=warehouse) 

@app.route("/warehouse/<warehouse_id>", methods = ['POST'])
def warehouse_update(warehouse_id):
    warehouse = Warehouse.get_by_id(warehouse_id)
    warehouse.location = request.form.get("warehouse_location")
    if warehouse.save():
        flash("Warehouse location successfully updated.", "success")
    else :
        flash("The location entered is same as the previous", "danger")
    return redirect(url_for('warehouse_show', warehouse_id = warehouse.id))

@app.route("/warehouse/<warehouse_id>/delete", methods = ['POST'])
def warehouse_delete(warehouse_id):
    warehouse = Warehouse.get_by_id(warehouse_id)
    if warehouse.delete_instance():
        flash("Warehouse successfull deleted.", "success")
    return redirect(url_for('warehouse_index'))

@app.route("/product/", methods = ['GET'])
def product_index():
    products = Product.select()
    return render_template('product_index.html',products=products)

@app.route("/product/<product_id>", methods = ['GET'])
def product_show(product_id):
    product = Product.get_by_id(product_id)
    return render_template('product_show.html', product=product) 


@app.route("/product/<product_id>", methods = ['POST'])
def product_update(product_id):
    product = Product.get_by_id(product_id)
    product.name = request.form.get("product_name")
    product.description = request.form.get("product_description")
    product.color = request.form.get("product_color")

    if product.save():
        flash("Product successfully updated.", "success")
    else :
        flash("The product entered is same as the previous", "danger")
    return redirect(url_for('product_show', product_id = product.id))

@app.route("/product/<product_id>/delete", methods = ['POST'])
def product_delete(product_id):
    product = Product.get_by_id(product_id)
    if product.delete_instance():
        flash("Product successfull deleted.", "success")
    return redirect(url_for('product_index'))



if __name__ == '__main__' :
   app.run()