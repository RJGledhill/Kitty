#Copyright (C) Robert Gledhill 2020, 2023
import os
import sys
from Status import Status

class Plots(object):
  """Manage producing graphical plots of data using gnuplot"""
  def __init__(self, status, dataDir, outputSVGFile, inputDataFile):
    self.m_status = status
    self.m_plotScripts = []
    # plot type 0 : a graph of one variable with labels price/timestamp
    self.m_plotScripts.append("""
set output '%s/%s'
set terminal svg size 800,600
set border lc rgb "#d0ffff"
unset key
set xlabel "Timestamp" tc rgb "#d0ffff"
set ylabel "Price" tc rgb "#d0ffff"
set grid lc rgb "#104030" linewidth 0.5
plot '%s' with lines lc rgb "#ffff00"
""" % (dataDir, outputSVGFile, inputDataFile))

  #------------------------------------------------------------------------------
  def runGnuPlot(self, plotScriptNumber, temporaryScriptFile, outputSVGFile):
    """Assuming data file is already written, run the given plot script to create an svg graph file"""
    # 1 write out the plotscript to a temporary file
    with open(temporaryScriptFile, 'w') as outfh:
      outfh.write(self.m_plotScripts[plotScriptNumber])
 
    # 2 run gnuplot on it
    cmd = "gnuplot %s" % (temporaryScriptFile)
    result = os.system(cmd)
    self.m_status.debug("Executed command [%s]" % cmd)
    self.m_status.debug(" -- obtained response [%s]" % result)

    # 3 delete the temporary plotscript file
    os.remove(temporaryScriptFile)



