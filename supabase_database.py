"""
Módulo para la gestión de la base de datos de asistencias usando Supabase
Reemplaza el adapter SQLite con PostgreSQL en Supabase
"""
from supabase import create_client, Client
from datetime import datetime
from typing import List, Dict, Optional
import os


class SupabaseDatabase:
    def __init__(self, url: str = None, key: str = None):
        """Inicializa la conexión con Supabase"""
        self.url = url or os.getenv("SUPABASE_URL")
        self.key = key or os.getenv("SUPABASE_KEY")

        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL y SUPABASE_KEY son requeridos")

        self.client: Client = create_client(self.url, self.key)
        self.init_db()

    def init_db(self):
        """Crea las tablas en Supabase si no existen"""
        # Las tablas se crean manualmente en Supabase para más control
        # Este método es un placeholder para compatibilidad
        pass

    # ===== GESTIÓN DE MIEMBROS =====

    def agregar_miembro(self, nombre: str, apellidos: str = "", instrumento: str = "",
                       email: str = "", telefono: str = "") -> int:
        """Agrega un nuevo miembro a la banda"""
        data = {
            "nombre": nombre,
            "apellidos": apellidos,
            "instrumento": instrumento,
            "email": email,
            "telefono": telefono,
            "activo": True,
            "fecha_alta": datetime.now().isoformat()
        }
        result = self.client.table("miembros").insert(data).execute()
        return result.data[0]['id'] if result.data else None

    def obtener_miembros(self, solo_activos: bool = True) -> List[Dict]:
        """Obtiene la lista de miembros"""
        query = self.client.table("miembros").select("*")

        if solo_activos:
            query = query.eq("activo", True)

        result = query.order("nombre").execute()
        return result.data if result.data else []

    def obtener_miembro(self, miembro_id: int) -> Optional[Dict]:
        """Obtiene un miembro por su ID"""
        result = self.client.table("miembros").select("*").eq("id", miembro_id).execute()
        return result.data[0] if result.data else None

    def actualizar_miembro(self, miembro_id: int, nombre: str, apellidos: str = "",
                          instrumento: str = "", email: str = "", telefono: str = ""):
        """Actualiza los datos de un miembro"""
        data = {
            "nombre": nombre,
            "apellidos": apellidos,
            "instrumento": instrumento,
            "email": email,
            "telefono": telefono
        }
        self.client.table("miembros").update(data).eq("id", miembro_id).execute()

    def eliminar_miembro(self, miembro_id: int):
        """Desactiva un miembro (soft delete)"""
        self.client.table("miembros").update({"activo": False}).eq("id", miembro_id).execute()

    def reactivar_miembro(self, miembro_id: int):
        """Reactiva un miembro previamente desactivado"""
        self.client.table("miembros").update({"activo": True}).eq("id", miembro_id).execute()

    # ===== GESTIÓN DE EVENTOS =====

    def agregar_evento(self, tipo: str, fecha: str, descripcion: str = "",
                      lugar: str = "", importe: float = 0) -> int:
        """Agrega un nuevo evento (ensayo o actuación)"""
        data = {
            "tipo": tipo,
            "fecha": fecha,
            "descripcion": descripcion,
            "lugar": lugar,
            "importe": importe,
            "created_at": datetime.now().isoformat()
        }
        result = self.client.table("eventos").insert(data).execute()
        return result.data[0]['id'] if result.data else None

    def obtener_eventos(self, tipo: Optional[str] = None) -> List[Dict]:
        """Obtiene la lista de eventos"""
        query = self.client.table("eventos").select("*")

        if tipo:
            query = query.eq("tipo", tipo)

        result = query.order("fecha", desc=True).execute()
        return result.data if result.data else []

    def obtener_evento(self, evento_id: int) -> Optional[Dict]:
        """Obtiene un evento por su ID"""
        result = self.client.table("eventos").select("*").eq("id", evento_id).execute()
        return result.data[0] if result.data else None

    def actualizar_evento(self, evento_id: int, tipo: str, fecha: str,
                         descripcion: str = "", lugar: str = "", importe: float = 0):
        """Actualiza un evento"""
        data = {
            "tipo": tipo,
            "fecha": fecha,
            "descripcion": descripcion,
            "lugar": lugar,
            "importe": importe
        }
        self.client.table("eventos").update(data).eq("id", evento_id).execute()

    def eliminar_evento(self, evento_id: int):
        """Elimina un evento y sus asistencias"""
        # Primero eliminar asistencias
        self.client.table("asistencias").delete().eq("evento_id", evento_id).execute()
        # Luego eliminar evento
        self.client.table("eventos").delete().eq("id", evento_id).execute()

    # ===== GESTIÓN DE ASISTENCIAS =====

    def registrar_asistencia(self, miembro_id: int, evento_id: int,
                           asistio: bool, observaciones: str = ""):
        """Registra la asistencia de un miembro a un evento"""
        # Primero intenta actualizar
        existing = self.client.table("asistencias").select("id").eq("miembro_id", miembro_id).eq("evento_id", evento_id).execute()

        data = {
            "miembro_id": miembro_id,
            "evento_id": evento_id,
            "asistio": asistio,
            "observaciones": observaciones
        }

        if existing.data:
            # Actualizar si existe
            self.client.table("asistencias").update(data).eq("miembro_id", miembro_id).eq("evento_id", evento_id).execute()
        else:
            # Insertar si no existe
            self.client.table("asistencias").insert(data).execute()

    def obtener_asistencias_evento(self, evento_id: int) -> List[Dict]:
        """Obtiene todas las asistencias de un evento específico"""
        result = self.client.table("asistencias").select(
            "id, miembro_id, evento_id, asistio, observaciones, miembros(nombre, apellidos, instrumento)"
        ).eq("evento_id", evento_id).order("miembros(nombre)").execute()

        # Flatten la estructura de datos
        data = result.data if result.data else []
        flattened = []
        for item in data:
            flat_item = {
                'id': item.get('id'),
                'miembro_id': item.get('miembro_id'),
                'evento_id': item.get('evento_id'),
                'asistio': item.get('asistio'),
                'observaciones': item.get('observaciones')
            }
            if item.get('miembros'):
                flat_item.update({
                    'nombre': item['miembros'].get('nombre'),
                    'apellidos': item['miembros'].get('apellidos'),
                    'instrumento': item['miembros'].get('instrumento')
                })
            flattened.append(flat_item)

        return flattened

    def obtener_asistencias_miembro(self, miembro_id: int) -> List[Dict]:
        """Obtiene todas las asistencias de un miembro específico"""
        result = self.client.table("asistencias").select(
            "id, miembro_id, evento_id, asistio, observaciones, eventos(tipo, fecha, descripcion, importe)"
        ).eq("miembro_id", miembro_id).order("eventos(fecha)", desc=True).execute()

        # Flatten la estructura de datos
        data = result.data if result.data else []
        flattened = []
        for item in data:
            flat_item = {
                'id': item.get('id'),
                'miembro_id': item.get('miembro_id'),
                'evento_id': item.get('evento_id'),
                'asistio': item.get('asistio'),
                'observaciones': item.get('observaciones')
            }
            if item.get('eventos'):
                flat_item.update({
                    'tipo': item['eventos'].get('tipo'),
                    'fecha': item['eventos'].get('fecha'),
                    'descripcion': item['eventos'].get('descripcion'),
                    'importe': item['eventos'].get('importe')
                })
            flattened.append(flat_item)

        return flattened

    # ===== CÁLCULOS DE PAGOS =====

    def calcular_pago_miembro(self, miembro_id: int) -> Dict:
        """
        Calcula el pago total de un miembro:
        - Suma de importes de actuaciones a las que asistió (dividido entre asistentes)
        - Resta 0.50€ por cada ensayo NO asistido
        """
        # Obtener actuaciones asistidas
        asistencias = self.client.table("asistencias").select(
            "evento_id, eventos(importe)"
        ).eq("miembro_id", miembro_id).eq("asistio", True).execute()

        total_actuaciones = 0.0

        for asistencia in asistencias.data:
            evento = asistencia.get('eventos')
            if evento:
                evento_id = asistencia.get('evento_id')
                importe = evento.get('importe', 0)

                # Contar cuántos asistieron a esta actuación
                contador = self.client.table("asistencias").select(
                    "id", count="exact"
                ).eq("evento_id", evento_id).eq("asistio", True).execute()

                num_asistentes = len(contador.data) if contador.data else 1
                if num_asistentes > 0:
                    total_actuaciones += importe / num_asistentes

        # Contar ensayos NO asistidos
        ensayos_no = self.client.table("asistencias").select(
            "id", count="exact"
        ).eq("miembro_id", miembro_id).eq("asistio", False).execute()

        ensayos_no_asistidos = len(ensayos_no.data) if ensayos_no.data else 0

        penalizacion = ensayos_no_asistidos * 0.50
        total_final = total_actuaciones - penalizacion

        return {
            'total_actuaciones': round(total_actuaciones, 2),
            'ensayos_no_asistidos': ensayos_no_asistidos,
            'penalizacion': round(penalizacion, 2),
            'total_final': round(total_final, 2)
        }
