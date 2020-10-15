import os
import peewee as pw
import datetime
from playhouse.postgres_ext import PostgresqlExtDatabase

db = PostgresqlExtDatabase(os.getenv('DATABASE'))

class BaseModel(pw.Model):
   created_at = pw.DateTimeField(default=datetime.datetime.now)
   updated_at = pw.DateTimeField(default=datetime.datetime.now)

   def save(self, *args, **kwargs):
        self.errors = []
        self.validate()

        if len(self.errors) == 0:
            self.updated_at = datetime.datetime.now()
            return super(BaseModel, self).save(*args, **kwargs)
        else:
            return 0
       
   class Meta:
       database = db
       legacy_table_names = False

class Store(BaseModel):
   name = pw.CharField(unique=True)
   
   def validate(self):
        duplicate_stores = Store.get_or_none(Store.name == self.name)

        if duplicate_stores:
            self.errors.append('Store name not unique')

class Warehouse(BaseModel):
   store = pw.ForeignKeyField(Store, backref='warehouses')
   location = pw.TextField()

   def validate(self):
        duplicate_warehouses = Warehouse.get_or_none(Warehouse.location == self.location)

        if duplicate_warehouses:
            self.errors.append('Warehouse location not unique')

class Product(BaseModel):
   name = pw.CharField(index=True)
   description = pw.TextField()
   warehouse = pw.ForeignKeyField(Warehouse, backref='products')
   color = pw.CharField(null=True)

   def validate(self):
        duplicate_products_name = Product.get_or_none(Product.name == self.name)
        duplicate_products_color = Product.get_or_none(Product.color == self.color)

        if duplicate_products_name and duplicate_products_color:
            self.errors.append('Product name and color not unique')