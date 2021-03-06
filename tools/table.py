#!/usr/bin/env python

import sys
import os

variants = ['baseline', 'tail', 'futhark-c', 'futhark-opencl', 'futhark-pyopencl', 'byhand-futhark-c', 'byhand-futhark-opencl', 'byhand-futhark-pyopencl']
programs = {'integral'
            : {'name': 'Integral',
               'size': '$N = 10,000,000$'},
            'signal'
            : {'name': 'Signal',
               'size': '$N = 50,000,000$'},
            'life'
            : {'name': 'Game of Life',
               'size': r'''$1200^2, N = 100$'''},
            'easter'
            : {'name': 'Easter',
               'size': '$N = 10,000,000$'},
            'blackscholes'
            : {'name': 'Black-Scholes',
               'size': '$N = 10,000,000$'},
            'sobol-pi'
            : {r'name': 'Sobol MC-$\pi$',
               'size': '$N = 10,000,000$'},
            'hotspot'
            : {r'name': 'HotSpot',
               'size': r'''$512^2, N = 360$'''},
            'mandelbrot1'
            : { 'name': 'Mandelbrot1',
                'size': r'''$1000^2, N = 255$'''},
            'mandelbrot2'
            : { 'name': 'Mandelbrot2',
                'size': r'''$1000^2, N = 255$'''}
            }
order = ['integral', 'signal', 'life', 'easter', 'blackscholes', 'sobol-pi', 'hotspot', 'mandelbrot1', 'mandelbrot2']

runtimes = {}
for program in programs:
    runtimes[program] = {}
    for variant in variants:
        with open(os.path.join('runtimes', program + '-' + variant + ".avgtime")) as f:
            runtime = float(f.read())
            runtimes[program][variant] = '-' if runtime == 0 else '%.2f' % runtime

print(r'''
\begin{tabular}{llrrrrrrrr}
& & & & \multicolumn{3}{c}{\textbf{TAIL Futhark}} & \multicolumn{3}{c}{\textbf{Hand-written Futhark}} \\
\textbf{Benchmark} & \textbf{Problem size} & \textbf{Baseline C} & \textbf{TAIL C} & \textbf{Sequential} & \textbf{OpenCL} & \textbf{PyOpenCL} & \textbf{Sequential} & \textbf{Parallel} & \textbf{PyOpenCL} \\''')

for program in order:
    program_runtimes = []
    for variant in variants:
        program_runtimes.append(runtimes[program][variant])
    print(programs[program]['name'] + ' & ' +
          programs[program]['size'] + ' & ' +
          ' & '.join(program_runtimes) + r''' \\''')

print(r'''\end{tabular}''')
