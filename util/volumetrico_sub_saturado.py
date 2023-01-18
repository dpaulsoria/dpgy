import numpy as np
import pandas as pd
from datetime import datetime as dt


tmp = []

def farenheit_to_rankine(temp):
  return temp + 459.67

def rankine_to_farenheit(temp):
  return temp - 459.67

def F(np, bo, wp, bw):
  return "{:7.6f}".format(np * bo + wp * bw)
  
def Eo(bo, boi):
  return "{:7.6f}".format(bo - boi)

def Efw(boi, deltaP, sw, cw, cf):
  tmp = (cw * sw + cf)/(1-sw)
  return "{:7.6f}".format(boi * tmp * deltaP)

def do(df, values):
  rows = df.shape[0]
  columns = df.shape[1]
  boi = np.float64(df['Bo'][0])
  P =  np.float64(df['P'][0])
  tmp.append([0, 0, 0, 0, 0])
  
  bw = values[5]
  sw = values[1]
  cf = values[6]
  cw = values[7]
  
  for row in range(1, rows):
    P1 = np.float64(df['P'][row])
    X = np.float64(df['X'][row])
    Bo = np.float64(df['Bo'][row])
    Np = np.float64(df['Np'][row])
    Wp = np.float64(df['Wp'][row])
    F1 = F(Np, Bo, Wp, bw)
    Eo1 = Eo(Bo, boi)
    deltaP = P - P1
    Efw1 = Efw(boi, deltaP, sw, cw, cf)
    EoEfw = "{:7.6f}".format( np.float64(Eo1) +  np.float64(Efw1))
    tmp.append([F1, Eo1, deltaP, Efw1, EoEfw])
  newDf= pd.DataFrame(tmp, columns=['F', 'Eo', 'deltaP', 'Efw', 'Eo+Efw'])
  tmpDf = pd.concat([df, newDf], axis=1)
  return tmpDf

def doCorr(currentCorr1, T, p, values):
  api = values[0]
  sw =  values[1]
  pb =  values[2]
  gg =  values[3]
  gp =  values[4]
  currentCorr = currentCorr1
  
  if (currentCorr == "Standing"):
    x = (0.0125 * api - (0.00091 * (farenheit_to_rankine(T) - 460)))
    rs = gg * ((p/18.2 + 1.4) * (10 ** x)) ** 1.2048
    bo = 0.9759 + 0.000120 * ((rs * ((gg/gp) ** 0.5) + 1.25 * (farenheit_to_rankine(T) - 460)) ** 1.2)
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