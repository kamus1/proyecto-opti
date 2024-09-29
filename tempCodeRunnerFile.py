    f.write("/* Restricciones 3: Asignaturas indispensables en 1 o 2 bloques dependiendo de D_i (incluye W_i = 0) */\n")
    for i in range(1, cantidad_asignaturas + 1):  # Para cada asignatura
        tipo_asignatura = lista_asignaturas[i-1][1]  # Obtener el tipo de la asignatura (indispensable o evaluación)
        cantidad_bloques = lista_asignaturas[i-1][3]  # Obtener la cantidad de bloques requeridos (1 o 2 bloques)
        
        # W_i: Asumimos que W_i es 1 si la asignatura es indispensable (tipo == 1), de lo contrario es 0.
        W_i = 1 if tipo_asignatura == 1 else 0
        
        # D_i: Es 1 si necesita 2 bloques, 0 si necesita 1 bloque.
        D_i = 1 if cantidad_bloques == 2 else 0
        
        # Generar la sumatoria para todos los bloques y salas para la asignatura i
        sumatoria = ""
        for j in range(1, 36):  # Bloques de 1 a 35
            for k in range(1, cantidad_salas + 1):  # Salas de 1 a cantidad_salas
                sumatoria += f"x{i}_{j}_{k} + "
        
        # Quitar el último " + "
        sumatoria = sumatoria.rstrip(" + ")

        # Escribir la restricción con la suma de W_i y D_i*W_i
        f.write(f"{sumatoria} >= {W_i} + {D_i} * {W_i};\n")
