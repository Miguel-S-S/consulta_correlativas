from django.shortcuts import render, redirect
from .logic.materias import PLAN_ESTUDIOS
from .logic.rules import MotorCorrelativas, Consulta, Alumno

def reiniciar_chat(request):
    """Limpia la memoria del agente para una nueva consulta."""
    request.session.flush()
    return redirect('chat_experto')

def chat_experto(request):

    if 'estado_alumno' not in request.session:
        request.session['estado_alumno'] = {}

    if request.method == 'POST':
        if 'materia_objetivo' in request.POST:
            request.session['materia_objetivo'] = request.POST['materia_objetivo']
            request.session['intencion'] = request.POST.get('intencion', 'cursar')
            request.session['estado_alumno'] = {} 

        elif 'materia_requisito' in request.POST:
            materia_req = request.POST['materia_requisito']
            estado_req = request.POST['estado_requisito']
            
            estado_alumno = request.session['estado_alumno']
            estado_alumno[f"materia_{materia_req}"] = estado_req
            request.session['estado_alumno'] = estado_alumno
            request.session.modified = True

    contexto = {
        'plan_estudios': PLAN_ESTUDIOS,
        'respuesta_motor': None,
        'materia_objetivo': request.session.get('materia_objetivo', None)
    }

    materia_objetivo = request.session.get('materia_objetivo')
    intencion = request.session.get('intencion')

    if materia_objetivo and intencion:
        motor = MotorCorrelativas()
        motor.reset()
        motor.declare(Consulta(intencion=intencion, materia=materia_objetivo))

        estado_alumno = request.session.get('estado_alumno', {})
        if estado_alumno:
            motor.declare(Alumno(**estado_alumno))

        motor.run()

        for fact in motor.facts.values():
            if fact.__class__.__name__ == 'Respuesta':
                contexto['respuesta_motor'] = fact
                break

    return render(request, 'chatbot/chat.html', contexto)