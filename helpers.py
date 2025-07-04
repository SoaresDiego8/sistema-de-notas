import os
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp
from werkzeug.security import generate_password_hash, check_password_hash

# 🔐 Funções utilitárias para hash de senha
def gerar_hash(senha_plana: str) -> str:
    return generate_password_hash(senha_plana)

def verificar_hash(hash_salvo: str, senha_digitada: str) -> bool:
    return check_password_hash(hash_salvo, senha_digitada)

# 📧 Formulário de Login
class FormularioLogin(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired(),Length(min=1, max=100),Email()])
    logar = SubmitField('Entrar')

# 📝 Formulário de Notas
class FormularioNotas(FlaskForm):
    nota = TextAreaField('Escreva a sua nota:', validators=[DataRequired(),Length(min=1, max=500)])
    salvar = SubmitField('Salvar')

# 🧾 Formulário de Cadastro
class FormularioCadastrar(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(),Length(min=1, max=75)])
    email = EmailField('E-mail', validators=[DataRequired(),Length(min=1, max=100),Email()])
    senha = PasswordField('Senha', validators=[DataRequired(),Length(min=8, max=100),Regexp(r'^(?=.*[A-Z])(?=.*[\W_]).+$',message="A senha deve conter ao menos uma letra maiúscula e um caractere especial.")])
    cadastrar = SubmitField('Cadastrar')
