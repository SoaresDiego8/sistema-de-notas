from app import db

class Login(db.Model):
    __tablename__ = 'login'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(500), nullable=False)
    def __repr__(self):
        return f'<Login {self.nome}>'


class Nota(db.Model):
    __tablename__ = 'lista_de_notas'
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_login  = db.Column(db.Integer, db.ForeignKey('login.id'), nullable=False)
    nota        = db.Column(db.Text, nullable=False)             # limite de 200 caracteres
    data_criacao = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    data_fim     = db.Column(db.DateTime, nullable=True)                # pode ficar NULL até ser concluída
    def __repr__(self):
        return f'<Nota %r>' % self.nota