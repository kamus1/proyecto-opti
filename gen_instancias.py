#Grupo 12 A=2 B=1 software a= LpSolve
from random import *


#------Parámetros-------#
cantidad_asignaturas = 1 #de tabla 1 
cantidad_salas       = 1  #de tabla 2 

#rangos interes asignatura
interes_asginatura_inferior=40 #40
interes_asignatura_superior=80 #80

#rangos capacidad sala
capacidad_sala_inferior=45 #45
capacidad_sala_superior=80 #80
#-----------------------#


#lista de tuplas de asignaturas (id_sala,)
lista_asignaturas = []

#calcular tipos (tipo 1 = indispensable, tipo 2 = evaluación)
#por cada 5 asigntaruas hay 1 indipispensable (tipo 1), es decir 20% tipo 1 y 80% tipo 2
num_indispensables = round(cantidad_asignaturas*0.2)
num_evaluacion     = round(cantidad_asignaturas*0.8)


#----- calculo de los bloques necesarios B=2 ----# #65% 1 bloque, y 35% 2 bloques
cantidad_asignaturas_1_bloque = round(cantidad_asignaturas*0.65)
cantidad_asignaturas_2_bloque = round(cantidad_asignaturas*0.35)


for i in range(1,cantidad_asignaturas+1):
    id_asignatura = i
    
    #tipo
    tipo = 0
    if num_indispensables >0:
        tipo = 1
        num_indispensables -=1
    elif num_evaluacion >0:
        tipo = 2#2
        num_evaluacion -=1        
    else:
        tipo = 0 # algo salió mal
        
    
    #calcular las prioridades de manera aleatoria entre los rangos correspondientes
    prioridad = 0
    if tipo == 1: #tipo indispensable
        prioridad = randint(6, 10)
    elif tipo ==2: #tipo evaluacion
        prioridad = randint(1,5)
    
    
    #asignar los bloques
    tipo_a_usar = randint(1,2)
    cantidad_bloques = 0
    
    if tipo_a_usar == 1:
        if cantidad_asignaturas_1_bloque !=0:
            cantidad_bloques = 1 #1
            cantidad_asignaturas_1_bloque -=1
        else:
            #si no hay de bloque 1 usar del 2
            cantidad_bloques = 2
            cantidad_asignaturas_2_bloque -=1
    elif tipo_a_usar ==2:
        if cantidad_asignaturas_2_bloque !=0:
            cantidad_bloques = 2
            cantidad_asignaturas_2_bloque -=1
        else:
            #si no hay de bloque 2 usar del 1
            cantidad_bloques = 1 #1
            cantidad_asignaturas_1_bloque -=1
    
    
    #generar horarios en los que el profe NO puede
    total_horarios =35  # 7 bloques horarios * 5 dias
    cantidad_no_puede = randint(7,21)
    horarios_profe_no_puede = []
    
    for i in range(1, cantidad_no_puede+1): #desde 1 cantidad_no_puede
        bloque_que_no_puede = randint(1,35)
        
        #si el bloque ya está en la lista de los que no puede generar un numero hasta que no esté
        while bloque_que_no_puede in horarios_profe_no_puede: 
            bloque_que_no_puede = randint(1,35)

        horarios_profe_no_puede.append(bloque_que_no_puede)


    
    #-----generar el interes en esta asignatura-----#
    #numero random entre 40 y 80
    interes = randint(interes_asginatura_inferior,interes_asignatura_superior)
    
    
    #agregar datos a la lista
    tupla_datos = (id_asignatura,tipo,prioridad, cantidad_bloques,horarios_profe_no_puede,interes)
    lista_asignaturas.append(tupla_datos)
    
#print (después exportar como .txt u otra cosa)
for e in lista_asignaturas:
    print("id_asignatura:", e[0] , "tipo:", e[1], "prioridad:", e[2], "num_bloques:", e[3],"interes:", e[5] ,"horario_no_puede_profe" , e[4])
    
    
#exportar a un .txt
with open('asignaturas.txt', 'w') as f:
    for e in lista_asignaturas:
        f.write(f"id_asignatura: {e[0]}, tipo: {e[1]}, prioridad: {e[2]}, num_bloques: {e[3]},interes: {e[5]}, horario_no_puede_profe: {e[4]}\n")

print("Datos exportados a 'asignaturas.txt'")


#generar salas
salas = []
for i in range(1,cantidad_salas+1):
    id_sala = i
    capacidad = randint(capacidad_sala_inferior,capacidad_sala_superior)
    
    tupla_salas = (id_sala, capacidad)
    salas.append(tupla_salas)
     
#exportar a un .txt
with open('salas.txt', 'w') as f:
    for e in salas:
        f.write(f"id_sala: {e[0]}, capacidad: {e[1]}\n")

print("Datos exportados a 'salas.txt'")



#generar el input de lpsolve
with open('input.lp', 'w') as f:
    #comentario fo
    f.write("/* Funcion Objetivo*/\n")
    #funcion objetivo
    f.write("Max:")
    for i in range(1, cantidad_asignaturas+1):
        index_de_asignatura = i-1
        for j in range (1, 36):
            for k in range(1, cantidad_salas+1):
                prioridad_ijk = lista_asignaturas[index_de_asignatura][2]  
                f.write(f"{prioridad_ijk} x{i}_{j}_{k} + ")
    
    #quitar el último " + "
    f.seek(f.tell() - 3)#elimina el último " + "
    f.write(";\n\n") #termina la línea de la función objetivo con un ";"

    f.write("/* Restricciones 1*/\n")
    for i in range(1, cantidad_asignaturas+1):
        cantidad_bloques = lista_asignaturas[i-1][3]  #obtener la cantidad de bloques requeridos (1 o 2 bloques)
        # D_i: es 1 si necesita 2 bloques, 0 si necesita 1 bloque.
        D_i = 1 if cantidad_bloques == 2 else 0 # si necesita 2 bloques D_i se activa

        for j in range (1, 36):
            for k in range(1, cantidad_salas+1):
                f.write(f"x{i}_{j}_{k} + ")

        f.seek(f.tell() - 3)  # elimina el último " + "
        # agregar la restricción <= 1
        valor_r1 = 1 + D_i
        #f.write(f" <= 1 +{D_i};\n") 
        f.write(f" <= {valor_r1};\n") 



    f.write("\n")
    f.write("/* Restricciones 2: Asignaturas solo se dictan en salas que cubran la capacidad de inscritos*/\n")
    for i in range(1, cantidad_asignaturas + 1):  #por cada asignatura
        interes_asignatura = lista_asignaturas[i-1][5]  #obtener el interés (I_i)
        for k in range(1, cantidad_salas + 1):  #paara cada sala
            capacidad_sala = salas[k-1][1]  #obtener la capacidad de la sala (C_k)
            for j in range(1, 36):  #para cada bloque de tiempo
                f.write(f"{interes_asignatura} x{i}_{j}_{k} <= {capacidad_sala};\n")
    
    f.write("\n/* Restricciones 3: Asignaturas indispensables en 1 o 2 bloques dependiendo de D_i (incluye W_i = 0) */\n")
    for i in range(1, cantidad_asignaturas + 1):  #por cada asignatura
        tipo_asignatura = lista_asignaturas[i-1][1]  #obtener el tipo de la asignatura (indispensable o evaluación)
        cantidad_bloques = lista_asignaturas[i-1][3]  # Obtener la cantidad de bloques requeridos (1 o 2 bloques)
        
        # W_i: Asumimos que W_i es 1 si la asignatura es indispensable (tipo == 1), de lo contrario es 0.
        W_i = 1 if tipo_asignatura == 1 else 0 # (si es del tipo 2 es no indispensable)
        
        # D_i: Es 1 si necesita 2 bloques, 0 si necesita 1 bloque.
        D_i = 1 if cantidad_bloques == 2 else 0 #si necesita 2 bloques D_i se activa
        
        # Generar la sumatoria para todos los bloques y salas para la asignatura i
        sumatoria = ""
        for j in range(1, 36):  # Bloques de 1 a 35
            for k in range(1, cantidad_salas + 1):  # Salas de 1 a cantidad_salas
                sumatoria += f"x{i}_{j}_{k} + "
        
        # Quitar el último " + "
        sumatoria = sumatoria.rstrip(" + ")

        # Escribir la restricción con la suma de W_i y D_i*W_i, usando paréntesis
        valor_r3 = 1*W_i + D_i*W_i
        #f.write(f"{sumatoria} >= 1 {W_i} + {D_i} {W_i};\n")
        f.write(f"{sumatoria} >= {valor_r3};\n")

    f.write("\n/* Restricciones 4: Bloques consecutivos en la misma sala si D_i = 1 */\n")
    for i in range(1, cantidad_asignaturas + 1):
        D_i = 1 if lista_asignaturas[i-1][3] == 2 else 0  # Si la asignatura necesita 2 bloques, D_i = 1
        
        if D_i == 1:
            for k in range(1, cantidad_salas + 1):  # Para cada sala
                for j in range(1, 35):  # Para cada bloque excepto el último de cada día
                    if j not in [7, 14, 21, 28, 35]:  # Bloques no al final de un día
                        # Añadir la restricción
                        f.write(f"{D_i} x{i}_{j}_{k} = {D_i} x{i}_{j+1}_{k};\n")
    
    f.write("\n/* Restriccion 5: No asignar bloques consecutivos que crucen de un dia a otro */\n")
    for i in range(1, cantidad_asignaturas + 1):
        D_i = 1 if lista_asignaturas[i-1][3] == 2 else 0  # Si la asignatura necesita 2 bloques, D_i = 1
        
        if D_i == 1:
            for k in range(1, cantidad_salas + 1):  # Para cada sala
                for j in [7, 14, 21, 28]:  # Bloques finales del día
                    # Añadir la restricción: D_i * (x_{ijk} + x_{i(j+1)k}) <= 1
                    f.write(f"{D_i} x{i}_{j}_{k} + {D_i} x{i}_{j+1}_{k} <= 1;\n")
    
    '''         
    f.write("\n/* Restriccion 6: Una asignatura no puede ser asignada en un bloque donde el profesor no está disponible */\n")
    for i in range(1, cantidad_asignaturas + 1):
        # Obtener la lista de bloques en los que el profesor de la asignatura i no puede
        bloques_no_disponibles = lista_asignaturas[i-1][4]  # lista con los bloques no disponibles para la asignatura i
        
        for j in bloques_no_disponibles:  # Para cada bloque en que el profesor no puede
            for k in range(1, cantidad_salas + 1):  # Para cada sala
                # Añadir la restricción: x_{ijk} <= 0
                f.write(f"x{i}_{j}_{k} = 0;\n")
    '''
    
    f.write("/* Restriccion 6: Una asignatura no puede realizarse en un bloque si el profesor no está disponible */\n")
    for i in range(1, cantidad_asignaturas + 1):
        # Obtener la lista de bloques en los que el profesor NO puede
        bloques_no_disponibles = lista_asignaturas[i-1][4]  # lista con los bloques no disponibles para la asignatura i
        
        for j in range(1, 36):  # Para cada bloque de tiempo
            R_ij = 0 if j in bloques_no_disponibles else 1  # Si el bloque está en la lista, R_ij = 0, si no, R_ij = 1
            for k in range(1, cantidad_salas + 1):  # Para cada sala
                # Escribir la restricción: sum_k x_{ijk} <= R_{ij}
                f.write(f"x{i}_{j}_{k} <= {R_ij};\n")
                
    f.write("/* Restriccion 7: Definir que las variables son binarias */\n")
    f.write("bin ")
    for i in range(1, cantidad_asignaturas + 1):
        for j in range(1, 36):  # Para cada bloque de tiempo
            for k in range(1, cantidad_salas + 1):  # Para cada sala
                # Declarar cada variable x_{ijk} como binaria
                f.write(f"x{i}_{j}_{k}, ")
    # Eliminar la última coma y agregar el punto y coma para terminar la declaración de variables binarias
    f.seek(f.tell() - 2)  # Eliminar la última coma
    f.write(";\n")