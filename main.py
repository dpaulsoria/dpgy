from datetime import datetime as dt
import dearpygui.dearpygui as dpg
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

width = 780
height = 620
currentCorr = 'Standing'
show_table = False

sw = 0.24
cw = 3.62e-6
cf = 4.95e-6
bw = 1
pb = 1500

def F(type, np, bo, wp, bw):
  if (type == "Volumétricos sub saturados"):
    return "{:7.6f}".format(np * bo + wp * bw)
  return ""
  
def Eo(bo, boi):
  return "{:7.6f}".format(bo - boi)

def Efw(boi, deltaP):
  tmp = (cw * sw + cf)/(1-sw)
  return "{:7.6f}".format(boi * tmp * deltaP)

def farenheit_to_rankine(temp):
  return temp + 459.67

def rankine_to_farenheit(temp):
  return temp - 459.67

tmp = []
api = 0
sw = 0
pb = 0
gg = 0
Tf = 0
gp = (141.5/(api + 131.5))
rs = 0


def doCorr(currentCorr1, T, p):
  api =  np.float64(dpg.get_value("API"))
  sw =  np.float64(dpg.get_value("SW"))
  pb =  np.float64(dpg.get_value("Pb"))
  gg =  np.float64(dpg.get_value("Gg"))
  gp =  np.float64((141.5/(api + 131.5)))
  currentCorr = currentCorr1
  if (currentCorr == "Standing"):
    x = (0.125 * api - (0.0009 * (farenheit_to_rankine(T) - 460)))
    rs = gg * ((p/18.2 + 1.4) * (10 ** x)) ** 1.2048
    bo = 0.0759 + 0.000120 * ((rs * ((gg/gp) ** 0.5) + 1.25 * (farenheit_to_rankine(T) - 460)) ** 1.2)
    # print("Standing:", f"{rs}, {bo}")
    return rs, bo
  else:
    if api <= 30: 
      c1 = 0.0362
      c2 = 1.0937
      c3 = 25.7240
    else: 
      c1 = 0.0178
      c2 = 1.1870
      c3 = 23.931
    rs = (c1 * gg * (p ** c2)) ** (c3 * (api/farenheit_to_rankine(T)))
    if api <= 30: 
      c1 = 4.677e-4
      c2 = 1.751e-5
      c3 = -1.811e-8
    else: 
      c1 = 4.670e-4
      c2 = 1.100e-5
      c3 = 1.337e-9
    bo = 1.0 + c1 * rs + (farenheit_to_rankine(T) - 520) * (api/gg) * (c2 + c3 * rs)
    # print("Beggs:", f"{rs}, {bo}")
    return rs, bo

# def getTheDate():
#   return dt.now().strftime("%d_%m_%Y_%Hh%Mm%Ss")

def saveExcel(df, currentCorr):
  name = f'output/fileCreatedAt_{dt.now().strftime("%d_%m_%Y_%Hh%Mm%Ss")}_{currentCorr}.xlsx'
  print("Saving...", name)
  df.to_excel(name, index=False)


def strToFloat(list):
  # print(list, "Original array")
  tmp = np.array([])
  for i in list:
    np.append(tmp, float(i))
  # print(tmp, 'Final array')
  return tmp

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
  # plt.draw()
  pass

def do(df, type):
  rows = df.shape[0]
  columns = df.shape[1]
  boi = np.float64(df['Bo'][0])
  P =  np.float64(df['P'][0])
  tmp.append([0, 0, 0, 0, 0])
  for row in range(1, rows):
    P1 = np.float64(df['P'][row])
    X = np.float64(df['X'][row])
    Bo = np.float64(df['Bo'][row])
    Np = np.float64(df['Np'][row])
    Wp = np.float64(df['Wp'][row])
    F1 = F(type, Np, Bo, Wp, bw)
    Eo1 = Eo(Bo, boi)
    deltaP = P - P1
    Efw1 = Efw(boi, deltaP)
    EoEfw = "{:7.6f}".format( np.float64(Eo1) +  np.float64(Efw1))
    tmp.append([F1, Eo1, deltaP, Efw1, EoEfw])
  newDf= pd.DataFrame(tmp, columns=['F', 'Eo', 'deltaP', 'Efw', 'Eo+Efw'])
  tmpDf = pd.concat([df, newDf], axis=1)
  create_table(tmpDf)
  doGraphic(tmpDf)
  saveExcel(tmpDf, currentCorr)


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
  api = dpg.get_value("API")
  sw = dpg.get_value("SW")
  pb = dpg.get_value("Pb")
  gg = dpg.get_value("Gg")
  gp = (141.5/(api + 131.5))
  currentCorr = dpg.get_value("corr")
  type = dpg.get_value("type")
  print("Ok was clicked")
  print("Sender: ", sender)
  print("App Data: ", app_data['file_path_name'])
  # data = pd.read_csv(app_data['file_path_name'])
  # print(data)
  # create_table(data)
  data = pd.read_excel(app_data['file_path_name'])
  # print(data)
  # do(data)
  tmpP = data["P"].tolist()
  corrResultBo = []
  corrResultRs = []
  for p in range(0, len(tmpP)):
    rs, bo = doCorr(currentCorr, Tf, p)
    rs = "{:7.6f}".format(rs)
    bo = "{:7.6f}".format(bo)
    corrResultBo.append(bo)
    corrResultRs.append(rs)
  boArray = np.array(corrResultBo)
  rsArray = np.array(corrResultRs)
  df = pd.DataFrame({'Bo': boArray, 'Rs': rsArray})
  # print(df)
  toWorkWith = pd.concat([data, df], axis=1)
  print(toWorkWith)
  do(toWorkWith, type)
  # do(data)

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

def generateOpenDialog():
  with dpg.file_dialog(
    directory_selector=False, 
    show=True, 
    callback=open,
    cancel_callback=close, 
    id="file_dialog_id", 
    width=width-width*0.3, height=height-height*0.3):
      dpg.add_file_extension(".xlsx", color=(81, 191, 89, 255), custom_text="[xlsx]")
      dpg.add_file_extension(".csv", color=(0, 255, 0, 255), custom_text="[csv]")
      # dpg.add_file_extension(".*")
      # dpg.add_file_extension("", color=(150, 255, 150, 255))
      # dpg.add_file_extension("Source files (*.cpp *.h *.hpp){.cpp,.h,.hpp}", color=(0, 255, 255, 255))
      # dpg.add_file_extension(".h", color=(255, 0, 255, 255), custom_text="[header]")

with dpg.window(
  label='Main Window', 
  no_title_bar=False,
  no_move=False, 
  width=width,
  height=height,
  no_resize=False,
):
  dpg.add_radio_button(items=['Standing', 'Beggs'], horizontal=True,callback=radio_callback, default_value=currentCorr, tag="corr")
  dpg.add_input_float(label="Gravedad API", source="float_value", tag="API")
  dpg.add_input_float(label="Saturación de agua", source="float_value", tag="SW")
  dpg.add_input_float(label="Presión de burbujeo", source="float_value", tag="Pb")
  dpg.add_input_float(label="Gravedad específica del gas", source="float_value", tag="Gg")
  dpg.add_input_float(label="Temperatura en F", source="float_value", tag="Tf")
  dpg.add_combo(
    label="Tipo de reservorio",
    items=[
      "Volumétricos sub saturados",
      "Volumétricos saturados",
      "Reservorios con empuje de capa de gas",
      "Reservorios con empuje de capa de agua",
      "Reservorios con empuje de capa de gas y agua",
      "Presión promedio del reservorio",
    ], tag="type")
  dpg.add_button(label="Buscar archivo", callback=generateOpenDialog)
  
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