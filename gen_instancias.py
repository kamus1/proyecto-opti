#Grupo 12 A=2 B=1 software a) LpSolve
from random import *


#------Parámetros-------#
cantidad_asignaturas = 10 #de tabla 1 
cantidad_salas       = 1  #de tabla 2 

#rangos de interes asignatura
interes_asginatura_inferior=40 #40
interes_asignatura_superior=80 #80

#rangos de capacidad sala
capacidad_sala_inferior=45 #45
capacidad_sala_superior=80 #80

bloques_no_validos = [7, 14, 21, 28, 35] #bloques no validos para asignaturas de 2 bloques consecutivos
#-----------------------#




lista_asignaturas = [] #lista de tuplas de asignaturas (id_asignatura, tipo, prioridad, cantidad_bloques, horarios_profe_no_puede, interes)


#calcular tipos (tipo 0 = no prioritaria, tipo 1 = prioritaria o indispensable)
#por cada 5 asignaturas hay 1 prioritaria (tipo 1), es decir 20% tipo 1 y 80% tipo 0
num_indispensables = round(cantidad_asignaturas*0.2)
num_no_prioritarias      = round(cantidad_asignaturas*0.8)
#crear una lista con los tipos según la proporción
lista_tipos = [1] * num_indispensables + [0] * num_no_prioritarias 
shuffle(lista_tipos) # barajar la lista de tipos para aleatoriedad


#calculo de los bloques necesarios B=2; 65% 1 bloque, y 35% 2 bloques
cantidad_asignaturas_1_bloque = round(cantidad_asignaturas*0.65)
cantidad_asignaturas_2_bloque = cantidad_asignaturas - cantidad_asignaturas_1_bloque  #round(cantidad_asignaturas*0.35) #puede pasar el caso 50*0.65 = 32.5 redondeando = 33, y 50*0.32 = 17,5 = 18 -> 18+33= 51 != 50 agrega uno más
#crear una lista con los bloques
lista_bloques = [1] * cantidad_asignaturas_1_bloque + [2] * cantidad_asignaturas_2_bloque
shuffle(lista_bloques) # barajar la lista para aleatoriedad





#------------------------------------------GENERAR LAS ASIGNATURAS--------------------------------------------------------------#
for i in range(1,cantidad_asignaturas+1):
    id_asignatura = i
    
    tipo = lista_tipos[i - 1] # asignar el tipo secuencialmente de la lista ya barajada
    cantidad_bloques = lista_bloques[i - 1]  # asignar el bloque de la lista barajada
    
    #calcular las prioridades de manera aleatoria entre los rangos correspondientes
    prioridad = randint(6, 10) if tipo == 1 else randint(1, 5)
    
    
    #generar horarios en los que el profe NO puede
    total_horarios =35  # 7 bloques horarios * 5 dias
    cantidad_no_puede = randint(7,21) # de manera aleatoria entre 7 y 21
    horarios_profe_no_puede = []
    
    for i in range(1, cantidad_no_puede+1): #desde 1 hasta cantidad_no_puede
        bloque_que_no_puede = randint(1,35) # cual bloque horario no puede es seleccionado de manera aleatoria
        
        #si el bloque ya está en la lista de los que no puede, generar un numero hasta que no esté en la lista
        while bloque_que_no_puede in horarios_profe_no_puede: 
            bloque_que_no_puede = randint(1,35)

        horarios_profe_no_puede.append(bloque_que_no_puede)


    #generar el interes en esta asignatura
    interes = randint(interes_asginatura_inferior,interes_asignatura_superior)
    
    #agregar datos a la lista
    tupla_datos = (id_asignatura, tipo, prioridad, cantidad_bloques, horarios_profe_no_puede,interes)
    lista_asignaturas.append(tupla_datos)
    
#print
#for e in lista_asignaturas: print("id_asignatura:", e[0] , "tipo:", e[1], "prioridad:", e[2], "num_bloques:", e[3],"interes:", e[5] ,"horario_no_puede_profe" , e[4])
    
    
#exportar asignaturas a un archivo .txt
with open('asignaturas.txt', 'w') as f:
    for e in lista_asignaturas:
        f.write(f"id_asignatura: {e[0]}, tipo: {e[1]}, prioridad: {e[2]}, num_bloques: {e[3]}, interes: {e[5]}, horario_no_puede_profe: {e[4]}\n")

print("Datos exportados a 'asignaturas.txt'")
#-----------------------------------------------------------------------------------------------------------------------------------#


#----------------------GENERAR LAS SALAS--------------------#
salas = []
for i in range(1,cantidad_salas+1):
    id_sala = i
    capacidad = randint(capacidad_sala_inferior,capacidad_sala_superior)
    
    tupla_salas = (id_sala, capacidad)
    salas.append(tupla_salas)
     
#exportar salas a un archivo .txt
with open('salas.txt', 'w') as f:
    for e in salas:
        f.write(f"id_sala: {e[0]}, capacidad: {e[1]}\n")

print("Datos exportados a 'salas.txt'")
#-----------------------------------------------------------#




#-----------------------GENERAR EL INPUT PARA LPSOLVE--------------------------------#
nombre_archivo_input= "input.lp"
with open(nombre_archivo_input, 'w') as f:

    #Función Objetivo
    f.write("/* Funcion Objetivo*/\n")
    f.write("Max:")
    for i in range(1, cantidad_asignaturas+1):
        index_de_asignatura = i-1
        for j in range (1, 36):
            for k in range(1, cantidad_salas+1):
                prioridad_ijk = lista_asignaturas[index_de_asignatura][2]  
                f.write(f"{prioridad_ijk} x{i}_{j}_{k} + ")
    
    f.seek(f.tell() - 3)#elimina el último " + "
    f.write(";\n")
    

    f.write("\n/* Restricciones 1: Controla cuantos bloques (1 o 2) puede ocupar una asignatura i */\n")
    for i in range(1, cantidad_asignaturas+1):
        cantidad_bloques = lista_asignaturas[i-1][3]  #obtener la cantidad de bloques requeridos (1 o 2 bloques)
        # D_i: es 1 si necesita 2 bloques, 0 si necesita 1 bloque.
        D_i = 1 if cantidad_bloques == 2 else 0 # si necesita 2 bloques D_i se activa

        for j in range (1, 36):
            for k in range(1, cantidad_salas+1):
                f.write(f"x{i}_{j}_{k} + ")

        f.seek(f.tell() - 3)  # elimina el último " + "
        valor_r1 = 1 + D_i
        #f.write(f" <= 1 +{D_i};\n") 
        f.write(f" <= {valor_r1};\n") 


    f.write("\n/* Restricciones 2: Solo una asignatura por bloque y sala */\n")
    for j in range(1, 36): #iterar sobre los bloques (1 a 35)
        for k in range(1, cantidad_salas+1):  #iterar sobre las salas
            for i in range(1, cantidad_asignaturas+1):  #iterar sobre las asignaturas
                f.write(f"x{i}_{j}_{k} + ")  # sumar todas las asignaturas que están en el bloque 'j' y sala 'k'
            
            f.seek(f.tell() - 3)  # elimina el último " + "
            f.write(" <= 1;\n")  # Asegura que solo una asignatura esté en el bloque 'j' y sala 'k'


    f.write("\n/* Restricciones 3: Asignaturas solo se dictan en salas que cubran la capacidad de inscritos*/\n")
    for i in range(1, cantidad_asignaturas + 1):  #por cada asignatura
        interes_asignatura = lista_asignaturas[i-1][5]  #obtener el interés (I_i)
        for k in range(1, cantidad_salas + 1):  #paara cada sala
            capacidad_sala = salas[k-1][1]  #obtener la capacidad de la sala (C_k)
            for j in range(1, 36):  #para cada bloque de tiempo
                f.write(f"{interes_asignatura} x{i}_{j}_{k} <= {capacidad_sala} x{i}_{j}_{k};\n")
    
    f.write("\n/* Restricciones 4: Asignaturas indispensables W_i se debene realizar en 1 o 2 bloques dependiendo de D_i */\n")
    for i in range(1, cantidad_asignaturas + 1):  #por cada asignatura
        tipo_asignatura = lista_asignaturas[i-1][1]  #obtener el tipo de la asignatura (indispensable o evaluación)
        cantidad_bloques = lista_asignaturas[i-1][3]  # Obtener la cantidad de bloques requeridos (1 o 2 bloques)
        
        #W_i es 1 si la asignatura es indispensable (tipo == 1), de lo contrario es 0 (no prioritaria).
        W_i =  1 if tipo_asignatura == 1 else 0 
        
        #D_i: Es 1 si necesita 2 bloques, 0 si necesita 1 bloque.
        D_i = 1 if cantidad_bloques == 2 else 0 #si necesita 2 bloques D_i se activa
        
        # generar la sumatoria para todos los bloques y salas para la asignatura i
        sumatoria = ""
        for j in range(1, 36): 
            for k in range(1, cantidad_salas+1):  
                sumatoria += f"x{i}_{j}_{k} + "
        
        # quitar el último " + "
        sumatoria = sumatoria.rstrip(" + ")

        valor_r3 = 1*W_i + D_i*W_i #calcular el valor antes por posibles problemas en lpsolve
        #f.write(f"{sumatoria} >= 1 {W_i} + {D_i} {W_i};\n")
        f.write(f"{sumatoria} >= {valor_r3};\n")

    f.write("\n/* Restricciones 5: Para salas de 2 bloques consecutivos y en la misma sala, verificando si son prioritarias o no*/\n")

    f.write("/* Restriccion: y_i >= W_i */\n")
    for i in range(1, cantidad_asignaturas + 1):
        tipo_asignatura = lista_asignaturas[i-1][1]  # tipo (1 if indispensable, 0 if evaluacion)
        W_i = 1 if tipo_asignatura == 1 else 0
        f.write(f"y{i} >= {W_i};\n")
        
    f.write("\n/* Restriccion: x_{ijk} <= y_i */\n")
    for i in range(1, cantidad_asignaturas + 1):
        for j in range(1, 36):
            for k in range(1, cantidad_salas + 1):
                f.write(f"x{i}_{j}_{k} - y{i} <= 0;\n")

    f.write("\n/* Restricciones: t_{ijk} <= x_{ijk} and t_{ijk} <= x_{i(j+1)k} */\n")
    for i in range(1, cantidad_asignaturas + 1):
        for j in range(1, 35):  # solo llega hasta 34, por eso no ocupamos el 36, cuando j=34 el j+1= 35
            if j not in bloques_no_validos:
                for k in range(1, cantidad_salas + 1):
                    f.write(f"t{i}_{j}_{k} - x{i}_{j}_{k} <= 0;\n")
                    f.write(f"t{i}_{j}_{k} - x{i}_{j+1}_{k} <= 0;\n")
    
    f.write("\n/* Restriccion: t_{ijk} >= x_{ijk} + x_{i(j+1)k} - 1 */\n")
    for i in range(1, cantidad_asignaturas + 1):
        for j in range(1, 35):
            if j not in bloques_no_validos:
                for k in range(1, cantidad_salas + 1):
                    f.write(f"t{i}_{j}_{k} - x{i}_{j}_{k} - x{i}_{j+1}_{k} >= -1;\n") #restriccion de activacion de t_ijk


    f.write("\n/* Restriction: sum de t_{ijk} = D_i * y_i */\n")
    for i in range(1, cantidad_asignaturas + 1):
        cantidad_bloques = lista_asignaturas[i-1][3]  # numero de bloques requeridos
        D_i = 1 if cantidad_bloques == 2 else 0
        sum_tijk = ""
        for j in range(1, 35): #solo hasta 34, t_35 no se puede activar 
            if j not in bloques_no_validos:
                for k in range(1, cantidad_salas + 1):
                    sum_tijk += f"t{i}_{j}_{k} + "
        if sum_tijk:
            sum_tijk = sum_tijk.rstrip(" + ")
            f.write(f"{sum_tijk} = {D_i} y{i};\n")
        else:
            # variables tijk no validas
            f.write(f"0 = {D_i} y{i};\n")
        
    f.write("\n/* Restriccion 6: No asignar bloques consecutivos que crucen de un dia a otro */\n")
    for i in range(1, cantidad_asignaturas + 1):
        D_i = 1 if lista_asignaturas[i-1][3] == 2 else 0  # Si la asignatura necesita 2 bloques, D_i = 1
        
        if D_i == 1:
            for k in range(1, cantidad_salas + 1):  
                for j in [7, 14, 21, 28]:  
                    # restricción: D_i * (x_{ijk} + x_{i(j+1)k}) <= 1
                    f.write(f"{D_i} x{i}_{j}_{k} + {D_i} x{i}_{j+1}_{k} <= 1;\n")
    
    
    #restricción de disponibilidad del profesor
    f.write("\n/* Restriccion 7: Una asignatura no puede realizarse en un bloque si el profesor no está disponible */\n")
    for i in range(1, cantidad_asignaturas + 1):
        bloques_no_disponibles = lista_asignaturas[i-1][4]  #lista de bloques en los que el profesor no puede dictar clases
        
        for j in range(1, 36):  # para cada bloque de tiempo
            R_ij = 0 if j in bloques_no_disponibles else 1  # R_ij = 0 si el profesor no puede, 1 si puede
            
            for k in range(1, cantidad_salas + 1):  
                f.write(f"x{i}_{j}_{k} <= {R_ij} x{i}_{j}_{k};\n")     
                    
                    
                
    f.write("/* Restriccion 8: Definir que las variables son binarias */\n")
    f.write("bin ")
    for i in range(1, cantidad_asignaturas + 1):
        for j in range(1, 36):  
            for k in range(1, cantidad_salas + 1):
                # declarar cada variable x_{ijk} como binaria
                f.write(f"x{i}_{j}_{k}, ")

    f.seek(f.tell() - 2) #eliminar la última coma
    f.write(";\n")
    
    #declarar t_ijk como variables binarias
    f.write("bin ")
    for i in range(1, cantidad_asignaturas + 1):
        for j in range(1, 35):  # para cada bloque de tiempo, excluyendo los finales
            if j not in [7, 14, 21, 28, 35]:
                for k in range(1, cantidad_salas + 1): 
                    f.write(f"t{i}_{j}_{k}, ")  # declarar t_{ijk} como binaria
    #eliminar la última coma
    f.seek(f.tell() - 2)  
    f.write(";\n")
    
    
    #declarar y_i como variables binarias
    f.write("bin ")
    for i in range(1, cantidad_asignaturas + 1):
        f.write(f"y{i}, ")
    f.seek(f.tell() - 2)
    f.write(";\n")

print("Input creado correctamente en " + nombre_archivo_input)
#------------------------------------------------------------------------------------#     
        
        