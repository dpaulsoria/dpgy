import dearpygui.dearpygui as dpg
import pandas as pd

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
  return "{:7.6f}".format(np * bo + wp * bw)
  
def Eo(bo, boi):
  return "{:7.6f}".format(bo - boi)

def Efw(boi, deltaP):
  tmp = (cw * sw + cf)/(1-sw)
  return "{:7.6f}".format(boi * tmp * deltaP)

def FtoR(n):
  return n+460

tmp = []

def do(df):
  rows = df.shape[0]
  columns = df.shape[1]
  boi = df['Bo'][0]
  P = df['P'][0]
  tmp.append([0, 0, 0, 0, 0])
  for row in range(1, rows):
    P1 = df['P'][row]
    X = df['X'][row]
    Bo = df['Bo'][row]
    Np = df['Np'][row]
    Wp = df['Wp'][row]
    F1 = F(currentCorr, Np, Bo, Wp, bw)
    Eo1 = Eo(Bo, boi)
    deltaP = P - P1
    Efw1 = Efw(boi, deltaP)
    EoEfw = float(Eo1) + float(Efw1)
    tmp.append([F1, Eo1, deltaP, Efw1, "{:7.6f}".format(EoEfw)])
  newDf= pd.DataFrame(tmp, columns=['F', 'Eo', 'deltaP', 'Efw', 'Eo+Efw'])
  tmpDf = pd.concat([df, newDf], axis=1)
  create_table(tmpDf)


def create_table(data):
  rows = data.shape[0]
  columns = data.shape[1]
  
  with dpg.window(label="Tabla"):
    with dpg.table(
      header_row=True, 
      policy=dpg.mvTable_SizingFixedFit, 
      row_background=True, 
      reorderable=True,
      resizable=True,
      no_host_extendX=False,
      hideable=True,
      borders_innerV=True,
      delay_search=True,
      borders_outerV=True,
      borders_innerH=True,
      borders_outerH=True,
      width=width-width*0.2,
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
  print("Ok was clicked")
  print("Sender: ", sender)
  print("App Data: ", app_data['file_path_name'])
  # data = pd.read_csv(app_data['file_path_name'])
  # print(data)
  # create_table(data)
  data = pd.read_excel(app_data['file_path_name'])
  print(data)
  do(data)

def close(sender, app_data):
  print("Cancel was clicked")
  print("Sender: ", sender)
  print("App Data: ", app_data)
  
def radio_callback(sender, app_data):
  print("Radio was clicked")
  print("Sender: ", sender)
  print("App Data: ", app_data)
  
dpg.create_context()
dpg.create_viewport(
  title='YACIMIENTOS',
  width=width,
  height=height,
  resizable=True,
)

with dpg.file_dialog(
  directory_selector=False, 
  show=False, 
  callback=open,
  cancel_callback=close, 
  id="file_dialog_id", 
  width=width-width*0.3, height=height-height*0.3):
    dpg.add_file_extension(".csv", color=(0, 255, 0, 255), custom_text="[csv]")
    dpg.add_file_extension(".xlsx", color=(81, 191, 89, 255), custom_text="[xlsx]")
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
  dpg.add_button(label="Buscar archivo", callback=lambda: dpg.show_item("file_dialog_id"))
  dpg.add_radio_button(items=['Standing', 'Beggs'], horizontal=True,callback=radio_callback, default_value=currentCorr)

  
  
def run():
  dpg.setup_dearpygui()
  dpg.show_viewport()  
  dpg.start_dearpygui()
  dpg.destroy_context()
  
if __name__ == '__main__':
  run()