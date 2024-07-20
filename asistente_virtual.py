import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes 
import webbrowser
import datetime
import wikipedia

# Escuchar microfono y devolverlo en texto

def transformar_audio(): 
    # almacenar recognizer
    r = sr.Recognizer()

    # configurar microfono
    with sr.Microphone() as origen:
        # tiempo de espera
        r.pause_threshold = 0.8
        # informar que comenzo la grabacion
        print("Ya puedes hablar...")

        # guardar lo que escuche como audio
        audio = r.listen(origen)
        print("PROCESANDO: \n")
        try:
            # buscar en google lo que escucho
            pedido = r.recognize_google(audio,language="es-ar")

            # prueba de que pudo ingresar

            print("Dijiste " + pedido)

            # devolver pedido 
            return pedido
            
        except sr.UnknownValueError:

            # prueba de que no comprendio el audio
            print("ups, no he entendido")

            # devolver error

            return "sigo esperando..."
        
            # en caso de no resolver el pedido
        except sr.RequestError:

            # prueba de que no comprendio el audio
            print("ups, no hay servicio")

            # devolver error

            return "sigo esperando..."
        
        # error inesperado
        except:
             # prueba de que no comprendio el audio
            print("ups, algo ha salido mal")

            # devolver error

            return "sigo esperando..."

# funcion para que el asistence hable
def hablar(mensaje):
    #encender el motor de pyttsx3

    engine = pyttsx3.init()

    # pronunciar mensaje

    engine.say(mensaje)
    engine.runAndWait()

def pedir_dia():
    # crear variable con datos de hoy

    dia = datetime.date.today()
    # crear variable para el dia de semana

    dia_semana = dia.weekday()
    calendario = {
        0: "Lunes",
        1: "Martes",
        2: "Miércoles",
        3: "Jueves",
        4: "Viernes",
        5: "Sábado",
        6: "Domingo"
    }
    

    hablar(f'Hoy es {calendario[dia_semana]} del dia {dia.day} del {dia.month} anio {dia.year}')

    # Decir dia de la semana

def pedir_hora():
    
    hora = datetime.datetime.now()
    
    hablar(f'La hora es: {hora.hour} con {hora.minute} minutos y {hora.second} segundos')

def opciones():
    # decir saludo

    # hablar("Hola soy Helena, tu asistente personal. Porfavor, dime en que te puedo ayudar!")
    # hablar("Ahora mismo estoy programada para poder decirte que dia es hoy y la hora del dia de hoy. Solamente para poder ingresar tienes que decirme la palabra clave Dia o la palabra clave Hora")

    bandera = True
    
    while bandera:
        mensaje = transformar_audio().lower()
        if "dia" in mensaje:
            pedir_dia()
        elif "hora" in mensaje:
            pedir_hora()
        else:
            hablar("Comando no reconocido, intenta nuevamente.")
        
        continuar = input("Quieres continuar? s/n\n")
        if(continuar.lower() == "s"):
            bandera = True
        else:
            bandera = False

def saludo_inicial():

    mensaje = ''

    hora = datetime.datetime.now()
    
    if(hora.hour < 6 or hora.hour > 20):
        mensaje = "Buenas noches"
    elif 6 <= hora.hour < 13:
        mensaje = "Buenas dias"
    else:
        mensaje = "Buenas tardes"

    hablar(f"Hola {mensaje}, me llamo Helena sere su asistente. Cualquier consulta aqui estare!!")

def pedir_cosas():

    # activar saludo

    saludo_inicial()

    # variable de corte

    comenzar = True

    # loop central
    while comenzar:
        
        # activar microfono y guardar en el pedido
        pedido = transformar_audio().lower()

        if "abrir youtube" in pedido or "abras youtube" in pedido:
                hablar("Con gusto, estoy abriendo YouTube...")
                webbrowser.open("https://www.youtube.com")
                continue
        elif "abrir navegador" in pedido or "abras navegador" in pedido:
                hablar("Claro, estoy en eso...")
                webbrowser.open("https://google.com")
                continue
        elif "cerrar" in pedido or "cierres" in pedido:
                hablar("Hasta luego !!")
                break
        elif "qué día es hoy" in pedido:
            pedir_dia()
            continue
        elif "qué hora es" in pedido:
            pedir_hora()
            continue
        elif "busca en wikipedia" in pedido:
            hablar("Buscando en wikipedia...")
            pedido = pedido.replace("busca en wikipedia"," ")
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido,sentences=1)
            hablar("Wikipedia dice lo siguiente: ")
            hablar(resultado)
            continue
        elif "busca en internet" in pedido:
            hablar("Ya mismo!!")
            pedido = pedido.replace("busca en internet"," ")
            pywhatkit.search(pedido)
            hablar("Esto es lo que he encontrado")
            continue
        elif "reproducir" in pedido:
            pedido.replace("reproducir","")
            pywhatkit.playonyt(pedido)
            continue
        elif "broma" in pedido:
            hablar(pyjokes.get_joke(language="es"))
            continue
        elif "precio de las acciones" in pedido:
            accion = pedido.split("de")[-1].strip().lower()
            cartera = {'apple':"AAPL",
                       "amazon": "AMZN",
                       "google": "GOOGL"}
            
            # Intentar buscar la acción en el diccionario
            if accion in cartera:
                accion_buscada = cartera[accion]

            try:
                accion_buscada = yf.Ticker(accion_buscada)
                print(accion_buscada)
                precio_actual = accion_buscada.fast_info['regularMarketPrice']
                print(precio_actual)
                hablar(f"La encontre, el precio de accion {accion} es {precio_actual}")
                continue
            except KeyError:
                hablar("Lo siento no lo he encontrado")
                continue
            except Exception as e:
                hablar(f"Ha ocurrido un error: {str(e)}")

pedir_cosas()





