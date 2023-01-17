from datetime import datetime as dt
import dearpygui.dearpygui as dpg
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from util.volumetrico_sub_saturado import *
from util.empuje_agua import *
from util.empuje_gas import *

width = 780
height = 620
currentCorr = 'Standing'
show_table = False

def saveExcel(df, currentCorr):
  name = f'output/fileCreatedAt_{dt.now().strftime("%d_%m_%Y_%Hh%Mm%Ss")}_{currentCorr}.xlsx'
  print("Saving...", name)
  df.to_excel(name, index=False)

def doGraphic(df):
  x = np.array(df['Eo+Efw'].tolist(), dtype=np.float64)
  y = np.array(df['F'].tolist(), dtype=np.float64)
  coefficients = np.polyfit(x, y, 1)
  plt.scatter(x, y)
  plt.plot(x, np.polyval(coefficients, x), 'r-')
  plt.xlabel('Eo+Efw')
  plt.ylabel('F')
  plt.title('Eo+Efw vs F')
  plt.show(block=True)


def makeByType(data, type, currentCorr):
  
  if ("Volumétricos sub saturados" == type):
    api =  np.float64(dpg.get_value("API"))
    sw =  np.float64(dpg.get_value("SW"))
    pb =  np.float64(dpg.get_value("Pb"))
    gg =  np.float64(dpg.get_value("Gg"))
    Tf =  np.float64(dpg.get_value("Tf"))
    Bw = np.float64(dpg.get_value("Bw"))
    Cf = np.float64(dpg.get_value("Cf"))
    Cw = np.float64(dpg.get_value("Cw"))
    gp =  np.float64((141.5/(api + 131.5)))
    values = [api, sw, pb, gg, gp, Bw, Cf, Cw]
    tmpP = data["P"].tolist()
    corrResultBo = []
    corrResultRs = []
    for p in range(0, len(tmpP)):
      rs, bo = doCorr(currentCorr, Tf, p, values)
      rs = "{:7.6f}".format(rs)
      bo = "{:7.6f}".format(bo)
      corrResultBo.append(bo)
      corrResultRs.append(rs)
    boArray = np.array(corrResultBo)
    rsArray = np.array(corrResultRs)
    df = pd.DataFrame({'Bo': boArray, 'Rs': rsArray})
    # print(df)
    toWorkWith = pd.concat([data, df], axis=1)
    # print(toWorkWith)
    resultDf = do(toWorkWith, values)
    create_table(resultDf)
    doGraphic(resultDf)
    saveExcel(resultDf, currentCorr)
    
  elif ("Reservorios con empuje de capa de agua" == type):
    dpg.show_item("buscar_archivo_button")
    wi = calcular(data)
  elif ("Reservorios con empuje de capa de gas" == type):
    pass

def create_table(data):
  rows = data.shape[0]
  columns = data.shape[1]
  
  with dpg.window(
    label="Tabla", 
    width=width,
    height=height-height*0.3
  ):
    with dpg.table(
      header_row=True, 
      policy=dpg.mvTable_SizingFixedFit, 
      row_background=True, 
      reorderable=True,
      resizable=True,
      no_host_extendX=True,
      hideable=True,
      borders_innerV=True,
      delay_search=True,
      borders_outerV=True,
      borders_innerH=True,
      borders_outerH=True,
      width=width+width*0.2,
      height=height-height*0.4,
    ):
      for column in data.columns:
        dpg.add_table_column(label=column.capitalize(), width_fixed=True)
      for row in range(0, rows):
        with dpg.table_row():
          for column in data.columns:
            dpg.add_text(data[column][row])  

# Functions
def open(sender, app_data):
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
  tmp = dpg.get_value("type")
  if ("Volumétricos sub saturados" == tmp):
    dpg.show_item("API")
    dpg.show_item("SW")
    dpg.show_item("Pb")
    dpg.show_item("Gg")
    dpg.show_item("Tf")
    dpg.show_item("Cf")
    dpg.show_item("Cw")
    dpg.show_item("Bw")
    dpg.show_item("buscar_archivo_button")
    dpg.show_item("corr")
  elif ("Reservorios con empuje de capa de agua" == tmp):
    dpg.show_item("buscar_archivo_button")
  elif ("Reservorios con empuje de capa de gas" == tmp):
    pass

def generateOpenDialog():
  with dpg.file_dialog(
    directory_selector=False, 
    show=True, 
    callback=open,
    cancel_callback=close, 
    id="file_dialog_id", 
    width=width-width*0.3, height=height-height*0.3
  ):
      dpg.add_file_extension(".xlsx", color=(81, 191, 89, 255), custom_text="[xlsx]")
      dpg.add_file_extension(".csv", color=(0, 255, 0, 255), custom_text="[csv]")

with dpg.window(
  label='Main Window', 
  no_title_bar=False,
  no_move=False, 
  width=width,
  height=height,
  no_resize=False,
):
  dpg.add_combo(
    label="Tipo de reservorio",
    items=[
      "Volumétricos sub saturados",
      "Reservorios con empuje de capa de gas",
      "Reservorios con empuje de capa de agua",
    ], tag="type",
    callback=combo_callback
  )
  dpg.add_radio_button(
    items=['Standing', 'Beggs'],
    horizontal=True,
    callback=radio_callback,
    default_value=currentCorr,
    tag="corr"
  )
  dpg.add_input_float(default_value=40.0, label="Gravedad API", source="float_value", tag="API", show=False, format="%.1f")
  dpg.add_input_float(default_value=0.24 ,label="Saturación de agua", source="float_value", tag="SW", show=False, format="%.3f")
  dpg.add_input_float(default_value=1500.0,label="Presión de burbujeo", source="float_value", tag="Pb", show=False, format="%.1f")
  dpg.add_input_float(default_value=0.85, label="Gravedad específica del gas", source="float_value", tag="Gg", show=False, format="%.3f")
  dpg.add_input_float(default_value=135.0, label="Temperatura en F", source="float_value", tag="Tf", show=False, format="%.3f")
  dpg.add_input_float(default_value=0.00000362, label="Cf", source="float_value", tag="Cf", show=False, format="%.9f")
  dpg.add_input_float(default_value=0.00000362, label="Cw", source="float_value", tag="Cw", show=False, format="%.9f")
  dpg.add_input_float(default_value=1.0, label="Bw", source="float_value", tag="Bw", show=False, format="%.3f")
  dpg.add_button(label="Buscar archivo", callback=generateOpenDialog, tag="buscar_archivo_button", show=False)
  
  api = dpg.get_value("API")
  sw = dpg.get_value("SW")
  pb = dpg.get_value("Pb")
  gg = dpg.get_value("Gg")
  gp = (141.5/(api + 131.5))
  
  
def run():
  dpg.setup_dearpygui()
  dpg.show_viewport()  
  dpg.start_dearpygui()
  dpg.destroy_context()
  
if __name__ == '__main__':
  run()