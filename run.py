from app import app, db, create_db
from app.training_data import try_csv

if __name__ == "__main__":
    
    db.drop_all()
    db.create_all()
    create_db()

    try_csv()




    app.run(host='localhost', port=5000, debug=True)