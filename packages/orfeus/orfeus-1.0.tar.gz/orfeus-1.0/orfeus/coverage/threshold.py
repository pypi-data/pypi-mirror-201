#!/usr/bin/env python

# -----------------------------------------------------------------------------
# Coverage threshold
# Author: Mary Richardson
# Date: 2020.06.04
# -----------------------------------------------------------------------------

from orfeus.coverage.sensitivity import sensitivity_simulation, plot_sensitivity
from orfeus.coverage.specificity import specificity_simulation, plot_specificity
from orfeus.coverage.accuracy import accuracy_simulation, plot_accuracy
from orfeus.coverage.count import plot_gene_coverage

NUCLEOTIDES = ['A','C','G','T']



def coverage_threshold_simulation(data_df,
                                  parameters,
                                  coverages,
                                  iters,
                                  window,
                                  outdir):

    # For each event type
    events = ['uORFdORF','pPRF','mPRF','SCR','ORF']
    for event in events:

        # Sensitivity simulation
        sensitivity = sensitivity_simulation(parameters,
                                             NUCLEOTIDES,
                                             coverages,
                                             iters,
                                             window,
                                             event)

        # Specificity simulation
        specificity = specificity_simulation(parameters,
                                             NUCLEOTIDES,
                                             coverages,
                                             iters,
                                             event)

        # Plot results
        sens_file = os.path.join(outdir, 'sensitivity_' + event + '.pdf')
        spec_file = os.path.join(outdir, 'specificity_' + event + '.pdf')
        plot_sensitivity(sensitivity, event, sens_file)
        plot_specificity(specificity, event, spec_file)

    # Accuracy simulation
    accuracy = accuracy_simulation(parameters,
                                   NUCLEOTIDES,
                                   coverages,
                                   iters)

    # Plot results
    acc_file = os.path.join(outdir, 'accuracy.pdf')
    cov_file = os.path.join(outdir, 'transcripts.pdf')
    plot_accuracy(accuracy, acc_file)
    plot_gene_coverage(data_df, coverages, cov_file)
