import sys, serial, argparse
import numpy as np
from time import sleep
from collections import deque

import matplotlib.pyplot as plt
import matplotlib.animation as animation

# plot class
class AnalogPlot:
  # constr
  def __init__(self, strPort, maxLen, baudRate):
      # open serial port
      self.ser = serial.Serial(strPort, baudRate)

      self.ax = deque([0.0]*maxLen)
      self.maxLen = maxLen

  # add to buffer
  def addToBuf(self, buf, val):
      if len(buf) < self.maxLen:
          buf.append(val)
      else:
          buf.pop()
          buf.appendleft(val)

  # update plot
  def update(self, frameNum, a0):
      try:
          data = float(self.ser.readline())
          self.addToBuf(self.ax, data)
          a0.set_data(range(self.maxLen), self.ax)
      except:
          pass

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
  parser.add_argument('--baudRate', dest='baudRate', type=int, default=9600)
  parser.add_argument('--ymin', dest='ymin', type=int, default=650)
  parser.add_argument('--ymax', dest='ymax', type=int, default=800)

  # parse args
  args = parser.parse_args()

  strPort = args.port
  maxLen = args.maxLen
  baudRate = args.baudRate
  ymin = args.ymin
  ymax = args.ymax
  print(maxLen)

  print('reading from serial port %s...' % strPort)

  # plot parameters
  analogPlot = AnalogPlot(strPort, maxLen, baudRate)

  print('plotting data...')

  # set up animation
  fig = plt.figure()
  ax = plt.axes(xlim=(0, maxLen), ylim=(ymin, ymax))
  a0, = ax.plot([], [])
  anim = animation.FuncAnimation(fig, analogPlot.update,
                                 fargs=(a0,),
                                 interval=5)

  # show plot
  plt.show()

  # clean up
  analogPlot.close()

  print('exiting.')

# call main
if __name__ == '__main__':
  main()
