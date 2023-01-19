import numpy as np

SubSaturado = ["corr", "API", "Sw", "Pb", "Gg", "Tf", "Cf", "Cw", "Bw", "Co"]
Saturado = SubSaturado.copy()
CapaAgua = ["deltaP", "ang"]
CapaGas = ["Rsi"]


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
  show(dpg, SubSaturado)
  hideSaturado(dpg)
  hideCapaAgua(dpg)
  hideCapaGas(dpg)

def showSaturado(dpg):
  show(dpg, Saturado)
  hideSubSaturado(dpg)
  hideCapaAgua(dpg)
  hideCapaGas(dpg)
  
def showCapaAgua(dpg):
  show(dpg, CapaAgua)
  hideSubSaturado(dpg)
  hideSaturado(dpg)
  hideCapaGas(dpg)
  
def showCapaGas(dpg):
  show(dpg, CapaGas)
  hideSubSaturado(dpg)
  hideSaturado(dpg)
  hideCapaAgua(dpg)
  
def getValues(dpg, list):
  x = dict()
  for value in list:
    x[value] = np.float64(dpg.get_value(value))
  return x

def getValuesSubSaturado(dpg):
  tmp = SubSaturado.copy()
  tmp.remove('corr')
  return getValues(dpg, tmp)
  
def getValuesSaturado(dpg):
  tmp = Saturado.copy()
  tmp.remove('corr')
  return getValues(dpg, tmp)
  