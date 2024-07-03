# Digipyze

This repository contains a python script used to digitalize a battery curve and to extract the parameters to insert in [MESSY](https://github.com/eml-eda/messy).

## Getting Started

TODO: explain venv 


## How to run it

The digitalized curves should be in the following format:

```txt
x, y
0.03410000,  3.00830000
0.04210000,  3.04570000
0.07820000,  3.14540000
0.09820000,  3.19110000
0.14030000,  3.26180000
0.20040000,  3.35320000
0.24450000,  3.41140000
0.30460000,  3.48610000
0.33670000,  3.51520000
0.39280000,  3.56090000
0.47700000,  3.60660000
0.55510000,  3.64400000
0.63730000,  3.70220000
0.70940000,  3.75620000
0.79360000,  3.83100000
0.83970000,  3.88500000
0.89780000,  3.95980000
0.93790000,  4.03460000
0.97190000,  4.09700000
0.98800000,  4.17590000
0.99600000,  4.23820000
```


The command to run is then 

```bash
python3 prova.py --first-curve-file first_curve_filename.txt --second-curve-file second_curve_filename.txt --battery-capacity battery_capacity_in_mah
```
