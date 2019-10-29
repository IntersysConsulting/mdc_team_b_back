from flask import render_template, Flask
from flask_mail import Message, Mail

app = Flask(__name__)


def send_receipt(product_list, email):
    print("Sending a receipt to {}".format(email))
    total = 0
    for product in product_list:
        total += product["unitary_price"] * product["quantity"]

    msg = Message("Ecommerce Receipt",
                  sender='itersysecommerce@gmail.com',
                  recipients=[email])  # Should be changed to customer's email
    with app.open_resource("../../../templates/logo.jpg") as fp:
        msg.attach('logo.jpg',
                   'image/jpg',
                   fp.read(),
                   'inline',
                   headers=[
                       ['Content-ID', '<Myimage>'],
                   ])
        msg.html = render_template('receipt.html',
                                   product_list=product_list,
                                   total=total)
    mail = Mail()
    mail.send(msg)