import numpy as np
import pandas as pd

def getN(df, col):
    F = np.float64(df['F'].tolist())
    Eo = np.float64(df['Eo'].tolist())
    NList = [0]
    print(col)
    for row in range(1, len(F)):
        print(F[row], Eo[row])
        N = F[row] / Eo[row]
        print(N)
        NList.append("{:7.8f}".format(N))

    NArray = np.array(NList)
    NDf = pd.DataFrame(NArray, columns=[col])
    return pd.concat([df, NDf], axis=1)

def getDeltaPEo(df):
    P = np.float64(df['P'].tolist())
    Eo = np.float64(df['Eo'].tolist())
    Pi = P[0]
    tmpList = [0]
    print("DeltaPEo")
    for row in range(1, len(P)):
        print(Pi, P[row], Eo[row])
        tmp = (Pi - P[row]) / Eo[row]
        print(tmp)
        tmpList.append("{:7.8f}".format(tmp))

    tmpArray = np.array(tmpList)
    tmpDf = pd.DataFrame(tmpArray, columns=["DeltaP/Eo"])
    return pd.concat([df, tmpDf], axis=1)

def getFEo(df):
    return getN(df, "F/Eo")

def doSaturado(df):
    data = getN(df, "N")
    data = getDeltaPEo(data)
    data = getFEo(data)
    return data