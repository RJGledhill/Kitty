#!/usr/bin/python3
#Copyright (C) Robert Gledhill 2020, 2023

import os
import sys
from MDI import MDI


# Tool to sketch out a bunch of fake made-up market data
# ------------------------------------------------------------------------------
def main():
  import textwrap
  USAGE = textwrap.dedent("""\
    Usage:
        marketDataInventor.py <command>
            where <command> is one of the following
        
        newdb
            -- Creates a new database file for the data if none exists, or quits with an error if a file is already present
        
        mdpopulate
            -- Populate the database with fake market data

        props <stockID>
            -- Calculate some properties of made up stock <stockid>
        """)
  programName = "Market Data Invention Tool"
  dbdir = "data"
  dbFileName = "%s/stockdata.db"%(dbdir)
  temporaryScriptFile = '%s/tmpGnuplotScriptFile.txt'%(dbdir)
  outputSVGFile = 'x.svg'
  inputDataFile = '%s/tmpGnuplotInputDataFile.txt'%(dbdir)
  logfile = "%s/logMDI.html"%dbdir
  outputPropertiesHTMLFile = "data/properties.html"
  stockID = 0

  if len(sys.argv) < 2:
    print (USAGE)
    return

  cmd = -1 # which command to do

  sys.argv = sys.argv[1:]
  a = sys.argv[0]
  if a == 'newdb':
    cmd = 1
  elif a == 'mdpopulate':
    cmd = 2
  elif a == 'props':
    cmd = 3
    print ("length of argv[] = %s"%len(sys.argv))  
    if len(sys.argv) == 2:
      stockID = sys.argv[1]
    else:
      print (USAGE)
      return
  else:
    print (USAGE)
    return

  myMDI = MDI(logfile, programName, dbFileName, temporaryScriptFile, dbdir, outputSVGFile, inputDataFile, outputPropertiesHTMLFile)
  if cmd == 1:
    myMDI.newdb()
    return
  elif cmd == 2:
    myMDI.mdpopulate()
    return
  elif cmd == 3:
    myMDI.props(stockID)
    return


#------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
