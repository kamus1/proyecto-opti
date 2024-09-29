from random import *

class Asignatura:
    def __init__(self):
        self.categoria = randint(0,1) # 0: en evaluación | 1: indispensable
        self.prioridad = randint(6,10) if self.categoria else randint(1,5)
        self.bloques = randint(1,2) # 1: 1 bloque | 2: 2 bloques
        self.interes = randint(40,80)
        self.horarios_profe_no_puede = []
        
        cantidad_no_puede = randint(7, 21)
        
        for i in range(cantidad_no_puede):
            bloque_que_no_puede = randint(1,35)
        
            # si el bloque ya está en la lista de los que no puede, generar un número hasta que no esté
            while bloque_que_no_puede in self.horarios_profe_no_puede: 
                bloque_que_no_puede = randint(1,35)

            self.horarios_profe_no_puede.append(bloque_que_no_puede)

        #print(f'Asignatura creada categoria: {"indispensable" if self.categoria else "en evaluación"} con prioridad: {self.prioridad} de {"2 bloque" if (self.bloques == 2) else "1 bloque"}, con interes de {self.interes}, el profesor no puede en los horarios: {self.horarios_profe_no_puede}')
        
class Problema:
    def __init__(self, num_asignaturas, num_salas):
        self.num_asignaturas = num_asignaturas
        
        # Generar salas con capacidad entre 45 y 80
        self.salas = [randint(45, 80) for _ in range(num_salas)]
        
        # Cálculos de las asignaturas
        num_asignaturas_indispensables = round(self.num_asignaturas*0.2)
        num_asignaturas_en_evaluacion = round(self.num_asignaturas*0.8)
        num_asignaturas_1_bloque = round(self.num_asignaturas*0.65)
        num_asignaturas_2_bloque = round(self.num_asignaturas*0.35)
        
        self.asignaturas = []
        
        # Distribuir asignaturas
        while (num_asignaturas_indispensables > 0 or num_asignaturas_en_evaluacion > 0 or num_asignaturas_1_bloque > 0 or num_asignaturas_2_bloque > 0):
            asignatura = Asignatura()
            if ((asignatura.categoria and asignatura.bloques == 2) and (num_asignaturas_indispensables > 0 and num_asignaturas_2_bloque > 0)): #indispensable y 2 bloques
                self.asignaturas.append(asignatura)
                num_asignaturas_indispensables -= 1
                num_asignaturas_2_bloque -= 1
            elif ((not asignatura.categoria and asignatura.bloques == 1) and (num_asignaturas_en_evaluacion > 0 and num_asignaturas_1_bloque > 0)): #en evaluacion y 1 bloque
                self.asignaturas.append(asignatura)
                num_asignaturas_en_evaluacion -= 1
                num_asignaturas_1_bloque -= 1
            elif ((not asignatura.categoria and asignatura.bloques == 2) and (num_asignaturas_en_evaluacion > 0 and num_asignaturas_2_bloque > 0)): #en evaluacion y 2 bloques
                self.asignaturas.append(asignatura)
                num_asignaturas_en_evaluacion -= 1
                num_asignaturas_2_bloque -= 1
            elif ((asignatura.categoria and asignatura.bloques == 1) and (num_asignaturas_indispensables > 0 and num_asignaturas_1_bloque > 0)): #indispensable y 1 bloque
                self.asignaturas.append(asignatura)
                num_asignaturas_indispensables -= 1
                num_asignaturas_1_bloque -= 1

def main():
    problema = Problema(40, 3) #40 asignaturas | 3 salas
    
    with open('problema.txt', 'w', encoding='utf8') as file:
        # Imprimir salas
        file.write('Salas:\n')
        print(problema.salas)
        for i, sala in enumerate(problema.salas):
            file.write(f'Sala {i + 1} con capacidad para {problema.salas[i]} alumnos.\n')
        
        # Imprimir asignaturas
        file.write('\nAsignaturas:\n')
        for i, asignatura in enumerate(problema.asignaturas):
            file.write(f'Asignatura {i + 1}: {"Indispensable" if problema.asignaturas[i].categoria else "En evaluación"} con prioridad: {problema.asignaturas[i].prioridad} de {"2 bloque" if (problema.asignaturas[i].bloques == 2) else "1 bloque"}, con interes de {problema.asignaturas[i].interes}, el profesor no puede en los horarios: {problema.asignaturas[i].horarios_profe_no_puede}.\n')

if '__main__' == __name__:
    main()