'''Este script es el script principal, y es el encargado de brindarle una
interfaz gráfica al usuario, de manera que le sea más sencilla la creación
de gráficos al usuario a partir de parámetros establecidos.'''

"""Importación de librerías:"""
#Tkinter, para el manejo de interfaces gráficas
import tkinter as tk
#DataGraph, que es el script donde generamos los gráficos
from DataGraph import DataGraph

#Creamos una clase para manejar la ventana ventana más fácilmente
class Application(tk.Frame):
    """Nueva ventana que contendrá todos los formularios que utilizaremos"""
    def __init__(self, root):
        #Primero invoca una nueva ventana con los parámetros por defecto del programa
        self.root = root
        tk.Frame.__init__(self, root)
        #Crea un espacio para colocar el frame principal
        self.canvas = tk.Canvas(root, borderwidth=0)
        #Crea el frame principal, que contendrá todos los widgets que se ocuparán
        self.frame = tk.Frame(self.canvas)
        #Crea una barra de navegación, que permitirá recorrer la ventana
        #de arriba a abajo
        self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        #Después la asocia al espacio completo de la ventana
        self.canvas.configure(yscrollcommand=self.vsb.set)

        #Añade a la ventana principal la barra de navegación y el
        #espacio para el frame principal
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side=tk.TOP, fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="n",
                                  tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)

        #Crea también un botón que al presionarlo, devolverá un gráfico
        #con los parámetros establecidos
        self.createButton = tk.Button(root,text='      Crear Gráfico!     ', command=self.generateGraphic , bg='green', fg='white', font=('helvetica', 12, 'bold'))
        self.createButton.pack(side=tk.BOTTOM,fill='x',expand=False)

        #Crea un objeto de la clase DataGraph, que ayudará a crear el gráfico
        self.DG = DataGraph()
        #Obtiene las columnas para desplegarlas en los formularios
        self.parameters = self.DG.get_cols()
        #Y una lista de variables que contendrá todos los parámetros a graficar
        self.variables = []

        #Crea un frame para especificar los rangos de tiempo, y otros frames para
        #organizar los formularios de manera ordenada
        self.time_frame = tk.LabelFrame(self.frame,text = 'Rango de tiempo')
        self.t_alert_label = tk.Label(self.time_frame,text="Por favor, inserte una fecha válida.",fg='red')
        self.t_frameN = tk.Frame(self.time_frame)
        self.t_frameC = tk.Frame(self.time_frame)
        self.t_frameS = tk.Frame(self.time_frame)

        #Agrega variables para el rango de tiempo
        #las variables que comienzan con I representan el tiempo inicial
        self.I_day = tk.Entry(self.t_frameN,width=2)
        self.I_month = tk.Entry(self.t_frameN,width=2)
        self.I_year = tk.Entry(self.t_frameN,width=5)
        self.I_hour = tk.Entry(self.t_frameS,width=2)
        self.I_day.insert(0,'18')
        self.I_month.insert(0,'05')
        self.I_year.insert(0,'2019')
        self.I_hour.insert(0,'00')
        self.I_hour.config(state="disabled")
        self.I_min = tk.Entry(self.t_frameS,width=2)
        self.I_min.insert(0,'00')
        self.I_min.config(state="disabled")

        #Las siguientes casillas dan la opción de separar las gráficas por días y parparámetros
        self.sepDays = 0
        self.sepDaysBox = tk.Checkbutton(self.t_frameC, text='Días Separados',variable=self.sepDays, onvalue=1, offvalue=0, command=self.enable_time)
        self.sepGraphs = 0.0
        self.sepGraphsBox = tk.Checkbutton(self.t_frameC, text='Graficas Separadas',variable=self.sepGraphs, onvalue=1, offvalue=0,command=self.enable_sepgraphs)

        #Las variables que comienzan con F, representan el tiempo final
        self.F_day = tk.Entry(self.t_frameN,width=2)
        self.F_month = tk.Entry(self.t_frameS,width=2)
        self.F_year = tk.Entry(self.t_frameS,width=5)
        self.F_hour = tk.Entry(self.t_frameS,width=2)
        self.F_day.insert(0,'3')
        self.F_hour.insert(0,'23')
        self.F_hour.config(state="disabled")
        self.F_min = tk.Entry(self.t_frameS,width=2)
        self.F_min.insert(0,'59')
        self.F_min.config(state="disabled")

        ###Tolerancia y valor base###
        self.tolcoin_frame = tk.LabelFrame(self.frame,text = 'Tolerancia y Valor Base')
        self.tolcoin_sup = tk.Frame(self.tolcoin_frame)
        self.tolcoin_mid = tk.Frame(self.tolcoin_frame)
        self.tolcoin_inf = tk.Frame(self.tolcoin_frame)

        self.coinbox = tk.Entry(self.tolcoin_sup,width=5)
        tk.Label(self.tolcoin_sup,text="Valor Base:").pack(side=tk.LEFT)
        self.coinbox.pack(side=tk.LEFT)

        self.tolbox = tk.Entry(self.tolcoin_mid,width=5)
        tk.Label(self.tolcoin_mid,text="Tolerancia(%):").pack(side=tk.LEFT)
        self.tolbox.pack(side=tk.LEFT)

        self.tolcoin_sup.pack(side=tk.TOP)
        self.tolcoin_mid.pack(side=tk.TOP)



        ###Main Buttons###
        #Crea un nuevo frame para guardar todos los botones paramétricos
        self.Menu_frame = tk.LabelFrame(self.frame,text = 'Operación')

        #Y crea uno por uno los botones por su nombre, y los va añadiendo al menu

        #Power Factor Frame
        self.pfFrame = tk.Frame(self.Menu_frame)
        self.pfButton = tk.Button(self.pfFrame,text='      Factor de Potencia     ', command=lambda: self.showOptions("pf") , bg='green', fg='white', font=('helvetica', 12, 'bold'))
        self.pfButton.pack(side=tk.TOP,fill='none',expand=True)

        #Real Power Frame
        self.rpFrame = tk.Frame(self.Menu_frame)
        self.rpButton = tk.Button(self.rpFrame,text='           Potencia Real          ', command=lambda: self.showOptions("rp") , bg='green', fg='white', font=('helvetica', 12, 'bold'))
        self.rpButton.pack(side=tk.TOP,fill='none',expand=True)

        #Total Harmonic Distortion Frame
        self.thdFrame = tk.Frame(self.Menu_frame)
        self.thdButton = tk.Button(self.thdFrame,text='     Distorsión Armónica   ', command=lambda: self.showOptions("thd") , bg='green', fg='white', font=('helvetica', 12, 'bold'))
        self.thdButton.pack(side=tk.TOP,fill='none',expand=True)

        #DesV Frame
        self.desvFrame = tk.Frame(self.Menu_frame)
        self.desvButton = tk.Button(self.desvFrame,text='            Des. Voltage           ', command=lambda: self.showOptions("desv") , bg='green', fg='white', font=('helvetica', 12, 'bold'))
        self.desvButton.pack(side=tk.TOP,fill='none',expand=True)

        #DesI Factor Frame
        self.desiFrame = tk.Frame(self.Menu_frame)
        self.desiButton = tk.Button(self.desiFrame,text='           Des. Corriente         ', command=lambda: self.showOptions("desi") , bg='green', fg='white', font=('helvetica', 12, 'bold'))
        self.desiButton.pack(side=tk.TOP,fill='none',expand=True)

        #Freq Frame
        self.freqFrame = tk.Frame(self.Menu_frame)
        self.freqButton = tk.Button(self.freqFrame,text='   Frecuencia Promedio   ', command=lambda: self.showOptions("freq") , bg='green', fg='white', font=('helvetica', 12, 'bold'))
        self.freqButton.pack(side=tk.TOP,fill='none',expand=True)


        ###Option Frames###
        #Crea los frames que se mostrarán al presionar cada botón, que incluiran los parámetros individuales
        #para cada clasificación
        self.opFrames = {}
        self.ActiveOptFrame = None

        #A cada uno le asigna una opción para saber si se encuentra habilitado, el frame al que pertenece
        #los parámetros indivisuales que engloba, y un checkbox para cada parámetro

        #Power Factor Frame
        self.opFrames["pf"] = {}
        self.opFrames["pf"]["enabled"] = False
        self.opFrames["pf"]["frame"] = tk.LabelFrame(self.pfFrame,text="Opciones")
        self.opFrames["pf"]["options"] = [
            'Phase A Total PF (Lagging is +)',
            'Phase A Displacement PF (Lagging is +)',
            'Phase B Total PF (Lagging is +)',
            'Phase B Displacement PF (Lagging is +)',
            'Phase C Total PF (Lagging is +)',
            'Phase C Displacement PF (Lagging is +)',
            'Total PF (Lagging is +)']
        self.opFrames["pf"]["checkers"] = {p:{"val":tk.IntVar(),"box":0} for p in self.opFrames["pf"]["options"]}

        #Total Harmonic Distortion Frame
        self.opFrames["thd"] = {}
        self.opFrames["thd"]["enabled"] = False
        self.opFrames["thd"]["frame"] = tk.LabelFrame(self.thdFrame,text="Opciones")
        self.opFrames["thd"]["options"] = [
            'Phase A Harmonic Current (A)',
            '% Phase A-N V-Harmonic 2nd',
            '% Phase A-N V-Harmonic 3rd',
            '% Phase A-N V-Harmonic 4th',
            '% Phase A-N V-Harmonic 5th',
            '% Phase A-N V-Harmonic 6th',
            '% Phase A-N V-Harmonic 7th',
            '% Phase A-N V-Harmonic 8th',
            '% Phase A-N V-Harmonic 9th',
            '% Phase A-N V-Harmonic 10th',
            '% Phase A-N V-Harmonic 11th',
            '% Phase A-N V-Harmonic 12th',
            '% Phase A-N V-Harmonic 13th',
            'Phase A I-Harmonic 2nd (A)',
            'Phase A I-Harmonic 3rd (A)',
            'Phase A I-Harmonic 4th (A)',
            'Phase A I-Harmonic 5th (A)',
            'Phase A I-Harmonic 6th (A)',
            'Phase A I-Harmonic 7th (A)',
            'Phase A I-Harmonic 8th (A)',
            'Phase A I-Harmonic 9th (A)',
            'Phase A I-Harmonic 10th (A)',
            'Phase A I-Harmonic 11th (A)',
            'Phase A I-Harmonic 12th (A)',
            'Phase A I-Harmonic 13th (A)',
            'Phase B Harmonic Current (A)',
            '% Phase B-N V-Harmonic 2nd',
            '% Phase B-N V-Harmonic 3rd',
            '% Phase B-N V-Harmonic 4th',
            '% Phase B-N V-Harmonic 5th',
            '% Phase B-N V-Harmonic 6th',
            '% Phase B-N V-Harmonic 7th',
            '% Phase B-N V-Harmonic 8th',
            '% Phase B-N V-Harmonic 9th',
            '% Phase B-N V-Harmonic 10th',
            '% Phase B-N V-Harmonic 11th',
            '% Phase B-N V-Harmonic 12th',
            '% Phase B-N V-Harmonic 13th',
            'Phase B I-Harmonic 2nd (A)',
            'Phase B I-Harmonic 3rd (A)',
            'Phase B I-Harmonic 4th (A)',
            'Phase B I-Harmonic 5th (A)',
            'Phase B I-Harmonic 6th (A)',
            'Phase B I-Harmonic 7th (A)',
            'Phase B I-Harmonic 8th (A)',
            'Phase B I-Harmonic 9th (A)',
            'Phase B I-Harmonic 10th (A)',
            'Phase B I-Harmonic 11th (A)',
            'Phase B I-Harmonic 12th (A)',
            'Phase B I-Harmonic 13th (A)',
            'Phase C Harmonic Current (A)',
            '% Phase C-N V-Harmonic 2nd',
            '% Phase C-N V-Harmonic 3rd',
            '% Phase C-N V-Harmonic 4th',
            '% Phase C-N V-Harmonic 5th',
            '% Phase C-N V-Harmonic 6th',
            '% Phase C-N V-Harmonic 7th',
            '% Phase C-N V-Harmonic 8th',
            '% Phase C-N V-Harmonic 9th',
            '% Phase C-N V-Harmonic 10th',
            '% Phase C-N V-Harmonic 11th',
            '% Phase C-N V-Harmonic 12th',
            '% Phase C-N V-Harmonic 13th',
            'Phase C I-Harmonic 2nd (A)',
            'Phase C I-Harmonic 3rd (A)',
            'Phase C I-Harmonic 4th (A)',
            'Phase C I-Harmonic 5th (A)',
            'Phase C I-Harmonic 6th (A)',
            'Phase C I-Harmonic 7th (A)',
            'Phase C I-Harmonic 8th (A)',
            'Phase C I-Harmonic 9th (A)',
            'Phase C I-Harmonic 10th (A)',
            'Phase C I-Harmonic 11th (A)',
            'Phase C I-Harmonic 12th (A)',
            'Phase C I-Harmonic 13th (A)']
        self.opFrames["thd"]["checkers"] = {p:{"val":tk.IntVar(),"box":0} for p in self.opFrames["thd"]["options"]}

        #Power Factor Frame
        self.opFrames["desv"] = {}
        self.opFrames["desv"]["enabled"] = False
        self.opFrames["desv"]["frame"] = tk.LabelFrame(self.desvFrame,text="Opciones")
        self.opFrames["desv"]["options"] = [
            'Phase A-B Avg Volts',
            'Phase B-C Avg Volts',
            'Phase C-A Avg Volts',
            'N-G Avg Volts']
        self.opFrames["desv"]["checkers"] = {p:{"val":tk.IntVar(),"box":0} for p in self.opFrames["desv"]["options"]}

        #Real Power Frame
        self.opFrames["rp"] = {}
        self.opFrames["rp"]["enabled"] = False
        self.opFrames["rp"]["frame"] = tk.LabelFrame(self.rpFrame,text="Opciones")
        self.opFrames["rp"]["options"] = [
            'Phase A-B Real Power (W)',
            'Phase B-C Real Power (W)',
            'Phase C-A Real Power (W)',
            'Total Real Power (W)']
        self.opFrames["rp"]["checkers"] = {p:{"val":tk.IntVar(),"box":0} for p in self.opFrames["rp"]["options"]}

        #DesI Frame
        self.opFrames["desi"] = {}
        self.opFrames["desi"]["enabled"] = False
        self.opFrames["desi"]["frame"] = tk.LabelFrame(self.desiFrame,text="Opciones")
        self.opFrames["desi"]["options"] = [
            'Phase A Avg Amps',
            'Phase B Avg Amps',
            'Phase C Avg Amps',
            'Neutral Avg Amps']
        self.opFrames["desi"]["checkers"] = {p:{"val":tk.IntVar(),"box":0} for p in self.opFrames["desi"]["options"]}

        #Freq Frame
        self.opFrames["freq"] = {}
        self.opFrames["freq"]["enabled"] = False
        self.opFrames["freq"]["frame"] = tk.LabelFrame(self.freqFrame,text="Opciones")
        self.opFrames["freq"]["options"] = ['Avg Frequency (Hz)']
        self.opFrames["freq"]["checkers"] = {p:{"val":tk.IntVar(),"box":0} for p in self.opFrames["freq"]["options"]}

        #Finalmente, se ejecuta el método populate(), para terminar de asignar
        #cada formulario al frame que le corresponde
        self.populate()
        return

    def enable_time(self):
        """Activa o desactiva los parámetros de tiempo, respectivo a la
        checkbox de 'días separados' """
        if(self.sepDays == 1):
            self.I_hour.delete(0,tk.END)
            self.I_min.delete(0,tk.END)
            self.F_hour.delete(0,tk.END)
            self.F_min.delete(0,tk.END)
            self.I_hour.insert(0,'00')
            self.I_min.insert(0,'00')
            self.F_hour.insert(0,'23')
            self.F_min.insert(0,'59')
            self.I_hour.config(state="disabled")
            self.I_min.config(state="disabled")
            self.F_hour.config(state="disabled")
            self.F_min.config(state="disabled")
            self.sepDays = 0
        else:
            self.I_hour.config(state="normal")
            self.I_min.config(state="normal")
            self.F_hour.config(state="normal")
            self.F_min.config(state="normal")
            self.sepDays = 1
        return

    def enable_sepgraphs(self):
        """Actualiza el valor de la casilla de gráficas separadas"""
        if(self.sepGraphs == 1):
            self.sepGraphs = 0
        else:
            self.sepGraphs = 1
        return

    def showOptions(self,par):
        """Muestra las opciones paramétricas para cada botón de clasificación"""
        #Si se encuentra un frame de opción paramétrica activo, lo desactiva
        if(self.ActiveOptFrame != None):
            self.ActiveOptFrame["frame"].pack_forget()

        #Si el frame seleccionado está desactivado, lo activa y coloca todos los elementos que le pertenecen
        if(self.opFrames[par]["enabled"] == False):
            for p in self.opFrames[par]["options"]:
                self.opFrames[par]["checkers"][p]["box"] = tk.Checkbutton(self.opFrames[par]["frame"], text=p,variable=self.opFrames[par]["checkers"][p]["val"], onvalue=1, offvalue=0)
                self.opFrames[par]["checkers"][p]["box"].pack(side="top")
            self.opFrames[par]["enabled"] = True
        #Si el frame que se desea activar, es distinto al que está activo, lo habilita en pantalla y lo convierte
        #En el nuevo frame activo
        #De lo contrario, sólo lo deshabilita y deja vacío el frame activo
        if(self.ActiveOptFrame != self.opFrames[par]):
            self.opFrames[par]["frame"].pack(side="top")
            self.ActiveOptFrame = self.opFrames[par]
        else:
            self.ActiveOptFrame["frame"].pack_forget()
            self.ActiveOptFrame = None
        return

    def populate(self):
        """Esta función asigna, en orden,cada formulario a su frame correspondiente"""
        #Primero se coloca el frame del tiempo a la ventana, de manera que sea
        #el primero
        self.time_frame.pack(side=tk.TOP,fill='x',expand=True)

        #Después va colocando los formularios para las variables de tiempo en
        #sus frames correspondientes.

        #Primero los iniciales
        tk.Label(self.t_frameN,text="A partir del: D:").pack(side="left")
        self.I_day.pack(side="left")
        tk.Label(self.t_frameN,text="/M:").pack(side="left")
        self.I_month.pack(side="left")
        tk.Label(self.t_frameN,text="/A:").pack(side="left")
        self.I_year.pack(side="left")
        tk.Label(self.t_frameN,text="Para un rango de:").pack(side="left")
        self.F_day.pack(side="left")
        tk.Label(self.t_frameN,text="días.").pack(side="left")
        #self.I_min.pack(side="left")

        #Después los finales
        tk.Label(self.t_frameS,text="De las:").pack(side="left")
        self.I_hour.pack(side="left")
        tk.Label(self.t_frameS,text=":").pack(side="left")
        self.I_min.pack(side="left")
        tk.Label(self.t_frameS,text=" A las:").pack(side="left")
        self.F_hour.pack(side="left")
        tk.Label(self.t_frameS,text=":").pack(side="left")
        self.F_min.pack(side="left")

        #Coloca los ckeckbox de días y gráficos separados
        self.sepDaysBox.pack(side="left")
        self.sepGraphsBox.pack(side="right")

        #Coloca cada frame, superior, central e inferior al frame de tiempo
        self.t_frameN.pack(side="top")
        self.t_frameC.pack(side="top")
        self.t_frameS.pack(side='bottom')

        #Coloca el frame de tolerancia y valor base
        self.tolcoin_frame.pack(side="top",fill="both",expand=True)

        #Coloca también cada botón de clasificación en el frame de menu
        self.pfFrame.pack(side="top")
        self.thdFrame.pack(side="top")
        self.desvFrame.pack(side="top")
        self.desiFrame.pack(side="top")
        self.rpFrame.pack(side="top")
        self.freqFrame.pack(side="top")

        #Y finalmente coloca el frame de menu en pantalla
        self.Menu_frame.pack(side=tk.TOP,fill="both",expand=True)
        return

    def onFrameConfigure(self, event):
        '''Reinicia la región de navegación para alinearse con el frame principal'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def statsWindow(self,params,sy,sm,sd,ndays,from_t,to_t):
        """Genera la ventana con las estadísticas para un parámetro con un rango de tiempo específico"""
        #Acomoda la presentación de la ventana
        statsWindow = tk.Toplevel(self.root)
        statsFrame = []
        for i in range(len(params)):
            #Marca los límites de tiempo para mostrar en la ventana
            start = "{yyyy}-{mm}-{dd} {hh}".format(yyyy=str(sy),mm=str(sm),dd=str(sd),hh=str(from_t))
            end = "{yyyy}-{mm}-{dd} {hh}".format(yyyy=str(sy),mm=str(sm),dd=str(int(sd)+int(ndays)),hh=str(to_t))
            #Obtiene los datos a partir de la función statistics() perteneciente a DataGraph
            stats = self.DG.statistics(start,end,params[i])[params[i]]
            #Acomoda la presentación de la ventana
            statsFrame.append(tk.Frame(statsWindow,borderwidth=2,relief="groove"))
            #E inserta todos los datos a través de labels
            tk.Label(statsFrame[i],text=" ").pack(side="top")
            tk.Label(statsFrame[i],text="Estadísticas: {}".format(params[i])).pack(side="top")
            tk.Label(statsFrame[i],text="Del {} al {}".format(start,end)).pack(side="top")
            tk.Label(statsFrame[i],text=" ").pack(side="top")
            tk.Label(statsFrame[i],text="Total de datos analizados: {:.3f}".format(float(stats["count"]))).pack(side="top")
            tk.Label(statsFrame[i],text="Media: {:.3f}".format(float(stats["mean"]))).pack(side="top")
            tk.Label(statsFrame[i],text="Moda: {:.3f}".format(float(stats["mode"]))).pack(side="top")
            tk.Label(statsFrame[i],text="Mediana: {:.3f}".format(float(stats["50%"]))).pack(side="top")
            tk.Label(statsFrame[i],text="Desviación Estándar: {:.3f}".format(float(stats["std"]))).pack(side="top")
            tk.Label(statsFrame[i],text="Valor Mínimo: {:.3f}".format(float(stats["min"]))).pack(side="top")
            tk.Label(statsFrame[i],text="Valor Máximo: {:.3f}".format(float(stats["max"]))).pack(side="top")
            tk.Label(statsFrame[i],text="25%: {:.3f}".format(float(stats["25%"]))).pack(side="top")
            tk.Label(statsFrame[i],text="75%: {:.3f}".format(float(stats["75%"]))).pack(side="top")
            statsFrame[i].grid(row=i//3,column=i%3,sticky="nsew")
        return

    def tableWindow(self,params,sy,sm,sd,ndays,from_t,to_t,Base):
        twindow = tk.Toplevel(self.root)
        tableFrame = tk.Frame(twindow)
        tableFrame.grid_rowconfigure(1,weight=1)
        tableFrame.grid_columnconfigure(0,weight=1)
        if("power" in params[0].lower()):
            m1 = "watts"
            m2 = "Potencia"
        else:
            m1 = "volts"
            m2 = "Tensión"
        tk.Label(tableFrame,text="\nTabla de cumplimiento de norma\nBajo valor base de: {} {}\n".format(str(Base),m1),borderwidth=2,relief="flat").grid(row=0,column=0,columnspan=7,sticky="nsew")
        tk.Label(tableFrame,text=m2+"\n",borderwidth=2,relief="sunken").grid(row=1,column=0,sticky="nsew")
        tk.Label(tableFrame,text="Máximo\n",borderwidth=2,relief="raised").grid(row=1,column=1,sticky="nsew")
        tk.Label(tableFrame,text="Promedio\n",borderwidth=2,relief="sunken").grid(row=1,column=2,sticky="nsew")
        tk.Label(tableFrame,text="Mínimo\n",borderwidth=2,relief="raised").grid(row=1,column=3,sticky="nsew")
        tk.Label(tableFrame,text="% de variación\nMáximo",borderwidth=2,relief="sunken").grid(row=1,column=4,sticky="nsew")
        tk.Label(tableFrame,text="% de variación\nMínimo",borderwidth=2,relief="raised").grid(row=1,column=5,sticky="nsew")
        tk.Label(tableFrame,text="Bajo Norma\n",borderwidth=2,relief="sunken").grid(row=1,column=6,sticky="nsew")

        start = "{yyyy}-{mm}-{dd} {hh}".format(yyyy=str(sy),mm=str(sm),dd=str(sd),hh=str(from_t))
        end = "{yyyy}-{mm}-{dd} {hh}".format(yyyy=str(sy),mm=str(sm),dd=str(int(sd)+int(ndays)),hh=str(to_t))
        offset = 2

        for i in range(len(params)):
            paramdata = self.DG.get_Param_Data(start,end,params[i])
            voltaje = params[i]
            tk.Label(tableFrame,text=voltaje,borderwidth=2,relief="groove").grid(row=offset+i,column=0,sticky="nsew")
            maximo = paramdata[voltaje].max()
            tk.Label(tableFrame,text="{:.3f}".format(maximo),borderwidth=2,relief="groove").grid(row=offset+i,column=1,sticky="nsew")
            mean = paramdata[voltaje].mean()
            tk.Label(tableFrame,text="{:.3f}".format(mean),borderwidth=2,relief="groove").grid(row=offset+i,column=2,sticky="nsew")
            minimo = paramdata[voltaje].min()
            tk.Label(tableFrame,text="{:.3f}".format(minimo),borderwidth=2,relief="groove").grid(row=offset+i,column=3,sticky="nsew")
            varmax = (maximo - Base) / Base
            tk.Label(tableFrame,text="{:.3f}".format(varmax),borderwidth=2,relief="groove").grid(row=offset+i,column=4,sticky="nsew")
            varmin = (minimo - Base) / Base
            tk.Label(tableFrame,text="{:.3f}".format(varmin),borderwidth=2,relief="groove").grid(row=offset+i,column=5,sticky="nsew")
            base_val = float(Base)
            tol = float(self.tolbox.get())
            if((varmax < base_val + ((base_val/100)*tol)) and (varmin > base_val - ((base_val/100)*tol))):
                cumple = "Si Cumple"
            else:
                cumple = "No Cumple"
            tk.Label(tableFrame,text=cumple,borderwidth=2,relief="groove").grid(row=offset+i,column=6,sticky="nsew")

        tableFrame.pack()
        return

    def generateGraphic(self):
        '''Método que genera la gráfica a partir de las variables establecidas'''
        #Pasa los valores de las variables de tiempo de la clase a variables locales
        #del método para su fácil manejo
        fy = self.I_year.get()
        fm = self.I_month.get()
        fd = self.I_day.get()
        fh = self.I_hour.get()
        fmin = self.I_min.get()

        ty = self.F_year.get()
        tm = self.F_month.get()
        td = self.F_day.get()
        th = self.F_hour.get()
        tmin = self.F_min.get()

        #Intenta obtener los valores de tolerancia y valor base de sus respectivas casillas
        #Si falla, los deja como valores nulos
        try:
            coin_val = float(self.coinbox.get())
            tol = float(self.tolbox.get())
        except(ValueError):
            coin_val = None
            tol = None

        #Se crea una lista para guardar los valores de los parámetros a graficar
        params = []
        #Se validan los parámetros que se van a guardar, a partir de la frame activa, revisando
        #si la checkbox que tienen asignada está marcada, y añadiendolos a params.
        for chk in self.ActiveOptFrame["checkers"].keys():
            if(self.ActiveOptFrame["checkers"][chk]["val"].get() == 1):
                params.append(chk)

        #Crea los dos strings que se van a pasar como tiempos inicial y final
        fdate = '{}-{}-{} {}:{}'.format(fy,fm,fd,fh,fmin)
        fdate = fdate.split(" ")
        tdate = '{}-{}-{} {}:{}'.format(ty,tm,td,th,tmin)
        tdate = tdate.split(" ")

        #Crea una lista para revisar los valores en las variables de tiempo, que
        #sean válidos para pasar como parámetros a DataGraph()
        checks = [fy,fm,fd,fh,fmin,td,th,tmin]

        #Si se ingresa un valor de tiempo inválido, el programa pide una fecha válida
        if('' in checks):
            if((fy == '') or (fm == '') or (fd == '')):
                self.t_alert_label["text"] = 'Por favor, inserte una fecha inicial válida.'
            else:
                self.t_alert_label["text"] = 'Por favor, inserte una fecha final válida.'
            #Si los datos no son válidos, activa la alerta y termina la función
            self.t_alert_label.pack(side=tk.BOTTOM)
            return
        else:
            #De lo contrario, desactiva la alerta, en caso de haber estado activada
            self.t_alert_label.pack_forget()
            #Y procede a mandar a llamar el gráfico con los parámetros de tiempo
            #y datos establecidos.
            if((coin_val != None) and (tol != None)):
                self.tableWindow(params,fy,fm,fd,td,fdate[1],tdate[1],coin_val)
            self.statsWindow(params,fy,fm,str(int(fd)),"0",fdate[1],tdate[1])

            for param in params:
                #Si se requieren días separados, se generan los gráficos día por día, de lo contrario
                #se genera un sólo gráfico para todo el rango de tiempo dado
                if(self.sepDays == 0):
                    #Y si el valor de valor base o tolerancia es inválido, no genera el gráfico de tolerancia
                    if((coin_val != None) and (tol != None)):
                        self.DG.coincidenceGraph(param,fy,fm,fd,td,fdate[1],tdate[1],coin_val,tol,self.sepGraphs,self.sepDays)
                    self.DG.poly_reg_graph(param,fy,fm,fd,td,fdate[1],tdate[1],self.sepGraphs,self.sepDays)
                else:
                    for i in range(int(td)):
                        if((coin_val != None) and (tol != None)):
                            self.DG.coincidenceGraph(param,fy,fm,str(int(fd)+i),"1",fdate[1],tdate[1],coin_val,tol,self.sepGraphs,self.sepDays)
                        self.DG.poly_reg_graph(param,fy,fm,str(int(fd)+i),"1",fdate[1],tdate[1],self.sepGraphs,self.sepDays)
        self.DG.show()
        return





if __name__ == "__main__":
    #Crea una nueva ventana con la función tk perteneciente a TKinter
    root=tk.Tk()
    #Cambia el título de la ventana
    root.title("PowerScape: Comparación de Datos")
    #Y añade un nuevo frame principal a la ventana
    Application(root).pack(side="top", fill="both", expand=True)
    #Y pone la ventana a correr.
    root.mainloop()
