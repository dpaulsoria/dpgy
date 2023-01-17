import math as m


def calcular(data):
  yacimiento = data['Yacimiento']
  acuifero  = data['Acuifero']
  
  y_r = yacimiento[0]
  y_porosidad = yacimiento[1]
  y_lpc_formacion = yacimiento[2]
  y_lpc_agua = yacimiento[3]
  y_espesor = yacimiento[4]
  
  a_r = acuifero[0]
  a_porosidad = acuifero[1]
  a_lpc_formacion = acuifero[2]
  a_lpc_agua = acuifero[3]
  a_espesor = acuifero[4]
  
  wi = (m.pi * (a_r ** 2 - y_r ** 2) * a_espesor * a_porosidad)/5.615
  # we = (y_lpc_formacion + a_lpc_formacion) * (wi * (10 ** 6)) * (80/360) * 200
  k = 1
  deltaP = 1
  we = k * deltaP
  N = 1
  K = 1
  Eo = 1
  FEo = N + K * (deltaP / Eo)
  return wi