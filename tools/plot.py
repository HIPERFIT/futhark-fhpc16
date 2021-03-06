#!/usr/bin/env python

# Based on http://matplotlib.org/examples/api/barchart_demo.html

import numpy as np
import sys

import matplotlib

matplotlib.use('Agg') # For headless use

import matplotlib.pyplot as plt
import os

outputfile = sys.argv[1]
programs = sys.argv[2:]
variants = ['baseline', 'tail', 'futhark-c', 'futhark-opencl', 'futhark-pyopencl', 'byhand-futhark-c', 'byhand-futhark-opencl', 'byhand-futhark-pyopencl']
legend = ['Baseline C', 'TAIL C', 'TAIL Futhark C', 'TAIL Futhark OpenCL' , 'TAIL Futhark PyOpenCL', 'Futhark C', 'Futhark OpenCL', 'Futhark PyOpenCL']
colours = ['#ccff33', '#ff5555', '#559955', '#5555ff', '#bbbbff', '#888888', '#aa7799', '#44ddff']

baseline_variant = 'baseline'

# Read the data
runtimes = {}
for variant in variants:
    runtimes[variant] = {}
    for program in programs:
        with open(os.path.join('runtimes', program + '-' + variant + ".avgtime")) as f:
            runtimes[variant][program] = float(f.read())

# Compute speedups
speedups = {}
for variant in variants:
    speedups[variant] = {}
    for program in programs:
        baseline = runtimes[baseline_variant][program]
        runtime = runtimes[variant][program]

        if runtime != 0:
            speedups[variant][program] = baseline / runtime
        else:
            speedups[variant][program] = 0

N = len(programs)
M = len(variants)

ind = np.arange(N)  # the x locations for the groups
width = 1.0/(M+1)        # the width of the bars

fig, ax = plt.subplots()

font = {'family': 'normal',
        'size' : 16}
plt.rc('font', **font)

ax.set_yscale('log')
ax.set_ylim([0.2,100.0])
ax.set_ylabel('Speedup')
ax.set_xticks(ind + M*width/2)
ax.set_xticklabels(programs)
plt.tick_params(axis='x', which='major', pad=60)

ax.yaxis.set_major_formatter(plt.ScalarFormatter())

allrects = []
for (i, variant) in zip(range(M), variants):
    values = []
    for program in programs:
        values.append(speedups[variant][program])
    rects = ax.bar(ind+i*width, values, width, color=colours[i])

    for rect in rects:
        height = 0.19
        if rect.get_height() > 0:
            ax.text(rect.get_x() + rect.get_width()/2., height,
                    '%.1f' % rect.get_height(),
                    ha='center', va='top', rotation='90')

    allrects.append(rects)

plt.grid(b=True, which='minor', color='#777777', linestyle='-')
ax.yaxis.grid(True, linestyle='-')


ax.legend([rects[0] for rects in allrects], legend, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

fig.set_size_inches(18.5, 6.5)
plt.rc('text', usetex=True)
plt.savefig(outputfile, bbox_inches='tight')
