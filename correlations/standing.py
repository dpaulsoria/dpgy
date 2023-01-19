from util.temperature import farenheit_to_rankine

def getRs(values, p):
  x = (0.0125 * values['API'] - (0.00091 * (farenheit_to_rankine(values['Tf']) - 460)))
  return values['Gg'] * ((values[p]/18.2 + 1.4) * (10 ** x)) ** 1.2048


def getBo1(values, rs):
  return 0.9759 + 0.000120 * ((rs * ((values['Gg']/values['Gp']) ** 0.5) + 1.25 * (farenheit_to_rankine(values['Tf']) - 460)) ** 1.2)

def getBo(values, bob, p):
  return bob ** (values['Co'] * (values['Pb'] - p))