#!/usr/bin/python3
#Copyright (C) Robert Gledhill 2020, 2023
import sys
import time

class TimeStamp(object):
  def __init__(self):
    self.m_timestruct = []
  
  def now(self):
    """Set this timestamp to the present value of GMT (_not_ local time -- 
    this will be an hour earlier than the clock on the wall in summer)"""
    self.m_timestruct = time.gmtime()
  
  def setFrom12DString(self, ts):
    """Set from a 12 digit string (date and time), e.g. '201507061008'"""
    self.m_timestruct = time.strptime(ts, "%Y%m%d%H%M")
  
  def setFrom8DString(self, ts):
    """Set from an 8 digit (date only) string, e.g. '20150706'"""
    self.m_timestruct = time.strptime(ts, "%Y%m%d")
    
  def get8DString(self):
    """Return an 8 digit (date only) string"""
    return time.strftime("%Y%m%d", self.m_timestruct)
  
  def get12DString(self):
    """Return a 12 digit (date and time) string"""
    return time.strftime("%Y%m%d%H%M", self.m_timestruct)    
  
  def setFromEpochSecs(self, secs):
    """Set this timestamp from an integer representing seconds from the
    UNIX epoch (0000GMT Jan 1 1970) in GMT (not local time)"""
    self.m_timestruct = time.gmtime(secs)
  
  def getEpochSecs(self):
    """Return timestamp as an integer representing seconds from the epoch"""
    return time.mktime(self.m_timestruct)
  