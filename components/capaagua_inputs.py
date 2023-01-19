def genCapaAguaInputs(dpg):
  dpg.add_input_float(default_value=200.0, label="Caída de presión", source="float_value", tag="deltaP", show=False, format="%.3f")
  dpg.add_input_float(default_value=80.0, label="Ángulo de intrusión", source="float_value", tag="ang", show=False, format="%.3f")