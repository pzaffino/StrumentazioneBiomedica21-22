import sys, serial, argparse
import numpy as np
from time import sleep
from collections import deque

import matplotlib.pyplot as plt
import matplotlib.animation as animation

# plot class
class AnalogPlot:
  # constr
  def __init__(self, strPort, maxLen):
      # open serial port
      self.ser = serial.Serial(strPort, 9600)

      self.hr = deque([0.0]*maxLen)
      self.o2 = deque([0.0]*maxLen)
      self.maxLen = maxLen

  # add to buffer
  def addToBuf(self, buf, val):
      if len(buf) < self.maxLen:
          buf.append(val)
      else:
          buf.pop()
          buf.appendleft(val)

  # update plot
  def update(self, frameNum, a0, a1):
      #print(self.ser.readline().strip().decode('utf8').split(","))
      try:
          values = self.ser.readline().strip().decode('utf8').split(",")
          hr_f, o2_f = float(values[0]), float(values[1])
          self.addToBuf(self.hr, hr_f)
          self.addToBuf(self.o2, o2_f)
          a0.set_data(range(self.maxLen), self.hr)
          a1.set_data(range(self.maxLen), self.o2)
      except:
          pass

      return a0, a1

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
  parser.add_argument('--maxLen', dest='maxLen', type=int, default=20)

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
  ax = plt.axes(xlim=(0, maxLen), ylim=(0, 200))
  a0, = ax.plot([], [], label="HR")
  a1, = ax.plot([], [], label="O2")
  anim = animation.FuncAnimation(fig, analogPlot.update,
                                 fargs=(a0,a1),
                                 interval=10)

  # show plot
  plt.legend(loc='upper right')
  plt.show()

  # clean up
  analogPlot.close()

  print('exiting.')

# call main
if __name__ == '__main__':
  main()
