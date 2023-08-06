#!/usr/bin/env python

# -----------------------------------------------------------------------------
# Specificity simulation
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


def find_event(path,
               event_idx):
    """
    Determine whether the specified event is present at in the
    path
    Args:
        path: state path
        event_idx: state indices of event
    Returns:
        True or False: whether the event is present
    Raises:

    """
    L = len(path)

    if any(j in path for j in event_idx):
       return True
    else: return False


def specificity_search(true_path,
                       pred_path,
                       altorfs_idx,
                       event):
    """
    Compares the true and predicted paths to determine whether an
    altORF event is incorrectly inferred
    Args:
        true_path: simulated path
        pred_path: predicted path
        altorfs_idx: dictionary mapping more general state type to
            state indices (0-indexed)
        event: event type to look for
            ORF = canonical ORF
            uORF = uORF only
            dORF = dORF only
            uORFdORF = uORF or dORF
            pPRF = +1 frameshift
            mPRF = -1 frameshift
            SCR = stop codon readthrough
    Returns:
        True or False: whether the event is incorrectly inferred
    Raises:

    """
    if event=='pPRF':
        idx = altorfs_idx['X1']
        return find_event(pred_path, idx)

    elif event=='mPRF':
        idx = altorfs_idx['X2']
        return find_event(pred_path, idx)

    elif event=='uORF':
        idx = altorfs_idx['uORF']
        return find_event(pred_path, idx)

    elif event=='dORF':
        idx = altorfs_idx['dORF']
        return find_event(pred_path, idx)

    elif event=='uORFdORF':
        idx = altorfs_idx['uORF'] + altorfs_idx['dORF']
        return find_event(pred_path, idx)

    elif event=='oORF':
        idx = altorfs_idx['oORF']
        return find_event(pred_path, idx)

    elif event=='iORF':
        idx = altorfs_idx['iORF']
        return find_event(pred_path, idx)

    elif event=='oORFiORF':
        idx = altorfs_idx['oORF'] + altorfs_idx['iORF']
        return find_event(pred_path, idx)

    elif event=='SCR':
        idx = altorfs_idx['SCR']
        return find_event(pred_path, idx)

    elif event=='ORF':
        return False

    else:
        logger.error(('Invalid event type specified for specificity calculation. '
                      'Choose from: uORF, dORF, uORFdORF, pPRF, mPRF, SCR, ORF'))


def specificity(p_emit_nt,
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
        coverage: riboseq coverage (mean reads/nt)
        event: event type to look for
            ORF = canonical ORF
            uORF = uORF only
            dORF = dORF only
            uORFdORF = uORF or dORF
            pPRF = +1 frameshift
            mPRF = -1 frameshift
            SCR = stop codon readthrough
    Returns:
        found: 0 if an event was found in the predicted sequence, 1 if not
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
                                      coverage,
                                      event)

    # Check whether the event was correctly predicted
    found = specificity_search(true_path,
                               pred_path,
                               altorfs_idx,
                               event)

    return int(found)


def specificity_simulation(parameters,
                           nts,
                           coverages,
                           iters,
                           event):
    """
    Simulates sequences and compares the true path to the predicted path
        in parallel to estimate specificity of event detection
    Args:
        parameters: all model transition and emission parameters
        nts: list of valid nucleotides
        coverages: mean riboseq coverages to simulate when simulating sequences
        iters: number of sequences to simulate at each coverage value
        event: event type to look for
            ORF = canonical ORF
            uORF = uORF only
            dORF = dORF only
            uORFdORF = uORF or dORF
            pPRF = +1 frameshift
            mPRF = -1 frameshift
            SCR = stop codon readthrough
    Returns:

    Raises:

    """
    states, states_idx, altorfs_idx, \
    p_emit_nt, p_emit_rho, rho_ranges, p_trans, p_trans_rev, \
    prev_states_options, next_states_options = parameters

    log_emit_nt = np.log(p_emit_nt)
    log_emit_rho = np.log(p_emit_rho)
    log_trans = np.log(p_trans)

    result = {}

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
                     coverage,
                     event)]
            results = pool.starmap(specificity, args * iters)
        pool.join()
        res = np.array(results)

        spec = sum(res)/len(res) # TP/(TP+FN)
        result[coverage] = spec
        print('%f coverage specificity: %f' % (coverage, spec))

    return result


def plot_specificity(specificity, event, file):
    """
    Plots mean riboseq coverage per transcript vs mean specificity
    Args:
        specificity: dict mapping mean riboseq coverage to mean specificity
        event: event type to look for
            pred_path = canonical ORF
            uORF = uORF only
            dORF = dORF only
            uORFdORF = uORF or dORF
            pPRF = +1 frameshift
            mPRF = -1 frameshift
            SCR = stop codon readthrough
        file: output file for plot
    Returns:

    Raises:

    """
    # Set plot color
    if event=='uORF' or event=='dORF' or event=='uORFdORF': c = colors[2]
    elif event=='pPRF': c = colors[4]
    elif event=='mPRF': c = colors[5]
    elif event=='SCR': c = colors[6]

    fig, ax = plt.subplots(figsize=(6,4))

    # Plot the results
    x = specificity.keys()
    y = specificity.values()
    ax.scatter(x, y, color=c)

    # Label the axes
    plt.ylim([0,1])
    plt.xlabel('Mean ORF coverage (footprints/nt)', fontsize=12)
    plt.ylabel('Specificity', fontsize=12, rotation='vertical')
    plt.title('Specificity', fontsize=14, weight='bold')

    # Save the plot
    plt.tight_layout()
    plt.savefig(file)
