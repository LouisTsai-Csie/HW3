# HW3

## Installation

1. python -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt
4. deactivate // leave the virtual environment

## Part 1

### Assignment Score

Problem 1 - equal weight portofolio

`python Markowitz.py --score eqw`

Problem 2 - risk parity portofolio

`python Markowitz.py --score rp`

Problem 3 - mean variance portofolio

`python Markowitz.py --score mv`

All Problems

`python Markowitz.py --score all`

### Asset Allocation

Problem 1 - equal weight portofolio

`python Markowitz.py --allocation eqw`

Problem 2 - risk parity portofolio

`python Markowitz.py --allocation rp`

Problem 3 - mean variance portofolio

`python Markowitz.py --allocation mv`

### Performance Check

Problem 3 - mean variance portofolio

`python Markowitz.py --performance mv`

### Evaluation Metric

Problem 3 - mean variance portofolio

`python Markowitz.py --report mv`

## Part 2

### Assignment Score

Problem 1 - Sharp Ratio > 1

`python Markowitz_2.py --score one`

Problem 2 - Sharp Ratio > SPY

`python Markowitz_2.py --score spy`

All Problems

`python Markowitz_2.py --score all`

### Asset Allocation

Problem 1 - Sharp Ratio > 1

`python Markowitz_2.py --allocation mp`

Problem 2 - Sharp Ration > SPY

`python Markowitz_2.py --allocation bmp`

### Performance Check

My Portofolio

`python Markowitz_2.py --performance mp`

`python Markowitz_2.py --performance bmp`

### Evaluation Metric

`python Markowitz_2.py --report mp`

`python Markowitz_2.py --report bmp`

### Cumulative Result

`python Markowitz_2.py --cumulative mp`

`python Markowitz_2.py --cumulative bmp`


