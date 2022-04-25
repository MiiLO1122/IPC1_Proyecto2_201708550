import random
import re
from flask import Flask, jsonify, request  # librerias
from datetime import date

app = Flask(__name__)

usuarios = []
libros = []
prestamos = []


@app.route('/')
def index():
    diccionario_envio = {
        "msg": 'Servidor funcionando correctamente',
        "status": 200
    }
    return jsonify(diccionario_envio)


# CREAR USUARIOS
@app.route('/user', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    if data.get('id') == "" or data.get('id') == " ":
        return jsonify({
            "msg": 'Por favor ingrese un ID para el usuario',
            "status": 444
        })
    for a in usuarios:
        if a.get('id') == data.get("id"):
            return jsonify({
                "msg": 'El ID ingresado ya existe',
                "status": 444
            })
        if a.get('nickname') == data.get("nickname"):
            return jsonify({
                "msg": 'El usuario ya esta registrado',
                "status": 444
            })
    usuarios.append(data)
    return jsonify({
        "msg": 'Usuario creado exitosamente',
        "status": 200
    })

# VER USUARIOS


@app.route("/user/:id", methods=['GET'])
def ver_usuarios():
    id = request.args.get('id')
    for i in range(len(usuarios)):
        if usuarios[i].get('id') == id:
            datos = usuarios[i]
            return jsonify(datos)

    return jsonify({
        "msg": 'Usuario no encontrado',
        "status": 400
    })


# MODIFICAR USUARIOS
@app.route('/user', methods=['PUT'])
def actualizar_usuarios():
    data = request.get_json()
    id = data.get('id')
    name = data.get('name')
    nickname = data.get('nickname')
    password = data.get('password')
    rol = data.get('rol')
    available = data.get('available')

    for i in range(len(usuarios)):
        if usuarios[i].get('id') == id:
            usuarios[i]['name'] = name
            usuarios[i]['nickname'] = nickname
            usuarios[i]['password'] = password
            usuarios[i]['rol'] = rol
            usuarios[i]['available'] = available
            return jsonify({
                "msg": "Usuario modificado exitosamente",
                "status": 201
            })
    return jsonify({
        "msg": "Usuario no encontrado",
        "status": 400
    })


# CREAR BIBLIOGRAFIAS
@app.route('/book', methods=['POST'])
def crear_libro():
    data = request.get_json()
    for i in range(len(data)):
        coincidencia = True
        for y in range(len(data)):
            if data[i].get('id_book') == data[y].get("id_book") and i != y:
                coincidencia = False
        if coincidencia == False:
            return jsonify(
                {
                    "msg": "No se pudo crear la bibliografia porque el ID ya existe",
                    "status": 405
                })
    if len(libros) > 0:
        for i in range(len(libros)):
            for y in range(len(data)):
                if libros[i].get('id_book') == data[y].get('id_book') and i != y:
                    return jsonify(
                        {
                            "msg": "No se pudo crear la bibliografia porque el ID ya existe",
                            "status": 405
                        })
    for libro in data:
        libros.append(libro)
    return jsonify(
        {
            "msg": "Bibliografia creada exitosamente",
            "status": 200
        })


# MODIFICAR BIBLIOGRAFIAS
@app.route("/book", methods=["PUT"])
def actualizar_libros():
    data = request.get_json()
    id = data.get('id_book')
    autor = data.get('book_author')
    titulo = data.get('book_title')
    edicion = data.get('book_edition')
    editorial = data.get('book_editorial')
    año = data.get('book_year')
    descripcion = data.get('book_description')
    copiasD = data.get('book_available_copies')
    copiasND = data.get('book_unavailable_copies')
    copias = data.get('book_copies')

    for i in range(len(libros)):
        if libros[i].get('id_book') == id:
            libros[i]['book_author'] = autor
            libros[i]['book_title'] = titulo
            libros[i]['book_edition'] = edicion
            libros[i]['book_editorial'] = editorial
            libros[i]['book_year'] = año
            libros[i]['book_description'] = descripcion
            libros[i]['book_available_copies'] = copiasD
            libros[i]['book_unavailable_copies'] = copiasND
            libros[i]['book_copies'] = copias
            return jsonify({
                "msg": "Bibliografia modificada exitosamente",
                "status": 201
            }
            )
        return jsonify({
            "msg": "Bibliografia no encontrada",
            "status": 404
        })


# ELIMINAR BIBLIOGRAFIAS
@app.route("/book/:id", methods=["DELETE"])
def eliminar_bibliografia():
    id = request.args.get("id")
    for i in range(len(libros)):
        if libros[i].get('id_book') == id:
            libros.pop(i)
            return jsonify(
                {
                    "msg": "Bibliografia eliminada exitosamente",
                    "status": 200
                })
    return jsonify(
        {
            "msg": "Bibliografia no encontrada",
            "status": 404
        })

# VER BIBLIOGRAFIAS


@app.route("/book", methods=["GET"])
def ver_libro():
    salida = []
    autor = request.args.get("autor")
    titulo = request.args.get("titulo")
    for libro in libros:
        if libro.get("book_author") == autor or libro.get("book_title") == titulo:
            salida.append(libro)
    if len(salida) > 0:
        return jsonify(salida)
    else:
        return jsonify(
            {
                "msg": "No se encontró ninguna coincidencia",
                "status": 404
            }
        )


# PRESTAR BIBLIOGRAFIAS
@app.route("/borrow", methods=["POST"])
def prestar():
    data = request.get_json()
    id_user = data.get("id_user")
    id_book = data.get('id_book')
    idP = random.randint(999, 9999)
    for p in prestamos:
        if p.get("id_borrow") == str(idP):
            prestar()
    fecha = str(date.today())
    for i in range(len(libros)):
        if libros[i].get('id_book') == id_book:
            x = i
        if libros[i].get('book_available_copies') == 0:
            return jsonify(
                {
                    "msg": "El libro no esta disponible",
                    "status": 444
                }
            )
    for j in range(len(usuarios)):
        if usuarios[j].get('id') == id_user:
            if usuarios[j].get('available') == False:
                return jsonify(
                    {"msg": "El usuario no tiene la opcion de prestamos habilitada",
                        "status": 444
                     })
            else:
                libros[x]["book_available_copies"] = libros[x].get(
                    'book_available_copies')-1
                libros[x]["book_unavailable_copies"] = libros[x].get(
                    'book_available_copies')+1
                infoP = {"id_borrow": str(idP), "borrow_date": fecha,
                         "returned": False, "borrow_book": libros[x]}
                prestamos.append(infoP)
                print(prestamos)
                return{
                    "msg": "Prestamo realizado con exito, ID: "+str(idP),
                    "status": 200
                }
        return jsonify(
            {
                "msg": "No fue posible crear el prestamo, verifique que el ID del libro y del Usuario existan",
                "status": 444
            })


# Ver Prestamo
@app.route("/borrow/:id", methods=['GET'])
def ver_prestamo():
    id = request.args.get('id')
    for i in range(len(prestamos)):
        if prestamos[i].get('id_borrow') == id:
            datos = prestamos[i]
            return jsonify(datos)
    return jsonify({
        "msg": 'Prestamo buscado no encontrado',
        "status": 404
    })

# Devolver libros


@app.route("/borrow/:id", methods=['PUT'])
def devolver_libros():
    id = request.args.get('id')
    for i in range(len(prestamos)):
        if prestamos[i].get('id_borrow') == id:
            if prestamos[i].get('returned') == False:
                libroP = prestamos[i].get('borrow_book')
                for j in range(len(libros)):
                    if libros[j].get('id_book') == libroP.get('id_book'):
                        libros[j]['book_available_copies'] = libros[j].get(
                            'book_available_copies')+1
                        libros[j]['book_unavailable_copies'] = libros[j].get(
                            'book_unavailable_copies')-1
                prestamos[i]['returned'] = True
                return jsonify({
                    "msg": "Prestamo devuelto con exito",
                    "status": 202
                })
            elif prestamos[i].get('returned') == True:
                return jsonify({
                    "msg": "Le libro ya ha sido devuelto previamente",
                    "status": 202
                })
    return jsonify({
        "msg": "No existe prestamo vinculado al ID: "+str(id),
        "status": 202
    })

# REPORTES
@app.route('/reportes', methods=['GET'])
def reportes():
    data = request.args.get("Reportar")
    if data == "usuarios" or data == "Usuarios" or data == "USUARIOS":
        return jsonify(usuarios)
    elif data == "bibliografias" or data == "Bibliografias" or data == "BIBLIOGRAFIAS":
        return jsonify(libros)
    elif data == "pretamos" or data == "Pretamos" or data == "PRESTAMOS":
        return jsonify (prestamos)
    elif data == "prestamos devueltos" or data == "Pretamos Devueltos" or data == "PRESTAMOS DEVUELTOS":
        info = []
        for p in prestamos:
            if p.get('returned')== True:
                p.append
        return jsonify (p)
    elif data == "pretamos pendientes" or data == "Pretamos Pendientes" or data == "PRESTAMOS PENDIENTES":
        info = []
        for p in prestamos:
            if p.get('returned')== False:
                p.append
        return jsonify (p)
    else:
        return jsonify(
            {
                "msg": "Por favor seleccione entre Usuarios, Bibliografías, Prestamos, Prestamos Devueltos, Prestamos Pendientes",
                "status": 202
            }
        )
if __name__ == '__main__':
    app.run(port=3004, debug=True)
    