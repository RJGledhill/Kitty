#Copyright (C) Robert Gledhill 2020, 2023
import Status
import numpy as np

class Sequence(object):
  """A sequence o float values (i.e. a vector), with functions to obtain various properties"""
  def __init__(self)
    m_d = np.ndarray()
    
# can create array of differences (i.e. change from one val to the next) like this:
# a = np.array([1,5,2,6])
# b = np.diff(a, 1, 0, 0) -- fourth value prepends a '0' to the array to give us a 4 element return array)
# -> b[0] = a[0] - 0 = 1  (that zero is the prepended zero)
# -> b[1] = a[1] - a[0] = 5 - 1 = 4
# -> etc.
#>>> print (b)
#[ 1  4 -3  4]
#>>> b[0] = 0
#>>> print (b)
#[ 0  4 -3  4]
