import sys, serial, argparse
import numpy as np
from time import sleep
from collections import deque

import matplotlib.pyplot as plt
import matplotlib.animation as animation

import scipy.signal

# plot class
class AnalogPlot:
  def __init__(self, strPort, maxLen):
      # open serial port
      self.ser = serial.Serial(strPort, 9600)

      self.batchSize = 10
      self.maxLen = maxLen

      self.ax = [0.0]*maxLen
      self.internal_buffer = [0.0]*self.batchSize

      self.counterValue = 0
      self.counterOffset = 0

  # update plot
  def update(self, frameNum, a0):
	  if self.counterValue < self.batchSize:
          try:
              data = float(self.ser.readline())
              self.internal_buffer[self.counterValue]=data
              self.counterValue += 1
          except:
              pass
      
      elif self.counterValue == self.batchSize:
          self.ax[self.counterOffset:self.counterOffset+self.batchSize] = scipy.signal.savgol_filter(self.internal_buffer,7,3)
          a0.set_data(range(self.maxLen), self.ax)
          self.internal_buffer = [0.0]*self.batchSize
          self.counterOffset += self.batchSize
          self.counterValue = 0

          if self.counterOffset + self.batchSize > self.maxLen:
              self.counterOffset = 0
      

      return a0,

  # clean up
  def close(self):
      # close serial
      self.ser.flush()
      self.ser.close()

# main() function
def main():
  # create parser
  parser = argparse.ArgumentParser(description="LDR serial")
  # add expected arguments
  parser.add_argument('--port', dest='port', required=True)
  parser.add_argument('--maxLen', dest='maxLen', type=int, default=300)

  # parse args
  args = parser.parse_args()

  strPort = args.port
  maxLen = args.maxLen

  print('reading from serial port %s...' % strPort)

  # plot parameters
  analogPlot = AnalogPlot(strPort, maxLen)

  print('plotting data...')

  # set up animation
  fig = plt.figure()
  ax = plt.axes(xlim=(0, maxLen), ylim=(200, 600))
  a0, = ax.plot([], [])
  anim = animation.FuncAnimation(fig, analogPlot.update,
                                 fargs=(a0,),
                                 interval=10)

  # show plot
  plt.show()

  # clean up
  analogPlot.close()

  print('exiting.')

# call main
if __name__ == '__main__':
  main()
