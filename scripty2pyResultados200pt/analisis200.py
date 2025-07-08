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
            
            # Extraer puntos dentro del círculo distribuido y secuencial
            matches_puntos = re.findall(r'Puntos dentro de la circunferencia: (\d+) de (\d+)', bloque)
            
            puntos_dentro_dist = None
            puntos_dentro_seq = None
            total_puntos = None
            
            if len(matches_puntos) >= 1:
                puntos_dentro_dist = int(matches_puntos[0][0])
                total_puntos = int(matches_puntos[0][1])
            
            if len(matches_puntos) >= 2:
                puntos_dentro_seq = int(matches_puntos[1][0])
            
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
    """Crea visualizaciones completas de los datos"""
    
    # Configurar el estilo
    plt.style.use('default')
    fig, axes = plt.subplots(3, 3, figsize=(20, 15))
    fig.suptitle('Análisis de Rendimiento: Algoritmo Distribuido vs Secuencial\n200 Puntos', fontsize=18, fontweight='bold')
    
    # 1. Tiempo de ejecución (escala logarítmica)
    axes[0,0].plot(df['Nodos'], df['Tiempo_Distribuido_ms'], 'o-', label='Distribuido', color='blue', linewidth=2, markersize=8)
    axes[0,0].plot(df['Nodos'], df['Tiempo_Secuencial_ms'], 's-', label='Secuencial', color='red', linewidth=2, markersize=8)
    axes[0,0].set_xlabel('Número de Nodos')
    axes[0,0].set_ylabel('Tiempo (ms)')
    axes[0,0].set_title('Tiempo de Ejecución')
    axes[0,0].legend()
    axes[0,0].grid(True, alpha=0.3)
    axes[0,0].set_yscale('log')
    
    # 2. Speedup
    axes[0,1].plot(df['Nodos'], df['Speedup'], 'o-', color='green', linewidth=3, markersize=8)
    axes[0,1].axhline(y=1, color='red', linestyle='--', alpha=0.7, label='Sin mejora')
    # Línea de speedup ideal (lineal)
    ideal_speedup = df['Nodos']
    axes[0,1].plot(df['Nodos'], ideal_speedup, '--', color='orange', alpha=0.7, label='Speedup Ideal')
    axes[0,1].set_xlabel('Número de Nodos')
    axes[0,1].set_ylabel('Speedup')
    axes[0,1].set_title('Speedup vs Número de Nodos')
    axes[0,1].legend()
    axes[0,1].grid(True, alpha=0.3)
    
    # 3. Radio del círculo (escala logarítmica)
    axes[0,2].plot(df['Nodos'], df['Radio_Distribuido'], 'o-', label='Distribuido', color='blue', linewidth=2, markersize=8)
    axes[0,2].plot(df['Nodos'], df['Radio_Secuencial'], 's-', label='Secuencial', color='red', linewidth=2, markersize=8)
    axes[0,2].set_xlabel('Número de Nodos')
    axes[0,2].set_ylabel('Radio')
    axes[0,2].set_title('Radio del Círculo Mínimo (Escala Log)')
    axes[0,2].legend()
    axes[0,2].grid(True, alpha=0.3)
    axes[0,2].set_yscale('log')
    
    # 4. Cantidad de puntos contenidos (valores absolutos)
    axes[1,0].plot(df['Nodos'], df['Puntos_Dentro_Distribuido'], 'o-', label='Distribuido', color='blue', linewidth=2, markersize=8)
    axes[1,0].plot(df['Nodos'], df['Puntos_Dentro_Secuencial'], 's-', label='Secuencial', color='red', linewidth=2, markersize=8)
    axes[1,0].axhline(y=200, color='gray', linestyle='--', alpha=0.5, label='Total (200)')
    axes[1,0].set_xlabel('Número de Nodos')
    axes[1,0].set_ylabel('Puntos Contenidos')
    axes[1,0].set_title('Cantidad de Puntos Contenidos')
    axes[1,0].legend()
    axes[1,0].grid(True, alpha=0.3)
    axes[1,0].set_ylim(0, 210)
    
    # 5. Comparación de tiempos (barras)
    x = np.arange(len(df['Nodos']))
    width = 0.35
    axes[1,1].bar(x - width/2, df['Tiempo_Distribuido_ms'], width, label='Distribuido', color='blue', alpha=0.7)
    axes[1,1].bar(x + width/2, df['Tiempo_Secuencial_ms'], width, label='Secuencial', color='red', alpha=0.7)
    axes[1,1].set_xlabel('Número de Nodos')
    axes[1,1].set_ylabel('Tiempo (ms)')
    axes[1,1].set_title('Comparación de Tiempos (Escala Log)')
    axes[1,1].set_xticks(x)
    axes[1,1].set_xticklabels(df['Nodos'])
    axes[1,1].legend()
    axes[1,1].set_yscale('log')
    
    # 6. Escalabilidad (tiempo distribuido vs ideal)
    tiempo_ideal = df['Tiempo_Distribuido_ms'].iloc[0] / df['Nodos']
    axes[1,2].plot(df['Nodos'], df['Tiempo_Distribuido_ms'], 'o-', label='Real', color='blue', linewidth=2, markersize=8)
    axes[1,2].plot(df['Nodos'], tiempo_ideal, '--', label='Ideal', color='orange', linewidth=2)
    axes[1,2].set_xlabel('Número de Nodos')
    axes[1,2].set_ylabel('Tiempo Distribuido (ms)')
    axes[1,2].set_title('Escalabilidad del Algoritmo Distribuido')
    axes[1,2].legend()
    axes[1,2].grid(True, alpha=0.3)
    axes[1,2].set_yscale('log')
    
    # 7. Eficiencia paralela
    eficiencia_paralela = (df['Tiempo_Distribuido_ms'].iloc[0] / df['Nodos']) / df['Tiempo_Distribuido_ms'] * 100
    axes[2,0].plot(df['Nodos'], eficiencia_paralela, 'o-', color='purple', linewidth=2, markersize=8)
    axes[2,0].axhline(y=100, color='red', linestyle='--', alpha=0.7, label='Eficiencia Ideal')
    axes[2,0].set_xlabel('Número de Nodos')
    axes[2,0].set_ylabel('Eficiencia Paralela (%)')
    axes[2,0].set_title('Eficiencia Paralela')
    axes[2,0].legend()
    axes[2,0].grid(True, alpha=0.3)
    axes[2,0].set_ylim(0, 110)
    
    # 8. Número absoluto de puntos cubiertos
    axes[2,1].bar(x - width/2, df['Puntos_Dentro_Distribuido'], width, label='Distribuido', color='blue', alpha=0.7)
    axes[2,1].bar(x + width/2, df['Puntos_Dentro_Secuencial'], width, label='Secuencial', color='red', alpha=0.7)
    axes[2,1].set_xlabel('Número de Nodos')
    axes[2,1].set_ylabel('Puntos Cubiertos')
    axes[2,1].set_title('Número de Puntos Cubiertos')
    axes[2,1].set_xticks(x)
    axes[2,1].set_xticklabels(df['Nodos'])
    axes[2,1].legend()
    axes[2,1].grid(True, alpha=0.3)
    
    # 9. Ratio de mejora en tiempo
    ratio_mejora = df['Tiempo_Secuencial_ms'] / df['Tiempo_Distribuido_ms']
    axes[2,2].plot(df['Nodos'], ratio_mejora, 'o-', color='darkgreen', linewidth=2, markersize=8)
    axes[2,2].set_xlabel('Número de Nodos')
    axes[2,2].set_ylabel('Ratio de Mejora')
    axes[2,2].set_title('Ratio de Mejora en Tiempo\n(Tiempo_Secuencial / Tiempo_Distribuido)')
    axes[2,2].grid(True, alpha=0.3)
    axes[2,2].set_yscale('log')
    
    plt.tight_layout()
    plt.savefig('analisis_rendimiento_200.png', dpi=300, bbox_inches='tight')
    plt.show()

def mostrar_tabla_resumen(df):
    """Muestra una tabla resumen de los resultados"""
    print("\n" + "="*120)
    print("TABLA RESUMEN: ANÁLISIS DE RENDIMIENTO - 200 PUNTOS")
    print("="*120)
    
    # Seleccionar las columnas más importantes para mostrar
    columnas_mostrar = [
        'Nodos', 
        'Tiempo_Distribuido_ms', 
        'Tiempo_Secuencial_ms', 
        'Speedup',
        'Eficiencia_Distribuido',
        'Eficiencia_Secuencial',
        'Radio_Distribuido',
        'Radio_Secuencial'
    ]
    
    df_mostrar = df[columnas_mostrar].copy()
    df_mostrar['Tiempo_Distribuido_ms'] = df_mostrar['Tiempo_Distribuido_ms'].round(2)
    df_mostrar['Tiempo_Secuencial_ms'] = df_mostrar['Tiempo_Secuencial_ms'].round(2)
    df_mostrar['Speedup'] = df_mostrar['Speedup'].round(2)
    df_mostrar['Eficiencia_Distribuido'] = df_mostrar['Eficiencia_Distribuido'].round(1)
    df_mostrar['Eficiencia_Secuencial'] = df_mostrar['Eficiencia_Secuencial'].round(1)
    df_mostrar['Radio_Distribuido'] = df_mostrar['Radio_Distribuido'].round(2)
    df_mostrar['Radio_Secuencial'] = df_mostrar['Radio_Secuencial'].round(2)
    
    print(df_mostrar.to_string(index=False))
    
    print("\n" + "="*120)
    print("ESTADÍSTICAS GENERALES")
    print("="*120)
    print(f"Mejor Speedup: {df['Speedup'].max():.2f}x con {df.loc[df['Speedup'].idxmax(), 'Nodos']} nodos")
    print(f"Menor tiempo distribuido: {df['Tiempo_Distribuido_ms'].min():.2f}ms con {df.loc[df['Tiempo_Distribuido_ms'].idxmin(), 'Nodos']} nodos")
    print(f"Mayor eficiencia distribuida: {df['Eficiencia_Distribuido'].max():.1f}% con {df.loc[df['Eficiencia_Distribuido'].idxmax(), 'Nodos']} nodos")
    print(f"Mayor eficiencia secuencial: {df['Eficiencia_Secuencial'].max():.1f}% con {df.loc[df['Eficiencia_Secuencial'].idxmax(), 'Nodos']} nodos")
    
    # Estadísticas adicionales
    eficiencia_paralela = (df['Tiempo_Distribuido_ms'].iloc[0] / df['Nodos']) / df['Tiempo_Distribuido_ms'] * 100
    print(f"Mejor eficiencia paralela: {eficiencia_paralela.max():.1f}% con {df.loc[eficiencia_paralela.idxmax(), 'Nodos']} nodos")
    
    # Análisis de consistencia
    casos_100_pct_dist = df[df['Eficiencia_Distribuido'] == 100.0]['Nodos'].tolist()
    casos_100_pct_seq = df[df['Eficiencia_Secuencial'] == 100.0]['Nodos'].tolist()
    
    print(f"\nCasos donde el método distribuido cubre 100% de puntos: {casos_100_pct_dist}")
    print(f"Casos donde el método secuencial cubre 100% de puntos: {casos_100_pct_seq}")
    
    # Análisis de estabilidad del radio
    radio_dist_cv = (df['Radio_Distribuido'].std() / df['Radio_Distribuido'].mean()) * 100
    radio_seq_cv = (df['Radio_Secuencial'].std() / df['Radio_Secuencial'].mean()) * 100
    
    print(f"\nVariabilidad del radio distribuido (CV): {radio_dist_cv:.1f}%")
    print(f"Variabilidad del radio secuencial (CV): {radio_seq_cv:.1f}%")
    
    # Análisis de correlación
    if len(df) > 1:
        correlacion_tiempo_nodos = df['Nodos'].corr(df['Tiempo_Distribuido_ms'])
        print(f"\nCorrelación Nodos vs Tiempo Distribuido: {correlacion_tiempo_nodos:.3f}")

def analisis_detallado(df):
    """Realiza un análisis más detallado de los resultados"""
    print("\n" + "="*120)
    print("ANÁLISIS DETALLADO")
    print("="*120)
    
    # 1. Análisis de escalabilidad
    print("\n1. ESCALABILIDAD:")
    for i in range(1, len(df)):
        speedup_teorico = df.iloc[i]['Nodos']
        speedup_real = df.iloc[i]['Speedup']
        eficiencia = (speedup_real / speedup_teorico) * 100
        print(f"   {df.iloc[i]['Nodos']} nodos: Speedup teórico={speedup_teorico:.1f}x, Real={speedup_real:.2f}x, Eficiencia={eficiencia:.1f}%")
    
    # 2. Análisis de calidad de solución
    print("\n2. CALIDAD DE SOLUCIÓN:")
    for i in range(len(df)):
        nodos = df.iloc[i]['Nodos']
        eff_dist = df.iloc[i]['Eficiencia_Distribuido']
        eff_seq = df.iloc[i]['Eficiencia_Secuencial']
        radio_dist = df.iloc[i]['Radio_Distribuido']
        radio_seq = df.iloc[i]['Radio_Secuencial']
        
        calidad = "BUENA" if eff_dist >= 95 else "REGULAR" if eff_dist >= 80 else "MALA"
        
        print(f"   {nodos} nodos: Eficiencia Dist={eff_dist:.1f}%, Seq={eff_seq:.1f}%, "
              f"Radio Dist={radio_dist:.1f}, Seq={radio_seq:.1f} - {calidad}")
    
    # 3. Recomendaciones
    print("\n3. RECOMENDACIONES:")
    
    # Mejor configuración por criterio
    mejor_speedup_idx = df['Speedup'].idxmax()
    mejor_eficiencia_idx = df['Eficiencia_Distribuido'].idxmax()
    menor_tiempo_idx = df['Tiempo_Distribuido_ms'].idxmin()
    
    print(f"   • Para máximo speedup: {df.iloc[mejor_speedup_idx]['Nodos']} nodos "
          f"(Speedup: {df.iloc[mejor_speedup_idx]['Speedup']:.2f}x)")
    print(f"   • Para máxima cobertura: {df.iloc[mejor_eficiencia_idx]['Nodos']} nodos "
          f"(Cobertura: {df.iloc[mejor_eficiencia_idx]['Eficiencia_Distribuido']:.1f}%)")
    print(f"   • Para mínimo tiempo: {df.iloc[menor_tiempo_idx]['Nodos']} nodos "
          f"(Tiempo: {df.iloc[menor_tiempo_idx]['Tiempo_Distribuido_ms']:.2f}ms)")
    
    # Equilibrio entre speedup y calidad
    df['Score'] = df['Speedup'] * (df['Eficiencia_Distribuido']/100)
    mejor_balance_idx = df['Score'].idxmax()
    print(f"   • Para mejor balance speedup/calidad: {df.iloc[mejor_balance_idx]['Nodos']} nodos "
          f"(Score: {df.iloc[mejor_balance_idx]['Score']:.2f})")

if __name__ == "__main__":
    # Cargar y procesar los datos
    print("Cargando datos del archivo puntos200Resultados.txt...")
    df = extraer_datos_resultados('puntos200Resultados.txt')
    
    if df.empty:
        print("Error: No se pudieron extraer datos del archivo.")
        exit(1)
    
    # Mostrar tabla resumen
    mostrar_tabla_resumen(df)
    
    # Análisis detallado
    analisis_detallado(df)
    
    # Crear visualizaciones
    print("\nGenerando visualizaciones...")
    crear_visualizaciones(df)
    
    # Guardar DataFrame en CSV para futuros análisis
    df.to_csv('analisis_200_puntos.csv', index=False)
    print("\nDatos guardados en 'analisis_200_puntos.csv'")
    print("Gráficos guardados en 'analisis_rendimiento_200.png'")
    
    print("\n" + "="*120)
    print("ANÁLISIS COMPLETADO")
    print("="*120)
