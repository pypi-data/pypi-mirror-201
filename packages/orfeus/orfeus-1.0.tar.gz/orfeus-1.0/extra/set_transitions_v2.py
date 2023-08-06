#!/usr/bin/env python

# -----------------------------------------------------------------------------
# Set transition probabilities
# Author: Mary Richardson
# Date: 2020.07.07, last update 2023.03.02
# -----------------------------------------------------------------------------

import logging
import numpy as np

logger = logging.getLogger(__name__)

from set_parameters_helper_functions import get_codon, get_nt, normalize


def get_feature_freqs(data_df,
                      f_5UTR=None,
                      f_3UTR=None):
    """
    Calculate the fraction of ORFs with 5'UTRs and 3'UTRs
    Args:
        data_df: pandas DataFrame with all annotation info
        f_5UTR: (optional) float indicating the fraction of ORFs having 5'UTRs
            default is to infer from the input data
        f_3UTR: (optional) float indicating the fraction of ORFs having 3'UTRs
            default is to infer from the input data
    Returns:
        f_5UTR: float indicating the fraction of ORFs having 5'UTRs
        f_3UTR: float indicating the fraction of ORFs having 3'UTRs
    Raises:
        ValueError: No ORFs found in dataset
    """
    # Calculate the total number of genes
    counts_gene = data_df[data_df['feature']=='ORF']['transcript_id'].nunique()

    # Calculate the fraction of genes that start with 5UTRs
    if not f_5UTR:
        counts_5UTR = data_df[data_df['feature']=='5UTR']['transcript_id'].nunique()
        f_5UTR = counts_5UTR/counts_gene

    # Calculate the fraction of genes that end with 3UTRs
    if not f_3UTR:
        counts_3UTR = data_df[data_df['feature']=='3UTR']['transcript_id'].nunique()
        f_3UTR = counts_3UTR/counts_gene

    # Check that gene count is positive
    if counts_gene <= 0:
        f_5UTR  = 0
        f_3UTR = 0
        logging.error('No ORFs found in dataset. Check annotations!')

    return f_5UTR, f_3UTR


def adjust_length(len, orf=False):
    """
    Adjust the mean lengths of 5'UTRs, 3'UTRs, and ORFs
    Args:
        len: int mean length
        orf: boolean indicating whether this length corresponds to an ORF
    Returns:
        adjusted_len: int length converted from nt to codons if it an ORF
    Raises:
        ValueError: Invalid mean length for UTR or ORF
    """
    # Convert to codons and subtract the start and stop codons
    if orf:
        len = len/3 - 2

    # Don't allow zero or negative lengths
    if len <= 0:
        len = 1
        logging.warning(('Invalid mean length for UTR or ORF. '
            'Length set to 1 nucleotide for UTRs or 1 codon for ORFs.'))

    return len


def get_feature_lengths(data_df,
                        len_5UTR=None,
                        len_3UTR=None,
                        len_orf=None,
                        len_uorf=None,
                        len_dorf=None):
    """
    Calculate the mean lengths of 5'UTRs, 3'UTRs, and ORFs
    Args:
        data_df: pandas DataFrame with all annotation info
        len_5UTR: (optional) float indicating the mean length of 5'UTRs
            default is to infer from the input data
        len_3UTR: (optional) float indicating the mean length of 3'UTRs
            default is to infer from the input data
        len_orf: (optional) float indicating the mean length of ORFs
            default is to infer from the input data
        len_uorf: (optional) float indicating the mean length of uORFs
            default is to set equal to len_orf
        len_dorf: (optional) float indicating the mean length of dORFs
            default is to set equal to len_orf
    Returns:
        len_5UTR: float indicating the mean length of 5'UTRs
        len_3UTR: float indicating the mean length of 3'UTRs
        len_orf: loat indicating the mean length of ORFs
        len_uorf: float indicating the mean length of uORFs
        len_dorf: float indicating the mean length of dORFs
    """
    # Group by feature and gene so each feature is counted only once
    group = data_df.groupby(['feature','transcript_id']).mean().reset_index()

    # Calculate the mean length of each feature that is not given
    if not len_5UTR:
        len_5UTR = group[group['feature']=='5UTR']['feature_len'].mean()
    if not len_3UTR:
        len_3UTR = group[group['feature']=='3UTR']['feature_len'].mean()
    if not len_orf:
        len_orf = group[group['feature']=='ORF']['feature_len'].mean()
    if not len_uorf:
        len_uorf = len_uorf
    if not len_dorf:
        len_dorf = len_dorf

    # Aujust the length
    len_5UTR = adjust_length(len_5UTR)
    len_3UTR = adjust_length(len_3UTR)
    len_orf = adjust_length(len_orf, orf=True)
    len_uorf = adjust_length(len_uorf, orf=True)
    len_dorf = adjust_length(len_dorf, orf=True)

    return len_5UTR, len_3UTR, len_orf, len_uorf, len_dorf


def get_feature_codon_freqs(data_df,
                            feature,
                            feature_codons=None):
    """
    Calculate the frequency of each valid codon in this feature
    Args:
        data_df: pandas DataFrame with all annotation info
        feature: string representing the feature ('START','STOP', or 'ORF')
        feature_codons: (optional) list of valid codons for this feature,
            default is to infer from the input data
    Returns:
        codon_freqs: dict mapping each codon to its frequency in this feature
    Raises:
        ValueError: Codons not observed in annotations present in list of
            codons provided for this feature
    """
    # Get the codon frequencies for this feature
    if feature_codons:
        codon_freqs = {}
        for codon in feature_codons:
            # Get the codon frequencies with a pseudocount
            # (in case codons in the list are not observed in annotations)
            codon_freqs[codon] = len(data_df[(data_df['codon_type']==feature) &
                                    (data_df['codon_seq']==codon)]) + 1

            # Warn if unannotated codon included in list
            if codon_freqs[codon] == 1:
                logging.warning(('Codon not observed in annotations present '
                    'in list of %s codons provided: %s.') % (feature, codon))

        codon_freqs = normalize(codon_freqs)

    else:
        # Get the codon frequencies without a pseudocount
        # (only consider codons observed in annotations)
        codon_freqs = data_df[(data_df['codon_type']==feature)] \
                        ['codon_seq'].value_counts(normalize=True).to_dict()

    return codon_freqs


def get_codon_freqs(data_df,
                    codons,
                    start_codons=None,
                    sense_codons=None,
                    stop_codons=None):
    """
    Calculate the frequency of start, sense, and stop codons
    Args:
        data_df: pandas DataFrame with all annotation info
        codons: list of valid codons
        start_codons: (optional) list of valid start codons,
            default is to infer from the input data
        sense_codons: (optional) list of valid sense codons,
            default is to infer from the input data
        stop_codons: (optional) list of valid stop codons,
            default is to infer from the input data
    Returns:
        start_codon_freqs: dict mapping each start codon to its frequency
        sense_codon_freqs: dict mapping each sense codon to its frequency
        stop_codon_freqs: dict mapping each stop codon to its frequency
    Raises:
        ValueError: Invalid codons filtered out of dataset
    """
    # Exclude NaN codons
    data_df = data_df[data_df['codon_seq'].notnull()]
    unfiltered_len = len(data_df)

    # Only consider codons that are valid
    # (exclude 2nt or 1nt fragments and invalid nucleotides)
    data_df = data_df[data_df['codon_seq'].isin(codons)]
    filtered_len = len(data_df)

    # Check if invalid codons were filtered out
    if filtered_len < unfiltered_len:
        logging.warning('Invalid codons filtered out of dataset.')

    # Get codon frequencies for each feature (with a pseudocount)
    start_codon_freqs = \
        get_feature_codon_freqs(data_df, 'START', feature_codons=start_codons)
    sense_codon_freqs = \
        get_feature_codon_freqs(data_df, 'ORF', feature_codons=sense_codons)
    stop_codon_freqs = \
        get_feature_codon_freqs(data_df, 'STOP', feature_codons=stop_codons)

    return start_codon_freqs, sense_codon_freqs, stop_codon_freqs


def set_constants(data_df,
                  codons,
                  f_5UTR=None,
                  f_3UTR=None,
                  len_5UTR=None,
                  len_3UTR=None,
                  len_orf=None,
                  len_uorf=None,
                  len_dorf=None,
                  start_codons=None,
                  sense_codons=None,
                  stop_codons=None):
    """
    Set the constants based on the current data and annotations
    Args:
        data_df: pandas DataFrame of all annotated transcripts
        codons: list of valid codons
        f_5UTR: (optional) float indicating the fraction of ORFs having 5'UTRs
            default is to infer from the input data
        f_3UTR: (optional) float indicating the fraction of ORFs having 3'UTRs
            default is to infer from the input data
        len_5UTR: (optional) float indicating the mean length of 5'UTRs
            default is to infer from the input data
        len_3UTR: (optional) float indicating the mean length of 3'UTRs
            default is to infer from the input data
        len_orf: (optional) float indicating the mean length of ORFs
            default is to infer from the input data
        len_uorf: (optional) float indicating the mean length of uORFs
            default is to set equal to len_orf
        len_dorf: (optional) float indicating the mean length of dORFs
            default is to set equal to len_orf
        start_codons: (optional) list of valid start codons,
            default is to infer from the input data
        sense_codons: (optional) list of valid sense codons,
            default is to infer from the input data
        stop_codons: (optional) list of valid stop codons,
            default is to infer from the input data
    Returns:
        f_5UTR: float indicating the fraction of ORFs having 5'UTRs
        f_3UTR: float indicating the fraction of ORFs having 3'UTRs
        len_5UTR: float indicating the mean length of 5'UTRs
        len_3UTR: float indicating the mean length of 3'UTRs
        len_orf: float indicating the mean length of ORFs
        len_uorf: float indicating the mean length of uORFs
        len_dorf: float indicating the mean length of dORFs
        start_codon_freqs: dict mapping each start codon to its frequency
        sense_codon_freqs: dict mapping each sense codon to its frequency
        stop_codon_freqs: dict mapping each stop codon to its frequency
    Raises:

    """
    # Get frequency of 5'UTRs and 3'UTRs
    f_5UTR, f_3UTR = get_feature_freqs(data_df,
                                       f_5UTR,
                                       f_3UTR)

    # Get mean lengths of 5'UTRs, 3'UTRs, and ORFs
    len_5UTR, len_3UTR, len_orf, len_uorf, len_dorf = \
            get_feature_lengths(data_df,
                                len_5UTR,
                                len_3UTR,
                                len_orf,
                                len_uorf,
                                len_dorf)

    # Get start, sense, and stop codon frequencies
    start_codon_freqs, sense_codon_freqs, stop_codon_freqs = \
        get_codon_freqs(data_df,
                        codons,
                        start_codons,
                        sense_codons,
                        stop_codons)

    return f_5UTR, f_3UTR, len_5UTR, len_3UTR, len_orf, len_uorf, len_dorf, \
            start_codon_freqs, sense_codon_freqs, stop_codon_freqs


def set_transition_probs(states,
                     states_idx,
                     f_5UTR,
                     f_3UTR,
                     len_5UTR,
                     len_3UTR,
                     len_orf,
                     len_uorf,
                     len_dorf,
                     start_codon_freqs,
                     sense_codon_freqs,
                     stop_codon_freqs,
                     parameters):
    """
    Set the probability of transitioning from each state to each other state
    Args:
        states: list of all states in the model
        states_idx: dictionary mapping each general state type to its
             state index (1-indexed)
        f_5UTR: float indicating the fraction of ORFs having 5'UTRs
        f_3UTR: float indicating the fraction of ORFs having 3'UTRs
        len_5UTR: float indicating the mean length of 5'UTRs
        len_3UTR: float indicating the mean length of 3'UTRs
        len_orf: float indicating the mean length of ORFs
        len_uorf: float indicating the mean length of uORFs
        len_dorf: float indicating the mean length of dORFs
        start_codon_freqs: dict mapping each start codon to its frequency
        stop_codon_freqs: dict mapping each stop codon to its frequency
        sense_codon_freqs: dict mapping each sense codon to its frequency
        parameters: altORF probability parameters
    Returns:
        p_trans: the transition probability matrix
    Raises:
        ValueError: Invalid parameter values
        ValueError: Invalid transition probability matrix
    """
    # Unpack parameters
    [alpha, beta, delta, gamma, zeta] = parameters

    # Don't allow invalid parameters
    for parameter in parameters:
        if parameter < 0 or parameter >= 1:
            logging.error(('Invalid parameter provided. Check that alpha, '
                'beta, gamma, delta, and zeta are each greater than or equal '
                'to zero and less than one.'))

    # Prepare the MxM transition matrix (add one to account for begin state)
    M = len(states)
    p_trans = np.zeros((M+1,M+1))


    ################ UTR states

    # Prob of transitioning from begin to 5UTR
    p_trans[0][states_idx['5UTR']+1] = f_5UTR

    # Prob of transitioning from 5UTR to 5UTR
    p_trans[states_idx['5UTR']+1][states_idx['5UTR']+1] = \
        (len_5UTR-1)/len_5UTR * (1-delta)

    # Prob of transitioning from 3UTR to 3UTR
    p_trans[states_idx['3UTR']+1][states_idx['3UTR']+1] = \
        (len_3UTR-1)/len_3UTR * (1-delta) * (1-zeta)

    # Prob of transitioning from 3UTR to end
    p_trans[states_idx['3UTR']+1][0] = 1/len_3UTR * (1-delta)


    ################ Normal states

    # For each START codon row of the transition matrix, update the values
    for i in states_idx['start']:
        codon = get_codon(i-1, states) # Sequence of this codon

        # Prob of transitioning from begin
        p_trans[0][i] = (1-f_5UTR) * start_codon_freqs[codon]

        # Prob of transitioning from 5UTR
        p_trans[states_idx['5UTR']+1][i] = \
            (1/len_5UTR) * start_codon_freqs[codon] * (1-delta)

        # Prob of transitioning from 3UTR(multiple ORFs)
        p_trans[states_idx['3UTR']+1][i] = \
            (len_3UTR-1)/len_3UTR * start_codon_freqs[codon] * (1-delta) * zeta

        # Prob of transitioning to the next SENSE codon
        for j in states_idx['sense']:
            next_codon = get_codon(j-1, states) # Sequence of this codon
            p_trans[i][j] = sense_codon_freqs[next_codon]

    # For each SENSE codon row of the transition matrix, update the values
    for i in states_idx['sense']:
        codon = get_codon(i-1, states) # Sequence of this codon

        # Prob of transitioning to the next SENSE codon
        for j in states_idx['sense']:
            next_codon = get_codon(j-1, states) # Sequence of this codon
            p_trans[i][j] = \
                (len_orf-1)/len_orf * sense_codon_freqs[next_codon] * (1-alpha)

        # Prob of transitioning to the next STOP codon
        for j in states_idx['stop']:
            next_codon = get_codon(j-1, states) # Sequence of this codon
            p_trans[i][j] = \
                1/len_orf * stop_codon_freqs[next_codon] * (1-gamma)

        # Prob of transitioning to the next SCR codon
        if gamma > 0:
            for j in states_idx['stop_SCR']:
                next_codon = get_codon(j-1, states) # Sequence of this codon
                p_trans[i][j] = \
                    1/len_orf * stop_codon_freqs[next_codon] * gamma

        # Prob of transitioning to X1
        if alpha > 0:
            p_trans[i][states_idx['X1']+1] = \
                (len_orf-1)/len_orf * alpha

        # Prob of transitioning from X1
        if alpha > 0:
            p_trans[states_idx['X1']+1][i] = \
                sense_codon_freqs[codon] * (1-beta)

        # Prob of transitioning from X2
        if beta > 0:
            p_trans[states_idx['X2']+1][i] = sense_codon_freqs[codon]

    # For each STOP codon row of the transition matrix, update the values
    for i in states_idx['stop']:
        codon = get_codon(i-1, states) # Sequence of this codon

        # Prob of transitioning to 3UTR
        p_trans[i][states_idx['3UTR']+1] = f_3UTR

        # Prob of transitioning to end
        p_trans[i][0] = (1-f_3UTR)


    ################ SCR states
    # For each SCR codon row of the transition matrix, update the values
    if gamma > 0:
        for i in states_idx['stop_SCR']:
            codon = get_codon(i-1, states) # Sequence of this codon

            # Prob of transitioning to the next SENSE codon
            for j in states_idx['sense']:
                next_codon = get_codon(j-1, states) # Sequence of this codon
                p_trans[i][j] = sense_codon_freqs[next_codon]


    ################ PRF states
    if alpha > 0 and beta > 0:
        # Prob of transitioning from X1 to X2
        p_trans[states_idx['X1']+1][states_idx['X2']+1] = beta


    ################ uORF states
    if delta > 0:
        # For each START codon row of the transition matrix, update the values
        for i in states_idx['start_uORF']:
            codon = get_codon(i-1, states) # Sequence of this codon

            # Prob of transitioning from 5UTR
            p_trans[states_idx['5UTR']+1][i] = \
                start_codon_freqs[codon] * delta

            # Prob of transitioning to the next SENSE codon
            for j in states_idx['sense_uORF']:
                next_codon = get_codon(j-1, states) # Sequence of this codon
                p_trans[i][j] = sense_codon_freqs[next_codon]

        # For each SENSE codon row of the transition matrix, update the values
        for i in states_idx['sense_uORF']:
            codon = get_codon(i-1, states) # Sequence of this codon

            # Prob of transitioning to the next SENSE codon
            for j in states_idx['sense_uORF']:
                next_codon = get_codon(j-1, states) # Sequence of this codon
                p_trans[i][j] = \
                    (len_uorf-1)/len_uorf * sense_codon_freqs[next_codon]

            # Prob of transitioning to the next STOP codon
            for j in states_idx['stop_uORF']:
                next_codon = get_codon(j-1, states) # Sequence of this codon
                p_trans[i][j] = \
                    1/len_uorf * stop_codon_freqs[next_codon]

        # For each STOP codon row of the transition matrix, update the values
        for i in states_idx['stop_uORF']:
            codon = get_codon(i-1, states) # Sequence of this codon

            # Prob of transitioning to 5UTR
            p_trans[i][states_idx['5UTR']+1] = 1


    ################ dORF states
    if delta > 0:
        # For each START codon row of the transition matrix, update the values
        for i in states_idx['start_dORF']:
            codon = get_codon(i-1, states) # Sequence of this codon

            # Prob of transitioning from 3UTR
            p_trans[states_idx['3UTR']+1][i] = \
                start_codon_freqs[codon] * delta

            # Prob of transitioning to the next SENSE codon
            for j in states_idx['sense_dORF']:
                next_codon = get_codon(j-1, states) # Sequence of this codon
                p_trans[i][j] = sense_codon_freqs[next_codon]

        # For each SENSE codon row of the transition matrix, update the values
        for i in states_idx['sense_dORF']:
            codon = get_codon(i-1, states) # Sequence of this codon

            # Prob of transitioning to the next SENSE codon
            for j in states_idx['sense_dORF']:
                next_codon = get_codon(j-1, states) # Sequence of this codon
                p_trans[i][j] = \
                    (len_dorf-1)/len_dorf * sense_codon_freqs[next_codon]

            # Prob of transitioning to the next STOP codon
            for j in states_idx['stop_dORF']:
                next_codon = get_codon(j-1, states) # Sequence of this codon
                p_trans[i][j] = 1/len_dorf * stop_codon_freqs[next_codon]

        # For each STOP codon row of the transition matrix, update the values
        for i in states_idx['stop_dORF']:
            codon = get_codon(i-1, states) # Sequence of this codon

            # Prob of transitioning to 3UTR
            p_trans[i][states_idx['3UTR']+1] = 1


    ################ oORF states
    if epsilon > 0:
        # For each +1 OVERLAP START codon row of the transition matrix, update the values
        for i in states_idx['sense_start_oORF1']:
            codon1, codon2 = get_overlap_codons(i-1, states)

            # Prob of transitioning from sense codon
            for j in states_idx['sense']:
                p_trans[i][j] = epsilon * \
                    sense_codon_freqs[codon1] * start_codon_freqs[codon2]

            # Prob of transitioning to next +1 oORF sense codon
            for j in states_idx['sense_sense_oORF1']:
                codon3, codon4 = get_overlap_codons(j-1, states)
                if codon2[2]==codon3[0]:
                    p_trans[i][j] = \
                        sense_codon_freqs[codon3] * sense_codon_freqs[codon4]

            p_trans[i][i+1] =

            # Prob of transitioning from overlapped nt2/nt1 to overlapped nt3/nt2 within this codon
            p_trans[i+1][i+2] = 1


        for i in range(states_idx['oORF1_sense_start'][0]+1, states_idx['oORF1_sense_start'][-1]+1, 2):
            sense_codon, start_codon = get_overlap_codons(i-1, states) # Sequences of these codons

            # Prob of transitioning from nt1 to nt2 within this codon
            p_trans[i][i+1] = 1

            # Prob of transitioning from nt2 to nt3 within this codon
            for j in range(states_idx['oORF1_start3'][0]+1, states_idx['oORF1_start3'][1]+1):
                next_sense_codon, next_start_codon = get_overlap_codons(j-1, states) # Sequences of these codons
                if start_codon==next_start_codon:
                    p_trans[i+1][j] = overlap1_start_sense_freqs[start_codon][next_sense_codon]

        # For each +2 OVERLAP START codon row of the transition matrix, update the values
        for i in range(states_idx['oORF2_start_extra'][0]+1, states_idx['oORF2_start_extra'][-1]+1, 2):
            sense_codon = get_codons(i-1, states) # Sequences of these codons


        for i in range(states_idx['oORF2_start23'][0]+1, states_idx['oORF2_start23'][1]+1, 2):
            sense_codon, start_codon = get_overlap_codons(i-1, states) # Sequences of these codons

            # Prob of transitioning from nt2 to nt3 within this codon
            p_trans[i][i+1] = 1

            # Prob of transitioning from nt1 to nt2 within this codon
            for j in range(states_idx['oORF2_start1'][0]+1, states_idx['oORF2_start1'][1]+1):
                prev_sense_codon, prev_start_codon = get_overlap_codons(j-1, states) # Sequences of these codons
                if start_codon==prev_start_codon:
                    p_trans[j][i] = overlap2_start_sense_freqs[start_codon][sense_codon]

            # Prob of transitioning into nt3 of this codon to OVERLAP SENSE
            for j in range(states_idx['oORF2_sense1'][0]+1, states_idx['oORF2_sense1'][1]+1):
                next_sense_codon1, next_sense_codon2 = get_overlap_codons(j-1, states) # Sequences of these codons
                if sense_codon==next_sense_codon1:
                    p_trans[i+1][j] = overlap2_sense1_freqs[sense_codon][next_sense_codon2]

        # For each +1 OVERLAP SENSE codon row of the transition matrix, update the values
        for i in range(states_idx['oORF1_sense12'][0]+1, states_idx['oORF1_sense12'][1]+1, 2):
            sense_codon1, sense_codon2 = get_overlap_codons(i-1, states) # Sequences of these codons

            # Prob of transitioning into nt1 of this codon from OVERLAP START
            for j in range(states_idx['oORF1_start3'][0]+1, states_idx['oORF1_start3'][1]+1):
                prev_sense_codon, prev_start_codon = get_overlap_codons(j-1, states) # Sequences of these codons
                if sense_codon1==prev_sense_codon:
                    p_trans[j][i] = overlap1_sense12_freqs[sense_codon1][sense_codon2]

            # Prob of transitioning into nt1 of this codon from OVERLAP SENSE
            for j in range(states_idx['oORF1_sense3'][0]+1, states_idx['oORF1_sense3'][1]+1):
                prev_sense_codon1, prev_sense_codon2 = get_overlap_codons(j-1, states) # Sequences of these codons
                if sense_codon1==prev_sense_codon1:
                    if sense_codon1 in overlap1_sense_stop_freqs:
                        p_trans[j][i] = (len_orf-1)/len_orf * overlap1_sense12_freqs[sense_codon1][sense_codon2]
                    else:
                        p_trans[j][i] = overlap1_sense12_freqs[sense_codon1][sense_codon2]

            # Prob of transitioning from nt1 to nt2 within this codon
            p_trans[i][i+1] = 1

            # Prob of transitioning from nt2 to the next OVERLAP SENSE codon
            for j in range(states_idx['oORF1_sense3'][0]+1, states_idx['oORF1_sense3'][1]+1):
                next_sense_codon1, next_sense_codon2 = get_overlap_codons(j-1, states) # Sequences of these codons
                if sense_codon2==next_sense_codon2:
                    if sense_codon2 in overlap2_sense_stop_freqs:
                        p_trans[i+1][j] = (len_orf-1)/len_orf * overlap1_sense3_freqs[sense_codon2][next_sense_codon1]
                    else:
                        p_trans[i+1][j] = overlap1_sense3_freqs[sense_codon2][next_sense_codon1]

        # For each +2 OVERLAP SENSE codon row of the transition matrix, update the values
        for i in range(states_idx['oORF2_sense23'][0]+1, states_idx['oORF2_sense23'][1]+1, 2):
            sense_codon1, sense_codon2 = get_overlap_codons(i-1, states) # Sequence of these codons

            # Prob of transitioning into nt2 of this codon from OVERLAP SENSE
            for j in range(states_idx['oORF2_sense1'][0]+1, states_idx['oORF2_sense1'][1]+1):
                prev_sense_codon1, prev_sense_codon2 = get_overlap_codons(j-1, states) # Sequences of these codons
                if sense_codon2==prev_sense_codon2:
                    if sense_codon2 in overlap1_sense_stop_freqs:
                        p_trans[j][i] = (len_orf-1)/len_orf * overlap2_sense23_freqs[prev_sense_codon2][sense_codon1]
                    else:
                        p_trans[j][i] = overlap2_sense23_freqs[prev_sense_codon2][sense_codon1]

            # Prob of transitioning from nt2 to nt3 within this codon
            p_trans[i][i+1] = 1

            # Prob of transitioning from nt3 to the next OVERLAP SENSE codon
            for j in range(states_idx['oORF2_sense1'][0]+1, states_idx['oORF2_sense1'][1]+1):
                next_sense_codon1, next_sense_codon2 = get_overlap_codons(j-1, states) # Sequences of these codons
                if sense_codon1==next_sense_codon1:
                    if sense_codon1 in overlap2_sense_stop_freqs:
                        p_trans[i+1][j] = (len_orf-1)/len_orf * overlap2_sense1_freqs[sense_codon1][next_sense_codon2]
                    else:
                        p_trans[i+1][j] = overlap2_sense1_freqs[sense_codon1][next_sense_codon2]

    if epsilon > 0:
        # For each +1 OVERLAP STOP codon row of the transition matrix, update the values
        for i in range(states_idx['oORF2_stop1'][0]+1, states_idx['oORF2_stop1'][1]+1):
            sense_codon, stop_codon = get_overlap_codons(i-1, states) # Sequences of these codons

            # Prob of transitioning into nt1 of this codon from OVERLAP SENSE
            for j in range(states_idx['oORF1_sense12'][0]+1, states_idx['oORF1_sense12'][1]+1, 2):
                prev_sense_codon1, prev_sense_codon2 = get_overlap_codons(j-1, states) # Sequences of these codons
                if sense_codon==prev_sense_codon2:
                    if sense_codon in overlap2_sense_stop_freqs:
                        p_trans[j+1][i] = 1/len_orf * overlap2_sense_stop_freqs[sense_codon][stop_codon]

        for i in range(states_idx['oORF2_stop23'][0]+1, states_idx['oORF2_stop23'][1]+1, 2):
            sense_codon, stop_codon = get_overlap_codons(i-1, states) # Sequences of these codons

            # Prob of transitioning into nt1 of this codon from OVERLAP STOP
            for j in range(states_idx['oORF2_stop1'][0]+1, states_idx['oORF2_stop1'][1]+1):
                prev_sense_codon, prev_stop_codon = get_overlap_codons(j-1, states) # Sequences of these codons
                if stop_codon==prev_stop_codon:
                    p_trans[j][i] = overlap2_stop_freqs[stop_codon][sense_codon]

            # Prob of transitioning from nt2 to nt3 within this codon
            p_trans[i][i+1] = 1

            # Prob of transitioning from nt3 to nt3 in the next SENSE codon
            for j in range(states_idx['sense'][0]+1, states_idx['sense'][1]+1, 3):
                next_codon = get_codon(j-1, states) # Sequences of these codons
                if sense_codon==next_codon:
                    p_trans[i+1][j+2] = 1

        # For each +2 OVERLAP STOP codon row of the transition matrix, update the values
        for i in range(states_idx['oORF1_stop12'][0]+1, states_idx['oORF1_stop12'][1]+1, 2):
            sense_codon, stop_codon = get_overlap_codons(i-1, states) # Sequences of these codons

            # Prob of transitioning into nt1 of this codon from OVERLAP SENSE
            for j in range(states_idx['oORF2_sense1'][0]+1, states_idx['oORF2_sense1'][1]+1):
                prev_sense_codon1, prev_sense_codon2 = get_overlap_codons(j-1, states) # Sequences of these codons
                if sense_codon==prev_sense_codon2:
                    if sense_codon in overlap1_sense_stop_freqs:
                        p_trans[j][i] = 1/len_orf * overlap1_sense_stop_freqs[sense_codon][stop_codon]

            # Prob of transitioning from nt1 to nt2 within this codon
            p_trans[i][i+1] = 1

        for i in range(states_idx['oORF1_stop3'][0]+1, states_idx['oORF1_stop3'][1]+1):
            sense_codon, stop_codon = get_overlap_codons(i-1, states) # Sequences of these codons

            # Prob of transitioning into nt1 of this codon from OVERLAP STOP
            for j in range(states_idx['oORF1_stop12'][0]+1, states_idx['oORF1_stop12'][1]+1, 2):
                prev_sense_codon, prev_stop_codon = get_overlap_codons(j-1, states) # Sequences of these codons
                if stop_codon==prev_stop_codon:
                    p_trans[j+1][i] = overlap1_stop_freqs[stop_codon][sense_codon]

            # Prob of transitioning from nt3 to nt2 in the next SENSE codon
            for j in range(states_idx['sense'][0]+1, states_idx['sense'][1]+1, 3):
                next_codon = get_codon(j-1, states) # Sequences of these codons
                if sense_codon==next_codon:
                    p_trans[i][j+1] = 1

    ################ iORF states
    if epsilon > 0:
        # For each +1 INTERNAL OVERLAP STOP codon row of the transition matrix, update the values
        for i in states_idx['iORF1_stop12']:
            sense_codon, stop_codon = get_overlap_codons(i-1, states) # Sequences of these codons

            # Prob of transitioning into nt1 of this codon from OVERLAP SENSE
            for j in range(states_idx['oORF1_sense3'][0]+1, states_idx['oORF1_sense3'][1]+1):
                prev_sense_codon1, prev_sense_codon2 = get_overlap_codons(j-1, states) # Sequences of these codons
                if sense_codon==prev_sense_codon1:
                    if sense_codon in overlap1_sense_stop_freqs:
                        p_trans[j][i] = 1/len_orf * overlap1_sense_stop_freqs[sense_codon][stop_codon]

            # Prob of transitioning from nt1 to nt2 within this codon
            p_trans[i][i+1] = 1

        for i in range(states_idx['iORF1_stop3'][0]+1, states_idx['iORF1_stop3'][1]+1):
            sense_codon, stop_codon = get_overlap_codons(i-1, states) # Sequences of these codons

            # Prob of transitioning into nt1 of this codon from INTERNAL OVERLAP STOP
            for j in range(states_idx['iORF1_stop12'][0]+1, states_idx['iORF1_stop12'][1]+1, 2):
                prev_sense_codon, prev_stop_codon = get_overlap_codons(j-1, states) # Sequences of these codons
                if stop_codon==prev_stop_codon:
                    p_trans[j+1][i] = overlap1_stop_freqs[stop_codon][sense_codon]

            # Prob of transitioning from nt3 to nt2 in the next SENSE codon
            for j in range(states_idx['sense'][0]+1, states_idx['sense'][1]+1, 3):
                next_codon = get_codon(j-1, states) # Sequences of these codons
                if sense_codon==next_codon:
                    p_trans[i][j+1] = 1

        # For each +2 INTERNAL OVERLAP STOP codon row of the transition matrix, update the values
        for i in range(states_idx['iORF2_stop1'][0]+1, states_idx['iORF2_stop1'][1]+1):
            sense_codon, stop_codon = get_overlap_codons(i-1, states) # Sequences of these codons

            # Prob of transitioning into nt1 of this codon from OVERLAP SENSE
            for j in range(states_idx['oORF2_sense23'][0]+1, states_idx['oORF2_sense23'][1]+1, 2):
                prev_sense_codon1, prev_sense_codon2 = get_overlap_codons(j-1, states) # Sequences of these codons
                if sense_codon==prev_sense_codon1:
                    if sense_codon in overlap2_sense_stop_freqs:
                        p_trans[j+1][i] = 1/len_orf * overlap2_sense_stop_freqs[sense_codon][stop_codon]

        for i in range(states_idx['iORF2_stop23'][0]+1, states_idx['iORF2_stop23'][1]+1, 2):
            sense_codon, stop_codon = get_overlap_codons(i-1, states) # Sequences of these codons

            # Prob of transitioning into nt1 of this codon from INTERNAL OVERLAP STOP
            for j in range(states_idx['iORF2_stop1'][0]+1, states_idx['iORF2_stop1'][1]+1):
                prev_sense_codon, prev_stop_codon = get_overlap_codons(j-1, states) # Sequences of these codons
                if stop_codon==prev_stop_codon:
                    p_trans[j][i] = overlap2_stop_freqs[stop_codon][sense_codon]

            # Prob of transitioning from nt2 to nt3 within this codon
            p_trans[i][i+1] = 1

            # Prob of transitioning from nt3 to nt3 in the next SENSE codon
            for j in range(states_idx['sense'][0]+1, states_idx['sense'][1]+1, 3):
                next_codon = get_codon(j-1, states) # Sequences of these codons
                if sense_codon==next_codon:
                    p_trans[i+1][j+2] = 1


    # Check that transition probabilities leaving each state sum to 1
    if not np.allclose(np.sum(p_trans, axis=1), np.ones(len(p_trans))):
        logging.error(('Invalid transition probability matrix. '
                    'Transitions leaving each state do not sum to 1.'))

    return p_trans


def rev_transition_probs(p_trans):
    """
    Calculate the the reverse transition probabilities for generating a
    sequence backwards
    Args:
        p_trans: the transition probability matrix
    Returns:
        p_trans_rev: the reverse transition probability matrix
    Raises:
        ValueError: Could not generate reverse transition matrix
    """
    # Calculate the stationary distribution (pi)
    try:
        # Calculate the eigenvector for the transpose of the transition probs
        w, v = np.linalg.eig(p_trans.T)

        # Find the eigenvalue that is approximately 1
        # calculate the difference array
        w1 = np.absolute(w-1.0).argmin()

        # Get the eigenvector corresponding to an eigenvalues of 1
        pi = np.real(v)[:,w1]

        # Normalize the eigenvector
        pi = pi/pi.sum()

        # Calcualte the backward transition probs
        M = len(p_trans)
        p_trans_rev = np.zeros([M,M])
        for j in range(M):
            for k in range(M):
                p_trans_rev[j,k] = pi[k] / pi[j] * p_trans[k,j]
        p_trans_rev = p_trans_rev/p_trans_rev.sum(axis=1, keepdims=True)

    except:
        logging.warning('Could not generate reverse transition matrix.')

    return p_trans_rev


def get_prev_states(p_trans):
    """
    Generate a list of all possible previous states for each state
    Args:
        p_trans: the transition probability matrix
    Returns:
        prev_state_options: list of indices of all possible
            (nonzero probability) previous states
    """
    prev_states_options = []

    for col in np.transpose(p_trans):
        this_prev_states = np.flatnonzero(col) # 1-indexed
        prev_states_options.append(this_prev_states)

    return np.array(prev_states_options, dtype=object)


def get_next_states(p_trans):
    """
    Generate a list of all possible next states for each state
    Args:
        p_trans: the transition probability matrix
    Returns:
        next_state_options: list of indices of all possible
            (nonzero probability) next states
    """
    next_states_options = []

    for row in p_trans:
        this_next_states = np.flatnonzero(row) # 1-indexed
        next_states_options.append(this_next_states)

    return np.array(next_states_options, dtype=object)
