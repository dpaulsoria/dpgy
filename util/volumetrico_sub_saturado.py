import numpy as np
import pandas as pd
import correlations.standing as standing
import correlations.beggs as beggs


tmp = []

def F(np, bo, wp, bw):
  return "{:8.10f}".format(np * bo + wp * bw)
  
def Eo(bo, boi):
  return "{:8.10f}".format(bo - boi)

def Efw(boi, deltaP, sw, cw, cf):
  return "{:8.10f}".format(boi * ((cw * sw + cf)/(1-sw)) * deltaP)

def doSubSaturado(df, values):
  rows = df.shape[0]
  columns = df.shape[1]
  boi = np.float64(df['Bo'][0])
  Pi =  np.float64(df['P'][0])
  tmp.append([0, 0, 0, 0, 0])
  
  bw = values['Bw']
  sw = values['Sw']
  cf = values['Cf']
  cw = values['Cw']
  for row in range(1, rows):   
    P = np.float64(df['P'][row])
    Bo = np.float64(df['Bo'][row])
    Np = np.float64(df['Np'][row])
    Wp = np.float64(df['Wp'][row])
    F1 = F(Np, Bo, Wp, bw)
    deltaP = Pi - P
    Eo1 = Eo(Bo, boi)
    Efw1 = Efw(boi, deltaP, sw, cw, cf)
    EoEfw = "{:8.10f}".format( np.float64(Eo1) +  np.float64(Efw1))
    tmp.append([F1, Eo1, deltaP, Efw1, EoEfw])
  newDf= pd.DataFrame(tmp, columns=['F', 'Eo', 'deltaP', 'Efw', 'Eo+Efw'])
  tmpDf = pd.concat([df, newDf], axis=1)
  return tmpDf

def doCorr(currentCorr, values, p, type):
  print("Init doCorr")
  print(currentCorr)
  if (currentCorr == "Standing"):
    if (values['Pb'] < p):
      rs = standing.getRs(values, 'Pb')
    else: 
      rs = standing.getRs(values, 'P')
    if (type == "SubSaturado"):
      bo = standing.getBo1(values, rs)
      bo = standing.getBo(values, bo, p)
    elif (type == "Saturado"):
      bo = standing.getBo1(values, rs)
    elif (type == "capaGas"):
      bo = standing.getBo1(values, rs)
    return rs, bo
  elif (currentCorr == "Beggs"):
    if (values['Pb'] < p):
      rs = standing.getRs(values, 'Pb')
    else: 
      rs = standing.getRs(values, 'P')
    if (type == "SubSaturado"):
      bo = beggs.getBo1(values, rs)
      bo = beggs.getBo(values, bo, p)
    elif (type == "Saturado"):
      bo = beggs.getBo1(values, rs)
    elif (type == "capaGas"):
      bo = beggs.getBo1(values, rs)
    return rs, bo
  

def useCorr(df, values, currentCorr, type):
  print("Init useCorr")
  api = np.float64(values['API'])
  values['Gp'] =  np.float64((141.5/(api + 131.5)))
  print('Gp: ', values['Gp'])
  print('API: ', api)
  PArray = np.array(df["P"].tolist(), dtype=np.float64)
  print("PArray: ")
  print(PArray)
  corrResultBo = []
  corrResultRs = []
  for row in range(0, len(PArray)):
    rs, bo = doCorr(currentCorr, values, PArray[row], type)
    rs = "{:8.10f}".format(rs)
    bo = "{:8.10f}".format(bo)
    corrResultBo.append(bo)
    corrResultRs.append(rs)
  boArray = np.array(corrResultBo)
  rsArray = np.array(corrResultRs)
  print("boArray: ")
  print(boArray)
  print("rsArray: ")
  print(rsArray)
  tmp = pd.DataFrame({'Bo': boArray, 'Rs': rsArray})
  return pd.concat([df, tmp], axis=1)