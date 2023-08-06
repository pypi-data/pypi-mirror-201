"""
Python library to parse the data from the Libre Hardware Monitor (LHM) json endpoint.
"""

from datetime import datetime
import json
import requests


class LHM_Parser:
  """
  A class to parse the data from the LHM json endpoint.

  Notes
  -----
  Pylint C0103: The module name would be too long if full name was used Libre_Hardware_Monitor_Parser
  Pylint R0904: This is a data source class its meant to have a lots of public methods


  Attributes
  ----------
  port : int
    The port of the LHM server.
  ip : str
    The ip of the LHM server.
  raw_data_json : str
    The raw data from the LHM server.
  """

  def __init__(self, port=8085, ip='127.0.0.1'):

    self.port = port
    self.ip = ip

    self.__ram_tree = {}
    self.__cpu_tree = {}
    self.__gpu_tree = {}

    self.update()

  def __download_data(self):
    """
    Download the data from the LHM server.
    """
    url = f'http://{self.ip}:{self.port}/data.json'
    date_measure = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    try:
      response = requests.get(url, timeout=10)
      response.raise_for_status()

      return response.content

    except requests.exceptions.HTTPError as err:
      print(err)
      return (None, date_measure)

  def update(self):
    """
    Update the data from the LHM server.
    """

    data = self.__download_data()
    # self.__raw_data_json = data
    self.__raw_data_dict = json.loads(data)

    self.__update_cpu_tree()
    self.__update_gpu_tree()
    self.__update_ram_tree()

  # def export_as_dict(self):
  #   """
  #   Export the data as a dictionary.
  #   """
  #   return self.__raw_data_dict

  def system_name(self):
    """
    Return the name of the system.
    """
    return self.__raw_data_dict['Children'][0]['Text']

  def __update_cpu_tree(self):
    """
    Update the CPU tree.
    """
    for component in self.__raw_data_dict['Children'][0]['Children']:
      if component['ImageURL'] == 'images_icon/cpu.png':
        self.__cpu_tree.clear()
        self.__cpu_tree = component

  def __update_gpu_tree(self):
    """
    Update the GPU tree.
    """
    for component in self.__raw_data_dict['Children'][0]['Children']:
      # TODO: add support for AMD GPUs
      if component['ImageURL'] == 'images_icon/nvidia.png':
        self.__gpu_tree.clear()
        self.__gpu_tree = component

  def __update_ram_tree(self):
    """
    Update the RAM tree.
    """
    for component in self.__raw_data_dict['Children'][0]['Children']:
      if component['ImageURL'] == 'images_icon/ram.png':
        self.__ram_tree.clear()
        self.__ram_tree = component

# CPU FUNCTIONS ========================================================================================================

  def cpu_name(self):
    """
    Return the name of the CPU.
    """
    return self.__cpu_tree['Text']

  def cpu_voltage_tree(self):
    """
    Return the CPU voltage tree.
    """
    output = None
    for component in self.__cpu_tree['Children']:
      if component['Text'] == 'Voltages':
        output = component
    return output

  def cpu_power_tree(self):
    """
    Return the CPU power tree.
    """
    output = None
    for component in self.__cpu_tree['Children']:
      if component['Text'] == 'Powers':
        output = component
    return output

  def cpu_clock_tree(self):
    """
    Return the CPU clock tree.
    """
    output = None
    for component in self.__cpu_tree['Children']:
      if component['Text'] == 'Clocks':
        output = component
    return output

  def cpu_temperature_tree(self):
    """
    Return the CPU temperature tree.
    """
    output = None
    for component in self.__cpu_tree['Children']:
      if component['Text'] == 'Temperatures':
        output = component
    return output

  def cpu_load_tree(self):
    """
    Return the CPU load tree.
    """
    output = None
    for component in self.__cpu_tree['Children']:
      if component['Text'] == 'Load':
        output = component
    return output

  def cpu_factor_tree(self):
    """
    Return the CPU factor tree.
    """
    output = None
    for component in self.__cpu_tree['Children']:
      if component['Text'] == 'Factors':
        output = component
    return output

# GPU FUNCTIONS ========================================================================================================

  def gpu_name(self):
    """
    Return the name of the GPU.
    """
    return self.__gpu_tree['Text']

  def gpu_power_tree(self):
    """
    Return the GPU power tree.
    """
    output = None
    for component in self.__gpu_tree['Children']:
      if component['Text'] == 'Powers':
        output = component
    return output

  def gpu_clock_tree(self):
    """
    Return the GPU clock tree.
    """
    output = None
    for component in self.__gpu_tree['Children']:
      if component['Text'] == 'Clocks':
        output = component
    return output

  def gpu_temperature_tree(self):
    """
    Return the GPU temperature tree.
    """
    output = None
    for component in self.__gpu_tree['Children']:
      if component['Text'] == 'Temperatures':
        output = component
    return output

  def gpu_load_tree(self):
    """
    Return the GPU load tree.
    """
    output = None
    for component in self.__gpu_tree['Children']:
      if component['Text'] == 'Load':
        output = component
    return output

  def gpu_fan_tree(self):
    """
    Return the GPU fan tree.
    """
    output = None
    for component in self.__gpu_tree['Children']:
      if component['Text'] == 'Fans':
        output = component
    return output

  def gpu_controls_tree(self):
    """
    Return the GPU controls tree.
    """
    output = None
    for component in self.__gpu_tree['Children']:
      if component['Text'] == 'Controls':
        output = component
    return output

  def gpu_data_tree(self):
    """
    Return the GPU data tree.
    """
    output = None
    for component in self.__gpu_tree['Children']:
      if component['Text'] == 'Data':
        output = component
    return output

  def gpu_throughput_tree(self):
    """
    Return the GPU throughput tree.
    """
    output = None
    for component in self.__gpu_tree['Children']:
      if component['Text'] == 'Throughput':
        output = component
    return output

# RAM FUNCTIONS ========================================================================================================

  def ram_name(self):
    """
    Return the name of the RAM.
    """
    return self.__ram_tree['Text']

  def ram_load_tree(self):
    """
    Return the RAM load tree.
    """
    output = None
    for component in self.__ram_tree['Children']:
      if component['Text'] == 'Load':
        output = component
    return output

  def ram_data_tree(self):
    """
    Return the RAM data tree.
    """
    output = None
    for component in self.__ram_tree['Children']:
      if component['Text'] == 'Data':
        output = component
    return output

# DEBUG FUNCTIONS ======================================================================================================

  def print_raw_data(self):
    """
    Print the raw dict data.
    """
    print(self.__raw_data_dict)

  def print_cpu_tree(self):
    """
    Print the CPU tree.
    """
    print(self.__cpu_tree)

  def print_gpu_tree(self):
    """
    Print the GPU tree.
    """
    print(self.__gpu_tree)

  def print_ram_tree(self):
    """
    Print the RAM tree.
    """
    print(self.__ram_tree)

# def print_cpu_voltage_tree(self):
#   for component in self.__cpu_tree['Children']:
#     if component['Text'] == 'Voltages':
#       print(component)

# def print_cpu_power_tree(self):
#   for component in self.__cpu_tree['Children']:
#     if component['Text'] == 'Powers':
#       print(component)

# def print_cpu_clock_tree(self):
#   for component in self.__cpu_tree['Children']:
#     if component['Text'] == 'Clocks':
#       print(component)

# def print_cpu_temperature_tree(self):
#   for component in self.__cpu_tree['Children']:
#     if component['Text'] == 'Temperatures':
#       print(component)

# def print_cpu_load_tree(self):
#   for component in self.__cpu_tree['Children']:
#     if component['Text'] == 'Load':
#       print(component)

# def print_cpu_factor_tree(self):
#   for component in self.__cpu_tree['Children']:
#     if component['Text'] == 'Factors':
#       print(component)
