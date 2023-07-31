from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost/clients"
db = SQLAlchemy()
db.init_app(app)

# Заказ (id, имя человека, контакты, адрес, описание)
class ClientOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    contacts = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    order_count = db.Column(db.Integer)


@app.route('/')
def homepage():
    orders = db.session.execute(db.select(ClientOrder)).scalars()
    clients = db.session.execute(db.select(Client)).scalars()
    return render_template(
        'index.html',
        orders=orders,
        clients=clients
    )

@app.route('/orders/')
def orders_list():
    orders = db.session.execute(db.select(ClientOrder)).scalars()
    return render_template('order_array.html', orders=orders)

@app.route('/order/<int:id>')
def order_detail(id):
    order_object = db.get_or_404(ClientOrder, id)
    return render_template('order_detail.html', order_object=order_object)


@app.route("/clients")
def clients():
    clients_query = db.session.execute(db.select(Client)).scalars()
    return render_template('clients.html', clients=clients_query)


with app.app_context():
    db.create_all()
