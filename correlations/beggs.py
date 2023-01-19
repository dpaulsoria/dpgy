from util.temperature import farenheit_to_rankine
import math

def getC_Rs(api):
  x = dict()
  if api <= 30: 
    x['c1'] = 0.0362
    x['c2'] = 1.0937
    x['c3'] = 25.7240
  else: 
    x['c1'] = 0.0178
    x['c2'] = 1.1870
    x['c3'] = 23.931
  return x

def getRs(values, p):
  c = getC_Rs(values['API'])
  return (c['c1'] * (values['Gp'] * (values[p] ** c['c2'])) * (math.e ** (c['c3'] * (values['Gp'] / (farenheit_to_rankine(values['Tf']) - 460)))))
  # return ((c['c1'] * (values['Gp'] * (p ** c['c2']))) ** (c['c3'] * (values['API']/farenheit_to_rankine(values['Tf']))))


def getC_Bo(api):
  x = dict()
  if api <= 30: 
    x['c1'] = 0.0004677
    x['c2'] = 0.00001751
    x['c3'] = -0.00000001811
  else: 
    x['c1'] = 0.0004670
    x['c2'] = 0.00001100
    x['c3'] = 0.000000001337
  return x

def getBo1(values, rs):
  c = getC_Bo(values['API'])
  return 1.0 + c['c1'] * rs + c['c2'] * (farenheit_to_rankine(values['Tf']) - 460) * (values['Gp']/values['Gg']) + c['c3'] * rs * (farenheit_to_rankine(values['Tf']) - 460) * (values['Gp']/values['Gg'])
  # return 1.0 + c['c1'] * rs + (farenheit_to_rankine(values['Tf']) - 520) * (values['API']/values['Gg']) * (c['c2'] + c['c3'] * rs)

def getBo(values, bob, p):
  return bob * (math.e) ** (values['Co'] * (values['Pb'] - p))