import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np

def parsear_resultados_resamano2(archivo):
    """Parsea los resultados del archivo resamano2.txt"""
    
    datos = []
    
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Dividir por bloques usando diferentes separadores
    bloques = re.split(r'[-]{50,}', contenido)
    
    for bloque in bloques:
        if 'Calculando' in bloque and 'nodos' in bloque:
            try:
                # Extraer número de nodos
                match_nodos = re.search(r'usando (\d+) nodos', bloque)
                if not match_nodos:
                    continue
                nodos = int(match_nodos.group(1))
                
                # Extraer tiempo distribuido
                match_tiempo_dist = re.search(r'tiempo distribuido\(ms\):\s*([\d.]+)', bloque)
                if not match_tiempo_dist:
                    continue
                tiempo_distribuido = float(match_tiempo_dist.group(1))
                
                # Extraer puntos cubiertos por algoritmo distribuido
                match_puntos_dist = re.search(r'Puntos dentro de la circunferencia:\s*(\d+)\s*de\s*(\d+)', bloque)
                if not match_puntos_dist:
                    continue
                puntos_cubiertos_dist = int(match_puntos_dist.group(1))
                total_puntos = int(match_puntos_dist.group(2))
                
                # Extraer tiempo secuencial (si existe)
                match_tiempo_seq = re.search(r'Tiempo secuencial\(ms\):\s*([\d.]+)', bloque)
                tiempo_secuencial = float(match_tiempo_seq.group(1)) if match_tiempo_seq else None
                
                # Extraer puntos cubiertos por algoritmo secuencial (buscar la segunda ocurrencia)
                matches_puntos = re.findall(r'Puntos dentro de la circunferencia:\s*(\d+)\s*de\s*(\d+)', bloque)
                puntos_cubiertos_seq = int(matches_puntos[1][0]) if len(matches_puntos) > 1 else 0
                
                # Extraer speedup
                match_speedup = re.search(r'Speedup:\s*([\d.]+)\s*x', bloque)
                speedup = float(match_speedup.group(1)) if match_speedup else None
                
                # Extraer radios
                match_radio_dist = re.search(r'Resultado Distribuido:.*?Radio:\s*([\d.]+)', bloque, re.DOTALL)
                radio_distribuido = float(match_radio_dist.group(1)) if match_radio_dist else None
                
                match_radio_seq = re.search(r'Resultado Secuencial.*?Radio:\s*([\d.]+)', bloque, re.DOTALL)
                radio_secuencial = float(match_radio_seq.group(1)) if match_radio_seq else None
                
                datos.append({
                    'Nodos': nodos,
                    'Tiempo_Distribuido_ms': tiempo_distribuido,
                    'Tiempo_Secuencial_ms': tiempo_secuencial,
                    'Puntos_Cubiertos_Distribuido': puntos_cubiertos_dist,
                    'Puntos_Cubiertos_Secuencial': puntos_cubiertos_seq,
                    'Total_Puntos': total_puntos,
                    'Speedup': speedup,
                    'Radio_Distribuido': radio_distribuido,
                    'Radio_Secuencial': radio_secuencial
                })
                
            except Exception as e:
                print(f"Error procesando bloque: {e}")
                continue
    
    df = pd.DataFrame(datos)
    
    # Reemplazar NaN con 0 en las columnas de puntos cubiertos
    df['Puntos_Cubiertos_Distribuido'] = df['Puntos_Cubiertos_Distribuido'].fillna(0)
    df['Puntos_Cubiertos_Secuencial'] = df['Puntos_Cubiertos_Secuencial'].fillna(0)
    
    return df

def crear_graficos_completos(df):
    """Crea visualizaciones completas de los datos"""
    
    # Configurar el estilo
    plt.style.use('default')
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('Análisis de Rendimiento: Algoritmo Distribuido vs Secuencial\n400 Puntos', 
                 fontsize=16, fontweight='bold')
    
    # Filtrar datos válidos para cada gráfico
    df_valid_time = df.dropna(subset=['Tiempo_Distribuido_ms', 'Tiempo_Secuencial_ms'])
    df_valid_points = df  # Ya no filtramos por NaN porque los convertimos a 0
    df_valid_speedup = df.dropna(subset=['Speedup'])
    
    # 1. Tiempo de ejecución
    if not df_valid_time.empty:
        axes[0,0].plot(df_valid_time['Nodos'], df_valid_time['Tiempo_Distribuido_ms'], 
                      'o-', label='Distribuido', color='blue', linewidth=2, markersize=8)
        axes[0,0].plot(df_valid_time['Nodos'], df_valid_time['Tiempo_Secuencial_ms'], 
                      's-', label='Secuencial', color='red', linewidth=2, markersize=8)
        axes[0,0].set_xlabel('Número de Nodos')
        axes[0,0].set_ylabel('Tiempo (ms)')
        axes[0,0].set_title('Tiempo de Ejecución')
        axes[0,0].legend()
        axes[0,0].grid(True, alpha=0.3)
        axes[0,0].set_yscale('log')
    
    # 2. Speedup
    if not df_valid_speedup.empty:
        axes[0,1].plot(df_valid_speedup['Nodos'], df_valid_speedup['Speedup'], 
                      'o-', color='green', linewidth=2, markersize=8)
        axes[0,1].axhline(y=1, color='red', linestyle='--', alpha=0.7, label='Sin mejora')
        axes[0,1].set_xlabel('Número de Nodos')
        axes[0,1].set_ylabel('Speedup')
        axes[0,1].set_title('Speedup vs Número de Nodos')
        axes[0,1].legend()
        axes[0,1].grid(True, alpha=0.3)
    
    # 3. Puntos cubiertos
    if not df_valid_points.empty:
        axes[0,2].plot(df_valid_points['Nodos'], df_valid_points['Puntos_Cubiertos_Distribuido'], 
                      'o-', label='Distribuido', color='blue', linewidth=2, markersize=8)
        axes[0,2].plot(df_valid_points['Nodos'], df_valid_points['Puntos_Cubiertos_Secuencial'], 
                      's-', label='Secuencial', color='red', linewidth=2, markersize=8)
        axes[0,2].axhline(y=400, color='gray', linestyle='--', alpha=0.5, label='Total (400)')
        axes[0,2].set_xlabel('Número de Nodos')
        axes[0,2].set_ylabel('Puntos Cubiertos')
        axes[0,2].set_title('Puntos Cubiertos por Algoritmo')
        axes[0,2].legend()
        axes[0,2].grid(True, alpha=0.3)
        axes[0,2].set_ylim(0, 410)
    
    # 4. Eficiencia de cobertura
    if not df_valid_points.empty:
        eficiencia_dist = (df_valid_points['Puntos_Cubiertos_Distribuido'] / 400) * 100
        eficiencia_seq = (df_valid_points['Puntos_Cubiertos_Secuencial'] / 400) * 100
        
        axes[1,0].plot(df_valid_points['Nodos'], eficiencia_dist, 
                      'o-', label='Distribuido', color='blue', linewidth=2, markersize=8)
        axes[1,0].plot(df_valid_points['Nodos'], eficiencia_seq, 
                      's-', label='Secuencial', color='red', linewidth=2, markersize=8)
        axes[1,0].axhline(y=100, color='gray', linestyle='--', alpha=0.5, label='100%')
        axes[1,0].set_xlabel('Número de Nodos')
        axes[1,0].set_ylabel('Eficiencia de Cobertura (%)')
        axes[1,0].set_title('Eficiencia de Cobertura')
        axes[1,0].legend()
        axes[1,0].grid(True, alpha=0.3)
        axes[1,0].set_ylim(0, 105)
    
    # 5. Radio del círculo
    df_valid_radio = df.dropna(subset=['Radio_Distribuido', 'Radio_Secuencial'])
    if not df_valid_radio.empty:
        axes[1,1].plot(df_valid_radio['Nodos'], df_valid_radio['Radio_Distribuido'], 
                      'o-', label='Distribuido', color='blue', linewidth=2, markersize=8)
        axes[1,1].plot(df_valid_radio['Nodos'], df_valid_radio['Radio_Secuencial'], 
                      's-', label='Secuencial', color='red', linewidth=2, markersize=8)
        axes[1,1].set_xlabel('Número de Nodos')
        axes[1,1].set_ylabel('Radio del Círculo')
        axes[1,1].set_title('Radio del Círculo Mínimo')
        axes[1,1].legend()
        axes[1,1].grid(True, alpha=0.3)
    
    # 6. Tiempo vs Puntos cubiertos (scatter)
    # Usar todos los datos ya que los NaN se convirtieron a 0
    df_scatter = df.dropna(subset=['Tiempo_Distribuido_ms'])
    df_scatter_seq = df.dropna(subset=['Tiempo_Secuencial_ms'])
    
    if not df_scatter.empty:
        scatter = axes[1,2].scatter(df_scatter['Tiempo_Distribuido_ms'], df_scatter['Puntos_Cubiertos_Distribuido'], 
                                   c=df_scatter['Nodos'], cmap='viridis', s=100, alpha=0.7, label='Distribuido')
        
        if not df_scatter_seq.empty:
            axes[1,2].scatter(df_scatter_seq['Tiempo_Secuencial_ms'], df_scatter_seq['Puntos_Cubiertos_Secuencial'], 
                             c=df_scatter_seq['Nodos'], cmap='plasma', s=100, alpha=0.7, marker='s', label='Secuencial')
        
        axes[1,2].set_xlabel('Tiempo de Ejecución (ms)')
        axes[1,2].set_ylabel('Puntos Cubiertos')
        axes[1,2].set_title('Tiempo vs Puntos Cubiertos')
        axes[1,2].legend()
        axes[1,2].grid(True, alpha=0.3)
        
        # Añadir colorbar
        cbar = plt.colorbar(scatter, ax=axes[1,2])
        cbar.set_label('Número de Nodos')
    
    plt.tight_layout()
    plt.savefig('analisis_resultados_400pt.png', dpi=300, bbox_inches='tight')
    plt.show()

def mostrar_tabla_resumen(df):
    """Muestra una tabla resumen de los resultados"""
    print("\n" + "="*80)
    print("TABLA RESUMEN DE RESULTADOS")
    print("="*80)
    
    # Formatear la tabla
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    
    # Crear tabla resumida
    tabla = df[['Nodos', 'Tiempo_Distribuido_ms', 'Tiempo_Secuencial_ms', 
                'Puntos_Cubiertos_Distribuido', 'Puntos_Cubiertos_Secuencial', 'Speedup']].copy()
    
    # Redondear valores (manteniendo NaN)
    tabla['Tiempo_Distribuido_ms'] = tabla['Tiempo_Distribuido_ms'].round(2)
    tabla['Tiempo_Secuencial_ms'] = tabla['Tiempo_Secuencial_ms'].round(2)
    tabla['Speedup'] = tabla['Speedup'].round(3)
    
    print(tabla.to_string(index=False))
    
    # Estadísticas adicionales
    print("\n" + "="*80)
    print("ESTADÍSTICAS GENERALES")
    print("="*80)
    
    # Mejor speedup (solo datos válidos)
    speedup_validos = df.dropna(subset=['Speedup'])
    if not speedup_validos.empty:
        mejor_speedup = speedup_validos.loc[speedup_validos['Speedup'].idxmax()]
        print(f"Mejor Speedup: {mejor_speedup['Speedup']:.3f}x con {mejor_speedup['Nodos']} nodos")
    
    # Mejor tiempo distribuido
    mejor_tiempo = df.loc[df['Tiempo_Distribuido_ms'].idxmin()]
    print(f"Mejor Tiempo Distribuido: {mejor_tiempo['Tiempo_Distribuido_ms']:.2f}ms con {mejor_tiempo['Nodos']} nodos")
    
    # Mejor cobertura distribuida
    if not df['Puntos_Cubiertos_Distribuido'].isna().all():
        mejor_cobertura = df.loc[df['Puntos_Cubiertos_Distribuido'].idxmax()]
        print(f"Mejor Cobertura Distribuida: {mejor_cobertura['Puntos_Cubiertos_Distribuido']}/400 puntos con {mejor_cobertura['Nodos']} nodos")
    
    # Estadísticas de cobertura
    cobertura_promedio_dist = (df['Puntos_Cubiertos_Distribuido'].mean() / 400) * 100
    print(f"Cobertura Promedio Distribuida: {cobertura_promedio_dist:.1f}%")
    
    cobertura_secuencial = df.dropna(subset=['Puntos_Cubiertos_Secuencial'])
    if not cobertura_secuencial.empty:
        cobertura_promedio_seq = (cobertura_secuencial['Puntos_Cubiertos_Secuencial'].mean() / 400) * 100
        print(f"Cobertura Promedio Secuencial: {cobertura_promedio_seq:.1f}%")

def analizar_tendencias(df):
    """Analiza las tendencias en los datos"""
    print("\n" + "="*80)
    print("ANÁLISIS DE TENDENCIAS")
    print("="*80)
    
    # Tendencia del tiempo distribuido
    if len(df) > 1:
        correlacion_tiempo_nodos = df['Nodos'].corr(df['Tiempo_Distribuido_ms'])
        print(f"Correlación Nodos vs Tiempo Distribuido: {correlacion_tiempo_nodos:.3f}")
        
        # Eficiencia promedio
        if not df['Puntos_Cubiertos_Distribuido'].isna().all():
            eficiencia_promedio_dist = (df['Puntos_Cubiertos_Distribuido'].mean() / 400) * 100
            print(f"Eficiencia Promedio Distribuido: {eficiencia_promedio_dist:.1f}%")
        
        if not df['Puntos_Cubiertos_Secuencial'].isna().all():
            eficiencia_promedio_seq = (df['Puntos_Cubiertos_Secuencial'].mean() / 400) * 100
            print(f"Eficiencia Promedio Secuencial: {eficiencia_promedio_seq:.1f}%")

if __name__ == "__main__":
    # Parsear los datos
    archivo = "resamano2.txt"
    
    try:
        df = parsear_resultados_resamano2(archivo)
        
        if df.empty:
            print("No se pudieron extraer datos del archivo.")
        else:
            print(f"Datos extraídos exitosamente. {len(df)} registros procesados.")
            
            # Mostrar los datos extraídos
            print("\nDatos extraídos:")
            print(df)
            
            # Crear visualizaciones
            crear_graficos_completos(df)
            
            # Mostrar tabla resumen
            mostrar_tabla_resumen(df)
            
            # Analizar tendencias
            analizar_tendencias(df)
            
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo}'")
    except Exception as e:
        print(f"Error inesperado: {e}")
