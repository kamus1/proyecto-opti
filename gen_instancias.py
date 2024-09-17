#Grupo 12 A=2 B=1 software a= LpSolve
from random import *


#------Parámetros-------#
cantidad_asignaturas = 40 #de tabla 1 
cantidad_salas       = 3  #de tabla 2 
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
        tipo =2
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
            cantidad_bloques = 1
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
            cantidad_bloques = 1
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
    interes = randint(40,80)
    
    
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
    capacidad = randint(45,80)
    
    tupla_salas = (id_sala, capacidad)
    salas.append(tupla_salas)
    
    
#exportar a un .txt
with open('salas.txt', 'w') as f:
    for e in salas:
        f.write(f"id_sala: {e[0]}, capacidad: {e[1]}\n")

print("Datos exportados a 'salas.txt'")
