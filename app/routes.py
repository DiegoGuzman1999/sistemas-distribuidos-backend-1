from flask import Blueprint, request, jsonify, session
from app.models import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'servicio': 'autenticacion'}), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return jsonify({'error': 'Usuario y contrasena son requeridos'}), 400

    usuario = Usuario.query.filter_by(username=username, password=password).first()

    if not usuario:
        return jsonify({'error': 'Credenciales incorrectas'}), 401

    session['usuario_id'] = usuario.id
    session['username'] = usuario.username
    session['rol'] = usuario.rol

    return jsonify({
        'mensaje': 'Login exitoso',
        'username': usuario.username,
        'rol': usuario.rol
    }), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'mensaje': 'Sesion cerrada correctamente'}), 200

@auth_bp.route('/verificar', methods=['GET'])
def verificar():
    if 'usuario_id' not in session:
        return jsonify({'autenticado': False}), 401
    return jsonify({
        'autenticado': True,
        'username': session.get('username'),
        'rol': session.get('rol')
    }), 200
