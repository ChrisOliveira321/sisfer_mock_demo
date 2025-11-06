# mock_sisfer_api.py
from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import uuid
import os
from functools import wraps

APP_PORT = int(os.getenv('MOCK_PORT', 5000))
DB_FILE = os.getenv('MOCK_DB', 'mock_sisfer.db')

app = Flask(__name__)
CORS(app)  # permite chamadas do front local (apenas para demo)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_FILE}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------- MODELOS ----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


class Carregamento(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    placa = db.Column(db.String(20))
    produto = db.Column(db.String(120))
    peso = db.Column(db.Float)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(40), default='AGENDADO')


# ---------------- AUTENTICAÇÃO ----------------
TOKENS = {}

def generate_token():
    return str(uuid.uuid4())

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return jsonify({'error': 'Unauthorized'}), 401
        token = auth.split(' ', 1)[1]
        usuario = TOKENS.get(token)
        if not usuario:
            return jsonify({'error': 'Invalid or expired token'}), 401
        g.current_user = User.query.filter_by(username=usuario).first()
        return f(*args, **kwargs)
    return decorated


# ---------------- ROTAS ----------------
@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'ok', 'time': datetime.utcnow().isoformat()})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    usuario = data.get('usuario')
    senha = data.get('senha')
    if not usuario or not senha:
        return jsonify({'error': 'usuario e senha obrigatorios'}), 400

    user = User.query.filter_by(username=usuario, password=senha).first()
    if not user:
        return jsonify({'error': 'credenciais invalidas'}), 401

    token = generate_token()
    TOKENS[token] = usuario
    return jsonify({'token': token, 'usuario': usuario})


@app.route('/carregamentos', methods=['POST'])
@auth_required
def criar_carregamento():
    data = request.get_json(force=True)
    placa = data.get('placa')
    produto = data.get('produto')
    peso = data.get('peso')

    if not placa or not produto or peso is None:
        return jsonify({'error': 'placa, produto e peso obrigatorios'}), 400

    novo = Carregamento(
        id=str(uuid.uuid4()),
        usuario_id=g.current_user.id,
        placa=placa,
        produto=produto,
        peso=float(peso),
        status='AGENDADO'
    )

    db.session.add(novo)
    db.session.commit()

    return jsonify({
        'id': novo.id,
        'status': novo.status,
        'criado_em': novo.criado_em.isoformat()
    })


@app.route('/carregamentos', methods=['GET'])
@auth_required
def listar_carregamentos():
    user = g.current_user
    items = Carregamento.query.filter_by(usuario_id=user.id).order_by(Carregamento.criado_em.desc()).all()
    out = []
    for it in items:
        out.append({
            'id': it.id,
            'placa': it.placa,
            'produto': it.produto,
            'peso': it.peso,
            'status': it.status,
            'criado_em': it.criado_em.isoformat()
        })
    return jsonify(out)


@app.route('/carregamentos/<string:cid>', methods=['GET'])
@auth_required
def obter_carregamento(cid):
    user = g.current_user
    it = Carregamento.query.filter_by(id=cid, usuario_id=user.id).first()
    if not it:
        return jsonify({'error': 'nao encontrado'}), 404
    return jsonify({
        'id': it.id,
        'placa': it.placa,
        'produto': it.produto,
        'peso': it.peso,
        'status': it.status,
        'criado_em': it.criado_em.isoformat()
    })


# ---------------- DELETE CORRIGIDO ----------------
@app.route("/carregamentos/<string:id>", methods=["DELETE"])
@auth_required
def deletar_carregamento(id):
    user = g.current_user
    carregamento = Carregamento.query.filter_by(id=id, usuario_id=user.id).first()
    if not carregamento:
        return jsonify({"message": "Carregamento não encontrado"}), 404

    db.session.delete(carregamento)
    db.session.commit()
    return jsonify({"message": "Carregamento deletado com sucesso!"}), 200


# ---------------- INICIALIZAÇÃO ----------------
def seed_data():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='transp1').first():
            u = User(username='transp1', password='senha123')
            db.session.add(u)
            db.session.commit()
            print('Usuário de teste criado: transp1 / senha123')


if __name__ == '__main__':
    seed_data()
    print(f'Rodando mock SISFER API na porta {APP_PORT} (db: {DB_FILE})')
    app.run(host='0.0.0.0', port=APP_PORT, debug=True)
