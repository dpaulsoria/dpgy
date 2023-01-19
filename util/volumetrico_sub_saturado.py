import numpy as np
import pandas as pd
import correlations.standing as standing
import correlations.beggs as beggs


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

def doSubSaturado(df, values):
  rows = df.shape[0]
  columns = df.shape[1]
  boi = np.float64(df['Bo'][0])
  P =  np.float64(df['P'][0])
  tmp.append([0, 0, 0, 0, 0])
  
  bw = values['Bw']
  sw = values['Sw']
  cf = values['Cf']
  cw = values['Cw']
  
  for row in range(1, rows):
    P1 = np.float64(df['P'][row])
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

def doCorr(currentCorr, values, p, type):
  if (currentCorr == "Standing"):
    if (values['Pb'] < p):
      rs = standing.getRs(values, 'Pb')
    else: 
      rs = standing.getRs(values, 'P')
    if (type == "SubSaturado"):
      bob = standing.getBo1(values, rs)
      bo = standing.getBo(values, bob, p)
    elif (type == "Saturado"):
      bo = standing.getBo1(values, rs)
    elif (type == "capaGas"):
      bo = standing.getBo1(values, rs)
    return rs, bo
  elif (currentCorr == "Beggs"):
    rs = beggs.getRs(values, p)
    if (type == "SubSaturado"):
      bob = beggs.getBo1(values, rs)
      bo = beggs.getBo(values, bob, p)
    elif (type == "Saturado"):
      bo = beggs.getBo1(values, rs)
    elif (type == "capaGas"):
      bo = beggs.getBo1(values, rs)
    return rs, bo
  
  
def useCorr(df, values, currentCorr, type):
  api = np.float64(values['API'])
  values['Gp'] =  np.float64((141.5/(api + 131.5)))
  
  PArray = np.array(df["P"].tolist(), dtype=np.float64)
  corrResultBo = []
  corrResultRs = []
  for row in range(0, len(PArray)):
    rs, bo = doCorr(currentCorr, values, PArray[row], type)
    rs = "{:7.7f}".format(rs)
    bo = "{:7.7f}".format(bo)
    corrResultBo.append(bo)
    corrResultRs.append(rs)
  boArray = np.array(corrResultBo)
  rsArray = np.array(corrResultRs)
  tmp = pd.DataFrame({'Bo': boArray, 'Rs': rsArray})
  return pd.concat([df, tmp], axis=1)