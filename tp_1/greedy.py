import sys
import argparse

def asignar_transacciones(transacciones_aproximadas, transacciones_sospechoso):
    asignaciones = dict()

    for tiempo,error in transacciones_aproximadas:
        indice = busqueda_recursiva( (tiempo - error, tiempo + error),transacciones_sospechoso, 0,len(transacciones_sospechoso)-1)
        if indice < 0:
            return None
        
        asignaciones[transacciones_sospechoso[indice]] = (tiempo, error)
    
    return asignaciones



def busqueda_recursiva( intervalo, transacciones , izq, der):
    if(izq == der):
        return izq
    
    if(izq > der ):
        return -1
    
    medio = (izq + der) // 2

    if(transacciones[medio] in range(*intervalo)):
        return medio 
    
    if(transacciones[medio] > intervalo[1]):
        return busqueda_recursiva( intervalo, transacciones , izq, medio - 1)
    
    return busqueda_recursiva( intervalo, transacciones , medio +1 , der)
    

def asignar_transacciones_2(transacciones_aproximadas, transacciones_sospechoso):
    n = len(transacciones_aproximadas)
    
    # Construimos la lista de intervalos con su índice original
    intervalos = []
    for i, (t, e) in enumerate(transacciones_aproximadas):
        a = t - e
        b = t + e
        intervalos.append((a, b, i))
    
    # Ordenamos los intervalos por su extremo derecho (b)
    intervalos.sort(key=lambda x: x[1])

    
    
    asignacion = [None] * n  # asignacion[i] guardará el timestamp asignado para la transacción con índice i
    
    usados = set()
    # Recorremos cada intervalo (en orden de b)
    for a, b, i in intervalos:
        j = 0  # puntero para transacciones_sospechoso
        while transacciones_sospechoso[j] < a or transacciones_sospechoso[j] > b or transacciones_sospechoso[j] in usados:
            j += 1
            if j >= n:
                return None
        
        asignacion[i] = transacciones_sospechoso[j]
        usados.add(transacciones_sospechoso[j])
        
    
    resultado = [(i, asignacion[i]) for i in range(n)]
    resultado.sort(key=lambda x: x[1])
    return resultado

def parse_file(file_path):
    """
    Lee el archivo y extrae:
      - Una lista de transacciones aproximadas, cada una como (t, e).
      - Una lista de transacciones del sospechoso (timestamps exactos).
      
    El archivo tiene el siguiente formato:
      - La segunda línea contiene un entero n.
      - Las siguientes n líneas tienen "t,e" (timestamp aproximado y error).
      - Las siguientes n líneas contienen un timestamp exacto por línea.
      
    Retorna: (transacciones_aproximadas, transacciones_sospechoso)
    """
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    
    # La segunda línea es la cantidad de transacciones
    n = int(lines[1])
    
    # Se leen los n intervalos aproximados
    transacciones_aproximadas = []
    for line in lines[2:n+2]:
        # Separa por coma y convierte a entero (o float, si es necesario)
        t_str, e_str = line.split(",")
        transacciones_aproximadas.append((int(t_str), int(e_str)))
    
    # Se leen los n timestamps del sospechoso
    transacciones_sospechoso = [int(line) for line in lines[n+2:n+2+n]]
    
    return transacciones_aproximadas, transacciones_sospechoso

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Testear la asignación de transacciones del sospechoso a intervalos aproximados.")
    parser.add_argument('archivo', type=str, nargs='?', help='ruta absoluta del archivo a procesar')
    
    args = parser.parse_args()
    

    if not args.archivo:
        print("No se proporcionó una ruta, se correrá con un ejemplo por defecto")
        trans_aprox = [
        (10, 2),  # intervalo [8, 12]
        (20, 3),  # intervalo [17, 23]
        (30, 4)   # intervalo [26, 34]
    ]
    
        # Transacciones del sospechoso (se asume ordenadas)
        trans_sospechoso  = [9, 21, 29]
    else:
        try:
            trans_aprox, trans_sospechoso = parse_file(args.archivo)
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            sys.exit(1)
        
    resultado = asignar_transacciones_2(trans_aprox, trans_sospechoso)
    
    if resultado is None:
        print("No es el sospechoso correcto")
    else:
        #resultado = list(resultado.items())
        #resultado.sort(key=lambda x: x[0])
        #for ts_sospechoso, t_e in resultado:
        #    print(f"{ts_sospechoso} --> {t_e[0]} ± {t_e[1]}")
        for i, ts in resultado:
            print(f"{ts} --> {trans_aprox[i][0]} ± {trans_aprox[i][1]}")