# --- PARCHE DE COMPATIBILIDAD PARA PYTHON 3.10+ ---
import collections
import collections.abc
collections.Mapping = collections.abc.Mapping
collections.Iterable = collections.abc.Iterable
collections.Sequence = collections.abc.Sequence
collections.MutableMapping = collections.abc.MutableMapping
# --- PARCHE ---

from experta import *
from .materias import nombre_materia


class Alumno(Fact):
    """Almacena el estado de las materias del alumno (materia_101='regular')"""
    pass

class Consulta(Fact):
    """Almacena lo que el alumno quiere hacer (intencion='cursar', materia='103')"""
    pass

class Respuesta(Fact):
    """La salida del motor: puede ser el veredicto final o una petición de más información"""
    pass


class MotorCorrelativas(KnowledgeEngine):

    @DefFacts()
    def _iniciar_evaluacion(self):
        yield Fact(accion="evaluar")

    # =========================
    # 101 Algoritmos y Estructuras de Datos I
    # =========================
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="101")
    )
    def m101(self, i):
        nombre = nombre_materia("101")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="101",
            mensaje=f"Podés {i} {nombre} (101). No tiene materias correlativas."
        ))

 # =========================
    # 102 Algebra
    # =========================
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="102")
    )
    def m102(self, i):
        nombre = nombre_materia("102")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="102",
            mensaje=f"Podés {i} {nombre} (102). No tiene materias correlativas."
        ))

    # =========================
    # 103 - Algoritmos y Estructuras de Datos II (requiere 101)
    # =========================

    # CASO A: Falta info para cursar o rendir
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="103"),
        NOT(Alumno(materia_101=W()))
    )
    def info_103(self, i):
        nombre = nombre_materia("103")
        req = nombre_materia("101")

        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="103",
            materia_requisito="101",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} {nombre} (103), necesito saber tu estado en {req} (101)."
        ))


    # =========================
    # CURSAR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="103"),
        OR(Alumno(materia_101="regular"), Alumno(materia_101="aprobada"))
    )
    def cursar_103_ok(self):
        nombre = nombre_materia("103")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="103",
            mensaje=f"Podés cursar {nombre} (103)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="103"),
        Alumno(materia_101="libre")
    )
    def cursar_103_no(self):
        nombre = nombre_materia("103")
        req = nombre_materia("101")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="103",
            mensaje=f"No podés cursar {nombre} (103). Debés regularizar {req} (101)."
        ))


    # =========================
    # RENDIR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="103"),
        Alumno(materia_101="aprobada")
    )
    def rendir_103_ok(self):
        nombre = nombre_materia("103")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="103",
            mensaje=f"Podés rendir {nombre} (103)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="103"),
        OR(Alumno(materia_101="regular"), Alumno(materia_101="libre"))
    )
    def rendir_103_no(self):
        nombre = nombre_materia("103")
        req = nombre_materia("101")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="103",
            mensaje=f"No podés rendir {nombre} (103). Debés tener aprobada {req} (101)."
        ))

    # =========================
    # 104 - Lógica y Matemática Computacional (requiere 102)
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="104"),
        NOT(Alumno(materia_102=W()))
    )
    def info_104(self, i):
        nombre = nombre_materia("104")
        req = nombre_materia("102")

        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="104",
            materia_requisito="102",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} {nombre} (104), necesito saber tu estado en {req} (102)."
        ))


    # =========================
    # CURSAR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="104"),
        OR(Alumno(materia_102="regular"), Alumno(materia_102="aprobada"))
    )
    def cursar_104_ok(self):
        nombre = nombre_materia("104")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="104",
            mensaje=f"Podés cursar {nombre} (104)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="104"),
        Alumno(materia_102="libre")
    )
    def cursar_104_no(self):
        nombre = nombre_materia("104")
        req = nombre_materia("102")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="104",
            mensaje=f"No podés cursar {nombre} (104). Necesitás regularizar {req} (102)."
        ))


    # =========================
    # RENDIR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="104"),
        Alumno(materia_102="aprobada")
    )
    def rendir_104_ok(self):
        nombre = nombre_materia("104")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="104",
            mensaje=f"Podés rendir {nombre} (104)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="104"),
        OR(Alumno(materia_102="regular"), Alumno(materia_102="libre"))
    )
    def rendir_104_no(self):
        nombre = nombre_materia("104")
        req = nombre_materia("102")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="104",
            mensaje=f"No podés rendir {nombre} (104). Necesitás tener aprobada {req} (102)."
        ))
        
    # =========================
    # 105 - Sistemas y Organizaciones
    # =========================
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="105")
    )
    def m105(self, i):
        nombre = nombre_materia("105")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="105",
            mensaje=f"Podés {i} {nombre} (105). No tiene materias correlativas."
        ))


    # =========================
    # 201 - Paradigmas y Lenguajes (requiere 103)
    # =========================

    # CASO A: falta info
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="201"),
        NOT(Alumno(materia_103=W()))
    )
    def info_201(self, i):
        nombre = nombre_materia("201")
        req = nombre_materia("103")

        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="201",
            materia_requisito="103",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} {nombre} (201), necesito saber tu estado en {req} (103)."
        ))


    # =========================
    # CURSAR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="201"),
        OR(Alumno(materia_103="regular"), Alumno(materia_103="aprobada"))
    )
    def cursar_201_ok(self):
        nombre = nombre_materia("201")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="201",
            mensaje=f"Podés cursar {nombre} (201)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="201"),
        Alumno(materia_103="libre")
    )
    def cursar_201_no(self):
        nombre = nombre_materia("201")
        req = nombre_materia("103")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="201",
            mensaje=f"No podés cursar {nombre} (201). Necesitás regularizar {req} (103)."
        ))


    # =========================
    # RENDIR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="201"),
        Alumno(materia_103="aprobada")
    )
    def rendir_201_ok(self):
        nombre = nombre_materia("201")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="201",
            mensaje=f"Podés rendir {nombre} (201)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="201"),
        OR(Alumno(materia_103="regular"), Alumno(materia_103="libre"))
    )
    def rendir_201_no(self):
        nombre = nombre_materia("201")
        req = nombre_materia("103")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="201",
            mensaje=f"No podés rendir {nombre} (201). Necesitás tener aprobada {req} (103)."
        ))

    # =========================
    # 201 - Paradigmas y Lenguajes (requiere 103)
    # =========================

    # CASO A: Falta información
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="201"),
        NOT(Alumno(materia_103=W()))
    )
    def info_201(self, i):
        nombre = nombre_materia("201")
        req = nombre_materia("103")

        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="201",
            materia_requisito="103",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} {nombre} (201), necesito saber tu estado en {req} (103)."
        ))


    # =========================
    # CURSAR
    # =========================

    # ✔ Puede cursar si tiene regular o aprobada la 103
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="201"),
        OR(
            Alumno(materia_103="regular"),
            Alumno(materia_103="aprobada")
        )
    )
    def cursar_201_ok(self):
        nombre = nombre_materia("201")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="201",
            mensaje=f"Podés cursar {nombre} (201)."
        ))


    # No puede cursar si la tiene libre
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="201"),
        Alumno(materia_103="libre")
    )
    def cursar_201_no(self):
        nombre = nombre_materia("201")
        req = nombre_materia("103")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="201",
            mensaje=f"No podés cursar {nombre} (201). Necesitás regularizar {req} (103)."
        ))


    # =========================
    # RENDIR
    # =========================

    # ✔ Puede rendir si tiene aprobada la 103
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="201"),
        Alumno(materia_103="aprobada")
    )
    def rendir_201_ok(self):
        nombre = nombre_materia("201")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="201",
            mensaje=f"Podés rendir {nombre} (201)."
        ))


    # No puede rendir si no está aprobada
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="201"),
        OR(
            Alumno(materia_103="regular"),
            Alumno(materia_103="libre")
        )
    )
    def rendir_201_no(self):
        nombre = nombre_materia("201")
        req = nombre_materia("103")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="201",
            mensaje=f"No podés rendir {nombre} (201). Necesitás tener aprobada {req} (103)."
        ))


   # =========================
    # 202 - Arquitectura y Organización de Computadoras (requiere 104 regular o aprobada y 101 aprobada para cursar)
    # (Para rendir, requiere 104 aprobada)
    # =========================

    # CASO A: Falta información
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="202"),
        NOT(Alumno(materia_104=W()))
    )
    def info_202_104(self, i):
        nombre = nombre_materia("202")
        req = nombre_materia("104")

        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="202",
            materia_requisito="104",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} {nombre} (202), necesito tu estado en {req} (104)."
        ))
    
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="202"),
        OR(
            Alumno(materia_104="regular"),
            Alumno(materia_104="aprobada")
        ),
        NOT(Alumno(materia_101=W()))
    )
    def info_202_101(self, i):
        nombre = nombre_materia("202")
        req = nombre_materia("101")

        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="202",
            materia_requisito="101",
            opciones=["aprobada", "regular", "libre"],
            mensaje=f"Para {i} {nombre} (202), también necesito tu estado en {req} (101)."
        ))


    # =========================
    # CURSAR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="202"),
        OR(
            Alumno(materia_104="regular"),
            Alumno(materia_104="aprobada")
        )
    )
    def cursar_202_ok(self):
        nombre = nombre_materia("202")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="202",
            mensaje=f"Podés cursar {nombre} (202)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="202"),
        Alumno(materia_104="libre")
    )
    def cursar_202_no(self):
        nombre = nombre_materia("202")
        req = nombre_materia("104")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="202",
            mensaje=f"No podés cursar {nombre} (202). Necesitás regularizar {req} (104)."
        ))


    # =========================
    # RENDIR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="202"),
        Alumno(materia_104="aprobada")
    )
    def rendir_202_ok(self):
        nombre = nombre_materia("202")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="202",
            mensaje=f"Podés rendir {nombre} (202)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="202"),
        OR(
            Alumno(materia_104="regular"),
            Alumno(materia_104="libre")
        )
    )
    def rendir_202_no(self):
        nombre = nombre_materia("202")
        req = nombre_materia("104")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="202",
            mensaje=f"No podés rendir {nombre} (202). Necesitás tener aprobada {req} (104)."
        ))

    # =========================
    # 203 - Cálculo Diferencial e Integral (requiere 104)
    # =========================

    # CASO A: Falta información
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="203"),
        NOT(Alumno(materia_104=W()))
    )
    def info_203(self, i):
        nombre = nombre_materia("203")
        req = nombre_materia("104")

        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="203",
            materia_requisito="104",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} {nombre} (203), necesito saber tu estado en {req} (104)."
        ))


    # =========================
    # CURSAR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="203"),
        OR(
            Alumno(materia_104="regular"),
            Alumno(materia_104="aprobada")
        )
    )
    def cursar_203_ok(self):
        nombre = nombre_materia("203")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="203",
            mensaje=f"Podés cursar {nombre} (203)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="203"),
        Alumno(materia_104="libre")
    )
    def cursar_203_no(self):
        nombre = nombre_materia("203")
        req = nombre_materia("104")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="203",
            mensaje=f"No podés cursar {nombre} (203). Necesitás regularizar {req} (104)."
        ))


    # =========================
    # RENDIR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="203"),
        Alumno(materia_104="aprobada")
    )
    def rendir_203_ok(self):
        nombre = nombre_materia("203")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="203",
            mensaje=f"Podés rendir {nombre} (203)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="203"),
        OR(
            Alumno(materia_104="regular"),
            Alumno(materia_104="libre")
        )
    )
    def rendir_203_no(self):
        nombre = nombre_materia("203")
        req = nombre_materia("104")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="203",
            mensaje=f"No podés rendir {nombre} (203). Necesitás tener aprobada {req} (104)."
        ))
    

    # =========================
    # 204 - Programación Orientada a Objetos (requiere 201)
    # =========================

    # CASO A: Falta información
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="204"),
        NOT(Alumno(materia_201=W()))
    )
    def info_204(self, i):
        nombre = nombre_materia("204")
        req = nombre_materia("201")

        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="204",
            materia_requisito="201",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} {nombre} (204), necesito saber tu estado en {req} (201)."
        ))


    # =========================
    # CURSAR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="204"),
        OR(
            Alumno(materia_201="regular"),
            Alumno(materia_201="aprobada")
        )
    )
    def cursar_204_ok(self):
        nombre = nombre_materia("204")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="204",
            mensaje=f"Podés cursar {nombre} (204)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="204"),
        Alumno(materia_201="libre")
    )
    def cursar_204_no(self):
        nombre = nombre_materia("204")
        req = nombre_materia("201")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="204",
            mensaje=f"No podés cursar {nombre} (204). Necesitás regularizar {req} (201)."
        ))


    # =========================
    # RENDIR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="204"),
        Alumno(materia_201="aprobada")
    )
    def rendir_204_ok(self):
        nombre = nombre_materia("204")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="204",
            mensaje=f"Podés rendir {nombre} (204)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="204"),
        OR(
            Alumno(materia_201="regular"),
            Alumno(materia_201="libre")
        )
    )
    def rendir_204_no(self):
        nombre = nombre_materia("204")
        req = nombre_materia("201")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="204",
            mensaje=f"No podés rendir {nombre} (204). Necesitás tener aprobada {req} (201)."
        ))

   # =========================
    # 205 - Sistemas Operativos (requiere 202)
    # =========================

    # CASO A: Falta información
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="205"),
        NOT(Alumno(materia_202=W()))
    )
    def info_205(self, i):
        nombre = nombre_materia("205")
        req = nombre_materia("202")

        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="205",
            materia_requisito="202",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} {nombre} (205), necesito saber tu estado en {req} (202)."
        ))


    # =========================
    # CURSAR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="205"),
        OR(
            Alumno(materia_202="regular"),
            Alumno(materia_202="aprobada")
        )
    )
    def cursar_205_ok(self):
        nombre = nombre_materia("205")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="205",
            mensaje=f"Podés cursar {nombre} (205)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="205"),
        Alumno(materia_202="libre")
    )
    def cursar_205_no(self):
        nombre = nombre_materia("205")
        req = nombre_materia("202")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="205",
            mensaje=f"No podés cursar {nombre} (205). Necesitás regularizar {req} (202)."
        ))


    # =========================
    # RENDIR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="205"),
        Alumno(materia_202="aprobada")
    )
    def rendir_205_ok(self):
        nombre = nombre_materia("205")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="205",
            mensaje=f"Podés rendir {nombre} (205)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="205"),
        OR(
            Alumno(materia_202="regular"),
            Alumno(materia_202="libre")
        )
    )
    def rendir_205_no(self):
        nombre = nombre_materia("205")
        req = nombre_materia("202")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="205",
            mensaje=f"No podés rendir {nombre} (205). Necesitás tener aprobada {req} (202)."
        ))

    # =========================
    # 206 - Administración y Gestión de Organizaciones (requiere 105)
    # =========================

    # CASO A: Falta información
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="206"),
        NOT(Alumno(materia_105=W()))
    )
    def info_206(self, i):
        nombre = nombre_materia("206")
        req = nombre_materia("105")

        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="206",
            materia_requisito="105",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} {nombre} (206), necesito saber tu estado en {req} (105)."
        ))


    # =========================
    # CURSAR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="206"),
        OR(
            Alumno(materia_105="regular"),
            Alumno(materia_105="aprobada")
        )
    )
    def cursar_206_ok(self):
        nombre = nombre_materia("206")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="206",
            mensaje=f"Podés cursar {nombre} (206)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="206"),
        Alumno(materia_105="libre")
    )
    def cursar_206_no(self):
        nombre = nombre_materia("206")
        req = nombre_materia("105")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="206",
            mensaje=f"No podés cursar {nombre} (206). Necesitás regularizar {req} (105)."
        ))


    # =========================
    # RENDIR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="206"),
        Alumno(materia_105="aprobada")
    )
    def rendir_206_ok(self):
        nombre = nombre_materia("206")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="206",
            mensaje=f"Podés rendir {nombre} (206)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="206"),
        OR(
            Alumno(materia_105="regular"),
            Alumno(materia_105="libre")
        )
    )
    def rendir_206_no(self):
        nombre = nombre_materia("206")
        req = nombre_materia("105")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="206",
            mensaje=f"No podés rendir {nombre} (206). Necesitás tener aprobada {req} (105)."
        ))

   # =========================
    # 206 - Administración y Gestión de Organizaciones (requiere 105)
    # =========================

    # CASO A: Falta información
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="206"),
        NOT(Alumno(materia_105=W()))
    )
    def info_206(self, i):
        nombre = nombre_materia("206")
        req = nombre_materia("105")

        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="206",
            materia_requisito="105",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} {nombre} (206), necesito saber tu estado en {req} (105)."
        ))


    # =========================
    # CURSAR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="206"),
        OR(
            Alumno(materia_105="regular"),
            Alumno(materia_105="aprobada")
        )
    )
    def cursar_206_ok(self):
        nombre = nombre_materia("206")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="206",
            mensaje=f"Podés cursar {nombre} (206)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="206"),
        Alumno(materia_105="libre")
    )
    def cursar_206_no(self):
        nombre = nombre_materia("206")
        req = nombre_materia("105")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="206",
            mensaje=f"No podés cursar {nombre} (206). Necesitás regularizar {req} (105)."
        ))


    # =========================
    # RENDIR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="206"),
        Alumno(materia_105="aprobada")
    )
    def rendir_206_ok(self):
        nombre = nombre_materia("206")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="206",
            mensaje=f"Podés rendir {nombre} (206)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="206"),
        OR(
            Alumno(materia_105="regular"),
            Alumno(materia_105="libre")
        )
    )
    def rendir_206_no(self):
        nombre = nombre_materia("206")
        req = nombre_materia("105")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="206",
            mensaje=f"No podés rendir {nombre} (206). Necesitás tener aprobada {req} (105)."
        ))

    # =========================
    # 302 - Comunicaciones de Datos (requiere 202)
    # =========================

    # CASO A: Falta información
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="302"),
        NOT(Alumno(materia_202=W()))
    )
    def info_302(self, i):
        nombre = nombre_materia("302")
        req = nombre_materia("202")

        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="302",
            materia_requisito="202",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} {nombre} (302), necesito saber tu estado en {req} (202)."
        ))


    # =========================
    # CURSAR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="302"),
        OR(
            Alumno(materia_202="regular"),
            Alumno(materia_202="aprobada")
        )
    )
    def cursar_302_ok(self):
        nombre = nombre_materia("302")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="302",
            mensaje=f"Podés cursar {nombre} (302)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="302"),
        Alumno(materia_202="libre")
    )
    def cursar_302_no(self):
        nombre = nombre_materia("302")
        req = nombre_materia("202")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="302",
            mensaje=f"No podés cursar {nombre} (302). Necesitás regularizar {req} (202)."
        ))


    # =========================
    # RENDIR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="302"),
        Alumno(materia_202="aprobada")
    )
    def rendir_302_ok(self):
        nombre = nombre_materia("302")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="302",
            mensaje=f"Podés rendir {nombre} (302)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="302"),
        OR(
            Alumno(materia_202="regular"),
            Alumno(materia_202="libre")
        )
    )
    def rendir_302_no(self):
        nombre = nombre_materia("302")
        req = nombre_materia("202")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="302",
            mensaje=f"No podés rendir {nombre} (302). Necesitás tener aprobada {req} (202)."
        ))

    # =========================
    # 303 (204 y 206)
    # =========================
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="303"),
        NOT(Alumno(materia_204=W()))
    )
    def info_204_303(self, i):
        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="303",
            materia_requisito="204",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} la materia 303 requiere que indiques el estado de la correlativa 204."
        ))

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="303"),
        OR(
            Alumno(materia_204="regular"),
            Alumno(materia_204="aprobada")
        ),
        NOT(Alumno(materia_206=W()))
    )
    def info_206_303(self, i):
        self.declare(Respuesta(
            estado="requiere_info",
            materia_requisito="206",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} en la materia 303 también necesito el estado de la correlativa 206."
        ))

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="303"),
        OR(Alumno(materia_204="regular"), Alumno(materia_204="aprobada")),
        OR(Alumno(materia_206="regular"), Alumno(materia_206="aprobada"))
    )
    def cursar_303_ok(self):
        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            mensaje="Puedes cursar la materia 303 porque cumples con ambas correlativas (204 y 206)."
        ))

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="303"),
        OR(
            Alumno(materia_204="libre"),
            Alumno(materia_206="libre")
        )
    )
    def cursar_303_no(self):
        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            mensaje="No puedes cursar la materia 303 porque al menos una correlativa está en estado libre."
        ))

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="303"),
        NOT(Alumno(materia_204=W()))
    )
    def info_rendir_303(self):
        self.declare(Respuesta(
            estado="requiere_info",
            materia_requisito="204",
            opciones=["regular", "aprobada", "libre"],
            mensaje="Para rendir 303 necesito el estado de la correlativa 204."
        ))

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="303"),
        Alumno(materia_204="aprobada"),
        Alumno(materia_206="aprobada")
    )
    def rendir_303_ok(self):
        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            mensaje="🎓 Puedes rendir la materia 303 porque ambas correlativas están aprobadas."
        ))

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="303"),
        OR(
            Alumno(materia_204="regular"),
            Alumno(materia_206="regular")
        )
    )
    def rendir_303_no(self):
        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            mensaje="❌ No puedes rendir 303 porque debes tener ambas correlativas aprobadas."
        ))


    # =========================
    # 304 - Taller de Programación II
    # Requiere: 301 y 303
    # =========================

    # CASO A1: Falta saber 301
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="304"),
        NOT(Alumno(materia_301=W()))
    )
    def info_301_304(self, i):
        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="304",
            materia_requisito="301",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} {nombre_materia('304')} (304), necesito saber tu estado en {nombre_materia('301')} (301)."
        ))


    # CASO A2: Tiene 301 pero falta 303
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="304"),
        OR(Alumno(materia_301="regular"), Alumno(materia_301="aprobada")),
        NOT(Alumno(materia_303=W()))
    )
    def info_303_304(self, i):
        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="304",
            materia_requisito="303",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Perfecto, ya tienes {nombre_materia('301')} (301). Ahora necesito saber tu estado en {nombre_materia('303')} (303)."
        ))


    # =========================
    # CURSAR
    # =========================

    # CASO B: Puede cursar (cumple ambas)
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="304"),
        OR(Alumno(materia_301="regular"), Alumno(materia_301="aprobada")),
        OR(Alumno(materia_303="regular"), Alumno(materia_303="aprobada"))
    )
    def cursar_304_ok(self):
        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="304",
            mensaje=f"Podés cursar {nombre_materia('304')} (304). Cumplís con las correlativas 301 y 303."
        ))


    # CASO C: Falla en 301
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="304"),
        Alumno(materia_301="libre")
    )
    def cursar_304_falla_301(self):
        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="304",
            mensaje=f"No podés cursar {nombre_materia('304')} (304). Debés regularizar {nombre_materia('301')} (301)."
        ))


    # CASO D: Falla en 303
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="304"),
        OR(Alumno(materia_301="regular"), Alumno(materia_301="aprobada")),
        Alumno(materia_303="libre")
    )
    def cursar_304_falla_303(self):
        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="304",
            mensaje=f"No podés cursar {nombre_materia('304')} (304). Te falta regularizar {nombre_materia('303')} (303)."
        ))


    # =========================
    # RENDIR
    # =========================

    # CASO A: Falta info para rendir (301)
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="304"),
        NOT(Alumno(materia_301=W()))
    )
    def info_rendir_301_304(self):
        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="304",
            materia_requisito="301",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para rendir {nombre_materia('304')} (304), necesito saber tu estado en {nombre_materia('301')} (301)."
        ))


    # CASO B: Tiene 301 pero falta 303
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="304"),
        Alumno(materia_301="aprobada"),
        NOT(Alumno(materia_303=W()))
    )
    def info_rendir_303_304(self):
        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="304",
            materia_requisito="303",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Ya tenés {nombre_materia('301')} (301). Ahora necesito saber tu estado en {nombre_materia('303')} (303)."
        ))


    # CASO C: Puede rendir
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="304"),
        Alumno(materia_301="aprobada"),
        Alumno(materia_303="aprobada")
    )
    def rendir_304_ok(self):
        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="304",
            mensaje=f"Podés rendir {nombre_materia('304')} (304)."
        ))


    # CASO D: Falla en 301
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="304"),
        OR(Alumno(materia_301="regular"), Alumno(materia_301="libre"))
    )
    def rendir_304_falla_301(self):
        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="304",
            mensaje=f"No podés rendir {nombre_materia('304')} (304). Necesitás tener aprobada {nombre_materia('301')} (301)."
        ))


    # CASO E: Falla en 303
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="304"),
        Alumno(materia_301="aprobada"),
        OR(Alumno(materia_303="regular"), Alumno(materia_303="libre"))
    )
    def rendir_304_falla_303(self):
        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="304",
            mensaje=f"No podés rendir {nombre_materia('304')} (304). Necesitás tener aprobada {nombre_materia('303')} (303)."
        ))
    

    # =========================
    # 305 - Probabilidad y Estadística (requiere 203)
    # =========================

    # CASO A: Falta info
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="305"),
        NOT(Alumno(materia_203=W()))
    )
    def info_203_305(self, i):
        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="305",
            materia_requisito="203",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} {nombre_materia('305')} (305), necesito saber tu estado en {nombre_materia('203')} (203)."
        ))


    # =========================
    # CURSAR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="305"),
        OR(Alumno(materia_203="regular"), Alumno(materia_203="aprobada"))
    )
    def cursar_305_ok(self):
        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="305",
            mensaje=f"Podés cursar {nombre_materia('305')} (305)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="305"),
        Alumno(materia_203="libre")
    )
    def cursar_305_no(self):
        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="305",
            mensaje=f"No podés cursar {nombre_materia('305')} (305). Necesitás regularizar {nombre_materia('203')} (203)."
        ))


    # =========================
    # RENDIR
    # =========================

    # Falta info para rendir
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="305"),
        NOT(Alumno(materia_203=W()))
    )
    def info_rendir_305(self):
        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="305",
            materia_requisito="203",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para rendir {nombre_materia('305')} (305), necesito saber tu estado en {nombre_materia('203')} (203)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="305"),
        Alumno(materia_203="aprobada")
    )
    def rendir_305_ok(self):
        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="305",
            mensaje=f"Podés rendir {nombre_materia('305')} (305)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="305"),
        OR(Alumno(materia_203="regular"), Alumno(materia_203="libre"))
    )
    def rendir_305_no(self):
        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="305",
            mensaje=f"No podés rendir {nombre_materia('305')} (305). Necesitás tener aprobada {nombre_materia('203')} (203)."
        ))
   

    # =========================
    # 306 - Bases de Datos I (requiere 204)
    # =========================

    # CASO A: Falta info
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="306"),
        NOT(Alumno(materia_204=W()))
    )
    def info_204_306(self, i):
        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="306",
            materia_requisito="204",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} {nombre_materia('306')} (306), necesito saber tu estado en {nombre_materia('204')} (204)."
        ))


    # =========================
    # CURSAR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="306"),
        OR(Alumno(materia_204="regular"), Alumno(materia_204="aprobada"))
    )
    def cursar_306_ok(self):
        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="306",
            mensaje=f"Podés cursar {nombre_materia('306')} (306)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="306"),
        Alumno(materia_204="libre")
    )
    def cursar_306_no(self):
        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="306",
            mensaje=f"No podés cursar {nombre_materia('306')} (306). Necesitás regularizar {nombre_materia('204')} (204)."
        ))


    # =========================
    # RENDIR
    # =========================

    # Falta info
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="306"),
        NOT(Alumno(materia_204=W()))
    )
    def info_rendir_306(self):
        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="306",
            materia_requisito="204",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para rendir {nombre_materia('306')} (306), necesito saber tu estado en {nombre_materia('204')} (204)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="306"),
        Alumno(materia_204="aprobada")
    )
    def rendir_306_ok(self):
        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="306",
            mensaje=f"Podés rendir {nombre_materia('306')} (306)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="306"),
        OR(Alumno(materia_204="regular"), Alumno(materia_204="libre"))
    )
    def rendir_306_no(self):
        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="306",
            mensaje=f"No podés rendir {nombre_materia('306')} (306). Necesitás tener aprobada {nombre_materia('204')} (204)."
        ))
    
    # =========================
    # 401 - Ingeniería de Software II (requiere 303)
    # =========================

    # CASO A: Falta info
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="401"),
        NOT(Alumno(materia_303=W()))
    )
    def info_401(self, i):
        nombre = nombre_materia("401")
        req = nombre_materia("303")

        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="401",
            materia_requisito="303",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} {nombre} (401), necesito saber tu estado en {req} (303)."
        ))


    # =========================
    # CURSAR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="401"),
        OR(Alumno(materia_303="regular"), Alumno(materia_303="aprobada"))
    )
    def cursar_401_ok(self):
        nombre = nombre_materia("401")
        req = nombre_materia("303")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="401",
            mensaje=f"Podés cursar {nombre} (401). Cumplís con {req}."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="401"),
        Alumno(materia_303="libre")
    )
    def cursar_401_no(self):
        nombre = nombre_materia("401")
        req = nombre_materia("303")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="401",
            mensaje=f"No podés cursar {nombre} (401). Necesitás regularizar {req} (303)."
        ))


    # =========================
    # RENDIR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="401"),
        Alumno(materia_303="aprobada")
    )
    def rendir_401_ok(self):
        nombre = nombre_materia("401")
        req = nombre_materia("303")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="401",
            mensaje=f"Podés rendir {nombre} (401). Tenés aprobada {req}."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="401"),
        OR(Alumno(materia_303="regular"), Alumno(materia_303="libre"))
    )
    def rendir_401_no(self):
        nombre = nombre_materia("401")
        req = nombre_materia("303")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="401",
            mensaje=f"No podés rendir {nombre} (401). Necesitás tener aprobada {req} (303)."
        ))



    # =========================
    # 402 - Economía Aplicada (requiere 303)
    # =========================

    # CASO A: Falta info
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="402"),
        NOT(Alumno(materia_303=W()))
    )
    def info_402(self, i):
        nombre = nombre_materia("402")
        req = nombre_materia("303")

        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="402",
            materia_requisito="303",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} {nombre} (402), necesito saber tu estado en {req} (303)."
        ))


    # =========================
    # CURSAR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="402"),
        OR(Alumno(materia_303="regular"), Alumno(materia_303="aprobada"))
    )
    def cursar_402_ok(self):
        nombre = nombre_materia("402")
        req = nombre_materia("303")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="402",
            mensaje=f"Podés cursar {nombre} (402). Cumplís con {req}."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="402"),
        Alumno(materia_303="libre")
    )
    def cursar_402_no(self):
        nombre = nombre_materia("402")
        req = nombre_materia("303")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="402",
            mensaje=f"No podés cursar {nombre} (402). Necesitás regularizar {req} (303)."
        ))


    # =========================
    # RENDIR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="402"),
        Alumno(materia_303="aprobada")
    )
    def rendir_402_ok(self):
        nombre = nombre_materia("402")
        req = nombre_materia("303")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="402",
            mensaje=f"Podés rendir {nombre} (402). Tenés aprobada {req}."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="402"),
        OR(Alumno(materia_303="regular"), Alumno(materia_303="libre"))
    )
    def rendir_402_no(self):
        nombre = nombre_materia("402")
        req = nombre_materia("303")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="402",
            mensaje=f"No podés rendir {nombre} (402). Necesitás tener aprobada {req} (303)."
        ))


    # =========================
    # 403 - Teoría de la Computación (requiere 305)
    # =========================

    # CASO A: Falta info
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="403"),
        NOT(Alumno(materia_305=W()))
    )
    def info_403(self, i):
        nombre = nombre_materia("403")
        req = nombre_materia("305")

        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="403",
            materia_requisito="305",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} {nombre} (403), necesito saber tu estado en {req} (305)."
        ))


    # =========================
    # CURSAR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="403"),
        OR(Alumno(materia_305="regular"), Alumno(materia_305="aprobada"))
    )
    def cursar_403_ok(self):
        nombre = nombre_materia("403")
        req = nombre_materia("305")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="403",
            mensaje=f"Podés cursar {nombre} (403). Cumplís con {req}."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="403"),
        Alumno(materia_305="libre")
    )
    def cursar_403_no(self):
        nombre = nombre_materia("403")
        req = nombre_materia("305")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="403",
            mensaje=f"No podés cursar {nombre} (403). Necesitás regularizar {req} (305)."
        ))


    # =========================
    # RENDIR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="403"),
        Alumno(materia_305="aprobada")
    )
    def rendir_403_ok(self):
        nombre = nombre_materia("403")
        req = nombre_materia("305")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="403",
            mensaje=f"Podés rendir {nombre} (403). Tenés aprobada {req}."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="403"),
        OR(Alumno(materia_305="regular"), Alumno(materia_305="libre"))
    )
    def rendir_403_no(self):
        nombre = nombre_materia("403")
        req = nombre_materia("305")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="403",
            mensaje=f"No podés rendir {nombre} (403). Necesitás tener aprobada {req} (305)."
        ))

    # =========================
    # 404 - Redes de Datos (requiere 302)
    # =========================

    # CASO A: Falta info
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="404"),
        NOT(Alumno(materia_302=W()))
    )
    def info_404(self, i):
        nombre = nombre_materia("404")
        req = nombre_materia("302")

        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="404",
            materia_requisito="302",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} {nombre} (404), necesito saber tu estado en {req} (302)."
        ))


    # =========================
    # CURSAR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="404"),
        OR(Alumno(materia_302="regular"), Alumno(materia_302="aprobada"))
    )
    def cursar_404_ok(self):
        nombre = nombre_materia("404")
        req = nombre_materia("302")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="404",
            mensaje=f"Podés cursar {nombre} (404). Cumplís con {req}."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="404"),
        Alumno(materia_302="libre")
    )
    def cursar_404_no(self):
        nombre = nombre_materia("404")
        req = nombre_materia("302")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="404",
            mensaje=f"No podés cursar {nombre} (404). Necesitás regularizar {req} (302)."
        ))


    # =========================
    # RENDIR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="404"),
        Alumno(materia_302="aprobada")
    )
    def rendir_404_ok(self):
        nombre = nombre_materia("404")
        req = nombre_materia("302")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="404",
            mensaje=f"Podés rendir {nombre} (404). Tenés aprobada {req}."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="404"),
        OR(Alumno(materia_302="regular"), Alumno(materia_302="libre"))
    )
    def rendir_404_no(self):
        nombre = nombre_materia("404")
        req = nombre_materia("302")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="404",
            mensaje=f" No podés rendir {nombre} (404). Necesitás tener aprobada {req} (302)."
        ))


    # =========================
    # 405 - Bases de Datos II (requiere 306)
    # =========================

    # CASO A: Falta info
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="405"),
        NOT(Alumno(materia_306=W()))
    )
    def info_405(self, i):
        nombre = nombre_materia("405")
        req = nombre_materia("306")

        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="405",
            materia_requisito="306",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} {nombre} (405), necesito saber tu estado en {req} (306)."
        ))


    # =========================
    # CURSAR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="405"),
        OR(Alumno(materia_306="regular"), Alumno(materia_306="aprobada"))
    )
    def cursar_405_ok(self):
        nombre = nombre_materia("405")
        req = nombre_materia("306")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="405",
            mensaje=f" Podés cursar {nombre} (405). Cumplís con {req}."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="405"),
        Alumno(materia_306="libre")
    )
    def cursar_405_no(self):
        nombre = nombre_materia("405")
        req = nombre_materia("306")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="405",
            mensaje=f" No podés cursar {nombre} (405). Necesitás regularizar {req} (306)."
        ))


    # =========================
    # RENDIR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="405"),
        Alumno(materia_306="aprobada")
    )
    def rendir_405_ok(self):
        nombre = nombre_materia("405")
        req = nombre_materia("306")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="405",
            mensaje=f"Podés rendir {nombre} (405). Tenés aprobada {req}."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="405"),
        OR(Alumno(materia_306="regular"), Alumno(materia_306="libre"))
    )
    def rendir_405_no(self):
        nombre = nombre_materia("405")
        req = nombre_materia("306")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="405",
            mensaje=f"No podés rendir {nombre} (405). Necesitás tener aprobada {req} (306)."
        ))


    # =========================
    # 406 - Métodos Computacionales (requiere 305)
    # =========================

    # CASO A: Falta info
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="406"),
        NOT(Alumno(materia_305=W()))
    )
    def info_406(self, i):
        nombre = nombre_materia("406")
        req = nombre_materia("305")

        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="406",
            materia_requisito="305",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} {nombre} (406), necesito saber tu estado en {req} (305)."
        ))


    # =========================
    # CURSAR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="406"),
        OR(Alumno(materia_305="regular"), Alumno(materia_305="aprobada"))
    )
    def cursar_406_ok(self):
        nombre = nombre_materia("406")
        req = nombre_materia("305")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="406",
            mensaje=f"Podés cursar {nombre} (406). Cumplís con {req}."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="406"),
        Alumno(materia_305="libre")
    )
    def cursar_406_no(self):
        nombre = nombre_materia("406")
        req = nombre_materia("305")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="406",
            mensaje=f"No podés cursar {nombre} (406). Necesitás regularizar {req} (305)."
        ))


    # =========================
    # RENDIR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="406"),
        Alumno(materia_305="aprobada")
    )
    def rendir_406_ok(self):
        nombre = nombre_materia("406")
        req = nombre_materia("305")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="406",
            mensaje=f"Podés rendir {nombre} (406). Tenés aprobada {req}."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="406"),
        OR(Alumno(materia_305="regular"), Alumno(materia_305="libre"))
    )
    def rendir_406_no(self):
        nombre = nombre_materia("406")
        req = nombre_materia("305")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="406",
            mensaje=f" No podés rendir {nombre} (406). Necesitás tener aprobada {req} (305)."
        ))

    # =========================
    # 501 - Proyecto Final de Carrera (requiere 404 y 405)
    # =========================

    # CASO A1: Falta info de 404
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="501"),
        NOT(Alumno(materia_404=W()))
    )
    def info_404_501(self, i):
        nombre = nombre_materia("501")
        req = nombre_materia("404")

        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="501",
            materia_requisito="404",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} {nombre} (501), necesito saber tu estado en {req} (404)."
        ))


    # CASO A2: Tiene 404 pero falta 405
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="501"),
        OR(Alumno(materia_404="regular"), Alumno(materia_404="aprobada")),
        NOT(Alumno(materia_405=W()))
    )
    def info_405_501(self, i):
        nombre = nombre_materia("501")
        req = nombre_materia("405")

        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="501",
            materia_requisito="405",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Perfecto. Ahora necesito tu estado en {req} (405)."
        ))


    # =========================
    # CURSAR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="501"),
        OR(Alumno(materia_404="regular"), Alumno(materia_404="aprobada")),
        OR(Alumno(materia_405="regular"), Alumno(materia_405="aprobada"))
    )
    def cursar_501_ok(self):
        nombre = nombre_materia("501")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="501",
            mensaje=f" Podés cursar {nombre} (501). Cumplís con las correlativas."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="501"),
        Alumno(materia_404="libre")
    )
    def cursar_501_falla_404(self):
        nombre = nombre_materia("501")
        req = nombre_materia("404")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="501",
            mensaje=f" No podés cursar {nombre} (501). Te falta regularizar {req} (404)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="501"),
        OR(Alumno(materia_404="regular"), Alumno(materia_404="aprobada")),
        Alumno(materia_405="libre")
    )
    def cursar_501_falla_405(self):
        nombre = nombre_materia("501")
        req = nombre_materia("405")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="501",
            mensaje=f" No podés cursar {nombre} (501). Te falta regularizar {req} (405)."
        ))


    # =========================
    # RENDIR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="501"),
        Alumno(materia_404="aprobada"),
        Alumno(materia_405="aprobada")
    )
    def rendir_501_ok(self):
        nombre = nombre_materia("501")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="501",
            mensaje=f" Podés rendir {nombre} (501). Tenés todas las correlativas aprobadas."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="501"),
        OR(
            Alumno(materia_404="regular"),
            Alumno(materia_404="libre"),
            Alumno(materia_405="regular"),
            Alumno(materia_405="libre")
        )
    )
    def rendir_501_no(self):
        nombre = nombre_materia("501")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="501",
            mensaje=f"No podés rendir {nombre} (501). Necesitás tener todas las correlativas aprobadas."
        ))

    # =========================
    # 502 - Auditoría y Seguridad Informática (requiere 404 y 405)
    # =========================

    # CASO A1: Falta info de 404
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="502"),
        NOT(Alumno(materia_404=W()))
    )
    def info_404_502(self, i):
        nombre = nombre_materia("502")
        req = nombre_materia("404")

        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="502",
            materia_requisito="404",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} {nombre} (502), necesito saber tu estado en {req} (404)."
        ))


    # CASO A2: Tiene 404 pero falta 405
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="502"),
        OR(Alumno(materia_404="regular"), Alumno(materia_404="aprobada")),
        NOT(Alumno(materia_405=W()))
    )
    def info_405_502(self, i):
        nombre = nombre_materia("502")
        req = nombre_materia("405")

        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="502",
            materia_requisito="405",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Perfecto. Ahora necesito tu estado en {req} (405)."
        ))


    # =========================
    # CURSAR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="502"),
        OR(Alumno(materia_404="regular"), Alumno(materia_404="aprobada")),
        OR(Alumno(materia_405="regular"), Alumno(materia_405="aprobada"))
    )
    def cursar_502_ok(self):
        nombre = nombre_materia("502")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="502",
            mensaje=f" Podés cursar {nombre} (502). Cumplís con las correlativas."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="502"),
        Alumno(materia_404="libre")
    )
    def cursar_502_falla_404(self):
        nombre = nombre_materia("502")
        req = nombre_materia("404")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="502",
            mensaje=f" No podés cursar {nombre} (502). Te falta regularizar {req} (404)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="502"),
        OR(Alumno(materia_404="regular"), Alumno(materia_404="aprobada")),
        Alumno(materia_405="libre")
    )
    def cursar_502_falla_405(self):
        nombre = nombre_materia("502")
        req = nombre_materia("405")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="502",
            mensaje=f" No podés cursar {nombre} (502). Te falta regularizar {req} (405)."
        ))


    # =========================
    # RENDIR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="502"),
        Alumno(materia_404="aprobada"),
        Alumno(materia_405="aprobada")
    )
    def rendir_502_ok(self):
        nombre = nombre_materia("502")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="502",
            mensaje=f" Podés rendir {nombre} (502). Tenés todas las correlativas aprobadas."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="502"),
        OR(
            Alumno(materia_404="regular"),
            Alumno(materia_404="libre"),
            Alumno(materia_405="regular"),
            Alumno(materia_405="libre")
        )
    )
    def rendir_502_no(self):
        nombre = nombre_materia("502")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="502",
            mensaje=f" No podés rendir {nombre} (502). Necesitás tener todas las correlativas aprobadas."
        ))

    # =========================
    # 503 - Optativa I
    # Requiere: 403
    # =========================

    # CASO A: Falta info
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="503"),
        NOT(Alumno(materia_403=W()))
    )
    def info_403_503(self, i):
        nombre = nombre_materia("503")
        req = nombre_materia("403")

        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="503",
            materia_requisito="403",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} {nombre} (503), necesito saber tu estado en {req} (403)."
        ))


    # =========================
    # CURSAR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="503"),
        OR(Alumno(materia_403="regular"), Alumno(materia_403="aprobada"))
    )
    def cursar_503_ok(self):
        nombre = nombre_materia("503")
        req = nombre_materia("403")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="503",
            mensaje=f" Podés cursar {nombre} (503). Cumplís con {req} (403)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="503"),
        Alumno(materia_403="libre")
    )
    def cursar_503_no(self):
        nombre = nombre_materia("503")
        req = nombre_materia("403")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="503",
            mensaje=f" No podés cursar {nombre} (503). Necesitás regularizar {req} (403)."
        ))


    # =========================
    # RENDIR
    # =========================

    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="503"),
        Alumno(materia_403="aprobada")
    )
    def rendir_503_ok(self):
        nombre = nombre_materia("503")
        req = nombre_materia("403")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="503",
            mensaje=f" Podés rendir {nombre} (503). Tenés aprobada {req} (403)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="503"),
        OR(Alumno(materia_403="regular"), Alumno(materia_403="libre"))
    )
    def rendir_503_no(self):
        nombre = nombre_materia("503")
        req = nombre_materia("403")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="503",
            mensaje=f" No podés rendir {nombre} (503). Necesitás tener aprobada {req} (403)."
        ))

    # =========================
    # 504 - Optativa II
    # Requiere: 404
    # =========================

    # =========================
    # CASO A: falta información
    # =========================
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="504"),
        NOT(Alumno(materia_404=W()))
    )
    def info_404_504(self, i):
        nombre = nombre_materia("504")
        req = nombre_materia("404")

        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="504",
            materia_requisito="404",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} {nombre} (504), necesito saber tu estado en {req} (404)."
        ))


    # =========================
    # CURSAR
    # =========================
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="504"),
        OR(Alumno(materia_404="regular"), Alumno(materia_404="aprobada"))
    )
    def cursar_504_ok(self):
        nombre = nombre_materia("504")
        req = nombre_materia("404")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="504",
            mensaje=f" Podés cursar {nombre} (504). Cumplís con {req} (404)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="504"),
        Alumno(materia_404="libre")
    )
    def cursar_504_no(self):
        nombre = nombre_materia("504")
        req = nombre_materia("404")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="504",
            mensaje=f" No podés cursar {nombre} (504). Necesitás regularizar {req} (404)."
        ))


    # =========================
    # RENDIR
    # =========================
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="504"),
        Alumno(materia_404="aprobada")
    )
    def rendir_504_ok(self):
        nombre = nombre_materia("504")
        req = nombre_materia("404")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="504",
            mensaje=f" Podés rendir {nombre} (504). Tenés aprobada {req} (404)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="504"),
        OR(Alumno(materia_404="regular"), Alumno(materia_404="libre"))
    )
    def rendir_504_no(self):
        nombre = nombre_materia("504")
        req = nombre_materia("404")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="504",
            mensaje=f" No podés rendir {nombre} (504). Necesitás tener aprobada {req} (404)."
        ))

# =========================
# 505 - Optativa III
# Requiere: 401
# =========================

    # =========================
    # CASO A: falta información
    # =========================
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion=MATCH.i, materia="505"),
        NOT(Alumno(materia_401=W()))
    )
    def info_401_505(self, i):
        nombre = nombre_materia("505")
        req = nombre_materia("401")

        self.declare(Respuesta(
            estado="requiere_info",
            materia_consultada="505",
            materia_requisito="401",
            opciones=["regular", "aprobada", "libre"],
            mensaje=f"Para {i} {nombre} (505), necesito saber tu estado en {req} (401)."
        ))


    # =========================
    # CURSAR
    # =========================
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="505"),
        OR(Alumno(materia_401="regular"), Alumno(materia_401="aprobada"))
    )
    def cursar_505_ok(self):
        nombre = nombre_materia("505")
        req = nombre_materia("401")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="505",
            mensaje=f"Podés cursar {nombre} (505). Cumplís con {req} (401)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="cursar", materia="505"),
        Alumno(materia_401="libre")
    )
    def cursar_505_no(self):
        nombre = nombre_materia("505")
        req = nombre_materia("401")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="505",
            mensaje=f"No podés cursar {nombre} (505). Necesitás regularizar {req} (401)."
        ))


    # =========================
    # RENDIR
    # =========================
    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="505"),
        Alumno(materia_401="aprobada")
    )
    def rendir_505_ok(self):
        nombre = nombre_materia("505")
        req = nombre_materia("401")

        self.declare(Respuesta(
            estado="completado",
            es_posible=True,
            materia_consultada="505",
            mensaje=f"Podés rendir {nombre} (505). Tenés aprobada {req} (401)."
        ))


    @Rule(
        Fact(accion="evaluar"),
        Consulta(intencion="rendir", materia="505"),
        OR(Alumno(materia_401="regular"), Alumno(materia_401="libre"))
    )
    def rendir_505_no(self):
        nombre = nombre_materia("505")
        req = nombre_materia("401")

        self.declare(Respuesta(
            estado="completado",
            es_posible=False,
            materia_consultada="505",
            mensaje=f"No podés rendir {nombre} (505). Necesitás tener aprobada {req} (401)."
        ))