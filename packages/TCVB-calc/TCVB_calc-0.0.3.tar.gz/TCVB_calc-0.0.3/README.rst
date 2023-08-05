TCVB_calc
=========

TCVB_calc is a simple Python library for performing simple mathematical
calculations with memory function.

Installation
------------

Use the package manager `pip <https://pip.pypa.io/en/stable/>`__ to
install TCVB_calc.

.. code:: bash

   pip install TCVB_calc

Functionality
-------------

List of calculator module functions and method calls: - Addition
(var.add()) - Subtraction (var.subtract()) - Division (var.divide()) -
Multiplication (var.multiply()) - Taking n-th root (var.n_root()) -
Resetting calculator memory (var.reset())

Created variable is stored in calculator memory, print(.result) will
print the current value of the variable.

Usage
-----

.. code:: python

   import TCVB_calc.calc_main

   # Instantiates an object with default value of 0
   my_var=TCVB_calc.calc_main.Calculator()

   # Adds 1 to the Calculator object
   my_var.add(1)

   # Resets calculator object value to 0
   my_var.reset()

Testing
-------

.. code:: python

   # prints 9 (square root of 81): 

   import TCVB_calc.calc_main 

   def n_root_test():
       test_var=TCVB_calc.calc_main.Calculator(81)
       test_var.n_root(2)
       print (test_var.result)

       

Contributing
------------

This module was written for learning purposes only, comments and
suggestions are welcome.

License
-------

[MIT](https://choosealicense.com/licenses/mit/
