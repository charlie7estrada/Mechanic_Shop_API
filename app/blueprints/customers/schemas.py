from app.extensions import ma
from app.models import Customer

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer #Creates a schema that validates the data as defined by our Users Model
 
customer_schema = CustomerSchema() 
customers_schema = CustomerSchema(many=True) #Allows this schema to translate a list of User objects all at once