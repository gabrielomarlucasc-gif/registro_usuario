import re
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash

app = Flask(__name__)

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
usuarios = {}  # almacenamiento en memoria, solo para el laboratorio


def validar_password(password: str) -> list:
    errores = []
    if len(password) < 8:
        errores.append("debe tener al menos 8 caracteres")
    if not re.search(r"[A-Z]", password):
        errores.append("debe incluir una mayúscula")
    if not re.search(r"[a-z]", password):
        errores.append("debe incluir una minúscula")
    if not re.search(r"\d", password):
        errores.append("debe incluir un número")
    if not re.search(r"[^\w\s]", password):
        errores.append("debe incluir un símbolo")
    return errores


@app.post("/registro_usuario")
def registro_usuario():
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        return jsonify({"ok": False, "errores": ["Se esperaba un cuerpo JSON"]}), 400

    email = str(datos.get("email", "")).strip().lower()
    password = str(datos.get("password", ""))

    errores = []
    if not EMAIL_RE.match(email):
        errores.append("El email no es válido")
    errores += [f"La contraseña {e}" for e in validar_password(password)]

    if errores:
        return jsonify({"ok": False, "errores": errores}), 422
    if email in usuarios:
        return jsonify({"ok": False, "errores": ["El email ya está registrado"]}), 409

    usuarios[email] = generate_password_hash(password)
    return jsonify({"ok": True, "mensaje": "Usuario registrado", "email": email}), 201


if __name__ == "__main__":
    app.run(debug=True)