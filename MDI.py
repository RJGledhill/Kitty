#Copyright (C) Robert Gledhill 2020, 2023
import os.path
import sys
from TimeStamp import TimeStamp
from Status import Status
from Plots import Plots
import sqlite3
import random
import numpy as np


#------------------------------------------------------------------------------
class MDI(object):
#------------------------------------------------------------------------------  
  def __init__(self, logfile ,programName, dbFileName, temporaryScriptFile, dataDir, outputSVGFile, inputDataFile, outputPropertiesHTMLFile):
    self.m_version = 1.0
    self.m_status = Status(logfile, programName)
    self.m_temporaryScriptFile = temporaryScriptFile
    self.m_outputPropertiesHTMLFile = outputPropertiesHTMLFile
    self.m_dataDir = dataDir
    self.m_outputSVGFile = outputSVGFile
    self.m_inputDataFile = inputDataFile
    self.m_plots = Plots(self.m_status, self.m_dataDir, self.m_outputSVGFile, self.m_inputDataFile)
    self.m_logfile = logfile
    self.m_dbFileName = dbFileName
    self.m_stockCount = 5
    self.m_meanInitStock = 100
    self.m_sdInitStock = 10
    self.m_variabilityInRisk = 5
    self.m_daysToTrade = 20
    ts = TimeStamp()
    ts.now()
    self.m_properties = {"Start time" : ts.get12DString()}

#------------------------------------------------------------------------------
  def dbDo(self, cmd):
    """Execute a commanp on the database connection; logging what is being done, but ignoring any return value"""
    self.m_status.debug("executing command <%s>"%cmd)
    self.m_connection.execute(cmd)

#------------------------------------------------------------------------------
  def newdb(self):
    """Create a new empty market data database file where one does not exist"""
    #1 check if a regular file already exists at the given path
    if os.path.isfile(self.m_dbFileName) == 1:
      self.m_status.fatal("DB file <%s> already exists; refusing to overwrite and quitting now."%self.m_dbFileName)
    else:
      self.m_status.debug("DB file <%s> not present, so proceeding to create a new one"%self.m_dbFileName)

    #2 create file
    try:
      self.m_connection = sqlite3.connect(self.m_dbFileName)
    except:
      self.m_status.fatal("Error creating sqlite db file <%s>"%self.m_dbFileName)
    self.m_connection.text_factory = str

    #3 create  tables
    self.m_connection.execute("CREATE TABLE adjclose(timepoint INTEGER, stockid INTEGER, adjclose REAL)")
    self.m_connection.commit()
    self.m_connection.close()

#------------------------------------------------------------------------------
  def mdpopulate(self):
    """Populate the market data db file with made-up market data"""
    if os.path.isfile(self.m_dbFileName) == 1:
      self.m_status.debug("DB file <%s> exists; opening it"%self.m_dbFileName)
    else:
      self.m_status.fatal("DB file <%s> not present; quitting"%self.m_dbFileName)
    try:
      self.m_connection = sqlite3.connect(self.m_dbFileName)
    except:
      self.m_status.fatal("Error opening stock data db")
    self.m_connection.text_factory = str

    self.m_status.debug("mdpopulate populating price table")
    self.m_status.update("Command", "mdpopulate")
    self.m_status.update("Status", "creating new random stock values")
    self.m_status.writeLogFile()

    for stockid in range (self.m_stockCount):
      price = random.gauss(self.m_meanInitStock, self.m_sdInitStock)
      risk = random.gauss(0.0, self.m_variabilityInRisk) 
      self.m_status.debug("Creating price for stockid %s, start price %s, risk %s"%(stockid, price, risk))  
      for timepoint in range(self.m_daysToTrade):
        price += random.gauss(0.0, risk)
        self.dbDo("INSERT INTO adjclose VALUES (%s, %s, %s)"%(timepoint, stockid, price))
        self.m_connection.commit()
    
    self.m_status.debug("finished populating price table")
    self.m_status.update("Status", "finished creating new random stock values")
    self.m_status.writeLogFile()
    self.m_connection.close()
    return 1

#------------------------------------------------------------------------------
  def props(self, stockid):
    """Create a new html report containing properties of a specified stockid"""
    # 0. open the database up 
    self.m_status.update("Command", "props")
    self.m_status.update("Status", "calculating properties of market data in db")
    self.m_status.writeLogFile()
    if os.path.isfile(self.m_dbFileName) == 1:
      self.m_status.debug("DB file <%s> exists; opening it"%self.m_dbFileName)
    else:
      self.m_status.fatal("DB file <%s> not present; quitting"%self.m_dbFileName)
    try:
      self.m_connection = sqlite3.connect(self.m_dbFileName)
    except:
      self.m_status.fatal("Error opening stock data db")
    self.m_connection.text_factory = str
  
    # 1. Write out a text file containing all data in the DB suitable for gnuplot
    with open(self.m_inputDataFile, 'w') as outfh:
      cur = self.m_connection.cursor()
      cur.execute("SELECT timepoint, adjclose FROM adjclose WHERE stockid=%s"%stockid)
      rows = cur.fetchall()
      dataset = np.array(rows)
      for row in rows:
        outfh.write("%s %s\n"%(row[0], row[1]))
    self.m_status.debug("obtained ndarray:%s"%dataset)
    mean = np.mean(dataset[0:,1])
    stdDev = np.std(dataset[0:,1])

    # 2. Call the plot function 
    self.m_plots.runGnuPlot(0, self.m_temporaryScriptFile, "%s/%s"%(self.m_dataDir, self.m_outputSVGFile))

    # 3. Delete the temporary input data file
    os.remove(self.m_inputDataFile)
    self.m_status.update("Command", "props")
    self.m_status.update("Status", "created svg file")
    self.m_status.writeLogFile()

    # 4. Calculate volatility of data (working off assumption it is a Weiner process and gaussian distributed)
    for row in dataset:
      

    # 5. Calculate max drawdown of data

    # 6. Create a new HTML file, overwriting anything already there
    with open(self.m_outputPropertiesHTMLFile, 'w') as outfh:
      outfh.write("""<html>
      <head>
      <title>Report on Instrument %s</title>
      <link rel="stylesheet" type="text/css" href="../styleKitty.css" />
      </head>
      <body>
      <center>
      <h1>Report on Instrument %s</h1><h2>Properties</h2><table>
      """%(stockid, stockid))

    # 7. Write out properties table

      outfh.write('<tr><td>Mean</td><td>%s</td></tr>'%mean)
      outfh.write('<tr><td>StandardDeviation</td><td>%s</td></tr>'%stdDev)

      outfh.write("""</table>""")
    # 8. Add in graph; file closes automtically
      outfh.write("""
      <div class="graph">
      <embed src="%s" type="image/svg+xml">
      </div>
      </center></body></html>
      """%self.m_outputSVGFile)


