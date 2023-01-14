import dearpygui.dearpygui as dpg
import pandas as pd

width = 720
height = 540
currentCorr = 'Standing'

# Functions
def open(sender, app_data):
  print("Ok was clicked")
  print("Sender: ", sender)
  print("App Data: ", app_data)

def close(sender, app_data):
  print("Cancel was clicked")
  print("Sender: ", sender)
  print("App Data: ", app_data)
  
def radio_callback(sender, app_data):
  print("Radio was clicked")
  print("Sender: ", sender)
  print("App Data: ", app_data)
  
dpg.create_context()
dpg.create_viewport(
  title='Custom Title',
  width=width,
  height=height
)

dpg.add_file_dialog(
  show=False,
  callback=open,
  cancel_callback=close,
  tag="file_dialog_id",
  width=width-width*0.2,
  height=height-height*0.2,
  
)

with dpg.window(
  label='Main Window', 
  no_title_bar=True,
  no_move=True, width=width,
  height=height,
  no_resize=True,
):


  dpg.add_button(label="Search file", callback=lambda: dpg.show_item("file_dialog_id"))
  dpg.add_radio_button(items=['Standing', 'Beggs'], horizontal=True,callback=radio_callback, default_value=currentCorr)
  
  # dpg.add_text("hello")
  # dpg.add_radio_button(items=['one', 'two', 'three'], horizontal=True)
  
def run():
  dpg.setup_dearpygui()
  dpg.show_viewport()
  
  
  dpg.start_dearpygui()
  dpg.destroy_context()
  
if __name__ == '__main__':
  run()