#!/usr/bin/env python

# -----------------------------------------------------------------------------
# Accuracy simulation
# Author: Mary Richardson
# Date: 2023.03.20
# -----------------------------------------------------------------------------

import logging
import numpy as np
import multiprocessing as mp
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

from orfeus.hmm.simulation import simulation

colors = ['#6F6F6F','#DDDDDD','#E0BA4D','#9ABC61','#5385AA','#C55A56','#A472A5']


def accuracy_calculation(true_path,
                         pred_path):
    """
    Compares the true and predicted paths to determine the accuracy of the
        prediction
    Args:
        true_path: simulated path
        pred_path: predicted path
    Returns:
        accuracy: mean fraction of states that are correctly assigned in the
            predicted path
    Raises:

    """
    T=0
    # Check how many positions are correctly predicted
    for i in range(len(true_path)):
        if true_path[i] == pred_path[i]:
            T += 1
    accuracy = T/len(true_path)

    return accuracy


def accuracy(p_emit_nt,
             p_emit_rho,
             p_trans,
             p_trans_rev,
             log_emit_nt,
             log_emit_rho,
             log_trans,
             prev_states_options,
             next_states_options,
             nts,
             rho_ranges,
             altorfs_idx,
             coverage,
             event):
    """
    Simulates a path and corresponding sequence of nts and rho values,
    then runs Viterbi on the sequence to predict the path
    Args:
        p_emit_nt: the nucleotide emission probability matrix
        p_emit_rho: the riboseq emission probability matrix
        p_trans: the transition probability matrix
        p_trans_rev: the reverse transition probability matrix
        log_emit_nt: the nucleotide log emission probability matrix
        log_emit_rho: the riboseq log emission probability matrix
        log_trans: the log transition probability matrix
        prev_state_options: list of indices of all possible
            (nonzero probability) previous states
        next_state_options: list of indices of all possible
            (nonzero probability) next states
        nts: list of valid nucleotides
        rho_ranges: array of riboseq emission bin ranges
        altorfs_idx: dictionary mapping more general state type to
            state indices (0-indexed)
    Returns:
        accuracy: mean fraction of states that are correctly assigned in the
            predicted path
    Raises:

    """
    # Simulate a sequence
    true_path, pred_path = simulation(p_emit_nt,
                                      p_emit_rho,
                                      p_trans,
                                      p_trans_rev,
                                      log_emit_nt,
                                      log_emit_rho,
                                      log_trans,
                                      prev_states_options,
                                      next_states_options,
                                      nts,
                                      rho_ranges,
                                      altorfs_idx,
                                      coverage)

    # Calculate the accuracy of the prediction
    accuracy = accuracy_calculation(true_path, pred_path)

    return accuracy


def accuracy_simulation(parameters,
                        nts,
                        coverages,
                        iters):
    """
    Simulates sequences and compares the true path to the predicted path
        in parallel to estimate specificity of event detection
    Args:
        parameters: all model transition and emission parameters
        nts: list of valid nucleotides
        coverages: mean riboseq coverages to simulate when simulating sequences
        iters: number of sequences to simulate at each coverage value
    Returns:

    Raises:

    """
    states, states_idx, altorfs_idx, \
    p_emit_nt, p_emit_rho, rho_ranges, p_trans, p_trans_rev, \
    prev_states_options, next_states_options = parameters

    log_emit_nt = np.log(p_emit_nt)
    log_emit_rho = np.log(p_emit_rho)
    log_trans = np.log(p_trans)

    accuracy = {}

    for coverage in coverages:
        # Simulate sequences in parallel
        with mp.Pool(processes=10) as pool:
            args = [(p_emit_nt,
                     p_emit_rho,
                     p_trans,
                     p_trans_rev,
                     log_emit_nt,
                     log_emit_rho,
                     log_trans,
                     prev_states_options,
                     next_states_options,
                     nts,
                     rho_ranges,
                     altorfs_idx,
                     coverage)]
            results = pool.starmap(accuracy, args * iters)
        pool.join()
        res = np.array(results)

        acc = np.mean(res)
        accuracy[coverage] = acc
        print('%f coverage accuracy: %f' % (coverage, acc))

    return accuracy


def plot_accuracy(accuracy, file):
    """
    Plots mean riboseq coverage per transcript vs mean accuracy
    Args:
        accuracy: dict mapping mean riboseq coverage to mean accuracy
        file: output file for plot
    Returns:

    Raises:

    """
    # Plot the results
    fig, ax = plt.subplots(figsize=(6,4))
    x = accuracy.keys()
    y = accuracy.values()

    ax.scatter(x, y, color=colors[0]) # Plot in grey

    # Label the axes
    plt.ylim([0,1])
    plt.xlabel('Mean ORF coverage (footprints/nt)', fontsize=12)
    plt.ylabel('Mean accuracy', fontsize=12, rotation='vertical')
    plt.title('Viterbi path accuracy', fontsize=14, weight='bold')

    # Save the plot
    plt.tight_layout()
    plt.savefig(plot_file)
