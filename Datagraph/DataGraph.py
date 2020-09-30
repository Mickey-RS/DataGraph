'''Este es el script que realiza toda la parte operacional del programa. se
encarga de obtener los datos del archivo "Completo.csv", y posteriormente los
mostrará en una gráfica.'''

"""Importación de librerías:"""
#Pandas para el manejo de tablas de datos de forma sencilla
import pandas as pd
#StringIO para simular datos de una variable como un archivo
from io import StringIO
#pyplot, de matplotlib, para convertir las tablas de datos a gráficos
from matplotlib import pyplot as plt
#numpy para operaciones numericas complejass
import numpy as np
#sklearn para regresiones lineales
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
#random para una selección aleatoria de colores al momento de generar las gráficas
from random import randint

class DataGraph:
    """Se crea una clase para facilitar el manejo de el código en conjunto con un
    entorno visual"""
    def __init__(self):
        #Al inicializar, se crean dos atributos para la clase
        self.__data = None
        self.__df = None
        #Después se llama el método __get_raw_data(), para tomar todos los datos
        #del archivo .csv
        self.__get_raw_data()

    def __get_raw_data(self):
        """Con este método asignaremos a nuestro objeto la información proveniente
        del archivo .csv"""
        write = False
        #Se obtiene la información del archivo y se convierte a lista para su
        #análisis
        cdata = open('Completo.csv','r')
        cdata = list(cdata)
        #Se obtinenen índices de dónde comienza y termina la información importante
        start = cdata.index('Interval Raw Data,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n')
        end = cdata.index('Event Raw Data,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n')
        #Luego se extrae dicha información de la información completa por medio
        #de los índices
        cdata = cdata[start+1:end-1]
        #Se convierte la información a texto plano
        raw_data = '\n'.join(cdata)
        #Se simula como archivo
        readable_data = StringIO(raw_data)
        #Y se pasa al método read_csv, perteneciente a la librería "pandas"
        #para que pueda convertir todos los datos a información legible para la
        #librería
        self.__data = pd.read_csv(readable_data,low_memory=True)
        #La información se pasa al método DataFrame, perteneciente a pandas,
        #para convertirla en una tabla de datos
        self.__df = pd.DataFrame(self.__data)#!!!
        #Se convierte la información de la columna "Time" a formato de tiempo
        self.__df['Time'] = self.__df['Time'].apply(pd.to_datetime)
        #Debido a que las cantidades con el ícono "%" causan conflicto al momento
        #de graficar, se hace la conversión a valor plano, mientras se cambia el
        #nombre de la columna para indicar que se trata de porcentajes
        #Se crea un arreglo para guardar los nombres de las columnas
        percents = []
        #Y se toma una lista auxiliar con los valores de todas las columnas de
        #la tabla de datos
        aux_col = list(self.__df.columns)
        #Se recorren todas las columnas para revisar cuales necesitan cambios
        for i in list(self.__df.columns):
            #Si guarda valores tipo string, se procede a analizar
            if(type(self.__df[i][0]) == str):
                #Si existe el signo de "%" en el primer valor, se hacen los cambios
                if('%' in self.__df[i][0]):
                    #Se añade el nombre de la columna a los que se modificarán
                    percents.append(i)
                    #Y en la lista auxiliar de columnas se edita directamente el nombre
                    ind = aux_col.index(i)
                    aux_col[ind] = "% "+i

        #Se realizan los cambios en la tabla de datos al contenido de
        #todas las columnas que fueron seleccionadas y añadidas a percent
        self.__df[percents] = self.__df[percents].replace("%","",regex=True)
        self.__df[percents] = self.__df[percents].apply(pd.to_numeric)
        #Despué´s se actualizan los nombres de columnas directamente en la tabla
        self.__df.columns = aux_col
        return

    def get_cols(self):
        """Esta función sólo retorna los valores de las columnas, a excepción de
        la columna "Time" que es la primera"""
        return list(self.__df.columns)[1:]

    def get_Param_Data(self,start,end,param):
        """Esta función devuelve los valores de la columna o columnas solicitadas
        #más la columna "Time", para un periodo de tiempo especificado"""

        #Después se filtra la información de todas las columnas por el rango de
        #tiempo especificado
        resframe = self.__df[(self.__df['Time'] >= start) & (self.__df['Time'] <= end)]

        rpAB = 'Phase A-B Real Power (W)'
        rpBC = 'Phase B-C Real Power (W)'
        rpCA = 'Phase C-A Real Power (W)'
        rps = [rpAB,rpBC,rpCA]
        par = ""

        if(param in rps):
            if(param == rpAB):
                parframe = resframe[["Phase A Real Power (W)","Phase B Real Power (W)"]].mean(axis=1)
                resframe[rpAB] = parframe
                par = rpAB

            elif(param == rpBC):
                parframe = resframe[["Phase B Real Power (W)","Phase C Real Power (W)"]].mean(axis=1)
                resframe[rpBC] = parframe
                par = rpBC

            else:
                parframe = resframe[["Phase A Real Power (W)","Phase C Real Power (W)"]].mean(axis=1)
                resframe[rpCA] = parframe
                par = rpCA
            return resframe[["Time",par]]


        avgAB = 'Phase A-B Avg Volts'
        avgBC = 'Phase B-C Avg Volts'
        avgCA = 'Phase C-A Avg Volts'
        avgs = [avgAB,avgBC,avgCA]
        par = ""

        if(param in avgs):
            if(param == avgAB):
                parframe = resframe[["Phase A-N Avg Volts","Phase B-N Avg Volts"]].mean(axis=1)
                resframe[avgAB] = parframe
                par = avgAB

            elif(param == avgBC):
                parframe = resframe[["Phase B-N Avg Volts","Phase C-N Avg Volts"]].mean(axis=1)
                resframe[avgBC] = parframe
                par = avgBC

            else:
                parframe = resframe[["Phase A-N Avg Volts","Phase C-N Avg Volts"]].mean(axis=1)
                resframe[avgCA] = parframe
                par = avgCA
            return resframe[["Time",par]]

        else:
            #Si se pide una lista de columnas las devolverá todas, de lo contrario
            #sólo devolverá una.
            if(type(param) == list):
                parameters = ['Time']+param
            elif(type(param) == str):
                parameters = ['Time']+[param]
            else:
                print('Error, parámetro inválido')

            #Y luego, se filtra la información respecto al tiempo, respecto a las
            #columnas especificadas.
            resframe = resframe[parameters]
            #Y se devuelve la información en forma de una nueva tabla de datos
            return resframe

    def get_Coincidence_Data(self,frame,coin,tol,param):
        """Esta función devuelve los valores de tolerancia, coincidencia e intolerancia de
        la columna solicitada, más la columna "Time", para un periodo de tiempo especificado"""
        #Crea un frame a parte para cada uno de los valores buscados
        #Coincidencia
        coin_frame = pd.DataFrame(frame[param])
        #Tolerancia
        tol_frame = pd.DataFrame(frame[param])
        #E intolerancia
        intol_frame = pd.DataFrame(frame[param])

        #Primero filtra los resultados de coincidencia, pidiendo todos los valores que sean iguales al valor
        #de coincidencia.
        coin_frame.loc[coin_frame[param]!=coin,param] = None

        #Despuées filtra los valores de tolerancia, buscando todos aquellos que se encuentren iguales o menores
        #al valor de coincidencia,, y mayores a el valor de coincidencia menos el porcentaje de tolerancia
        tolerance = np.float64(((tol_frame[param].max()) - (tol_frame[param].min()))/100)*tol
        tol_frame.loc[(tol_frame[param] > coin) | (tol_frame[param] < coin-tolerance),param] = None

        #Finalmente, la columna de intolerancia filtra los valores que sean menores al valor de coincidencia, menos
        #el procentaje de tolerancia
        intol_frame.loc[(intol_frame[param] > coin-tolerance),param] = None

        #Finalmente crea la columna de tiempo, y la añade junto con las otras 3 al frame final
        param_frame = pd.DataFrame(frame["Time"])
        param_frame["coincidence"] = coin_frame[param]
        param_frame["tolerance"] = tol_frame[param]
        param_frame["intolerance"] = intol_frame[param]

        #Y se devuelve la información en forma de una nueva tabla de datos
        return param_frame

    def coincidenceGraph(self,param,sy,sm,sd,ndays,from_t,to_t,coin_val,tol,s_par,s_days):
        """Esta función crea el gráfico a partir de la tabla de datos
        perteneciente a la clase, mas un gráfico que muestre los puntos de coincidencia con un dato en particular"""
        #Primero crea dos strings, de inicio y de fin, que servirán para marcar dónde comienza y termina la gráfica
        start = "{yyyy}-{mm}-{dd} {hh}".format(yyyy=str(sy),mm=str(sm),dd=str(int(sd)),hh=str(from_t))
        end = "{yyyy}-{mm}-{dd} {hh}".format(yyyy=str(sy),mm=str(sm),dd=str(int(sd)+int(ndays)-1),hh=str(to_t))

        #Decide de qué manera organizar en una o más gráficas los datos obtenidos, generando un título por el cuál
        #se manda a llamar el gráfico, a través de la función plt.figure(titulo)
        if((s_par == 1) and (s_days == 1)):
            title = param+": "+start.split(" ")[0]
        elif(s_days == 1):
            title = start.split(" ")[0]
        else:
            title = param
        title = "Coincidencia: "+title
        plt.figure(title).suptitle(title)

        #Y crea un nuevo frame, en el cuál guardará los datos de coincidencia,tolerancia  e intolerancia
        frame = self.get_Param_Data(start,end,param)
        coincidence = self.get_Coincidence_Data(frame,coin_val,tol,param)

        #Y procede a graficar los datos, respectivamente:
        #Tiempo
        plt.plot(
            frame['Time'],
            param,
            data=frame,
            markersize=6,
            color="black",
            zorder=1,
            linewidth=1)

        #Intolerancia
        plt.scatter(
            frame['Time'],
            #"intolerance",
            np.clip(coincidence["intolerance"],1e-10,2e10),
            s=30,
            color='orange',
            alpha=None,
            zorder=10,
            edgecolors='white'
        )

        #Tolerancia
        plt.scatter(
            frame["Time"],
            #"tolerance",
            np.clip(coincidence["tolerance"],1e-10,2e10),
            s=30,
            color='green',
            alpha=None,
            zorder=20,
            edgecolors='white'
        )

        #Coincidencia
        plt.scatter(
            frame['Time'],
            #"coincidence",
            np.clip(coincidence["coincidence"],1e-10,2e10),
            s=30,
            color='red',
            zorder=30,
            alpha=1,
            edgecolors='white'
        )

        #Finalmente se añade el nombre "Tiempo" al eje x, para identificar cómo
        #avanza el tiempo en el gráfico
        plt.xlabel("Tiempo")
        plt.xticks(rotation=30)
        plt.subplots_adjust(bottom=0.2)
        plt.legend()
        return

    def poly_reg_graph(self,param,sy,sm,sd,ndays,from_t,to_t,s_par,s_days):
        """Crea una gráfica de regresión polinomial, que sirve para visualizar los datos de forma más sencilla
        y poder detectar picos en el comportamiento de los datos"""
        #Crea un arreglo con varios colores y selecciona uno al azar para la gráfica que se va a realizar
        colors = ['red','blue','green','orange','purple','lime','brown',"pink",'cyan','black']
        color = colors[randint(0,9)]

        #Crea dos strings de tiempo, una de inicio y otra de fin, para filtrar los datos que se piden por tiempo
        start = "{yyyy}-{mm}-{dd} {hh}".format(yyyy=str(sy),mm=str(sm),dd=str(int(sd)),hh=str(from_t))
        end = "{yyyy}-{mm}-{dd} {hh}".format(yyyy=str(sy),mm=str(sm),dd=str(int(sd)+int(ndays)-1),hh=str(to_t))
        data = self.get_Param_Data(start,end,param)

        #Genera un arreglo x a partir del tiempo, y un arreglo y a partir del parámetro dado, que servirán para
        #generar la función polinomial
        x = np.arange(len(data['Time'])).reshape(-1,1)
        y = np.array(data[param])
        y = np.reshape(y,len(y))

        #A través de la librería sklearn, utiliza la función polynomialFeatures para crear una nueva función polinomial,
        #Y la inserta en un modelo de regresión para poder mostrarlo en un gráfico
        poly_reg = PolynomialFeatures(degree=4)
        x_poly = poly_reg.fit_transform(x)
        model = LinearRegression(fit_intercept=True,normalize=True)
        model.fit(x_poly,y)

        #Decide si se requiere generar una sóla gráfica o gráficas separadas, y qué título ponerles para administrarlas
        #con la función plt.figure(title)
        dia = "{}".format(str(start))
        y_pred = model.predict(poly_reg.fit_transform(x))

        if((s_par == 1) and (s_days == 1)):
            title = param+": "+dia.split(" ")[0]
        elif(s_par == 1):
            title = param
        elif(s_days == 1):
            title = start.split(" ")[0]
        if((s_par == 1) or (s_days == 1)):
            title = "Polinomial: "+title
        else:
            title = "Gráfico Polinomial"
        plt.figure(title).suptitle(title)

        #Después procede a graficar los datos reales y los datos de la regresión polinomial, respectivamente
        #Datos reales
        plt.scatter(
            data["Time"],
            np.clip(y,1e-100,2e10),
            color=color,
            zorder=0,
            edgecolors='white',
            s=15,
            alpha=0.9,
            label="Real: "+param
            )

        #Regresión polinomial
        plt.plot(
            data["Time"],
            np.clip(y_pred,1e-100,2e10),
            color=color,
            zorder=10,
            label="RP: "+param
            )

        #Finalmente da nombre al eje de tiempo y lo acomoda para una visualización más cómoda
        plt.xticks(rotation=30)
        plt.xlabel("Tiempo")
        plt.subplots_adjust(bottom=0.2)
        plt.legend()
        plt.axes().set_xbound(lower=np.datetime64(start),upper=np.datetime64(end))
        return

    def show(self):
        """Dispara la función show() de la librería pyplot, para mostrar todos los gráficos que se piden a la clase"""
        plt.show()
        return

    def statistics(self,start,end,param):
        """Devuelve un diccionario con todos los datos estadísticos sobre la consulta de un parámetro respecto al tiempo"""
        parameters = self.get_Param_Data(start,end,param)
        stats = {}
        stats = parameters.describe(include=[np.number]).to_dict()
        stats[param]['mode'] = parameters[param].mode()[0]
        return stats





if __name__ == '__main__':
    #Si este script se corre como principal, se corre con el ejemplo siguiente:
    #Un nuevo objeto de la clase DataGraph
    dg = DataGraph()
    #Y se invoca el método createGraph()
    #param = ['Phase A-N Avg Volts',
    colors = ['red','blue','green','orange','purple','lime','brown',"pink",'cyan','black']
    param = 'Phase A Total PF (Lagging is +)'#Parámetro(s) a graficar
    start = '2019-05-17 00:00'#Tiempo inicial
    end = '2019-05-21 23:00'#Tiempo final
    sy = '2019'
    sm = '05'
    sd = '20'
    ndays = 2
    from_t = "00:00"
    to_t = "23:59"

    dg.poly_reg_graph(param,sy,sm,sd,ndays,from_t,to_t,0,0)

    stats = dg.statistics(start,end,param)
    for j in list(stats.keys()):
        for i in list(stats[j].keys()):
            print("{key}: {val:10.3f}".format(key=i,val=stats[j][i]))
            print("##########")

    dg.coincidenceGraph(param,sy,sm,sd,ndays,from_t,to_t,0.851,5,0,0)
                #start,end,param,coin_param,coin_val,tol
    dg.show()
    exit()
