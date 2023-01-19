import numpy as np
import matplotlib.pyplot as plt

def createSearchFiles(dpg, open, close, height, width):
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
    
def genButton(dpg, callback):
  dpg.add_button(label="Buscar archivo", callback=callback, tag="buscar_archivo_button", show=False)
  
def genCombobox(dpg, items, callback):
  dpg.add_combo(
    label="Tipo de reservorio",
    items=items,
    tag="type",
    callback=callback,
    show=True
  )
  
def genRadioButton(dpg, items, callback, default_value="Standing"):
  dpg.add_radio_button(
    items= items,
    horizontal=True,
    callback=callback,
    default_value=default_value,
    tag="corr",
    show=True
  )
  
  
def genTable(dpg, df, width, height):
  rows = df.shape[0]
  columns = df.shape[1]
  
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
      for column in df.columns:
        dpg.add_table_column(label=column.capitalize(), width_fixed=True)
      for row in range(0, rows):
        with dpg.table_row():
          for column in df.columns:
            dpg.add_text(df[column][row])  
            


def doGraphic(df, ylabel, xlabel, jumpFirst):
  x = np.array(df[xlabel].tolist(), dtype=np.float64)
  y = np.array(df[ylabel].tolist(), dtype=np.float64)
  if (jumpFirst):
    x = x[1:]
    y = y[1:]
  coefficients = np.polyfit(x, y, 1)
  plt.scatter(x, y)
  plt.plot(x, np.polyval(coefficients, x), 'r-')
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.title(f'{xlabel} vs {ylabel}: O: {coefficients[1]} M: {coefficients[0]}')
  plt.show(block=True)