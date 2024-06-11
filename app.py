import random
from PIL import Image, ImageTk
import os
import platform

# ------------------------------------------------------- Construcción del objeto función --------------------------------------------------------
class App:
    def __init__(self, frame1, frame2, frame3, canvas):
        self.frame1 = frame1
        self.frame2 = frame2
        self.frame3 = frame3
        self.canvas = canvas

    # ----------------------------------------------------------- Iniciar juego -----------------------------------------------------------------------
    def iniciar_juego(self, boton):
        # Determinar el tamaño del tablero según la dificultad seleccionada
        if 'facil' in boton:
            self.tamaño_tablero = 9
        if 'medio' in boton:
            self.tamaño_tablero = 7
        if 'dificil' in boton:
            self.tamaño_tablero = 5

        # Inicializar las posiciones y turnos
        self.turno_raton = True
        self.posicion_gato = (0, 0)
        self.posicion_raton = (self.tamaño_tablero - 1, self.tamaño_tablero - 1)
        self.posicion_inicial_gato = self.posicion_gato

        # Generar el tablero y los obstáculos
        self.tablero_lista = self.generar_listas()
        self.obstaculos = self.generar_obstaculos()

        # Calcular el tamaño de cada celda
        self.tamaño_celda = 400 // self.tamaño_tablero
        # Cargar las imágenes para el gato, el ratón, los obstáculos y las celdas
        self.imagen_gato = self.imagen('templates/gato.png', self.tamaño_celda, self.tamaño_celda)
        self.imagen_raton = self.imagen('templates/raton.png', self.tamaño_celda, self.tamaño_celda)
        self.imagen_obstaculo = self.imagen('templates/ob1.png', self.tamaño_celda, self.tamaño_celda)
        self.imagen_celda = self.imagen('templates/f.png', self.tamaño_celda, self.tamaño_celda)

        # Cambiar a la vista del juego
        self.frame1.forget()
        self.frame2.pack()
        self.dibujar_tablero()

    # -------------------------------------------------------- Verificador de terminal --------------------------------------------------------------
    def verificar_terminal(self):
        # Detectar el sistema operativo
        sistema_operativo = platform.system()
        if sistema_operativo == "Windows":
            # Comando para limpiar la terminal en Windows
            os.system('cls')
        else:
            # Comando para limpiar la terminal en Unix (Linux y macOS)
            os.system('clear')

        # Obtener movimientos posibles para el gato y el ratón
        mov_posibles_g = self.movimientos_posibles(self.posicion_gato)
        mov_posibles_r = self.movimientos_posibles(self.posicion_raton)
        # Imprimir información de posiciones y movimientos posibles
        print(f'''
posicion_raton: {self.posicion_raton}
posicion_gato: {self.posicion_gato}
movimientos posibles gato: {mov_posibles_g}
movimientos posibles raton: {mov_posibles_r}''')

    # ------------------------------------------------------ Prepara las imágenes en formato TK ---------------------------------------------------------
    def imagen(self, ruta, ancho, alto):
        # Cargar y redimensionar la imagen
        imagen = Image.open(ruta)
        imagen = imagen.resize((ancho, alto))
        imagen_tk = ImageTk.PhotoImage(imagen)
        return imagen_tk

    # ---------------------------------------------- Genera la lista con el tamaño que tendrá el tablero -----------------------------------------------
    def generar_listas(self):
        # Generar una lista de listas que representará el tablero
        filas = [0] * self.tamaño_tablero
        listas = []
        for i in range(self.tamaño_tablero):
            listas.append(filas)
        return listas

    # -------------------------------------- Genera tuplas con números aleatorios para construir obstáculos en el tablero --------------------------
    def generar_obstaculos(self):
        # Inicializar un conjunto vacío para almacenar los obstáculos
        obstaculos = set()
        # Calcular el número total de celdas en el tablero
        total_celdas = self.tamaño_tablero * self.tamaño_tablero
        
        # Calcular el número de obstáculos como el 20% del total de celdas
        num_obstaculos = total_celdas // 5

        # Generar obstáculos hasta alcanzar el número deseado
        while len(obstaculos) < num_obstaculos:
            # Generar coordenadas aleatorias (x, y) dentro del rango del tablero
            x = random.randint(0, self.tamaño_tablero - 1)
            y = random.randint(0, self.tamaño_tablero - 1)
            
            # Verificar que la posición generada no sea la del gato ni la del ratón
            if (x, y) != self.posicion_gato and (x, y) != self.posicion_raton:
                # Añadir la posición al conjunto de obstáculos
                obstaculos.add((x, y))
        return obstaculos

    # ------------------------------ Genera el tablero a partir de una lista de listas y con los obstáculos en orden aleatorio -------------------------------
    def dibujar_tablero(self):
        # Limpiar el canvas
        self.canvas.delete("all")

        # Dibujar las celdas del tablero
        for fila in range(self.tamaño_tablero):
            for columna in range(self.tamaño_tablero):
                # Calcular las coordenadas de la esquina superior izquierda de la celda
                x1 = fila * self.tamaño_celda
                y1 = columna * self.tamaño_celda
                # Verificar si la celda actual es un obstáculo
                if (fila, columna) in self.obstaculos:
                    # Dibujar la imagen del obstáculo
                    self.canvas.create_image(x1, y1, anchor='nw', image=self.imagen_obstaculo)
                else:
                    # Dibujar la imagen de una celda vacía
                    self.canvas.create_image(x1, y1, anchor='nw', image=self.imagen_celda)
        # Actualizar las posiciones del gato y el ratón
        self.actualizar_posiciones()

    # -------------------------------------------- Actualiza la posición en el tablero del gato y el ratón ------------------------------------------------------
    def actualizar_posiciones(self):
        # Extraer las coordenadas de las posiciones actuales del gato y el ratón
        gato_x, gato_y = self.posicion_gato
        raton_x, raton_y = self.posicion_raton

        # Colocar las imágenes del gato y el ratón en sus posiciones correspondientes en el canvas
        self.canvas.create_image(gato_x * self.tamaño_celda, gato_y * self.tamaño_celda, anchor='nw', image=self.imagen_gato)
        self.canvas.create_image(raton_x * self.tamaño_celda, raton_y * self.tamaño_celda, anchor='nw', image=self.imagen_raton)

    # -------------------------------------------------------- Evento (click): selección de celda ----------------------------------------------------------------
    def seleccionar_celda(self, evento):
        # Determinar la celda seleccionada a partir de las coordenadas del evento de clic
        x = evento.x // self.tamaño_celda
        y = evento.y // self.tamaño_celda

        # Verificar si es el turno del ratón
        if self.turno_raton:
            # Obtener los movimientos posibles del ratón
            movimientos_posibles_raton = self.movimientos_posibles(self.posicion_raton)
            # Verificar si la celda seleccionada es un movimiento válido
            if (x, y) in movimientos_posibles_raton:
                # Actualizar la posición del ratón
                self.posicion_raton = (x, y)
                # Redibujar el tablero para reflejar los cambios
                self.dibujar_tablero()
                # Verificar si el ratón ha alcanzado la posición inicial del gato
                if self.posicion_raton == self.posicion_inicial_gato:
                    # Mostrar mensaje de victoria si el ratón ha ganado
                    self.frame2.forget()
                    self.frame3.pack()
                else:
                    # Cambiar el turno al gato
                    self.turno_raton = False
                    # Mover al gato
                    self.mover_gato()

    # ------------------------------------------------------------------ Mover gato -------------------------------------------------------------------
    def mover_gato(self):
        # Llamar al método minimax para encontrar el mejor movimiento para el gato
        estado_act_tablero, mejor_movimiento = self.minimax(
            self.posicion_gato,        # Pasar la posición actual del gato
            self.posicion_raton,       # Pasar la posición actual del ratón
            3,                         # Establecer la profundidad de búsqueda a 3
            True                       # Indicar que es el turno del jugador maximizador (el gato)
        )
        
        # Actualizar la posición del gato al mejor movimiento encontrado por minimax
        self.posicion_gato = mejor_movimiento
        
        # Redibujar el tablero para reflejar las nuevas posiciones del gato y del ratón
        self.dibujar_tablero()
        
        # Comprobar si el gato ha atrapado al ratón
        if self.posicion_gato == self.posicion_raton:
            # Mostrar mensaje indicando que el ratón ha sido atrapado
            self.frame2.forget()
            self.frame3.pack()
        
        # Cambiar el turno al ratón para que pueda hacer su movimiento
        self.turno_raton = True

    # ---------------------------------------------------------------- Evaluar estado -------------------------------------------------------------------
    def evaluar_estado(self, posicion_gato, posicion_raton):
        # Evaluar el estado actual del tablero
        if posicion_gato == posicion_raton:
            return float('inf')  # Gana el gato
        distancia = abs(posicion_gato[0] - posicion_raton[0]) + abs(posicion_gato[1] - posicion_raton[1])
        return -distancia  # Queremos minimizar la distancia para el gato

    # ----------------------------------------------------------------- Algoritmo minimax ---------------------------------------------------------------------
    def minimax(self, posicion_gato, posicion_raton, profundidad, max_jugador):
        ''' Evalúa la distancia entre el gato y el ratón haciendo una predicción de jugadas futuras 
            y eligiendo el mejor camino posible hacia el ratón disminuyendo la distancia entre ellos '''
        # Verificar si el juego ha terminado o si se ha alcanzado la profundidad máxima
        if posicion_gato == posicion_raton or profundidad == 0:
            # Evaluar el estado actual del tablero
            return self.evaluar_estado(posicion_gato, posicion_raton), posicion_gato
        
        if max_jugador:
            # Inicializar el valor máximo y el mejor movimiento para el gato
            max_eval = float('-inf')
            mejor_movimiento = posicion_gato
            # Iterar sobre todos los movimientos posibles del gato
            for mov in self.movimientos_posibles(posicion_gato):
                # Llamada recursiva a minimax para el turno del ratón
                eval, _ = self.minimax(mov, posicion_raton, profundidad - 1, False)
                # Actualizar el valor máximo y el mejor movimiento si se encuentra una mejor evaluación
                if eval > max_eval:
                    max_eval = eval
                    mejor_movimiento = mov
            return max_eval, mejor_movimiento
        else:
            # Inicializar el valor mínimo y el mejor movimiento para el ratón
            min_eval = float('inf')
            mejor_movimiento = posicion_raton
            # Iterar sobre todos los movimientos posibles del ratón
            for mov in self.movimientos_posibles(posicion_raton):
                # Llamada recursiva a minimax para el turno del gato
                eval, _ = self.minimax(posicion_gato, mov, profundidad - 1, True)
                # Actualizar el valor mínimo y el mejor movimiento si se encuentra una mejor evaluación
                if eval < min_eval:
                    min_eval = eval
                    mejor_movimiento = mov
            return min_eval, mejor_movimiento

    # ----------------------------------------------------------------- Movimientos posibles -------------------------------------------------------------------
    def movimientos_posibles(self, posicion):
        x, y = posicion
        posibles = []
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Posibles movimientos en las direcciones: arriba, abajo, izquierda, derecha
        for dx, dy in direcciones:
            nuevo_x = x + dx
            nuevo_y = y + dy
            # Verificar si el movimiento está dentro de los límites del tablero y no es un obstáculo
            dentro_de_limites = (0 <= nuevo_x < len(self.tablero_lista)) and (0 <= nuevo_y < len(self.tablero_lista))
            no_es_obstaculo = (nuevo_x, nuevo_y) not in self.obstaculos
            if dentro_de_limites and no_es_obstaculo:
                posibles.append((nuevo_x, nuevo_y))
        return posibles
