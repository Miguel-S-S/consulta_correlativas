from django.shortcuts import render, redirect
from .logic.materias import PLAN_ESTUDIOS
from .logic.rules import MotorCorrelativas, Consulta, Alumno

def reiniciar_chat(request):
    """Limpia la memoria del agente para una nueva consulta."""
    request.session.flush()
    return redirect('chat_experto')

def chat_experto(request):
    # 1. Inicializamos la memoria del agente en la sesión si no existe
    if 'estado_alumno' not in request.session:
        request.session['estado_alumno'] = {}

    contexto = {
        'plan_estudios': PLAN_ESTUDIOS,
        'respuesta_motor': None,
        'materia_objetivo': request.session.get('materia_objetivo', None)
    }

    if request.method == 'POST':
        # CASO A: El usuario selecciona la materia que quiere cursar (El objetivo inicial)
        if 'materia_objetivo' in request.POST:
            request.session['materia_objetivo'] = request.POST['materia_objetivo']
            request.session['intencion'] = request.POST.get('intencion', 'cursar')
            # Limpiamos el estado anterior si elige una nueva materia
            request.session['estado_alumno'] = {} 

        # CASO B: El usuario responde a una pregunta del motor (Aporta nuevos hechos)
        elif 'materia_requisito' in request.POST:
            materia_req = request.POST['materia_requisito']
            estado_req = request.POST['estado_requisito']
            
            # Actualizamos la memoria del agente
            estado_alumno = request.session['estado_alumno']
            estado_alumno[f"materia_{materia_req}"] = estado_req
            request.session['estado_alumno'] = estado_alumno
            request.session.modified = True

        # --- CICLO DE INFERENCIA DEL AGENTE ---
        materia_objetivo = request.session.get('materia_objetivo')
        intencion = request.session.get('intencion')

        if materia_objetivo and intencion:
            # 1. Instanciamos el motor experto
            motor = MotorCorrelativas()
            motor.reset()

            # 2. Inyectamos la meta del usuario
            motor.declare(Consulta(intencion=intencion, materia=materia_objetivo))

            # 3. Inyectamos la base de hechos actual (la memoria de la sesión)
            estado_alumno = request.session.get('estado_alumno', {})
            if estado_alumno:
                motor.declare(Alumno(**estado_alumno))

            # 4. Ejecutamos la inferencia (Forward Chaining)
            motor.run()

            # 5. Extraemos la conclusión a la que llegó el motor
            for fact in motor.facts.values():
                # Buscamos el Fact "Respuesta" que creamos en rules.py
                if fact.__class__.__name__ == 'Respuesta':
                    contexto['respuesta_motor'] = fact
                    break

    return render(request, 'chatbot/chat.html', contexto)
