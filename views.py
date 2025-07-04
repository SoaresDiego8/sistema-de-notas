from flask import render_template, session, flash, redirect, url_for, request
from helpers import *
from models import Login, Nota
from helpers import FormularioLogin, FormularioNotas, FormularioCadastrar
from app import app, db
@app.route('/', methods=['GET', 'POST'])
def index():
    # --- Verificação se o Usuário está logado
    email = session.get('email_logado')

    if not email:
        flash(f'Faça seu login')
        return redirect(url_for('login'))

    # --- Busca o usuário logado para só mostrar as notas dele
    login = Login.query.filter_by(email=email).first()
    if not login:
        flash('Usuário inválido.', 'danger')
        return redirect(url_for('logout'))  # força logout se algo corrompeu a sessão

    # --- Adição de novas notas
    form = FormularioNotas()
    if request.method == 'POST':
        acao = request.form.get('acao')
        nota_id = request.form.get('nota_id')

        if acao == "criar" and form.validate_on_submit():
            nova_nota = Nota(nota=form.nota.data, id_login=login.id)
            db.session.add(nova_nota)
            db.session.commit()
            flash(f'Nota {nova_nota} foi adicionada com sucesso!', 'success')
            return redirect(url_for('index'))
        elif acao == "finalizar" and nota_id:
            nota = Nota.query.filter_by(id=nota_id, id_login=login.id).first()
            if nota and not nota.data_fim:
                nota.data_fim = db.func.current_timestamp()
                db.session.commit()
                flash(f'Nota finalizada', 'success')
            return redirect(url_for('index'))
        elif acao == "apagar" and nota_id:
            nota = Nota.query.filter_by(id=nota_id, id_login=login.id).first()
            if nota:
                db.session.delete(nota)
                db.session.commit()
                flash(f'Nota apagada com sucesso!', 'success')
            return redirect(url_for('index'))

    # --- Listando todas as notas do usuário
    lista_notas = Nota.query.filter_by(id_login=login.id).order_by(Nota.id).all()
    return render_template('index.html', form=form, lista_notas=lista_notas, nome=login.nome)


@app.route('/login')
def login():
    proxima_pagina = request.form.get('proxima')
    form = FormularioLogin()
    return render_template('login.html', form=form, proxima_pagina=proxima_pagina)

@app.route('/autenticar_login', methods=['POST'])
def autenticar_login():
    form = FormularioLogin(request.form)
    logar = Login.query.filter_by(email=form.email.data).first()
    proxima_pagina = request.form.get('proxima')

    if logar:
        session['email_logado'] = logar.email
        flash(f"{session['email_logado']} logado com sucesso!", 'success')

        if not proxima_pagina or proxima_pagina == "None":
            return redirect(url_for('index'))
        return redirect(url_for(proxima_pagina))

    session.pop('email_logado', None)
    flash('O email digitado não está cadastrado, por favor, se cadastre primeiro!', 'danger')
    return redirect(url_for('login'))

@app.route('/cadastrar_login', methods=['GET', 'POST'])
def cadastrar_login():
    form = FormularioCadastrar()

    if form.validate_on_submit():
        nome = form.nome.data
        email = form.email.data

        email_cadastrado = Login.query.filter_by(email=email).first()
        nome_cadastrado = Login.query.filter_by(nome=nome).first()

        if email_cadastrado:
            flash('Esse e-mail já está em uso. Por favor, escolha outro.', 'warning')
            return redirect(url_for('cadastrar_login'))

        if nome_cadastrado:
            flash('Esse nome já está em uso. Por favor, escolha outro.', 'warning')
            return redirect(url_for('cadastrar_login'))

        senha = generate_password_hash(form.senha.data)
        nova_conta = Login(nome=nome, email=email, senha=senha)

        db.session.add(nova_conta)
        db.session.commit()
        flash('Conta cadastrada com sucesso!', 'success')
        return redirect(url_for('login'))

    return render_template('cadastrar_login.html', form=form)



@app.route('/logout')
def logout():
    session.pop('email_logado', None)
    flash('Logout foi efetuado com sucesso!', 'success')
    return redirect(url_for('login'))