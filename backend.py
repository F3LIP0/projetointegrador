from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'stockcenter',
    'port': 3306
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Rota de login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    nome_user = data.get('nome_user')
    senha = data.get('senha')
    
    if not nome_user or not senha:
        return jsonify({"message": "Nome de usuário e senha são obrigatórios!"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM Usuarios WHERE nome_user = %s AND senha = %s"
    cursor.execute(query, (nome_user, senha))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if usuario:
        return jsonify({"message": "Login bem-sucedido!", "perfil": usuario['perfil'], "id_user": usuario['id_user']})
    else:
        return jsonify({"message": "Credenciais inválidas!"}), 401

# Rota para adicionar um item
@app.route('/itens', methods=['POST'])
def adicionar_item():
    data = request.json
    required_fields = ['codigo_barras', 'nome_item', 'descricao', 'quantidade', 'id_local']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Todos os campos são obrigatórios!"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO Itens (codigo_barras, nome_item, descricao, quantidade, id_local) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (data['codigo_barras'], data['nome_item'], data['descricao'], data['quantidade'], data['id_local']))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Item adicionado com sucesso!"}), 201

# Rota para deletar um item
@app.route('/itens/<int:item_id>', methods=['DELETE'])
def deletar_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM Itens WHERE id_item = %s"
    cursor.execute(query, (item_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Item deletado com sucesso!"}), 200

# Rota para atualizar quantidade de um item
@app.route('/itens/<int:item_id>/quantidade', methods=['PATCH'])
def diminuir_quantidade(item_id):
    data = request.json
    quantidade = data.get('quantidade')
    if not isinstance(quantidade, int) or quantidade <= 0:
        return jsonify({"message": "Quantidade deve ser um número positivo!"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE Itens SET quantidade = quantidade - %s WHERE id_item = %s"
    cursor.execute(query, (quantidade, item_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Quantidade atualizada com sucesso!"}), 200

# Rota para mover um item para outro local
@app.route('/itens/mover/<int:item_id>', methods=['PUT'])
def mover_item(item_id):
    data = request.json
    id_local = data.get('id_local')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE Itens SET id_local = %s WHERE id_item = %s"
    cursor.execute(query, (id_local, item_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Item movido com sucesso!"}), 200

# Rota para adicionar um local
@app.route('/locais', methods=['POST'])
def adicionar_local():
    data = request.json
    nome_local = data.get('nome_local')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO Locais (nome_local) VALUES (%s)"
    cursor.execute(query, (nome_local,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Local adicionado com sucesso!"}), 201

# Rota para listar todos os itens
@app.route('/itens', methods=['GET'])
def listar_itens():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Itens")
    itens = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(itens)

# Rota para listar todos os locais
@app.route('/locais', methods=['GET'])
def listar_locais():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Locais")
    locais = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(locais)

# Rota para listar todos os usuários
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(usuarios)

# Rota para listar logs de auditoria
@app.route('/logs', methods=['GET'])
def listar_logs():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM logs_auditoria")
    logs = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(logs)

# Rota para listar movimentações
@app.route('/movimentacoes', methods=['GET'])
def listar_movimentacoes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM movimentacoes")
    movimentacoes = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(movimentacoes)

if __name__ == '__main__':
    app.run(debug=True)
