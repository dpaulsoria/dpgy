from datetime import datetime as dt
import dearpygui.dearpygui as dpg
import pandas as pd
import numpy as np

from util.volumetrico_sub_saturado import *
from util.volumetrico_saturado import *
from util.empuje_agua import *
from util.empuje_gas import *
from util.utils import *

from components.elements import *
from components.subsaturado_inputs import *
from components.capaagua_inputs import *
from components.capagas_inputs import *

width = 780
height = 620
currentCorr = 'Standing'

def saveExcel(df, currentCorr, type):
  name = f'output/result_{dt.now().strftime("%d_%m_%Y_%Hh%Mm%Ss")}_{currentCorr}_{type}.xlsx'
  print("Saving...", name)
  df.to_excel(name, index=False)



def makeByType(data, type, currentCorr):
  
  if ("Volumétricos sub saturados" == type):
    subSaturado = getValuesSubSaturado(dpg)
    df = useCorr(data, subSaturado, currentCorr, "SubSaturado")
    resultDf = doSubSaturado(df, subSaturado)
    genTable(dpg, resultDf, width, height)
    doGraphic(resultDf, 'F', 'Eo+Efw', True)
    saveExcel(resultDf, currentCorr, "subSaturado")
  
  elif ("Volumétricos saturados" == type):
    saturado = getValuesSaturado(dpg)
    df = doSaturado(data)
    tmp = useCorr(df, saturado, currentCorr, "Saturado")
    genTable(dpg, tmp, width, height)
    doGraphic(tmp, "F/Eo", "DeltaP/Eo", True)
    saveExcel(tmp, currentCorr, "saturado")
    
  elif ("Reservorios con empuje de capa de agua" == type):
    deltaP = dpg.get_value("deltaP")
    ang = dpg.get_value("ang")
    wi = calcular(data, deltaP, ang)
  elif ("Reservorios con empuje de capa de gas (N y m desconocidos)" == type):
    capaGas = getValuesCapaGas(dpg)
    df = doCapaGas(dpg, data)
    tmp = useCorr(df, capaGas, currentCorr, "capaGas")
    genTable(dpg, tmp, width, height)
    doGraphic(df, "F/Eo", "Eg/Eo", True)
    saveExcel(df, currentCorr, "capaGas")

# Functions
def openFile(sender, app_data):
  currentCorr = dpg.get_value("corr")
  type = dpg.get_value("type")
  print("Ok was clicked")
  print("Sender: ", sender)
  print("App Data: ", app_data['file_path_name'])
  data = pd.read_excel(app_data['file_path_name'])

  makeByType(data, type, currentCorr)

def close(sender, app_data):
  print("Cancel was clicked")
  print("Sender: ", sender)
  print("App Data: ", app_data)
  
def radio_callback(sender, app_data):
  print("Radio was clicked")
  print("Sender: ", sender)
  print("App Data: ", app_data)

# GUI 

dpg.create_context()
dpg.create_viewport(
  title='YACIMIENTOS',
  width=width,
  height=height,
  resizable=True,
)

def radio_callback():
  pass

def combo_callback():
  reservorioType = dpg.get_value("type")
  if ("Volumétricos sub saturados" == reservorioType):
    showSubSaturado(dpg)
    
  elif ("Volumétricos saturados" == reservorioType):
    showSaturado(dpg)
    
  elif ("Reservorios con empuje de capa de agua" == reservorioType):
    showCapaAgua(dpg)
    
  elif ("Reservorios con empuje de capa de gas (N y m desconocidos)" == reservorioType):
    showCapaGas(dpg)

  dpg.show_item("buscar_archivo_button")


def generateOpenDialog():
  createSearchFiles(dpg, openFile, close, height, width)

with dpg.window(
  label='Main Window', 
  no_title_bar=False,
  no_move=False, 
  width=width,
  height=height,
  no_resize=False,
):
  
  ComboboxItems = [
    "Volumétricos sub saturados",
    "Volumétricos saturados",
    "Reservorios con empuje de capa de agua",
    "Reservorios con empuje de capa de gas (N y m desconocidos)",
  ]
  RadioButtonsItems = ['Standing', 'Beggs']
  
  genCombobox(dpg, ComboboxItems, combo_callback)
  genRadioButton(dpg, RadioButtonsItems, radio_callback)
  
  genSubSaturadosInputs(dpg)
  genCapaAguaInputs(dpg)
  genCapaGasInputs(dpg)
  
  genButton(dpg, generateOpenDialog)


  
  
def run():
  dpg.setup_dearpygui()
  dpg.show_viewport()  
  dpg.start_dearpygui()
  dpg.destroy_context()
  
if __name__ == '__main__':
  run()