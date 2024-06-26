from flask import Flask, render_template, request, jsonify
import hmac
import hashlib
from urllib.parse import unquote
from flask_sqlalchemy import SQLAlchemy


def validate_init_data(init_data: str, bot_token: str):
    vals = {k: unquote(v) for k, v in [s.split('=', 1) for s in init_data.split('&')]}
    data_check_string = '\n'.join(f"{k}={v}" for k, v in sorted(vals.items()) if k != 'hash')

    secret_key = hmac.new("WebAppData".encode(), bot_token.encode(), hashlib.sha256).digest()
    h = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256)
    return h.hexdigest() == vals['hash']

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'

db = SQLAlchemy(app)



# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     userid = db.Column(db.String(21))
#     tokens = db.Column(db.String(15))
#     achivments = db.Column(db.String(100))
#     refrerals = db.Column(db.String(320))

#     def __repr__(self):
#         return f'User({self.id} - {self.tokens} - {self.achivments} - {self.refrerals})'



@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/earn-tokens')
def earn_page():
    return render_template('earn-tab.html')


@app.route('/process', methods=['GET', 'POST'])
def validate_user():
    data = request.get_json()
    if data and 'value' in data:
        print(data['value']['initDataUnsafe']['user']['first_name'])
        isvalid = validate_init_data(data['value']['initData'], '7434762383:AAGXvXBKNCKozRiewDvl1urcqnz5ZMVErfI')
        print(isvalid)
        
        # with app.app_context():
        #     db.create_all()
        #     t1 = User(username=tokens="0",achivments="",refrerals="")
        #     db.session.add(t1)
        #     db.session.commit()
        return jsonify(isvalid=isvalid)
    return jsonify(isvalid=False)


if __name__ == '__main__':
    app.run(port=8080)
