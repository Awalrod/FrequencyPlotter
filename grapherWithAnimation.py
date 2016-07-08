#!/usr/bin/python
import time
from numpy.fft import fft
from matplotlib import pyplot as plt
from matplotlib import animation
from serialHandler import SerialHandler
import sys
from serial.serialutil import SerialException

class GrapherWithAnimation:
  
  def __init__(self,handler,chunk_size):
    self.fig = plt.figure()
    ax = plt.axes(xlim=(0,100),ylim=(0,5000))
    self.line, = ax.plot([],[])
    self.handler = handler
    self.chunk_size = chunk_size
    
  def initialSetup(self):
    self.line.set_data([],[])
    return self.line,
  
  def animate(self,i):
    #param i is unused but necessary because the FuncAnimation sends the iteration count to the function
  
    #Currently I don't understand exactly what these two blocks of code do
    #They turn the accelleration data into frequencies and intensities
    accel_data = self.handler.readToDataTable(self.chunk_size) #the DataTable class is defined in serialHandler
    z_fft = fft(accel_data.z)
    z_mod = map(lambda x: abs(x),z_fft)
    z_mod_half = z_mod[0:len(z_mod)/2]
    
    sa = self.handler.getSampleRate()
    frequency_axis = range(0,len(accel_data.z)/2)      
    frequency_axis = map(lambda fa: fa*(sa/2)/(len(accel_data.z)/2), frequency_axis)
    
    self.line.set_data(frequency_axis, z_mod_half)
    return self.line,

def main():
  serialPortName = ""
  chunk_size = 0
  try:
    serialPortName = sys.argv[1]  
  except IndexError:
    print("No serial port given, using ttyUSB0")
    serialPortName = "ttyUSB0" #Default serial port. Usually works, but sometimes accelerometer uses ttyUSB1 
  try:
    chunk_size = int(sys.argv[2])
  except IndexError:
    print("No chunk size given, using 150")
    chunk_size = 150 #default chunk_size. A larger chuk_size yields more accurate graphs with slower animation
  except ValueError:
    print("Invalid chunk size, using 150")
    chunk_size = 150
  try: 			
    handler = SerialHandler(serialPortName)
  except SerialException:
    print("Wrong serial address, try another")
    return(-1)  
  time.sleep(.1) #Let serial port open and configure before sending messages
  #sample rate starts at 50 hertz.
  #we want to get it up to 200 hertz(max sample rate on accelerometer I'm using
  handler.doubleSampleRate()
  handler.doubleSampleRate()#sample rate should be at 200 now
  graph = GrapherWithAnimation(handler,chunk_size)
  anim = animation.FuncAnimation(graph.fig, graph.animate, init_func = graph.initialSetup, interval=100, blit=True)
  #the interval here doesn't really matter because the animation is limited by the Sample Rate
  plt.show()
  
main()