# Challenge Rappi - Modelo de fraude

## Estructura del repositorio:

a. ds_challenge_2021.csv: Data 

b. Analisis: Notebook que contiene el análisis y construcción de los modelos

c. Replica: Tiene el notebook que ayudará para replicar los modelos de manera local y masiva de manera local

d. Modelos: Tiene los pkls de los dos modelos y el segmento

    i. Modelo 1 - Modelo fraude nivel transacciones:

      - var_model_cliente_rl.pkl: Variables del modelo

      - scale_reg_log_trxs: Escalar las variables

      - reg_log_trxs.pkl: Modelo 1

    ii. Segmentación:  
    
      - var_cluster.pkl: Variables para la segmentación

      - scale_segm_kmeans.pkl: Escalar las variables

      - segm_kmeans.pkl: Segmentación
      
      iii. Modelo 2 - Modelo fraude nivel cliente:

      - var_model_cliente_lgbm.pkl: Variables del modelo

      - scale_lgbm_cliente.pkl: Escalar las variables

      - lgbm_cliente.pkl: Modelo 2    
      
  e. Despliegue del modelo transaccional: Se realizó de manera local
  
  	- Crear en miniconda
	- Los pkls están en en Modelos
	- El .py es app_trx.py
	
	Pasos: 
  
  	conda create -n ApiFraudeTrx
	conda activate ApiFraudeTrx
	conda install python3.10
	
	Cambiar direccion a la ubicacion de los archivos
	pip install -r requirements.txt
	streamlit run app_trx.py 
	
	Consideraciones:
	- Tomar la data entre 0 y 1 (ya normalizada)
	
Ejemplos:
![Image text](https://github.com/EdwinChirre/ds_challeng_rappi/blob/main/EjemploDespliegue/Ejemplos.png)
	
Máscara del despliegue:
![Image text](https://github.com/EdwinChirre/ds_challeng_rappi/blob/main/EjemploDespliegue/ModeloDespliegue.PNG)
  
  
 ## Conclusiones:
 
![Image text](https://github.com/EdwinChirre/ds_challeng_rappi/blob/55f677520cfd825daa16c388e838409e7a632cde/Conclusion_Modelo.png)
 
    a.	La proporción de la data a nivel trxs es: 97% no fraudulenta y 3% fraudulenta y a nivel cliente es: 83% usuario no fraudulento y 17% usuario fraudulento
    b.	Del descriptivo podemos ver que hay días con mayor índice de trxs fraudulentas (16,20 y 28 de enero)
    c.	Del bivariado podemos notar la relación que tiene la TC física con los fraudes, trxs en web son menos propensas a ser fraudulentas. Los montos bajos tienden a ser más fraude
    d.	Se tienen 4 segmentos, donde hay uno que es el de mayor interés, porque tiene un gran consumo (alto valor) y concentra mayor cantidad de clientes fraudulentos (Segmento alto valor con riesgo muy alto)
    e.	Se desarrollaron 2 modelos, uno a nivel trxs y otro a nivel cliente
    f.	Modelo a nivel trxs se hizo regresión logística con Oversampling (SMOTE). El modelo me ayuda a detectar el 40% de trxs fraudulentas realmente
    g.	Modelo a nivel cliente: Se un modelo LGBM con Oversampling (SMOTE). El modelo me ayuda a detectar el 59% de clientes fraudulentos que realmente lo son. También se encuentran 3 grupos que diferencian por su nivel de fraude (Alto, medio y bajo)

 
 ## Análisis detallado:
 
 1.	Análisis descriptivo:
a.	Analizando las trxs fraudulentas por día, se tiene que los días 16,20 y 28 de enero son los días con mayor índice de trxs fraudulentas
b.	Se analiza missing de variables, por lo que se eliminan las variables establecimiento y ciudad por tener más de 30% de missing y la variable model porque tiene un solo valor
c.	Análisis bivariado Variables categóricas vs Target:
Se elimina género por tener correlación con las otras variables independientes
En el bivariado:

-	Las TC físicas son más propensas a ser usadas como fraude
-	Cliente prime son menos propenso a tener una trxs fraudulenta
-	En android hay más probabilidad de que se realice un fraude y en web el menos probable
-	Los miércoles probablemente son los días con mayores casos de fraude y sábado y viernes con menos probabilidad
d.	Análisis bivariado Variables numéricas vs Target:

Por correlación por encima del 0.8, excluyo la variable creada: Porc_dscto (porcentaje de descuento)
En el bivariado con los gráficos de boxplot:

-	Montos más bajos son los que ligeramente tienden a ser fraudes
-	Cashback más bajos son más fraudulentos (correlacionado con monto)
-	A mayor línea menos fraude



2.	Clúster: 
Se encontraron 4 segmentos a nivel cliente que se perfilan principalmente por el consumo y nivel de fraude. Para la segmentación no se considera la variable fraude, ya que, en su momento, es una variable que no se tiene. Se usa la variable para perfilar y describir que tanto se relaciona con los segmentos.

a.	Bajo valor con riesgo bajo (13.5%): Grupo de cliente con bajo consumo, pero línea de TC intermedia y es el grupo de clientes con menos usuarios fraudulentos

b.	Bajo valor con riesgo intermedio (27%): Grupo de usuarios con línea de TC más alta y con una Tasa de interés alta, pero bajo consumo y con fraude intermedio.

c.	Mediano valor con riesgo alto (32.5%): Grupo de usuarios con una línea de TC intermedia con la Tasa de interés más baja y consumo intermedio. Con respecto al fraude, tiene un fraude alto con un gran número de txs rechazadas.

d.	Alto valor y riesgo muy alto: Grupo de clientes con gran consumo y menor línea de TC con tasa super alta y concentra la mayor cantidad de clientes con fraude

Después de realizar la segmentación, podemos hacer más foco en el segmento Alto valor y riesgo muy alto, ya que me generan buen consumo, pero a la vez, es el grupo con mayor riesgo.
Hacer la segmentación nos ayuda para concentrarnos en un segmento foco y generar un modelo para cada uno. Para nuestro caso, se hará uno global y se tomará el segmento como una variable

Nota: Si bien es cierto, los fraudes están asociados a trxs pero en el desafío no me queda claro si es a nivel trxs o a nivel cliente, por ello, hice 2 modelos

3.	Modelo a nivel trxs
La distribución de fraude es: 
No Fraude: 97.0 % del dataset con 26165 trxs 
Fraude: 3.0 % del dataset con 810 trxs


Se hace una regresión logística con SMOTE para hacer un oversampling ya que el target es muy desbalanceado


Importancia de variables:
-	Las variables más importantes son son monto, cashback, hora y las menos importante son is_prime y os_Android, siendo prime no significativa 

Interpretación:
-	Al tener coeficiente negativo el monto, significa que hay más probabilidad de que ocurra fraude si el monto es bajo
-	Para la hora, si es más tarde, más probabilidad de que haya una trxs fraudulenta

Trade-off:
-	El modelo acierta 40% de los que dice que son trxs fraudulentas y realmente lo son. Tiene un accuracy de 61%, donde puede identificar correctamente las trxs fraudulentas con las no fraudulentas.

-	Precisión: El modelo me da 3351 trxs no fraudulentos y 2044 trxs fraudulentos
-	De esos 3253 acierta y es precisión para la clase no fraudulenta
-	Para la no fraudulenta, solo es 3%, es decir, acierta 64 de los 2044
-	El riesgo de esto es que detuvo 1980 operaciones, pero acertó 64
-	Y por el otro lado, hubieron 98 trxs que pasaron como buenas, pero eran fraude
-	El recall parte de los que realmente son fraudes o no fraudes y cuanto de ellos se acertó y de los 159 fraudulentos el modeló acertó con 64
-	Y revisando los montos, si no tuviera un modelo sería 81,000 aprox, entonces nos centramos en que tengo 27% de gastos que ya no serán por fraude.

4.	Modelo a nivel cliente
A nivel cliente, la proporción de fraude cambia:
No Fraude: 83.12 % del dataset con 3325 Clientes
Fraude: 16.88 % del dataset con 675 Clientes
	
Se realizó un modelo LGBM y también se hizo SMOTE para balancear la clase de fraudulentos

Importancia de variables:
-	La variable más importante es las trxs que realiza en el mes
-	El tipo de TC, si usa física o no
-	Y el Os, si es Android o no
Interpretación:
Para hacer la interpretación de un modelo de caja negra, usé SHAPE value que está basado en la teoría de juegos.
-	Me indica que a mayor trxs, mayor probabilidad que el cliente sea fraudulento
-	Si hace pago en una TC física es más probable que sea fraudulento
-	Si paga por web es menos probable a ser fraudulento
Trade-off:
-	El modelo acierta 69% de clientes que dice que son fraudulentos y realmente lo son. Tiene un accuracy de 70% donde puede identificar correctamente los usuarios fraudulentos con los no fraudulentos.

-	Precisión: El modelo clasifica 508 no fraudulentos y 292 fraudulentos. De esos 466 acierta y es precisión para la clase no fraudulenta
-	Para la no fraudulenta, solo es 32%, es decir, acierta 93 de los 292
-	El riesgo de esto es que dice que 199 clientes era fraudulentos cuando no lo son y genera incomodidad por parte del usuario

-	Y por el otro lado, hubo 42 usuarios que pasaron como buenas pero eran fraudulentos

-	El recall parte de los que realmente son fraudulentos o no fraudulentos y cuanto de ellos se acertó. De los 135 fraudulentos acertó 93, donde se evidencia que se está prediciendo los fraudulentos por encima de la mitad y eso es bueno.

-	Adicional, se segmenta en 3 grupos, uno de riesgo de fraude alto, medio y bajo basado en la probabilidad de ser un cliente fraudulento para poder aplicar estrategias diferenciadas en la gestión de detección de fraude.

