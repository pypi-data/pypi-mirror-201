# pycalculator_TomasJ
A simple calculator that can add, subtract, multiply, divide and extract roots 
from a number in the calculator's memory. This package was created as a project 
for evaluation purposes only.  
 
The calculator is meant to be used with integer numbers, however after division 
and root extraction it will result in a floating point number. It follows basic 
arithmetic rules, therefore it is impossible to divide by zero as well as extract 
an even number root from a negative number. If the calculation were to return a 
number too large for the memory to handle, it will not perform the calculation. 

To install the package go to your command shell 
and install it via:  

`pip install pycalculator-TomasJ  `

Testing was done with the Hypothesis  and pytest modules.  

To use the calculator you must first instantiate a Calculator object. 
Default memory after instantiation is 0. All possible operations are done with 
the object's memory. Here's an example of how the module can be used:  

    from pycalculator_TomasJ.calculator import Calculator
    
    calc = Calculator()  
    calc.add(5)  
    > 5  
    calc.subtract(1)  
    > 4  
    calc.multiply_by(8)  
    > 32  
    calc.divide_by(2)  
    > 16.0  
    calc.root_extraction(4)  
    > 2.0  

contact information: tomasitassss@gmail.com  
Project uses the MIT license
