from app import app, usuarios


def cliente():
    usuarios.clear()
    return app.test_client()


def test_registro_exitoso():
    r = cliente().post("/registro_usuario",
                       json={"email": "ana@correo.com", "password": "Clave#2026"})
    assert r.status_code == 201 and r.get_json()["ok"] is True


def test_email_invalido():
    r = cliente().post("/registro_usuario",
                       json={"email": "ana@correo", "password": "Clave#2026"})
    assert r.status_code == 422


def test_password_debil():
    r = cliente().post("/registro_usuario",
                       json={"email": "ana@correo.com", "password": "12345"})
    assert r.status_code == 422


def test_email_duplicado():
    c = cliente()
    datos = {"email": "ana@correo.com", "password": "Clave#2026"}
    c.post("/registro_usuario", json=datos)
    assert c.post("/registro_usuario", json=datos).status_code == 409

def test_email_vacio():
    datos = {"email": "", "password": "Clave#2026"}
    r = cliente().post("/registro_usuario", json=datos)
    assert r.status_code == 422