from flask import Flask, render_template, request, redirect, url_for, session
from models import db, Item
from users import validate_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'  # Necessário para sessões

db.init_app(app)

@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if validate_user(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Usuário ou senha inválidos", 403
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/form', methods=['GET', 'POST'])
def form():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        item_id = request.form.get('id')

        if item_id:
            item = Item.query.get(item_id)
            item.nome = nome
            item.descricao = descricao
        else:
            item = Item(nome=nome, descricao=descricao)
            db.session.add(item)
        db.session.commit()
        return redirect(url_for('table'))

    item_id = request.args.get('id')
    if item_id:
        item = Item.query.get(item_id)
        return render_template('form.html', item=item)
    return render_template('form.html')

@app.route('/table')
def table():
    if 'username' not in session:
        return redirect(url_for('login'))

    items = Item.query.all()
    return render_template('table.html', items=items)

@app.route('/delete/<int:id>')
def delete(id):
    if 'username' not in session:
        return redirect(url_for('login'))

    item = Item.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('table'))

@app.route('/about')
def about():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('about.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
