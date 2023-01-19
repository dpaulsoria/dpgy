import numpy as np

SubSaturado = ["API", "Sw", "Pb", "Gg", "Tf", "Cf", "Cw", "Bw", "Co"]
Saturado = SubSaturado.copy()
CapaAgua = ["deltaP", "ang"]
CapaGas = ["Rsi", "Pb", "Co", "Gg", "API", "Tf"]


def hide(dpg, list):
  for value in list:
    dpg.hide_item(value)
    
def show(dpg, list):
  for value in list:
    dpg.show_item(value)

def hideSubSaturado(dpg):
  hide(dpg, SubSaturado)

def hideSaturado(dpg):
  hide(dpg, Saturado)

def hideCapaAgua(dpg):
  hide(dpg, CapaAgua)
    
def hideCapaGas(dpg):
  hide(dpg, CapaGas)
    
def showSubSaturado(dpg):
  # hideSaturado(dpg)
  hideCapaAgua(dpg)
  hideCapaGas(dpg)
  show(dpg, SubSaturado)

def showSaturado(dpg):
  # hideSubSaturado(dpg)
  hideCapaAgua(dpg)
  hideCapaGas(dpg)
  show(dpg, Saturado)
  
def showCapaAgua(dpg):
  hideSubSaturado(dpg)
  # hideSaturado(dpg)
  hideCapaGas(dpg)
  show(dpg, CapaAgua)
  
def showCapaGas(dpg):
  hideSubSaturado(dpg)
  # hideSaturado(dpg)
  hideCapaAgua(dpg)
  show(dpg, CapaGas)
  
def getValues(dpg, list):
  x = dict()
  for value in list:
    x[value] = np.float64(dpg.get_value(value))
  return x

def getValuesSubSaturado(dpg):
  return getValues(dpg, SubSaturado)
  
def getValuesSaturado(dpg):
  return getValues(dpg, Saturado)

def getValuesCapaGas(dpg):
  return getValues(dpg, CapaGas)
  
def getValuesCapaAgua(dpg):
  return getValues(dpg, CapaAgua)
  