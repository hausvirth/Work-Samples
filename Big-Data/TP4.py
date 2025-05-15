
#______________________________________________________________________________#
#            Universidad de San Andrés: Maestría en Economía                   #
#            Machine Learning para Economistas                                 #
#            TP4: Clasificación y regularización de desocupación usando la EPH #
#            Gaspar Hayduk, Carolina de Boeck, Martina Hausvirth               #
#______________________________________________________________________________#




#--------------------PARTE I: Análisis de la base de hogares y tipo de ocupación--------------------


#---------------------------EJERCICIO 2---------------------------


# Limpiamos memoria: 
globals().clear() 

# Importamos librerias:
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns 
import matplotlib.pyplot as plt
# Para comenzar, definimos la carpeta
carpeta = "/Users/gasparhayduk/Desktop/TP4"
os.chdir(carpeta) 


# Definimos los nombres de los archivos
individual_dta = "Individual_T104.dta"
hogar_dta = "Hogar_t104.dta"
individual_xls = "usu_individual_T124.xlsx"
hogar_xls = "usu_hogar_T124.xlsx"



# Cargamos las bases del 2004:
hogar_2004 = pd.read_stata(os.path.join(carpeta,hogar_dta))
individual_2004 = pd.read_stata(os.path.join(carpeta, individual_dta))

# Cargamos las bases del 2024:
hogar_2024 = pd.read_excel(os.path.join(carpeta,hogar_xls))
individual_2024 = pd.read_excel(os.path.join(carpeta, individual_xls)) 



# Nos quedamos con las observaciones correspondientes a Tucuman:
hogar_2004 = hogar_2004[hogar_2004['aglomerado']=="Gran Tucumán - Tafí Viejo"] 
individual_2004 = individual_2004[individual_2004['aglomerado']=="Gran Tucumán - Tafí Viejo"] 
hogar_2024 = hogar_2024[hogar_2024['AGLOMERADO']==29] 
individual_2024 = individual_2024[individual_2024['AGLOMERADO']==29]  



#-- Primero definimos las variables de cada dataframe con las que nos vamos a quedar:
variables_hogar_04 = ['CODUSU', 'nro_hogar', 'pondera', 'iv3', 'iv1', 'iv6', 'iv7', 'iv8', 'iv9', 'iv12_1','iv12_3', 'v1', 'v2', 'v3', 'v4',
                    'v5', 'v6', 'v8', 'v9', 'v10', 'v13', 'v14', 'v19_a', 'v19_b', 'IX_Tot', 'IX_Men10',
                    'IX_Mayeq10', 'ipcf'] 

variables_hogar_24 =  ['CODUSU', 'NRO_HOGAR', 'PONDERA', 'IV1', 'IV3', 'IV6', 'IV7', 'IV8', 'IV9', 'IV12_1', 'IV12_3',
                       'V1','V2', 'V3', 'V4', 'V5', 'V6', 'V8', 'V9', 'V10', 'V13', 'V14', 'V19_A', 'V19_B', 'IX_TOT', 'IX_MEN10',
                       'IX_MAYEQ10', 'IPCF'] 
    
    
variables_indiv_04 = ['CODUSU', 'nro_hogar', 'pondera', 'ch03', 'ch04', 'ch06', 'ch07', 'ch08', 'nivel_ed', 'estado', 'cat_inac']

variables_indiv_24 = ['CODUSU', 'NRO_HOGAR', 'PONDERA', 'CH03', 'CH04', 'CH06', 'CH07', 'CH08', 'NIVEL_ED', 'ESTADO', 'CAT_INAC'] 

#-- Nos quedamos con las columnas de interes:
hogar_2004 = hogar_2004[variables_hogar_04] 
hogar_2024 = hogar_2024[variables_hogar_24] 
individual_2024 = individual_2024[variables_indiv_24] 
individual_2004 = individual_2004[variables_indiv_04]


# Mergeamos la base a nivel hogares e individual para cada año:
data_04 = pd.merge(individual_2004, hogar_2004, on=['CODUSU', 'nro_hogar'], how='inner') 
  
data_24 = pd.merge(individual_2024, hogar_2024, on=['CODUSU', 'NRO_HOGAR'], how='inner')  

#---Borramos cada base por separado para no ocupar tanta memoria:
bases_borrar = ['hogar_2004', 'individual_2004', 'hogar_2024', 'individual_2024'] 

for var in bases_borrar:
    if var in globals():  # Verificar si la variable existe en el entorno global
        del globals()[var] 
        
        
        
    
 


#---------------------------EJERCICIO 3---------------------------

# Algunas variables categoricas de data_04 estan en string, hay que pasarlas a numericas. 

mapeos = {'iv1' : {'Casa':1, 'Departamento':2, 'Pieza de inquilinato':3, 'Pieza en hotel /pensión':4, 'Local no construido para habitación':5, ' Otro':6},
    'iv3' : {'Mosaico/baldosa/madera/cerámica/alfombra':1, 'Cemento/ladrillo fijo':2, 'Ladrillo suelto/tierra':3, 'Otro':4 }, 
    'iv6' : {'Por cañería dentro de la vivienda':1, 'Fuera de la vivienda pero dentro del terreno':2, 'Fuera del terreno':3},
    'iv7' : {'Red pública (agua corriente)':1, ' Perforación con bomba a motor':2, 'Perforación con bomba manual':3, 'Otra fuente':4},
    'iv8' : {'Sí':1, 'No':0},
    'iv9' : {'Dentro de la vivienda':1, 'Fuera de la vivienda pero dentro del terreno':2, 'Fuera del terreno':3},
    'iv12_1' : {'Sí': 1, 'No':0},
    'iv12_3': {'Sí':1, 'No':0}, 
    'v1' : {'Sí':1, 'No':0},
    'v2' : {'Sí':1, 'No':0},
    'v3' : {'Sí':1, 'No':0},
    'v4' : {'Sí':1, 'No':0},
    'v5' : {'Sí':1, 'No':0},
    'v6' : {'Sí':1, 'No':0},
    'v8' : {'Sí':1, 'No':0},
    'v9' : {'Sí':1, 'No':0},
    'v10' : {'Sí':1, 'No':0},
    'v13' : {'Sí':1, 'No':0}, 
    'v14' : {'Sí':1, 'No':0}, 
    'v19_a' : {'Sí':1, 'No':0}, 
    'v19_b' : {'Sí':1, 'No':0},
    'ch03': {'Jefe': 1, 'Cónyuge/Pareja': 0, 'Hijo/Hijastro': 0, 'Yerno/Nuera':0, 'Nieto':0, 'Madre/Padre' :0,  'Suegro':0, 'Hermano':0, 'Otros familiares':0, 'No familiares':0 },
    'ch04': {'Varón': 1, 'Mujer': 0},
    'ch06': {'Menos de 1 año': 0, '98 y más años': 99},
    'ch07': {'Unido': 1, 'Casado': 2, 'Separado o divorciado': 3, 'Viudo': 4, 'Soltero': 5, 'Ns./Nr.': 9},
    'ch08': {'Obra social (incluye PAMI)': 1, 'Mutual/Prepaga/Servicio de emergencia': 2, 'Planes y seguros públicos': 3, 'No paga ni le descuentan': 4, 'Ns./Nr.': 9, 'Obra social y mutual/prepaga/servicio de emergencia': 1, 'Obra social y planes y seguros públicos': 1, 'Obra social, mutual/prepaga/servicio de emergencia y planes': 1, 'Mutual/prepaga/servicio de emergencia/planes y seguros públi': 2},
    'nivel_ed': {'Primaria Incompleta (incluye educación especial)': 1, 'Primaria Completa': 2, 'Secundaria Incompleta': 3, 'Secundaria Completa': 4, 'Superior Universitaria Incompleta': 5, 'Superior Universitaria Completa': 6, 'Sin instrucción': 7, 'Ns./Nr.': 9},
    'estado': {'Entrevista individual no realizada (no respuesta al cuestion': 0, 'Ocupado': 1, 'Desocupado': 2, 'Inactivo': 3, 'Menor de 10 años': 4},
    'cat_inac': {'Jubilado/pensionado':1 ,'Rentista':2, 'Estudiante':3,'Ama de casa':4,  'Menor de 6 años':5, 'Discapacitado':6, 'Otros':7},

}

# 'ch03' vale 1 si el individuo es jefe de hogar y 0 si no. Esto lo creamos nosotros


# Aplicar mapeos condicionalmente con .apply
for col, mapeo in mapeos.items():
    data_04[col] = data_04[col].apply(lambda x: mapeo.get(x, x))  # Si no encuentra el valor, deja el original
    
# La variable 'IX_Men10' toma el valor de 'nan' cuando es cero. Hay que reemplazar eso:
data_04['IX_Men10'] = data_04['IX_Men10'].fillna(0) 

# Para data_24 en algunas variables hay 1 y 2 cuando quisieramos que haya 1 y 0s. Cambiamos eso:
data_24['CH04'] = data_24['CH04'].replace(2, 0) 
data_24['V1'] = data_24['V1'].replace(2, 0) 
data_24['V2'] = data_24['V2'].replace(2, 0)
data_24['V3'] = data_24['V3'].replace(2, 0)
data_24['V4'] = data_24['V4'].replace(2, 0)
data_24['V5'] = data_24['V5'].replace(2, 0)
data_24['V6'] = data_24['V6'].replace(2, 0)
data_24['V8'] = data_24['V8'].replace(2, 0)
data_24['V9'] = data_24['V9'].replace(2, 0)
data_24['V10'] = data_24['V10'].replace(2, 0)
data_24['V13'] = data_24['V13'].replace(2, 0)
data_24['V14'] = data_24['V14'].replace(2, 0)
data_24['V19_A'] = data_24['V19_A'].replace(2, 0)
data_24['V19_B'] = data_24['V19_B'].replace(2, 0) 
data_24['IV12_1'] = data_24['IV12_1'].replace(2,0) 
data_24['IV12_3'] = data_24['IV12_3'].replace(2,0) 

#Jefe de hogar. Lo creamos nosotros
data_24['CH03'] = data_24['CH03'].apply(lambda x: 1 if x == 1 else 0)


# Eliminamos valores negativos en la edad y en el ipcf:
data_04['ch06'] = pd.to_numeric(data_04['ch06'], errors='coerce')
data_04 = data_04.drop(data_04[data_04['ch06']<0].index)

data_24['CH06'] = pd.to_numeric(data_24['CH06'], errors='coerce')
data_24 = data_24.drop(data_24[data_24['CH06']<0].index)


data_24 = data_24.drop(data_24[data_24['IPCF']<0].index)
data_04 = data_04.drop(data_04[data_04['ipcf']<0].index) 


#---- Nos quedamos con los individuos que respondieron su estado de actividad. 
data_04 = data_04[data_04['estado']!= 0] 
data_24 = data_24[data_24['ESTADO']!= 0] 


#---- Debemos hacer One-Hot-Encoding en las variables donde cada valor representa una categoria. 

#las variables son: CH07, CH08, CH09, CH10, NIVEL_ED, CAT_INAC,  IV1, IV3, IV6, IV7, IV8, IV9 

#------ (I) 2024:
data_24 = pd.get_dummies(data_24, columns=['CH07'], prefix='civ') 
data_24 = pd.get_dummies(data_24, columns=['CH08'], prefix='cob')
data_24 = pd.get_dummies(data_24, columns=['NIVEL_ED'], prefix='nivel_ed')
data_24 = pd.get_dummies(data_24,columns=['CAT_INAC'], prefix='incap') 
data_24 = pd.get_dummies(data_24,columns=['IV1'], prefix='vivienda')
data_24 = pd.get_dummies(data_24,columns=['IV3'], prefix='piso')
data_24 = pd.get_dummies(data_24,columns=['IV6'], prefix='agua')
data_24 = pd.get_dummies(data_24,columns=['IV7'], prefix='redagua')
data_24 = pd.get_dummies(data_24,columns=['IV9'], prefix='baño') 


#------ (II) 2004:
data_04 = pd.get_dummies(data_04, columns=['ch07'], prefix='civ') 
data_04 = pd.get_dummies(data_04, columns=['ch08'], prefix='cob')
data_04 = pd.get_dummies(data_04, columns=['nivel_ed'], prefix='nivel_ed')
data_04 = pd.get_dummies(data_04,columns=['cat_inac'], prefix='incap') 
data_04 = pd.get_dummies(data_04,columns=['iv1'], prefix='vivienda')
data_04 = pd.get_dummies(data_04,columns=['iv3'], prefix='piso')
data_04 = pd.get_dummies(data_04,columns=['iv6'], prefix='agua')
data_04 = pd.get_dummies(data_04,columns=['iv7'], prefix='redagua')
data_04 = pd.get_dummies(data_04,columns=['iv9'], prefix='baño') 






#---------------------------EJERCICIO 4---------------------------

#---- (I) proporción de personas que trabajan en el hogar: hogares con una alta proporción de ocupados podrían estar en mejor posición económica, reduciendo la probabilidad de desocupación individual.

data_24['prop_ocupados_hogar'] = data_24.groupby(['CODUSU', 'NRO_HOGAR'])['ESTADO'].transform(lambda x: (x == 1).mean())
data_04['prop_ocupados_hogar'] = data_04.groupby(['CODUSU', 'nro_hogar'])['estado'].transform(lambda x: (x == 1).mean())



#---- (II) Jefe de hogar ocupado: si el jefe de hogar está ocupado puede ser un factor protector contra la desocupación:

#-- 2024
# Creo una variable que vale 1 si el jefe de hogar esta ocupado: esta hay que dropearla despues
data_24['jefe_ocupado'] = ((data_24['CH03'] == 1) & (data_24['ESTADO'] == 1)).astype(int)

# Agrupo por hogar:
data_24['hogar_jefe_ocupado'] = data_24.groupby(['CODUSU', 'NRO_HOGAR'])['jefe_ocupado'].transform('max')

#-- 2004
# Creo una variable que vale 1 si el jefe de hogar esta ocupado: esta hay que dropearla despues
data_04['jefe_ocupado'] = ((data_04['ch03'] == 1) & (data_04['estado'] == 1)).astype(int)

# Agrupo por hogar:
data_04['hogar_jefe_ocupado'] = data_04.groupby(['CODUSU', 'nro_hogar'])['jefe_ocupado'].transform('max')



#---- (III) Jefe de Hogar con nivel universitario completo: esto puede servir como un actor protector contra la desocupación para los otros miembros del hogar

# 2024
data_24['jefe_univ'] = data_24.groupby(['CODUSU', 'NRO_HOGAR'])['nivel_ed_6'].transform(
    lambda x: ((data_24['CH03'] == 1) & (x == 1)).max().astype(int))

# 2004:
data_04['jefe_univ'] = data_04.groupby(['CODUSU', 'nro_hogar'])['nivel_ed_6'].transform(
        lambda x: ((data_04['ch03'] == 1) & (x == 1)).max().astype(int))



#---------------------------EJERCICIO 5---------------------------
data_24['desocupado'] = (data_24['ESTADO'] == 2)
data_04['desocupado'] = (data_04['estado'] == 2)


#----- (I) Boxplot de cantidad de miembros del hogar segun desocupados y no desocupados:
    # Boxplot para Cantidad de Miembros del Hogar según Desocupación en 2004
plt.figure(figsize=(10, 6))
data_04.boxplot(column='IX_Men10', by='desocupado', grid=False)
plt.title('Boxplot de Cantidad de Menores en el Hogar por Desocupación (2004)')
plt.suptitle('')  # Elimina el título por defecto de pandas
plt.xlabel('Desocupado')
plt.ylabel('Cantidad de Menores en el Hogar')
plt.xticks([1, 2], ['No', 'Sí'])
plt.savefig("boxplot_menores10_2004.png", format="png", dpi=300)
plt.show()

# Boxplot para Cantidad de Miembros del Hogar según Desocupación en 2024
plt.figure(figsize=(10, 6))
data_24.boxplot(column='IX_MEN10', by='desocupado', grid=False)
plt.title('Boxplot de Cantidad de Menores en el Hogar por Desocupación (2024)')
plt.suptitle('')  # Elimina el título por defecto de pandas
plt.xlabel('Desocupado')
plt.ylabel('Cantidad de Menores en el Hogar')
plt.xticks([1, 2], ['No', 'Sí'])
plt.savefig("boxplot_menores10_2024.png", format="png", dpi=300)
plt.show()




#----- (II) Tasa de Desocupados segun sexo:
# Crear tabla de tasas de desocupación según sexo para 2004
tasa_desocupacion_04 = data_04.groupby('ch04')['desocupado'].mean() * 100

# Crear tabla de tasas de desocupación según sexo para 2024
tasa_desocupacion_24 = data_24.groupby('CH04')['desocupado'].mean() * 100

# Mostrar resultados
print("Tasa de desocupación según sexo - 2004:")
print(tasa_desocupacion_04)

print("Tasa de desocupación según sexo - 2024:")
print(tasa_desocupacion_24)

# Graficar tasas de desocupación para 2004
plt.figure(figsize=(8, 6))
tasa_desocupacion_04.plot(kind='bar', color=['skyblue', 'orange'])
plt.title('Tasa de Desocupación según Sexo (2004)')
plt.xlabel('Sexo (1 = Hombre, 0= Mujer)')
plt.ylabel('Tasa de Desocupación (%)')
plt.xticks(rotation=0)
plt.savefig("tasa_desocupacion_sexo_2004.png", dpi=300)
plt.show()

# Graficar tasas de desocupación para 2024
plt.figure(figsize=(8, 6))
tasa_desocupacion_24.plot(kind='bar', color=['skyblue', 'orange'])
plt.title('Tasa de Desocupación según Sexo (2024)')
plt.xlabel('Sexo (1 = Hombre, 0 = Mujer)')
plt.ylabel('Tasa de Desocupación (%)')
plt.xticks(rotation=0)
plt.savefig("tasa_desocupacion_sexo_2024.png", dpi=300)
plt.show()

#----- (III) Tasa de Desocupacion segun rango etario:
    # Definir rangos de edad
bins = [0, 17, 24, 34, 44, 54, 64, 100]
labels = ['<18', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']

# Crear variable de rangos de edad para 2004 y 2024
data_04['edad_rango'] = pd.cut(data_04['ch06'], bins=bins, labels=labels)
data_24['edad_rango'] = pd.cut(data_24['CH06'], bins=bins, labels=labels)

# Tasa de desocupación según rangos de edad para 2004
tasa_desocupacion_04 = data_04.groupby('edad_rango')['desocupado'].mean() * 100

# Tasa de desocupación según rangos de edad para 2024
tasa_desocupacion_24 = data_24.groupby('edad_rango')['desocupado'].mean() * 100

# Mostrar resultados
print("Tasa de desocupación según rangos de edad - 2004:")
print(tasa_desocupacion_04)

print("Tasa de desocupación según rangos de edad - 2024:")
print(tasa_desocupacion_24)

# Graficar tasas de desocupación para 2004
plt.figure(figsize=(10, 6))
tasa_desocupacion_04.plot(kind='bar', color='skyblue')
plt.title('Tasa de Desocupación según Rangos de Edad (2004)')
plt.xlabel('Rangos de Edad')
plt.ylabel('Tasa de Desocupación (%)')
plt.xticks(rotation=45)
plt.savefig("tasa_desocupacion_edad_2004.png", dpi=300)
plt.show()

# Graficar tasas de desocupación para 2024
plt.figure(figsize=(10, 6))
tasa_desocupacion_24.plot(kind='bar', color='orange')
plt.title('Tasa de Desocupación según Rangos de Edad (2024)')
plt.xlabel('Rangos de Edad')
plt.ylabel('Tasa de Desocupación (%)')
plt.xticks(rotation=45)
plt.savefig("tasa_desocupacion_edad_2024.png", dpi=300)
plt.show()


#----- (IV) Proporcion de Ocupados por Hogar

# Media según desocupación
print(data_04.groupby('desocupado')['prop_ocupados_hogar'].mean())

# Boxplot
plt.figure(figsize=(8, 6))
data_04.boxplot(column='prop_ocupados_hogar', by='desocupado', grid=False)
plt.title('Proporción de Ocupados en el Hogar según Desocupación (2004)')
plt.suptitle('')  # Eliminar título por defecto
plt.xlabel('Desocupado')
plt.ylabel('Proporción de Ocupados en el Hogar')
plt.xticks([1, 2], ['No', 'Sí'])
plt.savefig('boxplot_prop_ocupados_hogar_2004.png', dpi=300)
plt.show()


# Boxplot
plt.figure(figsize=(8, 6))
data_24.boxplot(column='prop_ocupados_hogar', by='desocupado', grid=False)
plt.title('Proporción de Ocupados en el Hogar según Desocupación (2024)')
plt.suptitle('')  # Eliminar título por defecto
plt.xlabel('Desocupado')
plt.ylabel('Proporción de Ocupados en el Hogar')
plt.xticks([1, 2], ['No', 'Sí'])
plt.savefig('boxplot_prop_ocupados_hogar_2024.png', dpi=300)
plt.show()


#----- (V) Tasa de Desocupacion segun si la vivienda esta cerca de un basural
# Tasa de desocupación según cercanía a un basural (V_Basural) para 2004
tasa_desocupacion_basural_04 = data_04.groupby('iv12_1')['desocupado'].mean() * 100

# Tasa de desocupación según cercanía a un basural (V_Basural) para 2024
tasa_desocupacion_basural_24 = data_24.groupby('IV12_1')['desocupado'].mean() * 100

# Mostrar resultados
print("Tasa de desocupación según cercanía a un basural - 2004:")
print(tasa_desocupacion_basural_04)

print("Tasa de desocupación según cercanía a un basural - 2024:")
print(tasa_desocupacion_basural_24)

# Gráfico para 2004
plt.figure(figsize=(8, 6))
tasa_desocupacion_basural_04.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Tasa de Desocupación según Cercanía a un Basural (2004)')
plt.xlabel('Cerca de un Basural (0 = No, 1 = Sí)')
plt.ylabel('Tasa de Desocupación (%)')
plt.xticks(rotation=0)
plt.savefig('tasa_desocupacion_basural_2004.png', dpi=300)
plt.show()

# Gráfico para 2024
plt.figure(figsize=(8, 6))
tasa_desocupacion_basural_24.plot(kind='bar', color='orange', edgecolor='black')
plt.title('Tasa de Desocupación según Cercanía a un Basural (2024)')
plt.xlabel('Cerca de un Basural (0 = No, 1 = Sí)')
plt.ylabel('Tasa de Desocupación (%)')
plt.xticks(rotation=0)
plt.savefig('tasa_desocupacion_basural_2024.png', dpi=300)
plt.show()




#---------------------------EJERCICIO 6---------------------------

# En el TP3 calcularon la tasa de desocupación según INDEC y economía laboral, para el 1er trimestre de 2024. 
# Utilice una sola observación por hogar y sumen el ponderador PONDERA que permite expandir la muestra de la EPH al total de la población que representa 
# ¿Cuál es la tasa de hogares con desocupación para su aglomerado?


# 1. Crear una columna que marque hogares con al menos un desocupado
# 'ESTADO' == 2 indica desocupación
data_24['desocupado'] = (data_24['ESTADO'] == 2)

# 2. Identificar si hay al menos un desocupado por hogar
# Agrupamos por hogar y calculamos el máximo (True = 1 si hay algún desocupado)
data_24['desocupado_hogar'] = data_24.groupby(['CODUSU', 'NRO_HOGAR'])['desocupado'].transform('max')

# 3. Seleccionar solo una fila por hogar
hogares = data_24.drop_duplicates(subset=['CODUSU', 'NRO_HOGAR'])

# 4. Calcular la tasa de hogares con desocupación ponderada
tasa_desocupacion = (
    hogares['PONDERA_x'][hogares['desocupado_hogar'] == True].sum() / hogares['PONDERA_x'].sum()
) * 100

# 5. Mostrar el resultado
print(f"La tasa de hogares con desocupación es: {tasa_desocupacion:.2f}%")






#--------------------PARTE II: Clasificación y regularización --------------------

#---------------------------EJERCICIO 1---------------------------

# Genero la columna desocupado para data_04:
data_04['desocupado'] = (data_04['estado'] == 2)

# Primero me quedo con las variables que usaremos para la regresion. 
# Borramos CODUSU, PONDERA y NRO_HOGAR. 
# Algo que me di cuenta es que de las variables cantidad de miembros del hogar, miembros menores a 10 años y miembros
# mayores a 10 años es que debo eliminar una para que no haya multicolinealidad.
# Elimino cantidad de miembros mayores a 10 años:

data_04 = data_04.drop(['CODUSU', 'nro_hogar', 'pondera_x', 'pondera_y', 'estado','IX_Mayeq10', 'jefe_ocupado', 'edad_rango'], axis=1).copy() 
data_24 = data_24.drop(['CODUSU', 'NRO_HOGAR', 'PONDERA_x', 'PONDERA_y', 'ESTADO', 'desocupado_hogar', 'IX_MAYEQ10', 'jefe_ocupado', 'edad_rango'], axis=1).copy() 

# Paso a ceros y unos los True y False:
data_04 = data_04.astype(int)
data_24 = data_24.astype(int) 



#------ Importo librerias:
import numpy as np
from ISLP import load_data

from sklearn.preprocessing import scale
from sklearn.linear_model import Lasso, LassoCV, Ridge, RidgeCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler #para estandarizar. 
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, recall_score 
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn.metrics import RocCurveDisplay
from sklearn.metrics import log_loss

import seaborn as sns




#-------- Parto en TRAIN y TEST para cada año:
    
# Para 2004
X_train_04, X_test_04, y_train_04, y_test_04 = train_test_split(data_04.loc[:, data_04.columns!='desocupado'], data_04['desocupado'],test_size=0.3, random_state=101) 

# Para 2024
X_train_24, X_test_24, y_train_24, y_test_24 = train_test_split(data_24.loc[:, data_24.columns!= 'desocupado' ], data_24['desocupado'],test_size=0.3, random_state=101) 


#------ Tengo que estandarizar las X. Estandarizo para train y test por separado para cada año: 


# Para 2024
sc_24 = StandardScaler()
X_train_24_transformed = pd.DataFrame(sc_24.fit_transform(X_train_24), index=X_train_24.index, columns=X_train_24.columns)
X_test_24_transformed = pd.DataFrame(sc_24.transform(X_test_24), index=X_test_24.index, columns=X_test_24.columns)

# Para 2004
sc_04 = StandardScaler()
X_train_04_transformed = pd.DataFrame(sc_04.fit_transform(X_train_04), index=X_train_04.index, columns=X_train_04.columns)
X_test_04_transformed = pd.DataFrame(sc_04.transform(X_test_04), index=X_test_04.index, columns=X_test_04.columns)




# Agrego el Intercepto:
X_train_04_transformed["intercepto"]=1
X_test_04_transformed["intercepto"]=1
X_train_24_transformed["intercepto"]=1
X_test_24_transformed["intercepto"]=1  






#---------------------------EJERCICIO 4 ---------------------------

    
# --- (I) Regresion Logistica para 2024 ---

# i) LASSO
log_reg_24_lasso = LogisticRegression(penalty='l1', solver='liblinear').fit(X_train_24_transformed, y_train_24)

# Predicciones
y_test_pred_score_24_lasso = log_reg_24_lasso.predict_proba(X_test_24_transformed)[:,1]
y_test_pred_24_lasso = log_reg_24_lasso.predict(X_test_24_transformed)

#--AUC y ROC
auc_24_lasso = roc_auc_score(y_test_24, y_test_pred_score_24_lasso)
print('AUC LASSO 2024: %.4f' % auc_24_lasso)
fpr_24_lasso, tpr_24_lasso, thresholds_24_lasso = roc_curve(y_test_24, y_test_pred_score_24_lasso)

display = RocCurveDisplay(fpr=fpr_24_lasso, tpr=tpr_24_lasso, roc_auc=auc_24_lasso, estimator_name='Regresión Logística Lasso 2024')
display.plot()  
plt.plot([0, 1], [0, 1], color='red', linestyle='--')
plt.savefig("curva_roc_log_lasso_2024.png", format="png", dpi=300)
plt.show()

#--Matriz de confusion
matriz_confusion_log_24_lasso = confusion_matrix(y_test_24, y_test_pred_24_lasso)
print('Matriz de Confusion LASSO:')
print(matriz_confusion_log_24_lasso) 

# Ploteo la matriz de confusion:
group_names = ['Verdaderos Negativos','Falsos Positivos','Falsos Negativos','Verdaderos Positivos']

group_counts = ["{0:0.0f}".format(value) for value in
                matriz_confusion_log_24_lasso.flatten()]

group_percentages = ["{0:.2%}".format(value) for value in
                     matriz_confusion_log_24_lasso.flatten()/np.sum(matriz_confusion_log_24_lasso)]

labels = [f"{v1}\n{v2}\n{v3}" for v1, v2, v3 in
          zip(group_names,group_counts,group_percentages)]

labels = np.asarray(labels).reshape(2,2)
plt.figure(figsize=(8, 6))
ax = sns.heatmap(matriz_confusion_log_24_lasso, annot=labels, fmt='', cmap='Greens')

ax.set_title('Matriz de Confusión para el método de regresión logística Lasso para el 2024\n\n');
ax.set_xlabel('\nValores Predichos')
ax.set_ylabel('Valores Reales');
ax.xaxis.set_ticklabels(['False','True'])
ax.yaxis.set_ticklabels(['False','True'])
plt.savefig("matriz_confusion_log_lasso_2024.png", format="png", dpi=300)
plt.show()

#-- Accuracy
ac_log_24_lasso = accuracy_score(y_test_24, y_test_pred_24_lasso)
print('Accuracy para el modelo logístico LASSO para el 2024 :','%.3f' % ac_log_24_lasso) 



# ii) RIDGE
log_reg_24_ridge = LogisticRegression(penalty='l2', solver='lbfgs').fit(X_train_24_transformed, y_train_24)

# Predicciones
y_test_pred_score_24_ridge = log_reg_24_ridge.predict_proba(X_test_24_transformed)[:,1]
y_test_pred_24_ridge = log_reg_24_ridge.predict(X_test_24_transformed)

#--AUC y ROC
auc_24_ridge = roc_auc_score(y_test_24, y_test_pred_score_24_ridge)
print('AUC RIDGE 2024: %.4f' % auc_24_ridge)
fpr_24_ridge, tpr_24_ridge, thresholds_24_ridge = roc_curve(y_test_24, y_test_pred_score_24_ridge)

display = RocCurveDisplay(fpr=fpr_24_ridge, tpr=tpr_24_ridge, roc_auc=auc_24_ridge, estimator_name='Regresión Logística Ridge 2024')
display.plot()  
plt.plot([0, 1], [0, 1], color='red', linestyle='--')
plt.savefig("curva_roc_log_ridge_2024.png", format="png", dpi=300)
plt.show()


#--Matriz de confusion
matriz_confusion_log_24_ridge = confusion_matrix(y_test_24, y_test_pred_24_ridge)
print('Matriz de Confusion RIDGE:')
print(matriz_confusion_log_24_ridge) 

# Ploteo la matriz de confusion:
group_counts = ["{0:0.0f}".format(value) for value in
                matriz_confusion_log_24_ridge.flatten()]

group_percentages = ["{0:.2%}".format(value) for value in
                     matriz_confusion_log_24_ridge.flatten()/np.sum(matriz_confusion_log_24_ridge)]

labels = [f"{v1}\n{v2}\n{v3}" for v1, v2, v3 in
          zip(group_names,group_counts,group_percentages)]

labels = np.asarray(labels).reshape(2,2)
plt.figure(figsize=(8, 6))
ax = sns.heatmap(matriz_confusion_log_24_ridge, annot=labels, fmt='', cmap='Greens')

ax.set_title('Matriz de Confusión para el método de regresión logística Ridge para el 2024\n\n');
ax.set_xlabel('\nValores Predichos')
ax.set_ylabel('Valores Reales');
ax.xaxis.set_ticklabels(['False','True'])
ax.yaxis.set_ticklabels(['False','True'])
plt.savefig("matriz_confusion_log_ridge_2024.png", format="png", dpi=300)
plt.show()

#-- Accuracy
ac_log_24_ridge = accuracy_score(y_test_24, y_test_pred_24_ridge)
print('Accuracy para el modelo logístico RIDGE para el 2024 :','%.3f' % ac_log_24_ridge)





#--------- (II) Regresion Logistica para 2004:
# i) LASSO
# Ajustamos el clasificador con el metodo fit() 

log_reg_04_lasso = LogisticRegression(penalty='l1', solver='liblinear').fit(X_train_04_transformed, y_train_04)

# Predicciones
y_test_pred_score_04_lasso = log_reg_04_lasso.predict_proba(X_test_04_transformed)[:,1]
y_test_pred_04_lasso = log_reg_04_lasso.predict(X_test_04_transformed) 

#--AUC y ROC
auc_04_lasso = roc_auc_score(y_test_04, y_test_pred_score_04_lasso)
print('AUC LASSO 2004: %.4f' % auc_04_lasso)
fpr_04_lasso, tpr_04_lasso, thresholds_04_lasso = roc_curve(y_test_04, y_test_pred_score_04_lasso)

display = RocCurveDisplay(fpr=fpr_04_lasso, tpr=tpr_04_lasso, roc_auc=auc_04_lasso, estimator_name='Regresión Logística Lasso 2004')
display.plot()  
plt.plot([0, 1], [0, 1], color='red', linestyle='--')
plt.savefig("curva_roc_log_lasso_2004.png", format="png", dpi=300)
plt.show()


#--Matriz de confusion
matriz_confusion_log_04_lasso = confusion_matrix(y_test_04, y_test_pred_04_lasso)

print('Matriz de Confusion LASSO:')
print(matriz_confusion_log_04_lasso) 

# Ploteo la matriz de confusion:
group_names = ['Verdaderos Negativos','Falsos Positivos','Falsos Negativos','Verdaderos Positivos']

group_counts = ["{0:0.0f}".format(value) for value in
                matriz_confusion_log_04_lasso.flatten()]

group_percentages = ["{0:.2%}".format(value) for value in
                     matriz_confusion_log_04_lasso.flatten()/np.sum(matriz_confusion_log_04_lasso)]

labels = [f"{v1}\n{v2}\n{v3}" for v1, v2, v3 in
          zip(group_names,group_counts,group_percentages)]

labels = np.asarray(labels).reshape(2,2)
plt.figure(figsize=(8, 6))
ax = sns.heatmap(matriz_confusion_log_04_lasso, annot=labels, fmt='', cmap='Greens')

ax.set_title('Matriz de Confusión para el método de regresión logística Lasso para el 2004\n\n');
ax.set_xlabel('\nValores Predichos')
ax.set_ylabel('Valores Reales');
ax.xaxis.set_ticklabels(['False','True'])
ax.yaxis.set_ticklabels(['False','True'])
plt.savefig("matriz_confusion_log_lasso_2004.png", format="png", dpi=300)
plt.show()

#-- Accuracy
ac_log_04_lasso = accuracy_score(y_test_04, y_test_pred_04_lasso)
print('Accuracy para el modelo logístico LASSO para el 2004 :','%.3f' % ac_log_04_lasso) 





# ii) RIDGE
# Ajustamos el clasificador con el metodo fit() 

log_reg_04_ridge = LogisticRegression(penalty='l2', solver='lbfgs').fit(X_train_04_transformed, y_train_04)

# Predicciones
y_test_pred_score_04_ridge = log_reg_04_ridge.predict_proba(X_test_04_transformed)[:,1]
y_test_pred_04_ridge = log_reg_04_ridge.predict(X_test_04_transformed) 

#--AUC y ROC
auc_04_ridge = roc_auc_score(y_test_04, y_test_pred_score_04_ridge)
print('AUC RIDGE 2004: %.4f' % auc_04_ridge)
fpr_04_ridge, tpr_04_ridge, thresholds_04_ridge = roc_curve(y_test_04, y_test_pred_score_04_ridge)

display = RocCurveDisplay(fpr=fpr_04_ridge, tpr=tpr_04_ridge, roc_auc=auc_04_ridge, estimator_name='Regresión Logística Ridge 2004')
display.plot()  
plt.plot([0, 1], [0, 1], color='red', linestyle='--')
plt.savefig("curva_roc_log_ridge_2004.png", format="png", dpi=300)
plt.show()


#--Matriz de confusion
matriz_confusion_log_04_ridge = confusion_matrix(y_test_04, y_test_pred_04_ridge)

print('Matriz de Confusion RIDGE:')
print(matriz_confusion_log_04_ridge) 

# Ploteo la matriz de confusion:
group_counts = ["{0:0.0f}".format(value) for value in
                matriz_confusion_log_04_ridge.flatten()]

group_percentages = ["{0:.2%}".format(value) for value in
                     matriz_confusion_log_04_ridge.flatten()/np.sum(matriz_confusion_log_04_ridge)]

labels = [f"{v1}\n{v2}\n{v3}" for v1, v2, v3 in
          zip(group_names,group_counts,group_percentages)]

labels = np.asarray(labels).reshape(2,2)
plt.figure(figsize=(8, 6))
ax = sns.heatmap(matriz_confusion_log_04_ridge, annot=labels, fmt='', cmap='Greens')

ax.set_title('Matriz de Confusión para el método de regresión logística Ridge para el 2004\n\n');
ax.set_xlabel('\nValores Predichos')
ax.set_ylabel('Valores Reales');
ax.xaxis.set_ticklabels(['False','True'])
ax.yaxis.set_ticklabels(['False','True'])
plt.savefig("matriz_confusion_log_ridge_2004.png", format="png", dpi=300)
plt.show()

#-- Accuracy
ac_log_04_ridge = accuracy_score(y_test_04, y_test_pred_04_ridge)
print('Accuracy para el modelo logístico RIDGE para el 2004 :','%.3f' % ac_log_04_ridge)
 



#---------------------------EJERCICIO 5 ---------------------------



# defino la barrida de lambdas
lambdas = [10**n for n in range(-5, 7)] 

# Defino K-CV:
K = 10
kf = KFold(n_splits = K, shuffle=True, random_state=100)


# Para almacenar resultados
ridge_results_24 = pd.DataFrame(columns=["lambda", "particion", "log_loss"],
                                dtype=float)
lasso_results_24 = pd.DataFrame(columns=["lambda", "particion", "log_loss"],
                                dtype=float) 

lasso_zero_prop_24 = []
lasso_zero_prop_04 = []





# -------- (I) 2024 --------
   
#----- RIDGE -----      
ridge_results_list = [] # Lista temporal para almacenar resultados  
for l in lambdas:
    # --- Ridge (L2) con regresión logística ---
    ridge = LogisticRegression(penalty='l2', C=1/l, solver='liblinear', max_iter=10000)
    for i, (train_index2, val_index2) in enumerate(kf.split(X_train_24)):
        # Selección de datos con iloc para evitar errores de índice
        X_train_fold, X_val_fold = X_train_24_transformed.iloc[train_index2], X_train_24_transformed.iloc[val_index2]
        y_train_fold, y_val_fold = y_train_24.iloc[train_index2], y_train_24.iloc[val_index2]

        # Entrenar el modelo
        ridge.fit(X_train_fold, y_train_fold)

        # Predecir probabilidades
        y_pred = ridge.predict_proba(X_val_fold)[:, 1]

        # Calcular log_loss como error
        error = log_loss(y_val_fold, y_pred)

        # Guardar resultados
        ridge_results_list .append({"lambda": l, "particion": i, "log_loss": error})
        
# Convertir a DataFrame
ridge_results_24 = pd.DataFrame(ridge_results_list ) 

# --- Boxplots ---
plt.figure(figsize=(10, 6))
sns.boxplot(x="lambda", y="log_loss", data=ridge_results_24)
plt.title("Distribución del error de predicción (log_loss) para Regularización Ridge para 2024  para cada λ")
plt.xlabel("Lambda (log10)")
plt.ylabel("Log Loss")
plt.xticks(ticks=range(len(lambdas)), labels=[f"10^{int(np.log10(l))}" for l in lambdas], rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("log_loss_ridge_2024.png", format="png", dpi=300)
plt.show() 
        

 


#----- LASSO ----- 

lasso_results_list = [] # Lista temporal para almacenar resultados  
lasso_zero_prop_24 = [] # Proporción de ceros por lambda

for l in lambdas:
    # --- Lasso (L1) con regresión logística ---
    lasso = LogisticRegression(penalty='l1', C=1/l, solver='liblinear', max_iter=10000)
    zeros = []  # Lista para almacenar proporción de ceros por fold
    
    for i, (train_index2, val_index2) in enumerate(kf.split(X_train_24)):
        # Selección de datos con iloc
        X_train_fold, X_val_fold = X_train_24_transformed.iloc[train_index2], X_train_24_transformed.iloc[val_index2]
        y_train_fold, y_val_fold = y_train_24.iloc[train_index2], y_train_24.iloc[val_index2]

        # Entrenar el modelo
        lasso.fit(X_train_fold, y_train_fold)

        # Predecir probabilidades
        y_pred = lasso.predict_proba(X_val_fold)[:, 1]

        # Calcular log_loss
        error = log_loss(y_val_fold, y_pred)

        # Guardar resultados
        lasso_results_list.append({"lambda": l, "particion": i, "log_loss": error})

        # Calcular proporción de coeficientes en cero
        zero_proportion = np.mean(lasso.coef_ == 0)
        zeros.append(zero_proportion)

    # Promedio de coeficientes en cero para este lambda
    lasso_zero_prop_24.append(np.mean(zeros))

# Convertir a DataFrame
lasso_results_24 = pd.DataFrame(lasso_results_list)

# --- Boxplots ---
plt.figure(figsize=(10, 6))
sns.boxplot(x="lambda", y="log_loss", data=lasso_results_24)
plt.title("Distribución del error de predicción (log_loss) para Regularización Lasso para 2024 para cada λ")
plt.xlabel("Lambda (log10)")
plt.ylabel("Log Loss")
plt.xticks(ticks=range(len(lambdas)), labels=[f"10^{int(np.log10(l))}" for l in lambdas], rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("log_loss_lasso_2024.png", format="png", dpi=300)
plt.show() 



# --- Line plot: Proporción de variables ignoradas ---
plt.figure(figsize=(10, 6))
plt.plot([np.log10(l) for l in lambdas], lasso_zero_prop_24, marker='o', linestyle='-', markersize=6)
plt.title("Proporción de coeficientes en cero vs Lambda (Lasso)")
plt.xlabel("Lambda (log10)")
plt.ylabel("Proporción de coeficientes en cero")
plt.grid(True)
plt.tight_layout()
plt.savefig("zero_proportions_lasso_2024.png", format="png", dpi=300)
plt.show()






# -------- (II) 2004 --------
ridge_results_04 = pd.DataFrame(columns=["lambda", "particion", "log_loss"],
                                dtype=float)
lasso_results_04 = pd.DataFrame(columns=["lambda", "particion", "log_loss"],
                                dtype=float) 
lasso_zero_prop_04 = []


#----- RIDGE -----      
ridge_results_list = [] # Lista temporal para almacenar resultados  
for l in lambdas:
    # --- Ridge (L2) con regresión logística ---
    ridge = LogisticRegression(penalty='l2', C=1/l, solver='liblinear', max_iter=10000)
    for i, (train_index2, val_index2) in enumerate(kf.split(X_train_04)):
        # Selección de datos con iloc para evitar errores de índice
        X_train_fold, X_val_fold = X_train_04_transformed.iloc[train_index2], X_train_04_transformed.iloc[val_index2]
        y_train_fold, y_val_fold = y_train_04.iloc[train_index2], y_train_04.iloc[val_index2]

        # Entrenar el modelo
        ridge.fit(X_train_fold, y_train_fold)

        # Predecir probabilidades
        y_pred = ridge.predict_proba(X_val_fold)[:, 1]

        # Calcular log_loss como error
        error = log_loss(y_val_fold, y_pred)

        # Guardar resultados
        ridge_results_list .append({"lambda": l, "particion": i, "log_loss": error})
        
# Convertir a DataFrame
ridge_results_04 = pd.DataFrame(ridge_results_list ) 

# --- Boxplots ---
plt.figure(figsize=(10, 6))
sns.boxplot(x="lambda", y="log_loss", data=ridge_results_04)
plt.title("Distribución del error de predicción (log_loss) para Regularización Ridge para 2004 para cada λ")
plt.xlabel("Lambda (log10)")
plt.ylabel("Log Loss")
plt.xticks(ticks=range(len(lambdas)), labels=[f"10^{int(np.log10(l))}" for l in lambdas], rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("log_loss_ridge_2004.png", format="png", dpi=300)
plt.show() 
        

       


#----- LASSO ----- 

lasso_results_list = [] # Lista temporal para almacenar resultados  
lasso_zero_prop_04 = [] # Proporción de ceros por lambda

for l in lambdas:
    # --- Lasso (L1) con regresión logística ---
    lasso = LogisticRegression(penalty='l1', C=1/l, solver='liblinear', max_iter=10000)
    zeros = []  # Lista para almacenar proporción de ceros por fold
    
    for i, (train_index2, val_index2) in enumerate(kf.split(X_train_04)):
        # Selección de datos con iloc
        X_train_fold, X_val_fold = X_train_04_transformed.iloc[train_index2], X_train_04_transformed.iloc[val_index2]
        y_train_fold, y_val_fold = y_train_04.iloc[train_index2], y_train_04.iloc[val_index2]

        # Entrenar el modelo
        lasso.fit(X_train_fold, y_train_fold)

        # Predecir probabilidades
        y_pred = lasso.predict_proba(X_val_fold)[:, 1]

        # Calcular log_loss
        error = log_loss(y_val_fold, y_pred)

        # Guardar resultados
        lasso_results_list.append({"lambda": l, "particion": i, "log_loss": error})

        # Calcular proporción de coeficientes en cero
        zero_proportion = np.mean(lasso.coef_ == 0)
        zeros.append(zero_proportion)

    # Promedio de coeficientes en cero para este lambda
    lasso_zero_prop_04.append(np.mean(zeros))

# Convertir a DataFrame
lasso_results_04 = pd.DataFrame(lasso_results_list)

# --- Boxplots ---
plt.figure(figsize=(10, 6))
sns.boxplot(x="lambda", y="log_loss", data=lasso_results_04)
plt.title("Distribución del error de predicción (log_loss) para Regularización Lasso para 2004 para cada λ")
plt.xlabel("Lambda (log10)")
plt.ylabel("Log Loss")
plt.xticks(ticks=range(len(lambdas)), labels=[f"10^{int(np.log10(l))}" for l in lambdas], rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("log_loss_lasso_2004.png", format="png", dpi=300)
plt.show() 



# --- Line plot: Proporción de variables ignoradas ---
plt.figure(figsize=(10, 6))
plt.plot([np.log10(l) for l in lambdas], lasso_zero_prop_04, marker='o', linestyle='-', markersize=6)
plt.title("Proporción de coeficientes en cero vs Lambda (Lasso)")
plt.xlabel("Lambda (log10)")
plt.ylabel("Proporción de coeficientes en cero")
plt.grid(True)
plt.tight_layout()
plt.savefig("zero_proportions_lasso_2004.png", format="png", dpi=300)
plt.show()



#---------------------------EJERCICIO 6 ---------------------------

#------ Seleccion del lambda optimo ------
# Si bien visualizando el boxplot nos damos cuanta que el menor error de pronostico se da en lambda = 10^(0) = 1, 
# podemos hacer un codigo que nos diga exactamente para qué lambda se da el minimo error:
    
#------ (I) 2024 ------

#----- RIDGE:

error_ridge_24 = ridge_results_24.groupby('lambda').agg({'log_loss': 'mean'})
error_ridge_24.reset_index(inplace = True)
error_ridge_24.astype({"lambda":int})

# Función para seleccionar 
min_error_r_24 = np.Inf
lambda_r_24 = None

for index, row in error_ridge_24.iterrows():
    if row['log_loss'] < min_error_r_24:
        min_error_r_24 = row['log_loss']
        lambda_r_24= row['lambda'].astype(int)

print('El mínimo error para Ridge 2024 es', round(min_error_r_24, 2), 'y se da con un lambda igual a', lambda_r_24)


#----- LASSO:

error_lasso_24 = lasso_results_24.groupby('lambda').agg({'log_loss': 'mean'})
error_lasso_24.reset_index(inplace = True)
error_lasso_24.astype({"lambda":int})


# Función para seleccionar 
min_error_l_24 = np.Inf
lambda_l_24 = None

for index, row in error_lasso_24.iterrows():
    if row['log_loss'] < min_error_l_24:
        min_error_l_24 = row['log_loss']
        lambda_l_24 = row['lambda'].astype(int)

print('El mínimo error para Lasso 2024 es', round(min_error_l_24, 2), 'y se da con un lambda igual a', lambda_l_24)



#------ (II) 2004 ------

#----- RIDGE:

error_ridge_04 = ridge_results_04.groupby('lambda').agg({'log_loss': 'mean'})
error_ridge_04.reset_index(inplace = True)
error_ridge_04.astype({"lambda":int})

# Función para seleccionar 
min_error_r_04 = np.Inf
lambda_r_04 = None

for index, row in error_ridge_04.iterrows():
    if row['log_loss'] < min_error_r_04:
        min_error_r_04 = row['log_loss']
        lambda_r_04 = row['lambda'].astype(int)

print('El mínimo error para Ridge 2004 es', round(min_error_r_04, 2), 'y se da con un lambda igual a', lambda_r_04)


#----- LASSO:

error_lasso_04 = lasso_results_04.groupby('lambda').agg({'log_loss': 'mean'})
error_lasso_04.reset_index(inplace = True)
error_lasso_04.astype({"lambda":int})


# Función para seleccionar 
min_error_l_04 = np.Inf
lambda_l_04 = None

for index, row in error_lasso_04.iterrows():
    if row['log_loss'] < min_error_l_04:
        min_error_l_04 = row['log_loss']
        lambda_l_04 = row['lambda'].astype(int)

print('El mínimo error para Lasso 2004 es', round(min_error_l_04, 2), 'y se da con un lambda igual a', lambda_l_04)


#------- Ahora que sé el lambda, tengo que estimar de vuelta y ver qué coeficientes son iguales a cero:
    
#------ (I) 2024 ------

#----LASSO: 
lasso_optimo_24 = LogisticRegression(penalty='l1', C=1/lambda_l_24, solver='liblinear', max_iter=10000)
lasso_optimo_24.fit(X_train_24_transformed, y_train_24) 

# Obtener coeficientes del modelo
coeficientes_l_24 = lasso_optimo_24.coef_[0]

# Crear un DataFrame para mostrar los resultados
variables_24 = X_train_24_transformed.columns  # Nombres de las variables
coef_df_24 = pd.DataFrame({'Variable': variables_24, 'Coeficiente': coeficientes_l_24})

# Filtrar variables con coeficientes cero
coef_cero_24 = coef_df_24[coef_df_24['Coeficiente'] == 0]

# Mostrar resultados
print("Variables con coeficientes iguales a cero para Regularización Lasso para el 2024:")
print(coef_cero_24)

# Crear la tabla en LaTeX
tabla_latex = coef_df_24.to_latex(index=False, float_format="%.4f", caption="Coeficientes del modelo LASSO para 2024", label="tab:lasso_2024")

# Guardar la tabla en un archivo .tex
with open("coeficientes_lasso_2024.tex", "w") as file:
    file.write(tabla_latex)

print("Tabla en LaTeX guardada como 'coeficientes_lasso_2024.tex'")




#-------- Guardo coeficientes iguales a cero para Lasso 2024

# Modelo LASSO para 2024
lasso_optimo_24 = LogisticRegression(penalty='l1', C=1/lambda_l_24, solver='liblinear', max_iter=10000)
lasso_optimo_24.fit(X_train_24_transformed, y_train_24) 

# Obtener coeficientes del modelo
coeficientes_l_24 = lasso_optimo_24.coef_[0]

# Crear un DataFrame para mostrar los resultados
variables_24 = X_train_24_transformed.columns  # Nombres de las variables
coef_df_24 = pd.DataFrame({'Variable': variables_24, 'Coeficiente': coeficientes_l_24})

# Filtrar variables con coeficientes cero
coef_cero_24 = coef_df_24[coef_df_24['Coeficiente'] == 0]

# Mostrar resultados
print("Variables con coeficientes iguales a cero para Regularización Lasso para el 2024:")
print(coef_cero_24)

# Crear la tabla en LaTeX solo con coeficientes cero
tabla_latex_cero_24 = coef_cero_24.to_latex(index=False, float_format="%.4f", caption="Coeficientes iguales a cero del modelo LASSO para 2024", label="tab:lasso_2024_cero")

# Guardar la tabla en un archivo .tex
with open("coeficientes_lasso_2024_cero.tex", "w") as file:
    file.write(tabla_latex_cero_24)

print("Tabla en LaTeX guardada como 'coeficientes_lasso_2024_cero.tex'")



#------ (II) 2004 ------

#----LASSO: 
lasso_optimo_04 = LogisticRegression(penalty='l1', C=1/lambda_l_04, solver='liblinear', max_iter=10000)
lasso_optimo_04.fit(X_train_04_transformed, y_train_04) 

# Obtener coeficientes del modelo
coeficientes_l_04 = lasso_optimo_04.coef_[0]

# Crear un DataFrame para mostrar los resultados
variables_04 = X_train_04_transformed.columns  # Nombres de las variables
coef_df_04 = pd.DataFrame({'Variable': variables_04, 'Coeficiente': coeficientes_l_04})

# Filtrar variables con coeficientes cero
coef_cero_04 = coef_df_04[coef_df_04['Coeficiente'] == 0]

# Mostrar resultados
print("Variables con coeficientes iguales a cero para Regularización Lasso para el 2004:")
print(coef_cero_04)

# Crear la tabla en LaTeX
tabla_latex_04 = coef_df_04.to_latex(index=False, float_format="%.4f", caption="Coeficientes del modelo LASSO para 2004", label="tab:lasso_2004")

# Guardar la tabla en un archivo .tex
with open("coeficientes_lasso_2004.tex", "w") as file:
    file.write(tabla_latex_04)

print("Tabla en LaTeX guardada como 'coeficientes_lasso_2004.tex'")




#-------- Guardo coeficientes iguales a cero para Lasso 2004

# Modelo LASSO para 2004
lasso_optimo_04 = LogisticRegression(penalty='l1', C=1/lambda_l_04, solver='liblinear', max_iter=10000)
lasso_optimo_04.fit(X_train_04_transformed, y_train_04) 

# Obtener coeficientes del modelo
coeficientes_l_04 = lasso_optimo_04.coef_[0]

# Crear un DataFrame para mostrar los resultados
variables_04 = X_train_04_transformed.columns  # Nombres de las variables
coef_df_04 = pd.DataFrame({'Variable': variables_04, 'Coeficiente': coeficientes_l_04})

# Filtrar variables con coeficientes cero
coef_cero_04 = coef_df_04[coef_df_04['Coeficiente'] == 0]

# Mostrar resultados
print("Variables con coeficientes iguales a cero para Regularización Lasso para el 2024:")
print(coef_cero_04)

# Crear la tabla en LaTeX solo con coeficientes cero
tabla_latex_cero_04 = coef_cero_04.to_latex(index=False, float_format="%.4f", caption="Coeficientes iguales a cero del modelo LASSO para 2004", label="tab:lasso_2004_cero")

# Guardar la tabla en un archivo .tex
with open("coeficientes_lasso_2004_cero.tex", "w") as file:
    file.write(tabla_latex_cero_04)

print("Tabla en LaTeX guardada como 'coeficientes_lasso_2004_cero.tex'")






#---------------------------EJERCICIO 7 ---------------------------
from sklearn.metrics import mean_squared_error

# Vamos a elegir lambda = 10 para Ridge 2024 y lambda = 10 para Ridge 2004 y comparar mirando el ECM. 

#------Modelo RIDGE Optimo para 2004
ridge_optimo_04 = LogisticRegression(penalty='l2', C=1/lambda_r_04, solver='liblinear', max_iter=10000)
ridge_optimo_04.fit(X_train_04_transformed, y_train_04) 

# Predicciones para el conjunto de prueba
y_pred_04 = ridge_optimo_04.predict_proba(X_test_04_transformed)[:, 1]

# Calcular el ECM
ecm_r_04 = mean_squared_error(y_test_04, y_pred_04)
print("ECM para el modelo Ridge Optimo 2004:", ecm_r_04)

# Calculo log_loss
ll_r_04 = log_loss(y_test_04, y_pred_04) 

print("Log-Loss para el modelo Ridge Optimo 2004:", ll_r_04)


#-----Modelo RIDGE Optimo para 2024
ridge_optimo_24 = LogisticRegression(penalty='l2', C=1/lambda_r_24, solver='liblinear', max_iter=10000)
ridge_optimo_24.fit(X_train_24_transformed, y_train_24) 

# Predicciones para el conjunto de prueba
y_pred_24 = ridge_optimo_24.predict_proba(X_test_24_transformed)[:, 1]

# Calcular el ECM
ecm_r_24 = mean_squared_error(y_test_24, y_pred_24)

print("ECM para el modelo Ridge Optimo 2024:", ecm_r_24)

# Calculo log_loss
ll_r_24 = log_loss(y_test_24, y_pred_24) 

print("Log-Loss para el modelo Ridge Optimo 2024:", ll_r_24)


#------ Modelo LASSO Optimo 2024: 
lasso_optimo_24 = LogisticRegression(penalty='l1', C=1/lambda_l_24, solver='liblinear', max_iter=10000)
lasso_optimo_24.fit(X_train_24_transformed, y_train_24) 

# Predicciones para el conjunto de prueba
y_pred_24 = lasso_optimo_24.predict_proba(X_test_24_transformed)[:, 1]

# Calcular el ECM
ecm_l_24 = mean_squared_error(y_test_24, y_pred_24)

print("ECM para el modelo Lasso Optimo 2024:", ecm_l_24)

# Calculo log_loss
ll_l_24 = log_loss(y_test_24, y_pred_24) 

print("Log-Loss para el modelo Lasso Optimo 2024:", ll_l_24)
    






    

