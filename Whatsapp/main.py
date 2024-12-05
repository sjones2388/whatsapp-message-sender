from flask import Flask, request, jsonify, render_template
import os
from scripts.whatsapp import get_connected_devices, enviar_mensaje

# Configuración inicial
app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

# Subir archivo Excel
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No se subió ningún archivo."}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    return jsonify({"message": "Archivo subido correctamente.", "filepath": filepath})

# Identificar dispositivos conectados
@app.route('/devices', methods=['GET'])
def devices():
    devices = get_connected_devices()
    if not devices:
        return jsonify({"error": "No se encontraron dispositivos conectados."}), 404
    return jsonify({"devices": devices})

# Enviar mensajes
@app.route('/send', methods=['POST'])
def send_messages():
    data = request.json
    filepath = data.get('filepath')
    message_template = data.get('message_template')
    devices = data.get('devices')

    if not filepath or not os.path.exists(filepath):
        return jsonify({"error": "Archivo no encontrado."}), 400
    if not message_template:
        return jsonify({"error": "Plantilla de mensaje no proporcionada."}), 400
    if not devices:
        return jsonify({"error": "No se seleccionaron dispositivos."}), 400

    try:
        enviar_mensaje(filepath, message_template, devices)
        return jsonify({"message": "Mensajes enviados correctamente."})
    except Exception as e:
        return jsonify({"error": f"Error al enviar mensajes: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
