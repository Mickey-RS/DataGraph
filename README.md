# Datagraph

A través del uso de la librería *matplotlib*, permite la graficación de datos dados a través de un csv, un registro de gasto energético.

### Como instalar

Corre bajo el intérprete de Python 3.7, y hace uso de las librerías incluídas en el archivo *requirements.txt*. Todas las librerías pueden instalarse a través del archivo *Instalar_Requerimientos.bat*, siempre que el sistema cuente con el PIP para ello.

### Como usar

Se requiere ejecutar el archivo Graficos_Powerscape.pyw para iniciar el programa, ya que este se encuentra dividido en 2 partes: Motor y entorno gráfico.
Toma al rededor de 15 segundos en leer toda la información incluída en el archivo *Completo.csv*, y una vez que los tiene, muestra una interfáz que pide al usuario ingresar un rango de tiempo, seleccionar parámetros de graficación, y pedir un valor base y un rango de tolerancia en % para evaluar los datos dados.
Una vez que se grafica, devuelve una regresión polinomial sobre la información obtenida, esto con el fin de entender con mayor facilidad el comportamiento del sistema eléctrico con respecto al tiempo.
A su vez, si un valor base y una tolerancia fueron dadas, mostrará en otra gráfica todos los momentos en los que se cumplió el valor base, y todos aquellos en los que el sistema trabajó por encima y por debajo de la tolerancia.
Finalmente, mostrará un par de tablas con valores estadísticos respecto a los intervalos de de datos establecidos.

##### Los módulos más importantes utilizados para la creación de este proyecto son:
* matplotlib: Para graficar los datos obtenidos.
* pandas: Para organizar los datos en tablas, con el fin de manipularlos de manera más sencilla.
* scikit-learn y sklearn: Para realizar los gráficos polinomiales .
* scipy y numpy: Para obtener los datos estadísticos de los intervalos de datos.