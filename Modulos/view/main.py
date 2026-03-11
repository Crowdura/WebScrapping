#Librerias
from pathlib import Path
#Tkinder
import tkinter
import customtkinter as custoM
from tkinter import filedialog
#Modulos
from Modulos.logic.WebScrapping import WebScrapping
from Modulos.logic.LlmOllama import ModelOllama
from Modulos.Func.valOllama import getListLLM as getLisL

class ScreenPrin(custoM.CTk):
    def __init__(self, fg_color=None, **kwargs):
        super().__init__(fg_color=fg_color, **kwargs)
        self._contrView()
        #self.state('zoomed')
        self._set_appearance_mode('dark')
        self.title('Vista busqueda web Scrapping')
        self.geometry("500x300")
        
    def __call__(self, *args, **kwds):
        return super().__call__(*args, **kwds)
    
    def _contrView(self):
        lti_olLLm = getLisL()
        lti_modelos = [m["name"] for m in lti_olLLm["models"]]
        self.ruta = Path.cwd()
        #Frame reach
        lo_frame = custoM.CTkFrame(master=self)
        lo_frame.grid( row=0, column=0 ,sticky=tkinter.NSEW)
        lo_frame.configure(width=0, height=0)

        lo_labelTitle = custoM.CTkLabel(master=lo_frame, text='WebScrapping', bg_color="#1e1e1e")
        lo_labelTitle.grid(row=0, column=0,ipady=2,padx=15,pady=15,sticky=custoM.EW, columnspan=5)
        lo_labelTitle.grid_columnconfigure(0, weight=1)
        lo_labelTitle.grid_rowconfigure(0, weight=1)

        lo_labelReach = custoM.CTkLabel(master=lo_frame, text='Busqueda' , bg_color='#0812A5' )
        lo_labelReach.grid(row=2, column=0,sticky=custoM.EW)
        lo_labelReach.grid_columnconfigure(0, weight=1)
        lo_labelReach.grid_rowconfigure(0, weight=1)

        self._lo_reachUrl = custoM.CTkEntry(master=lo_frame, bg_color='#0812A5')
        self._lo_reachUrl.grid(row=2, column=1, sticky=custoM.EW,pady=5, padx=65)
        self._lo_reachUrl.grid_columnconfigure(0, weight=1)
        self._lo_reachUrl.grid_rowconfigure(0, weight=2)
        self._lo_reachUrl.insert(0, 'https://listado.mercadolibre.com.co/')
        
        lo_labelParam = custoM.CTkLabel(master=lo_frame, text='Parametro de busqueda' , bg_color='#0812A5' )
        lo_labelParam.grid(row=3, column=0, ipady=1, ipadx=5,sticky=custoM.EW)
        lo_labelParam.grid_columnconfigure(0, weight=1)
        lo_labelParam.grid_rowconfigure(0, weight=1)

        self._lo_reachParam = custoM.CTkEntry(master=lo_frame, bg_color='#0812A5')
        self._lo_reachParam.grid(row=3,column=1,sticky=custoM.EW, pady=5, padx=65)
        self._lo_reachParam.grid_columnconfigure(0, weight=1)
        self._lo_reachParam.grid_rowconfigure(0, weight=1)

        lo_labelCantidPag = custoM.CTkLabel(master=lo_frame, text='cantidad de pagina de lectura', bg_color='#0812A5')
        lo_labelCantidPag.grid(row=4, column=0, ipady=1, ipadx=5,sticky=custoM.EW)
        lo_labelCantidPag.grid_columnconfigure(0,weight=1)
        lo_labelCantidPag.grid_rowconfigure(0, weight=2)

        self._lo_cantPag = custoM.CTkEntry(master=lo_frame, bg_color='#0812A5')
        self._lo_cantPag.grid(row=4,column=1,sticky=custoM.EW, pady=5, padx=65)
        self._lo_cantPag.grid_columnconfigure(0, weight=1)
        self._lo_cantPag.grid_rowconfigure(0, weight=2)

        lo_labelSelMod = custoM.CTkLabel(master=lo_frame, text='Seleccionar Modelo' , bg_color='#0812A5' )
        lo_labelSelMod.grid(row=5, column=0, ipady=1, ipadx=5,sticky=custoM.EW)
        lo_labelSelMod.grid_columnconfigure(0, weight=1)
        lo_labelSelMod.grid_rowconfigure(0, weight=1)

        self._lo_mainDelModel = custoM.CTkOptionMenu(master=lo_frame, bg_color='#0812A5', values=lti_modelos)
        self._lo_mainDelModel.grid(row=5,column=1,sticky=custoM.EW, pady=5, padx=65)
        self._lo_mainDelModel.grid_columnconfigure(0, weight=1)
        self._lo_mainDelModel.grid_rowconfigure(0, weight=2)
        #Frame dir
        lo_frameSelDir = custoM.CTkFrame(master=self)
        lo_frameSelDir.grid(row=1, column=0, sticky=tkinter.NSEW)

        lo_buttonReach = custoM.CTkButton( master=lo_frameSelDir, text='Realizar busqueda',command= self.hadlderEvent)
        lo_buttonReach.grid(row=0, column=0, ipady=2,padx=15,pady=15)
        lo_buttonSelectDir = custoM.CTkButton(master=lo_frameSelDir, text='Seleccionar Carpeta', command= self.hadlderEventDil)
        lo_buttonSelectDir.grid(row=0, column=1, ipady=2,padx=15,pady=15)
        lo_buttonSelectDirBas = custoM.CTkButton(master=lo_frameSelDir, text='Carpeta Base', command= self.hadlderEventDilBas)
        lo_buttonSelectDirBas.grid(row=0, column=2, ipady=2,padx=15,pady=15)
        return
    def hadlderEventDil(self):
        lo_carpeta = filedialog.askdirectory(title="Selecciona carpeta destino")
        print(lo_carpeta)
        if lo_carpeta:
            self.ruta = Path(lo_carpeta)
        return
    def hadlderEventDilBas(self):
        self.ruta = Path.cwd()
        return
    def hadlderEvent(self):
        lv_cantVal = int(self._lo_cantPag.get()) if self._lo_cantPag.get() != '' else 0
        lo_scrapping = WebScrapping(self._lo_reachUrl.get(), self._lo_reachParam.get(), lv_cantVal)
        lo_df = lo_scrapping.getDf()
        ruta_base = Path(self.ruta) / "logs"

        # Crear la carpeta si no existe
        ruta_base.mkdir(parents=True, exist_ok=True)
        lv_rutWrit = str(ruta_base) + "\\resultados.csv"
        lo_df.write_csv(lv_rutWrit)
        lv_context = f"Contexto español. Validar cuales no se tenga rating. Resume los resultados obtenidos. Validar cual tiene mejor precio calidad. Cuando se haga una referencia hacer uso de la lista datosLinkComp para la obtención del link: {lo_df.head(4).to_dicts()}"
        lo_ollam = ModelOllama(url="http://localhost:11434/api/generate", context=lv_context, typeCon='request', modelOllama=self._lo_mainDelModel.get())
        lo_ollam.wrArchi(dir=self.ruta)
        return
    
