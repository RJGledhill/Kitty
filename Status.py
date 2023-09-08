#!/usr/bin/python3
#Copyright (C) Robert Gledhill 2020, 2023

import sys
from TimeStamp import TimeStamp


#------------------------------------------------------------------------------
class Status(object):
  """Keep track of situation.  Make notes of time.  Log errors and other info."""
  def __init__(self, logfile, programName):
    ts = TimeStamp()
    ts.now()
    self.m_programName = programName
    self.m_logfile = logfile
    self.m_state = {"Start time" : ts.get12DString(),\
                    "Command" : "UNK",\
                    "Last update" : ts.get12DString(),\
                    "Status" : "Starting"}


#------------------------------------------------------------------------------
  def writeLogFile(self):
    """Write out an HTML log file."""
    ts = TimeStamp()
    ts.now()
    self.m_state["Last update"] = ts.get12DString()
    try:
      f = open(self.m_logfile, 'w')
    except:
      self.fatal("Could not open log file <%s> for writing"%self.m_logfile)

    f.write('<html><head><title>%s</title><link rel="stylesheet" type="text/css" href="../styleKitty.css" /></head><body><center>'%self.m_programName)
    f.write('<h1>%s</h1><h2>%s</h2><table>'%(self.m_programName, self.m_state["Command"]))

    for k in self.m_state.keys():
      if k in ["Command", "url"]:
        continue
      f.write('<tr><td>%s</td><td>%s</td></tr>'%(k, self.m_state[k]))
    f.write('</table></center></body></html>')
    f.close()


#------------------------------------------------------------------------------
  def update(self, key, val):
    """Update the current info for what state we are in"""
    self.m_state[key] = val


#------------------------------------------------------------------------------
  def increment(self, type, increment):
    """Increment one of the status variables, creating it if necessary"""
    if type in self.m_state:
      self.m_state[type] = self.m_state[type] + increment
    else:
      self.m_state[type] = increment

#------------------------------------------------------------------------------
  def warning(self, type, details):
    """Honk out a warning message that something is wrong, also keeping a count of the type"""
    self.increment(type, 1)
    print ("[WARNING] %s <%s>"%(details, self.m_state["url"]))
  

#------------------------------------------------------------------------------
  def fatal(self, string):
    """Print the given string and terminate with a -1"""
    print ("[FATAL] ", string)
    sys.exit(-1)


#------------------------------------------------------------------------------
  def regularExit(self, string):
    """Print the given string and terminate with a 0"""
    print ("[Regular Exit] ", string)
    sys.exit(0)
  
  
#------------------------------------------------------------------------------
  def debug(self, string):
    """Write a flow of debug chatter to the terminal"""
    print ("[DEBUG] ", string)
  
