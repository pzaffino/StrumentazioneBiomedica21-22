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
      self.respirazione = deque([0.0]*maxLen)
      self.temperatura = deque([0.0]*maxLen)
      self.ecg = deque([0.0]*maxLen)
      self.maxLen = maxLen

  # add to buffer
  def addToBuf(self, buf, val):
      if len(buf) < self.maxLen:
          buf.append(val)
      else:
          buf.pop()
          buf.appendleft(val)

  # update plot
  def update(self, frameNum, a0, a1, a2, a3, a4):
      #print(self.ser.readline().strip().decode('utf8').split(","))
      try:
          values = self.ser.readline().strip().decode('utf8').split(",")
          hr_f, o2_f, respirazione_f, temp_f, ecg_f = float(values[0]), float(values[1]), float(values[2]), float(values[3]), float(values[4])

          self.addToBuf(self.hr, hr_f)
          self.addToBuf(self.o2, o2_f)
          self.addToBuf(self.respirazione, respirazione_f)
          self.addToBuf(self.temperatura, temp_f)
          self.addToBuf(self.ecg, ecg_f)

          a0.set_data(range(self.maxLen), self.hr)
          a1.set_data(range(self.maxLen), self.o2)
          a2.set_data(range(self.maxLen), self.respirazione)
          a3.set_data(range(self.maxLen), self.temperatura)
          a4.set_data(range(self.maxLen), self.ecg)
      except:
          pass

      return a0, a1, a2, a3, a4

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
  a2, = ax.plot([], [], label="respirazione")
  a3, = ax.plot([], [], label="temperatura")
  a4, = ax.plot([], [], label="ecg")
  anim = animation.FuncAnimation(fig, analogPlot.update,
                                 fargs=(a0,a1,a2,a3,a4),
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
