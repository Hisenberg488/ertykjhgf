from main import db
from main import app
from main import User



with app.app_context():
    db.create_all()
    t1 = User(tokens="0",achivments="",refrerals="")
    db.session.add(t1)
    db.session.commit()