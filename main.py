import dearpygui.dearpygui as dpg
import pandas as pd

width = 480
height = 620
currentCorr = 'Standing'
show_table = False

def create_table(data):
  show_table = True


# Functions
def open(sender, app_data):
  print("Ok was clicked")
  print("Sender: ", sender)
  print("App Data: ", app_data['file_path_name'])
  data = pd.read_csv(app_data['file_path_name'])
  print(data)
  create_table(data)

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
  height=height,
  resizable=False,
)

with dpg.file_dialog(directory_selector=False, show=False, callback=open, cancel_callback=close, id="file_dialog_id", width=width-width*0.3, height=height-height*0.3):
    dpg.add_file_extension(".csv", color=(0, 255, 0, 255), custom_text="[csv]")
    # dpg.add_file_extension(".*")
    # dpg.add_file_extension("", color=(150, 255, 150, 255))
    # dpg.add_file_extension("Source files (*.cpp *.h *.hpp){.cpp,.h,.hpp}", color=(0, 255, 255, 255))
    # dpg.add_file_extension(".h", color=(255, 0, 255, 255), custom_text="[header]")

with dpg.window(
  label='Main Window', 
  no_title_bar=True,
  no_move=True, width=width,
  height=height,
  no_resize=True,
):
  dpg.add_button(label="Buscar archivo", callback=lambda: dpg.show_item("file_dialog_id"))
  dpg.add_radio_button(items=['Standing', 'Beggs'], horizontal=True,callback=radio_callback, default_value=currentCorr)
  with dpg.table(header_row=False, show=show_table):
      dpg.add_table_column()
      dpg.add_table_column()
      dpg.add_table_column()
      
      for i in range(0, 4):
        with dpg.table_row():
          for j in range(0, 3):
            dpg.add_text(f"Row {i} Column {j}")
  
  # dpg.add_text("hello")
  # dpg.add_radio_button(items=['one', 'two', 'three'], horizontal=True)
  
def run():
  dpg.setup_dearpygui()
  dpg.show_viewport()
  
  
  dpg.start_dearpygui()
  dpg.destroy_context()
  
if __name__ == '__main__':
  run()