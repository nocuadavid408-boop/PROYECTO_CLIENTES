# gestor_notas.py
notas = []

def crear_nota(tarea, fecha_inicio, fecha_final):
    nota = {
        'id': len(notas) + 1,
        'tarea': tarea,
        'fecha_inicio': fecha_inicio,
        'fecha_final': fecha_final,
        'estado': 'pendiente'
    }
    notas.append(nota)
    return nota

def ver_notas():
    return notas

def cambiar_estado(id_nota, nuevo_estado):
    for nota in notas:
        if nota['id'] == id_nota:
            nota['estado'] = nuevo_estado
            return True
    return False
