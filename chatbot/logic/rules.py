# --- INICIO DEL PARCHE DE COMPATIBILIDAD PARA PYTHON 3.10+ ---
import collections
import collections.abc
collections.Mapping = collections.abc.Mapping
collections.Iterable = collections.abc.Iterable
collections.Sequence = collections.abc.Sequence
collections.MutableMapping = collections.abc.MutableMapping
# --- FIN DEL PARCHE ---

# logic/rules.py
from experta import *

# --- 1. Definición de la Ontología ---
class Alumno(Fact):
    """Almacena el estado de las materias del alumno (ej: materia_101='regular')"""
    pass

class Consulta(Fact):
    """Almacena lo que el alumno quiere hacer (ej: intencion='cursar', materia='103')"""
    pass

class Respuesta(Fact):
    """La salida del motor: puede ser el veredicto final o una petición de más información"""
    pass

# --- 2. El Motor de Conocimiento ---
class MotorCorrelativas(KnowledgeEngine):
    
    @DefFacts()
    def _iniciar_evaluacion(self):
        """Inicia el ciclo del motor"""
        yield Fact(accion="evaluar")

    # =========================================================
    # REGLAS PARA LA MATERIA 103 (Algoritmos II)
    # Correlativa para cursar: 101 (Regularizada) [cite: 4]
    # =========================================================

    # CASO A: si faltan datos en el entorno (El motor necesita preguntar)
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="103"),
        NOT(Alumno(materia_101=W())) # W() detecta si existe o no el campo materia_101
    )
    def requerir_info_101_para_103(self):
        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="103",
            materia_requisito="101",
            nombre_requisito="Algoritmos y Estructuras de Datos I",
            opciones=["regular", "aprobada", "ninguna"],
            mensaje="Para saber si puedes cursar Algoritmos II (103), necesito saber: ¿Cuál es tu estado actual en Algoritmos y Estructuras de Datos I (101)?"
        ))

    # CASO B: Tiene los requisitos cumplidos
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="103"),
        OR(Alumno(materia_101="regular"), Alumno(materia_101="aprobada"))
    )
    def puede_cursar_103(self):
        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            mensaje="Estás en condiciones de cursar Algoritmos y Estructuras de Datos II (103). Cumples con la correlatividad de la materia 101."
        ))

    # CASO C: No tiene los requisitos cumplidos
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="103"),
        Alumno(materia_101="ninguna")
    )
    def no_puede_cursar_103(self):
        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            mensaje="❌ No puedes cursar Algoritmos II (103). El plan de estudios exige tener regularizada Algoritmos I (101)."
        ))

# =========================================================
    # REGLAS PARA LA MATERIA 303 (Ingeniería de Software I)
    # Correlativas para cursar: 204 y 206 (Regularizadas)
    # =========================================================

    # CASO A1: Falta el estado de la materia 204
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="303"),
        NOT(Alumno(materia_204=W()))
    )
    def requerir_info_204_para_303(self):
        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="303",
            materia_requisito="204",
            opciones=["regular", "aprobada", "ninguna"],
            mensaje="Para cursar Ingeniería de Software I (303), primero necesito saber: ¿Cuál es tu estado en Programación Orientada a Objetos (204)?"
        ))

    # CASO A2: Ya sabemos que tiene la 204 (regular o aprobada), pero falta la 206
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="303"),
        OR(Alumno(materia_204="regular"), Alumno(materia_204="aprobada")),
        NOT(Alumno(materia_206=W()))
    )
    def requerir_info_206_para_303(self):
        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="303",
            materia_requisito="206",
            opciones=["regular", "aprobada", "ninguna"],
            mensaje="Excelente, cumples con la 204. Ahora, ¿Cuál es tu estado en Administración y Gestión de Organizaciones (206)?"
        ))

    # CASO B: Tiene AMBAS materias cumplidas (La conjunción Lógica AND)
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="303"),
        OR(Alumno(materia_204="regular"), Alumno(materia_204="aprobada")),
        OR(Alumno(materia_206="regular"), Alumno(materia_206="aprobada"))
    )
    def puede_cursar_303(self):
        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            mensaje="Estás en condiciones de cursar Ingeniería de Software I (303). Cumples con las correlatividades de la 204 y la 206."
        ))

    # CASO C: Falla en la 204 (No importa la 206, ya no puede cursar)
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="303"),
        Alumno(materia_204="ninguna")
    )
    def falla_204_para_303(self):
        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            mensaje="No puedes cursar Ingeniería de Software I (303) porque te falta regularizar Programación Orientada a Objetos (204)."
        ))

    # CASO D: Falla en la 206 (Incluso si tiene la 204)
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="303"),
        OR(Alumno(materia_204="regular"), Alumno(materia_204="aprobada")),
        Alumno(materia_206="ninguna")
    )
    def falla_206_para_303(self):
        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            mensaje="No puedes cursar Ingeniería de Software I (303). Tienes la 204, pero te falta regularizar Administración y Gestión de Organizaciones (206)."
        ))