#!/usr/bin/env python

# -----------------------------------------------------------------------------
# Set model states
# Author: Mary Richardson
# Date: 2020.07.07, last update 2023.03.02
# -----------------------------------------------------------------------------

import numpy as np


def set_states(start_codon_freqs,
               sense_codon_freqs,
               stop_codon_freqs,
               parameters):
    """
    Generate a list of all states for this model
    Args:
        start_codon_freqs: dict mapping each start codon to its frequency
        stop_codons_freqs: dict mapping each stop codon to its frequency
        sense_codons_freqs: dict mapping each sense codon to its frequency
        parameters: list of parameter values for
            alpha, beta, gamma, delta, zeta
    Returns:
        states: list of state names
        states_idx: dictionary mapping state type to
            state indices (1-indexed)
        altorfs_idx: dictionary mapping more general state type to
            state indices (0-indexed)
    Raises:
        ValueError: Invalid parameter values. Make sure all parameter values
        are greater than or equal to zero.
    """
    # Unpack parameters
    [alpha, beta, gamma, delta, zeta] = parameters

    # List states and their corresponding indices in the
    # transition and emission matrices
    states = []
    states_idx = {}

    # Create dictionary to store all indices for each type of state
    altorfs_idx = {'5UTR':[],
                   '3UTR':[],
                   'ORF':[],
                   'start':[],
                   'sense':[],
                   'stop':[],
                   'X1':[],
                   'X2':[],
                   'PRF':[],
                   'SCR':[],
                   'uORF':[],
                   'dORF':[],
                   'oORF':[],
                   'iORF':[]}

    # Begin counting indices
    idx = 0

    # Add UTR states
    for state in ['5UTR','3UTR']:
        states += [state]
        states_idx[state] = idx
        altorfs_idx[state] = idx
        idx += 1

    # Add start codon states
    start_states = [(codon + '#') for codon in sorted(start_codon_freqs)]
    states += start_states
    n = len(start_states)
    states_idx['start'] = list(range(idx, idx+n))
    altorfs_idx['start'] = list(range(idx, idx+n))
    altorfs_idx['ORF'] = list(range(idx, idx+n))
    idx += n

    # Add sense codon states
    sense_states = [(codon) for codon in sorted(sense_codon_freqs)]
    states += sense_states
    n = len(sense_states)
    states_idx['sense'] = list(range(idx, idx+n))
    altorfs_idx['sense'] = list(range(idx, idx+n))
    altorfs_idx['ORF'] += list(range(idx, idx+n))
    idx += n

    # Add stop codon states
    stop_states = [(codon + '*') for codon in sorted(stop_codon_freqs)]
    states += stop_states
    n = len(stop_states)
    states_idx['stop'] = list(range(idx, idx+n))
    altorfs_idx['stop'] = list(range(idx, idx+n))
    altorfs_idx['ORF'] += list(range(idx, idx+n))
    idx += n

    # Add PRF states
    if alpha > 0:

        # Add X1 state
        states += ['X1']
        states_idx['X1'] = idx
        altorfs_idx['X1'] = idx
        altorfs_idx['PRF'] = [idx]
        idx += 1

    if alpha > 0 and beta > 0:

        # Add X2 state
        states += ['X2']
        states_idx['X2'] = idx
        altorfs_idx['X2'] = idx
        altorfs_idx['PRF'] += [idx]
        idx += 1

    # Add SCR states
    if gamma > 0:

        # Add stop codon readthrough states
        stop_states = [(codon + '**') for codon in sorted(stop_codon_freqs)]
        states += stop_states
        n = len(stop_states)
        states_idx['stop_SCR'] = list(range(idx, idx+n))
        altorfs_idx['SCR'] = list(range(idx, idx+n))
        idx += n

    # Add uORF and dORF states
    if delta > 0:

        # Add uORF start codon states
        start_states = [(codon + '#u') for codon in sorted(start_codon_freqs)]
        states += start_states
        n = len(start_states)
        states_idx['start_uORF'] = list(range(idx, idx+n))
        altorfs_idx['start_uORF'] = list(range(idx, idx+n))
        altorfs_idx['uORF'] = list(range(idx, idx+n))
        idx += n

        # Add uORF sense codon states
        sense_states = [(codon + 'u') for codon in sorted(sense_codon_freqs)]
        states += sense_states
        n = len(sense_states)
        states_idx['sense_uORF'] = list(range(idx, idx+n))
        altorfs_idx['uORF'] += list(range(idx, idx+n))
        idx += n

        # Add uORF stop codon states
        stop_states = [(codon + '*u') for codon in sorted(stop_codon_freqs)]
        states += stop_states
        n = len(stop_states)
        states_idx['stop_uORF'] = list(range(idx, idx+n))
        altorfs_idx['stop_uORF'] = list(range(idx, idx+n))
        altorfs_idx['uORF'] += list(range(idx, idx+n))
        idx += n

        # Add dORF start codon states
        start_states = [(codon + '#d') for codon in sorted(start_codon_freqs)]
        states += start_states
        n = len(start_states)
        states_idx['start_dORF'] = list(range(idx, idx+n))
        altorfs_idx['start_dORF'] = list(range(idx, idx+n))
        altorfs_idx['dORF'] = list(range(idx, idx+n))
        idx += n

        # Add dORF sense codon states
        sense_states = [(codon + 'd') for codon in sorted(sense_codon_freqs)]
        states += sense_states
        n = len(sense_states)
        states_idx['sense_dORF'] = list(range(idx, idx+n))
        altorfs_idx['dORF'] += list(range(idx, idx+n))
        idx += n

        # Add dORF stop codon states
        stop_states = [(codon + '*d') for codon in sorted(stop_codon_freqs)]
        states += stop_states
        n = len(stop_states)
        states_idx['stop_dORF'] = list(range(idx, idx+n))
        altorfs_idx['stop_dORF'] = list(range(idx, idx+n))
        altorfs_idx['dORF'] += list(range(idx, idx+n))
        idx += n

    # Add oORF states
    if epsilon > 0:

        states_idx['sense_start_oORF1'] = []
        states_idx['sense_start_oORF2'] = []
        states_idx['sense_sense_oORF1'] = []
        states_idx['sense_sense_oORF2'] = []
        states_idx['stop_sense_oORF1'] = []
        states_idx['stop_sense_oORF2'] = []
        states_idx['sense_stop_iORF1'] = []
        states_idx['sense_stop_iORF2'] = []
        states_idx['sense_iORF1'] = []
        states_idx['sense_iORF2'] = []

        altorfs_idx['start_oORF'] = []
        altorfs_idx['sense_oORF'] = []
        altorfs_idx['stop_oORF'] = []
        altorfs_idx['stop_iORF'] = []
        altorfs_idx['oORF']
        altorfs_idx['iORF']

        for codon1 in sorted(sense_codon_freqs):

            # Add +1 and +2 overlapping start codon states
            for codon2 in sorted(start_codon_freqs):
                if codon1[1] == codon2[0] and codon1[2] == codon2[1]:
                    states += [(codon1 + '_' + codon2 + '#')]
                    states_idx['sense_start_oORF1'] += [idx]
                    altorfs_idx['start_oORF'] += [idx]
                    altorfs_idx['oORF'] += [idx]
                    idx += 1
                if codon1[2] == codon2[0]:
                    states += [(codon1 + '_' + codon2 + '#')]
                    states_idx['sense_start_oORF2'] += [idx]
                    altorfs_idx['start_oORF'] += [idx]
                    altorfs_idx['oORF'] += [idx]
                    idx += 1

            # Add +1 and +2 overlapping sense codon states
            for codon2 in sorted(sense_codon_freqs):
                if codon1[1] == codon2[0] and codon1[2] == codon2[1]:
                    states += [(codon1 + '_' + codon2)]
                    states_idx['sense_sense_oORF1'] += [idx]
                    altorfs_idx['sense_oORF'] += [idx]
                    altorfs_idx['oORF'] += [idx]
                    idx += 1
                if codon1[2] == codon2[0]:
                    states += [(codon1 + '_' + codon2)]
                    states_idx['sense_sense_oORF2'] += [idx]
                    altorfs_idx['sense_oORF'] += [idx]
                    altorfs_idx['oORF'] += [idx]
                    idx += 1

            # Add +1 and +2 overlapping stop codon states
            for codon2 in sorted(stop_codon_freqs):
                if codon2[1] == codon1[0] and codon2[2] == codon1[1]:
                    states += [(codon2 + '*' + '_' + codon1)]
                    states_idx['stop_sense_oORF1'] += [idx]
                    altorfs_idx['stop_oORF'] += [idx]
                    altorfs_idx['oORF'] += [idx]
                    idx += 1
                if codon2[2] == codon1[0]:
                    states += [(codon2 + '*' + '_' + codon1)]
                    states_idx['stop_sense_oORF1'] += [idx]
                    altorfs_idx['stop_oORF'] += [idx]
                    altorfs_idx['oORF'] += [idx]
                    idx += 1

            # Add +1 and +2 internal stop codon states
            for codon2 in sorted(stop_codon_freqs):
                if codon1[1] == codon2[0] and codon1[2] == codon2[1]:
                    states += [(codon1 + '_' + codon2 + '*')]
                    states_idx['sense_stop_iORF1'] += [idx]
                    altorfs_idx['stop_iORF'] += [idx]
                    altorfs_idx['iORF'] += [idx]
                    idx += 1
                if codon1[2] == codon2[0]:
                    states += [(codon1 + '_' + codon2 + '*')]
                    states_idx['sense_stop_iORF1'] += [idx]
                    altorfs_idx['stop_iORF'] += [idx]
                    altorfs_idx['iORF'] += [idx]
                    idx += 1

            # Add +1 and +2 extra sense codon states after iORF
            states += [(codon1)]
            states_idx['sense_iORF1'] += [idx]
            idx += 1
            states += [(codon1)]
            states_idx['sense_iORF2'] += [idx]
            idx += 1

    return states, states_idx, altorfs_idx
