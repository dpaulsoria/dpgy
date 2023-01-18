import math as m

def F(n, Eo, m, Eg, We):
  return n * Eo + We

# Intrusión del agua acumulada
# Cw es la compresibilidad del agua del acuifero
# Cf es la compresibilidad de la roca del acuifero
# Wi es el volumen inicial del acuifero
# deltaP es Pi - P
# pi es la presión inicial del yacimiento y p la presión actual
def We(Cw, Cf, Wi, deltaP):
  return (Cw + Cf) * Wi * deltaP

def f(ang):
  return ang/360




def calcular(data, deltaP, ang):
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

  # Wc = K * deltaP
  we = We(a_lpc_agua, a_lpc_formacion, wi, deltaP)
  
  # F/Eo = deltaP / Eo
  # N es el intercepto
  # K es la endiente
  N = 1
  K = 1
  Eo = 1
  
  FEo = N + K * (deltaP / Eo)
  return wi