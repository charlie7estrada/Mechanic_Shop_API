from app.models import db
from app import create_app


app = create_app('DevelopmentConfig')


# Create the table
with app.app_context():
    # db.drop_all()
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)