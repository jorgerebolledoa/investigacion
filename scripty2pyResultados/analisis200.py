import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np

def extraer_datos_resultados(archivo):
    """Extrae datos del archivo de resultados y los organiza en un DataFrame"""
    
    datos = []
    
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Dividir por bloques de resultados
    bloques = contenido.split('------------------------------------------------------------------------------')
    
    for bloque in bloques:
        if 'Calculando círculo mínimo para' in bloque or 'Calculando cÝrculo mÝnimo para' in bloque:
            # Extraer número de nodos
            match_nodos = re.search(r'usando (\d+) nodos', bloque)
            if not match_nodos:
                continue
            nodos = int(match_nodos.group(1))
            
            # Extraer tiempo distribuido
            match_tiempo_dist = re.search(r'Tiempo distribuido: ([\d.]+) ms', bloque)
            if not match_tiempo_dist:
                continue
            tiempo_distribuido = float(match_tiempo_dist.group(1))
            
            # Extraer tiempo secuencial
            match_tiempo_seq = re.search(r'Tiempo secuencial: ([\d.]+) ms', bloque)
            if not match_tiempo_seq:
                continue
            tiempo_secuencial = float(match_tiempo_seq.group(1))
            
            # Extraer speedup
            match_speedup = re.search(r'Speedup: ([\d.]+)x', bloque)
            if not match_speedup:
                continue
            speedup = float(match_speedup.group(1))
            
            # Extraer radio del círculo distribuido
            match_radio_dist = re.search(r'Resultado Distribuido:.*?Radio: ([\d.]+)', bloque, re.DOTALL)
            radio_distribuido = float(match_radio_dist.group(1)) if match_radio_dist else None
            
            # Extraer radio del círculo secuencial  
            match_radio_seq = re.search(r'Resultado Secuencial.*?Radio: ([\d.]+)', bloque, re.DOTALL)
            radio_secuencial = float(match_radio_seq.group(1)) if match_radio_seq else None
            
            # Extraer puntos dentro del círculo distribuido
            match_puntos_dist = re.search(r'Puntos dentro de la circunferencia: (\d+) de (\d+)', bloque)
            puntos_dentro_dist = int(match_puntos_dist.group(1)) if match_puntos_dist else None
            total_puntos = int(match_puntos_dist.group(2)) if match_puntos_dist else None
            
            # Extraer puntos dentro del círculo secuencial
            matches_puntos = re.findall(r'Puntos dentro de la circunferencia: (\d+) de (\d+)', bloque)
            puntos_dentro_seq = int(matches_puntos[1][0]) if len(matches_puntos) > 1 else None
            
            datos.append({
                'Nodos': nodos,
                'Tiempo_Distribuido_ms': tiempo_distribuido,
                'Tiempo_Secuencial_ms': tiempo_secuencial,
                'Speedup': speedup,
                'Radio_Distribuido': radio_distribuido,
                'Radio_Secuencial': radio_secuencial,
                'Puntos_Dentro_Distribuido': puntos_dentro_dist,
                'Puntos_Dentro_Secuencial': puntos_dentro_seq,
                'Total_Puntos': total_puntos,
                'Eficiencia_Distribuido': (puntos_dentro_dist/total_puntos)*100 if puntos_dentro_dist and total_puntos else None,
                'Eficiencia_Secuencial': (puntos_dentro_seq/total_puntos)*100 if puntos_dentro_seq and total_puntos else None
            })
    
    return pd.DataFrame(datos)

def crear_visualizaciones(df):
    """Crea visualizaciones de los datos"""
    
    # Configurar el estilo
    plt.style.use('default')
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Análisis de Rendimiento: Algoritmo Distribuido vs Secuencial\n200 Puntos', fontsize=16, fontweight='bold')
    
    # 1. Tiempo de ejecución
    axes[0,0].plot(df['Nodos'], df['Tiempo_Distribuido_ms'], 'o-', label='Distribuido', color='blue', linewidth=2)
    axes[0,0].plot(df['Nodos'], df['Tiempo_Secuencial_ms'], 's-', label='Secuencial', color='red', linewidth=2)
    axes[0,0].set_xlabel('Número de Nodos')
    axes[0,0].set_ylabel('Tiempo (ms)')
    axes[0,0].set_title('Tiempo de Ejecución')
    axes[0,0].legend()
    axes[0,0].grid(True, alpha=0.3)
    axes[0,0].set_yscale('log')
    
    # 2. Speedup
    axes[0,1].plot(df['Nodos'], df['Speedup'], 'o-', color='green', linewidth=2)
    axes[0,1].axhline(y=1, color='red', linestyle='--', alpha=0.7, label='Sin mejora')
    axes[0,1].set_xlabel('Número de Nodos')
    axes[0,1].set_ylabel('Speedup')
    axes[0,1].set_title('Speedup vs Número de Nodos')
    axes[0,1].legend()
    axes[0,1].grid(True, alpha=0.3)
    
    # 3. Radio del círculo
    axes[0,2].plot(df['Nodos'], df['Radio_Distribuido'], 'o-', label='Distribuido', color='blue', linewidth=2)
    axes[0,2].plot(df['Nodos'], df['Radio_Secuencial'], 's-', label='Secuencial', color='red', linewidth=2)
    axes[0,2].set_xlabel('Número de Nodos')
    axes[0,2].set_ylabel('Radio')
    axes[0,2].set_title('Radio del Círculo Mínimo')
    axes[0,2].legend()
    axes[0,2].grid(True, alpha=0.3)
    
    # 4. Eficiencia (% puntos dentro del círculo)
    axes[1,0].plot(df['Nodos'], df['Eficiencia_Distribuido'], 'o-', label='Distribuido', color='blue', linewidth=2)
    axes[1,0].plot(df['Nodos'], df['Eficiencia_Secuencial'], 's-', label='Secuencial', color='red', linewidth=2)
    axes[1,0].set_xlabel('Número de Nodos')
    axes[1,0].set_ylabel('Eficiencia (%)')
    axes[1,0].set_title('Porcentaje de Puntos Contenidos')
    axes[1,0].legend()
    axes[1,0].grid(True, alpha=0.3)
    axes[1,0].set_ylim(0, 105)
    
    # 5. Comparación de tiempos (barras)
    x = np.arange(len(df['Nodos']))
    width = 0.35
    axes[1,1].bar(x - width/2, df['Tiempo_Distribuido_ms'], width, label='Distribuido', color='blue', alpha=0.7)
    axes[1,1].bar(x + width/2, df['Tiempo_Secuencial_ms'], width, label='Secuencial', color='red', alpha=0.7)
    axes[1,1].set_xlabel('Número de Nodos')
    axes[1,1].set_ylabel('Tiempo (ms)')
    axes[1,1].set_title('Comparación de Tiempos')
    axes[1,1].set_xticks(x)
    axes[1,1].set_xticklabels(df['Nodos'])
    axes[1,1].legend()
    axes[1,1].set_yscale('log')
    
    # 6. Escalabilidad (tiempo distribuido vs ideal)
    tiempo_ideal = df['Tiempo_Distribuido_ms'].iloc[0] / df['Nodos']
    axes[1,2].plot(df['Nodos'], df['Tiempo_Distribuido_ms'], 'o-', label='Real', color='blue', linewidth=2)
    axes[1,2].plot(df['Nodos'], tiempo_ideal, '--', label='Ideal', color='orange', linewidth=2)
    axes[1,2].set_xlabel('Número de Nodos')
    axes[1,2].set_ylabel('Tiempo Distribuido (ms)')
    axes[1,2].set_title('Escalabilidad del Algoritmo Distribuido')
    axes[1,2].legend()
    axes[1,2].grid(True, alpha=0.3)
    axes[1,2].set_yscale('log')
    
    plt.tight_layout()
    plt.savefig('analisis_rendimiento.png', dpi=300, bbox_inches='tight')
    plt.show()

def mostrar_tabla_resumen(df):
    """Muestra una tabla resumen de los datos"""
    print("\n" + "="*100)
    print("TABLA RESUMEN: ANÁLISIS DE RENDIMIENTO")
    print("="*100)
    
    # Seleccionar las columnas más importantes para mostrar
    columnas_mostrar = [
        'Nodos', 
        'Tiempo_Distribuido_ms', 
        'Tiempo_Secuencial_ms', 
        'Speedup',
        'Eficiencia_Distribuido',
        'Eficiencia_Secuencial'
    ]
    
    df_mostrar = df[columnas_mostrar].copy()
    df_mostrar['Tiempo_Distribuido_ms'] = df_mostrar['Tiempo_Distribuido_ms'].round(2)
    df_mostrar['Tiempo_Secuencial_ms'] = df_mostrar['Tiempo_Secuencial_ms'].round(2)
    df_mostrar['Speedup'] = df_mostrar['Speedup'].round(2)
    df_mostrar['Eficiencia_Distribuido'] = df_mostrar['Eficiencia_Distribuido'].round(1)
    df_mostrar['Eficiencia_Secuencial'] = df_mostrar['Eficiencia_Secuencial'].round(1)
    
    print(df_mostrar.to_string(index=False))
    
    print("\n" + "="*100)
    print("ESTADÍSTICAS GENERALES")
    print("="*100)
    print(f"Mejor Speedup: {df['Speedup'].max():.2f}x con {df.loc[df['Speedup'].idxmax(), 'Nodos']} nodos")
    print(f"Menor tiempo distribuido: {df['Tiempo_Distribuido_ms'].min():.2f}ms con {df.loc[df['Tiempo_Distribuido_ms'].idxmin(), 'Nodos']} nodos")
    print(f"Mayor eficiencia distribuida: {df['Eficiencia_Distribuido'].max():.1f}% con {df.loc[df['Eficiencia_Distribuido'].idxmax(), 'Nodos']} nodos")
    print(f"Mayor eficiencia secuencial: {df['Eficiencia_Secuencial'].max():.1f}% con {df.loc[df['Eficiencia_Secuencial'].idxmax(), 'Nodos']} nodos")

if __name__ == "__main__":
    # Cargar y procesar los datos
    print("Cargando datos del archivo puntos200Resultados.txt...")
    df = extraer_datos_resultados('puntos200Resultados.txt')
    
    # Mostrar tabla resumen
    mostrar_tabla_resumen(df)
    
    # Crear visualizaciones
    print("\nGenerando visualizaciones...")
    crear_visualizaciones(df)
    
    # Guardar DataFrame en CSV para futuros análisis
    df.to_csv('analisis_200_puntos.csv', index=False)
    print("\nDatos guardados en 'analisis_200_puntos.csv'")
    print("Gráficos guardados en 'analisis_rendimiento.png'")
