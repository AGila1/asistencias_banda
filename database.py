"""
Módulo para la gestión de la base de datos de asistencias
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import os


class Database:
    def __init__(self, db_path: str = "asistencias.db"):
        """Inicializa la conexión con la base de datos"""
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        """Crea una conexión a la base de datos"""
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Inicializa las tablas de la base de datos"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Tabla de miembros
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS miembros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellidos TEXT,
                instrumento TEXT,
                email TEXT,
                telefono TEXT,
                activo BOOLEAN DEFAULT 1,
                fecha_alta DATE DEFAULT CURRENT_DATE
            )
        ''')

        # Tabla de eventos (ensayos y actuaciones)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL CHECK(tipo IN ('ensayo', 'actuacion')),
                fecha DATE NOT NULL,
                descripcion TEXT,
                lugar TEXT,
                importe REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabla de asistencias
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS asistencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                miembro_id INTEGER NOT NULL,
                evento_id INTEGER NOT NULL,
                asistio BOOLEAN NOT NULL,
                observaciones TEXT,
                FOREIGN KEY (miembro_id) REFERENCES miembros(id),
                FOREIGN KEY (evento_id) REFERENCES eventos(id),
                UNIQUE(miembro_id, evento_id)
            )
        ''')

        conn.commit()
        conn.close()

    # ===== GESTIÓN DE MIEMBROS =====

    def agregar_miembro(self, nombre: str, apellidos: str = "", instrumento: str = "",
                       email: str = "", telefono: str = "") -> int:
        """Agrega un nuevo miembro a la banda"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO miembros (nombre, apellidos, instrumento, email, telefono)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, apellidos, instrumento, email, telefono))
        miembro_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return miembro_id

    def obtener_miembros(self, solo_activos: bool = True) -> List[Dict]:
        """Obtiene la lista de miembros"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if solo_activos:
            cursor.execute('SELECT * FROM miembros WHERE activo = 1 ORDER BY nombre')
        else:
            cursor.execute('SELECT * FROM miembros ORDER BY nombre')

        miembros = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return miembros

    def obtener_miembro(self, miembro_id: int) -> Optional[Dict]:
        """Obtiene un miembro por su ID"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM miembros WHERE id = ?', (miembro_id,))
        miembro = cursor.fetchone()
        conn.close()
        return dict(miembro) if miembro else None

    def actualizar_miembro(self, miembro_id: int, nombre: str, apellidos: str = "",
                          instrumento: str = "", email: str = "", telefono: str = ""):
        """Actualiza los datos de un miembro"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE miembros
            SET nombre = ?, apellidos = ?, instrumento = ?, email = ?, telefono = ?
            WHERE id = ?
        ''', (nombre, apellidos, instrumento, email, telefono, miembro_id))
        conn.commit()
        conn.close()

    def eliminar_miembro(self, miembro_id: int):
        """Desactiva un miembro (no lo borra físicamente)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE miembros SET activo = 0 WHERE id = ?', (miembro_id,))
        conn.commit()
        conn.close()

    def reactivar_miembro(self, miembro_id: int):
        """Reactiva un miembro previamente desactivado"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE miembros SET activo = 1 WHERE id = ?', (miembro_id,))
        conn.commit()
        conn.close()

    # ===== GESTIÓN DE EVENTOS =====

    def agregar_evento(self, tipo: str, fecha: str, descripcion: str = "",
                      lugar: str = "", importe: float = 0) -> int:
        """Agrega un nuevo evento (ensayo o actuación)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO eventos (tipo, fecha, descripcion, lugar, importe)
            VALUES (?, ?, ?, ?, ?)
        ''', (tipo, fecha, descripcion, lugar, importe))
        evento_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return evento_id

    def obtener_eventos(self, tipo: Optional[str] = None) -> List[Dict]:
        """Obtiene la lista de eventos"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if tipo:
            cursor.execute('SELECT * FROM eventos WHERE tipo = ? ORDER BY fecha DESC', (tipo,))
        else:
            cursor.execute('SELECT * FROM eventos ORDER BY fecha DESC')

        eventos = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return eventos

    def obtener_evento(self, evento_id: int) -> Optional[Dict]:
        """Obtiene un evento por su ID"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM eventos WHERE id = ?', (evento_id,))
        evento = cursor.fetchone()
        conn.close()
        return dict(evento) if evento else None

    def actualizar_evento(self, evento_id: int, tipo: str, fecha: str,
                         descripcion: str = "", lugar: str = "", importe: float = 0):
        """Actualiza un evento"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE eventos
            SET tipo = ?, fecha = ?, descripcion = ?, lugar = ?, importe = ?
            WHERE id = ?
        ''', (tipo, fecha, descripcion, lugar, importe, evento_id))
        conn.commit()
        conn.close()

    def eliminar_evento(self, evento_id: int):
        """Elimina un evento y sus asistencias"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM asistencias WHERE evento_id = ?', (evento_id,))
        cursor.execute('DELETE FROM eventos WHERE id = ?', (evento_id,))
        conn.commit()
        conn.close()

    # ===== GESTIÓN DE ASISTENCIAS =====

    def registrar_asistencia(self, miembro_id: int, evento_id: int,
                           asistio: bool, observaciones: str = ""):
        """Registra la asistencia de un miembro a un evento"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO asistencias (miembro_id, evento_id, asistio, observaciones)
            VALUES (?, ?, ?, ?)
        ''', (miembro_id, evento_id, asistio, observaciones))
        conn.commit()
        conn.close()

    def obtener_asistencias_evento(self, evento_id: int) -> List[Dict]:
        """Obtiene todas las asistencias de un evento específico"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.*, m.nombre, m.apellidos, m.instrumento
            FROM asistencias a
            JOIN miembros m ON a.miembro_id = m.id
            WHERE a.evento_id = ?
            ORDER BY m.nombre
        ''', (evento_id,))
        asistencias = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return asistencias

    def obtener_asistencias_miembro(self, miembro_id: int) -> List[Dict]:
        """Obtiene todas las asistencias de un miembro específico"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.*, e.tipo, e.fecha, e.descripcion, e.importe
            FROM asistencias a
            JOIN eventos e ON a.evento_id = e.id
            WHERE a.miembro_id = ?
            ORDER BY e.fecha DESC
        ''', (miembro_id,))
        asistencias = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return asistencias

    # ===== CÁLCULOS DE PAGOS =====

    def calcular_pago_miembro(self, miembro_id: int) -> Dict:
        """
        Calcula el pago total de un miembro:
        - Suma de importes de actuaciones a las que asistió (dividido entre asistentes)
        - Resta 0.50€ por cada ensayo NO asistido
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        # Obtener actuaciones asistidas
        cursor.execute('''
            SELECT e.id, e.importe
            FROM asistencias a
            JOIN eventos e ON a.evento_id = e.id
            WHERE a.miembro_id = ? AND a.asistio = 1 AND e.tipo = 'actuacion'
        ''', (miembro_id,))
        actuaciones_asistidas = cursor.fetchall()

        total_actuaciones = 0
        for actuacion_id, importe in actuaciones_asistidas:
            # Contar cuántos asistieron a esta actuación
            cursor.execute('''
                SELECT COUNT(*) FROM asistencias
                WHERE evento_id = ? AND asistio = 1
            ''', (actuacion_id,))
            num_asistentes = cursor.fetchone()[0]

            if num_asistentes > 0:
                total_actuaciones += importe / num_asistentes

        # Contar ensayos NO asistidos
        cursor.execute('''
            SELECT COUNT(*)
            FROM asistencias a
            JOIN eventos e ON a.evento_id = e.id
            WHERE a.miembro_id = ? AND a.asistio = 0 AND e.tipo = 'ensayo'
        ''', (miembro_id,))
        ensayos_no_asistidos = cursor.fetchone()[0]

        penalizacion = ensayos_no_asistidos * 0.50
        total_final = total_actuaciones - penalizacion

        conn.close()

        return {
            'total_actuaciones': round(total_actuaciones, 2),
            'ensayos_no_asistidos': ensayos_no_asistidos,
            'penalizacion': round(penalizacion, 2),
            'total_final': round(total_final, 2)
        }

    def obtener_resumen_pagos(self) -> List[Dict]:
        """Obtiene el resumen de pagos de todos los miembros activos"""
        miembros = self.obtener_miembros(solo_activos=True)
        resumen = []

        for miembro in miembros:
            pago = self.calcular_pago_miembro(miembro['id'])
            resumen.append({
                'miembro_id': miembro['id'],
                'nombre': miembro['nombre'],
                'apellidos': miembro['apellidos'],
                'instrumento': miembro['instrumento'],
                **pago
            })

        # Ordenar por total final descendente
        resumen.sort(key=lambda x: x['total_final'], reverse=True)
        return resumen

    # ===== ESTADÍSTICAS =====

    def obtener_estadisticas_miembro(self, miembro_id: int) -> Dict:
        """Obtiene estadísticas de asistencia de un miembro"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Total de eventos
        cursor.execute('''
            SELECT COUNT(*) FROM asistencias WHERE miembro_id = ?
        ''', (miembro_id,))
        total_eventos = cursor.fetchone()[0]

        # Asistencias totales
        cursor.execute('''
            SELECT COUNT(*) FROM asistencias
            WHERE miembro_id = ? AND asistio = 1
        ''', (miembro_id,))
        total_asistencias = cursor.fetchone()[0]

        # Ensayos
        cursor.execute('''
            SELECT COUNT(*)
            FROM asistencias a
            JOIN eventos e ON a.evento_id = e.id
            WHERE a.miembro_id = ? AND e.tipo = 'ensayo'
        ''', (miembro_id,))
        total_ensayos = cursor.fetchone()[0]

        cursor.execute('''
            SELECT COUNT(*)
            FROM asistencias a
            JOIN eventos e ON a.evento_id = e.id
            WHERE a.miembro_id = ? AND e.tipo = 'ensayo' AND a.asistio = 1
        ''', (miembro_id,))
        ensayos_asistidos = cursor.fetchone()[0]

        # Actuaciones
        cursor.execute('''
            SELECT COUNT(*)
            FROM asistencias a
            JOIN eventos e ON a.evento_id = e.id
            WHERE a.miembro_id = ? AND e.tipo = 'actuacion'
        ''', (miembro_id,))
        total_actuaciones = cursor.fetchone()[0]

        cursor.execute('''
            SELECT COUNT(*)
            FROM asistencias a
            JOIN eventos e ON a.evento_id = e.id
            WHERE a.miembro_id = ? AND e.tipo = 'actuacion' AND a.asistio = 1
        ''', (miembro_id,))
        actuaciones_asistidas = cursor.fetchone()[0]

        conn.close()

        porcentaje_general = (total_asistencias / total_eventos * 100) if total_eventos > 0 else 0
        porcentaje_ensayos = (ensayos_asistidos / total_ensayos * 100) if total_ensayos > 0 else 0
        porcentaje_actuaciones = (actuaciones_asistidas / total_actuaciones * 100) if total_actuaciones > 0 else 0

        return {
            'total_eventos': total_eventos,
            'total_asistencias': total_asistencias,
            'porcentaje_general': round(porcentaje_general, 2),
            'total_ensayos': total_ensayos,
            'ensayos_asistidos': ensayos_asistidos,
            'porcentaje_ensayos': round(porcentaje_ensayos, 2),
            'total_actuaciones': total_actuaciones,
            'actuaciones_asistidas': actuaciones_asistidas,
            'porcentaje_actuaciones': round(porcentaje_actuaciones, 2)
        }
