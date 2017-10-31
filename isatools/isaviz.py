"""Functions for visualizing ISA content from ISA model objects."""
from __future__ import absolute_import
import os
import matplotlib as mpl
import matplotlib.pyplot as plt

__author__ = 'djcomlab@gmail.com (David Johnson)'

if os.environ.get('DISPLAY','') == '':
    mpl.use('Agg')

tableau_colours = ('tab:blue', 'tab:orange', 'tab:green', 'tab:red',
                   'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray',
                   'tab:olive', 'tab:cyan')


def make_study_summary(study, target_directory=''):
    num_sources = len(study.sources)
    num_samples = len(study.samples)
    filepath = os.path.join(target_directory,
                            '{}.png'.format(next(iter(
                                os.path.splitext(study.filename)))))

    _make_pie([num_sources, num_samples], '', tableau_colours[:2],
              ['{} sources'.format(num_sources),
               '{} samples'.format(num_samples)], filepath)


def make_assay_summary(assay, target_directory=''):
    num_samples = len(assay.samples)
    num_other_material = len(assay.other_material)
    num_data_files = len(assay.data_files)
    filepath = os.path.join(target_directory,
                            '{}.png'.format(next(iter(
                                os.path.splitext(assay.filename)))))
    _make_pie([num_samples, num_other_material, num_data_files], '',
              tableau_colours[:3],
              ['{} samples'.format(num_samples),
               '{} other material'.format(num_other_material),
               '{} data files'.format(num_data_files)], filepath)


def _make_pie(sizes, text, colours, labels, filename):

    fig, ax = plt.subplots()
    ax.axis('equal')
    width = 0.35
    kwargs = dict(colors=colours, startangle=180)
    outside, _ = ax.pie(sizes, radius=1, pctdistance=1 - width / 2,
                        labels=labels, **kwargs)
    plt.setp(outside, width=width, edgecolor='white')

    kwargs = dict(size=20, fontweight='bold', va='center')
    ax.text(0, 0, text, ha='center', **kwargs)
    if filename == '':
        plt.show()
    else:
        plt.savefig(filename, bbox_inches='tight')