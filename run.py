from app import app, db, create_db

if __name__ == "__main__":
    
    db.drop_all()
    db.create_all()
    create_db()


    app.run(host='localhost', port=5000, debug=True)