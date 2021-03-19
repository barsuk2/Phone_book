import re
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
# manager=M
# app.debug = True
app.config['SECRET_KEY'] = 'a really really really really long secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123@localhost:5433/phone_book'

db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    phone_book = PhoneBook.query.order_by('name').paginate(page, per_page, error_out=False)
    return render_template('index.html', phone_book=phone_book)


@app.route('/add_phone', methods=['POST', 'GET'])
def add_phone():
    if request.method == 'POST':
        name = request.form['name']
        if name == '':
            flash('Имя пустое')
            return redirect('')
        phone = request.form['phone']
        phone = int(re.sub('\D', '', phone))

        if (PhoneBook.query.filter_by(name=name).count() != 0) or \
                (PhoneBook.query.filter_by(phone=phone).count() != 0):
            flash('Имя или телефон существуют')
            return redirect('')
        obj = PhoneBook(name=name, phone=phone)
        db.session.add(obj)
        db.session.commit()
    return redirect('/')


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'GET':
        name = request.args['search']
    phone_book = PhoneBook.query.filter(PhoneBook.name.contains(name))
    if phone_book.count() == 0:
        flash('Совпадений не найдено')
    else:
        flash(f'Найдено {phone_book.count()} записи(ей)')
    return render_template('search.html', phone_book=phone_book)


class PhoneBook(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True, )
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.BigInteger(), nullable=False)

    def __repr__(self):
        return f'Book:{self.name}'


if __name__ == '__main__':
    # app.run(debug=False)
    app.run()
