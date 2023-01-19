import numpy as np
import pandas as pd

def F(N, Eo, m, Eg):
  return N * (Eo + m * Eg)

def Eg(Boi, Bg, Bgi):
  return Boi * (Bg/Bgi - 1)


def getRp(df):
  Gp = np.float64(df['Gp'].tolist())
  Np = np.float64(df['Np'].tolist())
  RpList = [0]
  for row in range(1, len(Gp)):
    Rp = Gp[row] / Np[row]
    RpList.append("{:7.6f}".format(Rp))
  RpArray = np.array(RpList) 
  RpDf = pd.DataFrame(RpArray, columns=["Rp"])
  print("Actual:")
  print(df)
  print("RpDf:")
  print(RpDf)
  return pd.concat([df, RpDf], axis=1)

def getF(df, Rsi):
  Np = np.float64(df['Np'].tolist())
  Bt = np.float64(df['Bt'].tolist())
  Rp = np.float64(df['Rp'].tolist())
  Bg = np.float64(df['Bg'].tolist())
  FList = []
  for row in range(0, len(Np)):
    F = Np[row] * (Bt[row] * (Rp[row] - Rsi) * Bg[row])
    FList.append("{:7.6f}".format(F))
  FArray = np.array(FList)
  FDf = pd.DataFrame(FArray, columns=["F"])
  print("Actual:")
  print(df)
  print("FDf:")
  print(FDf)
  return pd.concat([df, FDf], axis=1)

def getEo(df):
  Bt = np.float64(df['Bt'].tolist())
  Bti = Bt[0]
  EoList = []
  for row in range(0, len(Bt)):
    Eo = Bt[row] - Bti
    EoList.append("{:7.6f}".format(Eo))
  EoArray = np.array(EoList)
  EoDf = pd.DataFrame(EoArray, columns=["Eo"])
  print("Actual:")
  print(df)
  print("EoDf:")
  print(EoDf)
  return pd.concat([df, EoDf], axis=1)

def getEg(df):
  Bt = np.float64(df['Bt'].tolist())
  Bti = Bt[0]
  Bg = np.float64(df['Bg'].tolist())
  Bgi = Bg[0]
  EgList = []
  for row in range(0, len(Bt)):
    Eg = Bti * (Bg[row]/Bgi - 1)
    EgList.append("{:7.6f}".format(Eg))
  EgArray = np.array(EgList)
  EgDf = pd.DataFrame(EgArray, columns=["Eg"])
  print("Actual:")
  print(df)
  print("EgDf:")
  print(EgDf)
  return pd.concat([df, EgDf], axis=1)

def getFEo(df):
  F = np.float64(df['F'].tolist())
  Eo = np.float64(df['Eo'].tolist())
  FEoList = [0]
  for row in range(1, len(F)):
    FEo = F[row] / Eo[row]
    FEoList.append("{:7.6f}".format(FEo))
  FEoArray = np.array(FEoList)
  FEoDf = pd.DataFrame(FEoArray, columns=["F/Eo"])
  print("Actual:")
  print(df)
  print("FEoDf:")
  print(FEoDf)
  return pd.concat([df, FEoDf], axis=1)

def getEgEo(df):
  Eg = np.float64(df['Eg'].tolist())
  Eo = np.float64(df['Eo'].tolist())
  EgEoList = [0]
  for row in range(1, len(Eg)):
    EgEo = Eg[row] / Eo[row]
    EgEoList.append("{:7.6f}".format(EgEo))
  EgEoArray = np.array(EgEoList)
  EgEoDf = pd.DataFrame(EgEoArray, columns=["Eg/Eo"])
  print("Actual:")
  print(df)
  print("EgEoDf:")
  print(EgEoDf)
  return pd.concat([df, EgEoDf], axis=1)

def doCapaGas(dpg, data):
  df = getRp(data)
  df = getF(df, np.float64(dpg.get_value("Rsi")))
  df = getEo(df)
  df = getEg(df)
  df = getFEo(df)
  df = getEgEo(df)
  return df