#!/usr/bin/python
import serial
import re
from decimal import Decimal
import datetime
import time
import threading
import multiprocessing


#UNUSED
#loop_chunk_size = 150
#A larger size will yield more accurate graphs, but slower resfresh rate
#A smaller size will yield innaccurate graphs, but a higher refresh rate

class SerialHandler():
     
  
  
  def __init__(self,con_name):
    self.con_name = con_name
    self.ser_con = serial.Serial("/dev/"+con_name,115200)
    self.defaultSampleRate()
    #reset frequency to 50
    self.sample_rate = 50
    self.listeners = []#unused
    #frequency in hertz
  
  
  #START unused block
  #this section of code was used by a different version of app without animation
  #didn't work very well        
  """  def addListener(self, listener):
    #listener class must implement onDataUpdate(DataTable)
    try:
      listener.onDataUpdate
      self.listeners.append(listener)
    except AttributeError:
      print("Listener must implement onDataUpdate(DataTable)")
  
  def updateListeners(self,dataTable):
    for listener in self.listeners:
      listener.onDataUpdate(dataTable)
  
  def runInLoop(self):
    self.defaultSampleRate()
    time.sleep(.1)
    self.doubleSampleRate()
    self.doubleSampleRate()
    
    thread = multiprocessing.Process(target=self.dataReadLoop, args=())
    thread.start()
    
  def dataReadLoop(self):
    while True:
      self.updateListeners(self.readToDataTable(loop_chunk_size))"""
  #END unused block    
  def defaultSampleRate(self):
    self.ser_con.write("x")#returns the sample rate to 50
    self.sample_rate = 50
      
  def doubleSampleRate(self):
    if self.sample_rate < 200: #max sample rate is 200 hertz, so we can't go above that
      self.sample_rate *= 2
      self.ser_con.write("+")
    else:
      print("200 Hertz is Max Frequency")
  
  def halfSampleRate(self):
    self.sample_rate /= 2
    self.ser_con.write("-")
  
  def getSampleRate(self):
    return self.sample_rate
    
  def readRawChunk(self,chunk_size):
    lines = []
    
    #if you want to look at the raw data uncomment these lines
    #log_file = open("log_file","a")
    #log_file.write("Data Read at: " + str(datetime.datetime.now())+ "\n")
    
    for x in range(chunk_size):
      line = self.ser_con.readline()
      #log_file.write(line) #and this one
      lines.append(line)
    #log_file.close() #and this one
    return lines
  
  #The accelerometer may send comments back when settings are adjusted
  #This function ignores those comments
  def filterChunk(self, chunk):
    filtered_chunk = []
    for data_line in chunk:
      data_line = data_line.strip()
      s = re.search(r"[a-zA-Z;]+",data_line) #comments contain alpha characters and ";"
      if(s == None):
        filtered_chunk.append(data_line)
      else:
        print("Removing line: " + data_line)
    return filtered_chunk
  
  def readChunk(self, chunk_size):
    chunk = self.readRawChunk(chunk_size)
    chunk = self.filterChunk(chunk)
    return chunk

  def readToDataTable(self, chunk_size):
    chunk = self.readChunk(chunk_size)
    return DataTable(chunk)

  def stripEnd(self, data_line): #to be mapped to a chunk of data
    return data_line.strip()
    
#very simple container for accelerometer data        
class DataTable:

 def __init__(self,chunk):
   self.time = []
   self.x = []
   self.y = []
   self.z = []
   for data_line in chunk:
     split_line = data_line.split(",")
     if(len(split_line)==4):
       self.time.append(Decimal(split_line[0]))
       self.x.append(int(split_line[1]))
       self.y.append(int(split_line[2]))
       self.z.append(int(split_line[3]))
      	 
def runTest():
  s = SerialHandler("ttyUSB0")
  s.doubleSampleRate()
  print(s.readToDataTable(100).x)  
    

  