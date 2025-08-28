from django.shortcuts import render


# Create your views here.
def inicio(request):
    dispositivos = [
        {"nombre": "Sensor Temperatura", "consumo": 50},
        {"nombre": "Medidor Solar", "consumo": 120},
        {"nombre": "Sensor Movimiento", "consumo": 30},
        {"nombre": "Calefactor", "consumo": 200},
    ]
    consumo_maximo = 100
    dispositivos_criticos = 0
    advertencias = []

    for dispositivo in dispositivos:
        if dispositivo["consumo"] > consumo_maximo:
            dispositivo["estado"] = "Exceso"
            dispositivo["color"] = "red"
            dispositivos_criticos += 1
        else:
            dispositivo["estado"] = "Correcto"
            dispositivo["color"] = "green"
            
    return render(request, "dispositivos/inicio.html",{
        "dispositivos": dispositivos,
        "consumo_maximo": consumo_maximo,
        "advertencias": advertencias,
        "dispositivos_criticos": dispositivos_criticos
    
    })