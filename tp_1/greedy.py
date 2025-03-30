import sys
import argparse

def asignar_transacciones(transacciones_aproximadas, transacciones_sospechoso):
    n = len(transacciones_aproximadas)

    transacciones_aproximadas.sort(key=lambda x: x[0] + x[1])
    
    asignacion = []
    
    usados = [False] * n
        
            
    for t, e in transacciones_aproximadas:
        j = 0
        while transacciones_sospechoso[j] < t - e or transacciones_sospechoso[j] > t + e or usados[j]:
            j += 1
            if j >= n:
                return None
            
        asignacion.append((transacciones_sospechoso[j], (t, e)))
        usados[j] = True

    return asignacion


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
        # Separa por coma y convierte a entero
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
        transacciones_sospechoso  = [9, 21, 29]
    else:
        try:
            transacciones_aproximadas, transacciones_sospechoso = parse_file(args.archivo)
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            sys.exit(1)
        
    resultado = asignar_transacciones(transacciones_aproximadas, transacciones_sospechoso)
    
    if resultado is None:
        print("No es el sospechoso correcto")
    else:
        resultado.sort(key=lambda x: x[0])
        for ts_sospechoso, t_e in resultado:
            print(f"{ts_sospechoso} --> {t_e[0]} ± {t_e[1]}")