#!/usr/bin/env python

# -----------------------------------------------------------------------------
# Hidden Markov Model
# Author: Adapted from code by Sebastian Böck <sebastian.boeck@jku.at>
# available from https://github.com/CPJKU/schimmel/blob/master/hmm.pyx
# Date: 2022.06.10
# -----------------------------------------------------------------------------

import numpy as np
cimport numpy as np
cimport cython
from cython.parallel cimport prange

cdef extern from 'math.h':
    float INFINITY


NUCLEOTIDES = ['A','C','G','T']
CODONS = [''.join(i) for i in it.product(NUCLEOTIDES, repeat = 3)]



class States():
    """States class for an HMM"""

    def __init__(self,
                 parameters,
                 start_codons=[],
                 sense_codons=[],
                 stop_codons=[]):
        """
        Construct a Transitions instance
        Args:
            states: list of state indices
            parameters: list of parameter values for
                            alpha, beta, gamma, delta, zeta
        Returns:

        Raises:

        """
        self.parameters = parameters
        self.start_codons = start_codons
        self.sense_codons = sense_codons
        self.stop_codons = stop_codons
        self.states, self.states_idx, self.altorfs_idx = \
            set_states(start_codons,
                       sense_codons,
                       stop_codons,
                       parameters)

    @property
    def num_states(self):
        """Number of states"""
        return len(self.states)

    @staticmethod
    def set_states(start_codons,
                   sense_codons,
                   stop_codons,
                   parameters):
        """
        Generate a list of all states for this model
        Args:
            start_codons: list of valid start codons
            sense_codons: list of valid sense codons
            stop_codons: list of valid stop codons
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
        # List parameters
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
                       'SCR':[],
                       'uORF':[],
                       'dORF':[]}

        # Begin counting indices
        idx = 0

        # Add UTR states
        for state in ['5UTR','3UTR']:
            states += [state]
            states_idx[state] = idx
            altorfs_idx[state] = idx
            idx += 1

        # Add start codon states
        states += [(codon + '#') for codon in sorted(start_codon_freqs)]
        n = len(start_codon_freqs)
        states_idx['start'] = list(range(idx, idx+n))
        altorfs_idx['start'] = list(range(idx, idx+n))
        altorfs_idx['ORF'] = list(range(idx, idx+n))
        idx += n

        # Add sense codon states
        states += [(codon) for state in sorted(sense_codon_freqs)]
        n = len(sense_codon_freqs)
        states_idx['sense'] = list(range(idx, idx+n))
        altorfs_idx['sense'] = list(range(idx, idx+n))
        altorfs_idx['ORF'] += list(range(idx, idx+n))
        idx += n

        # Add stop codon states
        states += [(codon + '*') for state in sorted(stop_codon_freqs)]
        n = len(stop_codon_freqs)
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
            idx += 1

        if alpha > 0 and beta > 0:

            # Add X2 state
            states += ['X2']
            states_idx['X2'] = idx
            altorfs_idx['X2'] = idx
            idx += 1

        # Add SCR states
        if gamma > 0:

            # Add stop codon readthrough states
            states += [(codon + '**') for state in sorted(stop_codon_freqs)]
            n = len(stop_codon_freqs)
            states_idx['stop_SCR'] = list(range(idx, idx+n))
            altorfs_idx['SCR'] = list(range(idx, idx+n))
            idx += n

        # Add uORF and dORF states
        if delta > 0:

            # Add uORF start codon states
            states += [(codon + '#u') for state in sorted(start_codon_freqs)]
            n = len(start_codon_freqs)
            states_idx['start_uORF'] = list(range(idx, idx+n))
            altorfs_idx['start_uORF'] = list(range(idx, idx+n))
            altorfs_idx['uORF'] += list(range(idx, idx+n))
            idx += n

            # Add uORF sense codon states
            states += [(codon + 'u') for state in sorted(sense_codon_freqs)]
            n = len(sense_codon_freqs)
            states_idx['sense_uORF'] = list(range(idx, idx+n))
            altorfs_idx['uORF'] += list(range(idx, idx+n))
            idx += n

            # Add uORF stop codon states
            states += [(codon + '*u') for state in sorted(stop_codon_freqs)]
            n = len(stop_codon_freqs)
            states_idx['stop_uORF'] = list(range(idx, idx+n))
            altorfs_idx['stop_uORF'] = list(range(idx, idx+n))
            altorfs_idx['uORF'] += list(range(idx, idx+n))
            idx += n

            # Add dORF start codon states
            states += [(codon + '#d') for state in sorted(start_codon_freqs)]
            n = len(start_codon_freqs)
            states_idx['start_dORF'] = list(range(idx, idx+n))
            altorfs_idx['start_dORF'] = list(range(idx, idx+n))
            altorfs_idx['dORF'] = list(range(idx, idx+n))
            idx += n

            # Add dORF sense codon states
            states += [(codon + 'd') for state in sorted(sense_codon_freqs)]
            n = len(sense_codon_freqs)
            states_idx['sense_dORF'] = list(range(idx, idx+n))
            altorfs_idx['dORF'] += list(range(idx, idx+n))
            idx += n

            # Add dORF stop codon states
            states += [(codon + '*d') for state in sorted(stop_codon_freqs)]
            n = len(stop_codon_freqs)
            states_idx['stop_dORF'] = list(range(idx, idx+n))
            altorfs_idx['stop_dORF'] = list(range(idx, idx+n))
            altorfs_idx['dORF'] += list(range(idx, idx+n))
            idx += n

        return states, states_idx, altorfs_idx



class Transitions():
    """Transition probabilities class for an HMM"""

    def __init__(self,
                 states,
                 pointers,
                 probabilities):
        """
        Construct a Transitions instance
        Args:
            states: list of state indices
            pointers: states transitioning to state s are stored in
                states[pointers[s]:pointers[s+1]]
            probabilities: corresponding transition probabilities are stored in
                probabilities[pointers[s]:pointers[s+1]]
        Returns:

        Raises:

        """
        self.states = states
        self.pointers = pointers
        self.probabilities = probabilities

    @property
    def num_transitions(self):
        """Number of transitions"""
        return len(self.probabilities)

    @property
    def log_probabilities(self):
        """Transition log probabilities"""
        return np.log(self.probabilities)

    @staticmethod
    def make_sparse(dense_transitions):
        """
        Generate a sparse representation of transition probabilities
        Allows for fast and parallel Viterbi decoding
        Args:
            dense_transitions: numpy array of transition matrix probabilities,
                where each value is the probability of transitioning from state
                row into state col
        Returns:
            states: list of state indices
            pointers: states transitioning to state s are stored in
                indices[pointers[s]:pointers[s+1]]
            probabilities: corresponding transition probabilities are stored in
                probabilities[pointers[s]:pointers[s+1]]
        Raises:
            ValueError: Invalid transition probability matrix
        """
        from scipy.sparse import csr_matrix

        # Check that transition probabilities leaving each state sum to 1
        if not np.allclose(np.sum(dense_transitions(axis=0))), len(dense_transitions)):
            raise ValueError('Invalid transition probability matrix. \
                            Transitions leaving each state do not sum to 1.')

        # Convert transitions to a sparse CSR matrix
        # Transpose so each value is the probability of
        # transitioning from state col into state row
        transitions = csr_matrix(dense_transitions.T)

        # Extract the states, pointers, and probabilities
        # defining the sparse matrix
        states = transitions.states.astype(np.uint32)
        pointers = transitions.indptr.astype(np.uint32)
        probabilities = transitions.data.astype(dtype=np.float)

        return states, pointers, probabilities

    @classmethod
    def from_dense(cls, dense_transitions):
        """
        Create a Transitions instance from a transitions matrix
        Args:
            dense_transitions: numpy array of transition matrix probabilities,
                where each value is the probability of transitioning from state
                row into state col
        Returns:
            transitions: Transitions instance of the transition matrix
        Raises:

        """
        # Generate a sparse representation of the transitions matrix
        transitions = cls.make_sparse(dense_transitions)

        # Return a new Transitions instance
        return cls(*transitions)


class ORFeusTransitions(Transitions):

    def __init__(self,
                 data_df,
                 model_states,
                 len_5UTR=None,
                 len_3UTR=None,
                 len_orf=None,
                 len_uorf=None,
                 len_dorf=None):

        # Generate the transitions matrix as a dense array
        dense_transitions = set_probabilities(data_df,
                                              model_states,
                                              len_5UTR=None,
                                              len_3UTR=None,
                                              len_orf=None,
                                              len_uorf=None,
                                              len_dorf=None)

        # Convert the transitions matrix to a sparse array
        sparse_transitions = self.from_dense(dense_transitions)

        # Instantiate
        super(ORFeusTransitions, self).__init__(*sparse_transitions)

    @staticmethod
    def normalize(d):
        """Normalize the values of a dictionary
        Args:
            d: dictionary with numerical values
        Returns:
            normalized_d: dictionary with values normalized so they sum to 1
        """
        factor = 1.0/sum(d.values())
        normalized_d = {k: v*factor for k, v in d.items()}
        return normalized_d

    def get_codon(self, i):
        """Get the codon sequence for this state
        Args:
            i: index of state
        Returns:
            codon: codon sequence
        """
        state = self.states[i]   # Label for this state (e.g. 'ATG1#')
        codon = state[:3]        # Sequence of this codon
        return codon

    def get_nt(self, i):
        """Get the subcodon nucleotide position for this state
        Args:
            i: index of state
        Returns:
            nt: nucleotide position in codon (1, 2, or 3)
        """
        state = self.states[i] # Label for this state (e.g. 'ATG1#')
        nt = int(state[3])  # Subcodon nucleotide of this codon
        nt = nt-1
        return nt

    @staticmethod
    def get_feature_freqs(data_df):
        """
        Calculate the fraction of ORFs with 5'UTRs and 3'UTRs
        Args:
            data_df: pandas DataFrame with all annotation info
        Returns:
            f_5UTR: float indicating the fraction of ORFs having 5'UTRs
            f_3UTR: float indicating the fraction of ORFs having 3'UTRs
        Raises:
            ValueError: No ORFs found in dataset
        """
        # Calculate the total number of each feature (5UTR, 3UTR, gene)
        counts_5UTR = data_df[data_df['feature']=='5UTR']['gene_id'].nunique()
        counts_gene = data_df[data_df['feature']=='ORF']['gene_id'].nunique()
        counts_3UTR = data_df[data_df['feature']=='3UTR']['gene_id'].nunique()

        # Calculate the fraction of 5UTRs and 3UTRs
        f_5UTR = counts_5UTR/counts_gene  # Fraction of genes starting with 5'UTR
        f_3UTR = counts_3UTR/counts_gene  # Fraction of genes ending with 3'UTR

        # Check that gene count is positive
        if counts_gene <= 0:
            raise ValueError('No ORFs found in dataset.')

        return f_5UTR, f_3UTR

    @staticmethod
    def adjust_length(len,
                      orf=False):
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
        # Don't allow zero or negative lengths
        if len <= 0:
            adjusted_len = 1
            raise ValueError('Invalid mean length for UTR or ORF. \
                Length set to 1.')

        # Convert to codons and subtract the start and stop codons
        if orf:
            adjusted_len = adjusted_len/3 - 2

        return adjusted_len

    @staticmethod
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
        Returns:
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
        Raises:

        """
        # Group by feature and gene so each feature is counted only once
        group = data_df.groupby(['feature','gene_id']).mean().reset_index()

        # Calculate the mean length of each feature that is not given
        if not len_5UTR:
            len_5UTR = group[group['feature']=='5UTR']['feature_length'].mean()
        if not len_3UTR:
            len_3UTR = group[group['feature']=='3UTR']['feature_length'].mean()
        if not len_orf:
            len_orf = group[group['feature']=='ORF']['feature_length'].mean()
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

    @staticmethod
    def get_feature_codon_freqs(data_df,
                                feature,
                                codons=[]):
        """
        Calculate the frequency of each valid codon in this feature
        Args:
            data_df: pandas DataFrame with all annotation info
            feature: string representing the feature ('START','STOP', or 'ORF')
            codons: (optional) list of valid codons for this feature,
                default is to infer from the input data
        Returns:
            codon_freqs: dict mapping each codon to its frequency in this feature
            codons: list of codons for this feature
        Raises:

        """
        # Get the codon frequencies for this feature (with a pseudocount)
        if codons != []:
            codon_freqs = {}
            for codon in codons:
                codon_freqs[codon] = len(data_df[(data_df['codon_type']==feature) &
                                        (data_df['codon_seq']==codon)]) + 1
            codon_freqs = normalize(codon_freqs)
        else:
            codon_freqs = data_df[(data_df['codon_type']==feature)]
                            ['codon_seq'].value_counts(normalize=True).to_dict()
            codons = codon_freqs.keys()

        return codon_freqs, codons

    @staticmethod
    def get_codon_freqs(data_df,
                        start_codons=[],
                        sense_codons=[],
                        stop_codons=[]):
        """
        Calculate the frequency of start, sense, and stop codons
        Args:
            data_df: pandas DataFrame with all annotation info
            start_codons: (optional) list of valid start codons,
                default is to infer from the input data
            sense_codons: (optional) list of valid sense codons,
                default is to infer from the input data
            stop_codons: (optional) list of valid stop codons,
                default is to infer from the input data
        Returns:
            start_codons: list of start codons
            sense_codons: list of sense codons
            stop_codons: list of stop codons
            start_codon_freqs: dict mapping each start codon to its frequency
            stop_codons_freqs: dict mapping each stop codon to its frequency
            sense_codons_freqs: dict mapping each sense codon to its frequency
        Raises:
            ValueError: Invalid codons filtered out of dataset.
        """
        # Exclude NaN codons
        data_df = data_df[data_df['codon_seq'].notnull()]
        unfiltered_len = len(data_df)

        # Only consider codons that are valid
        # (exclude 2nt or 1nt fragments and invalid nucleotides)
        data_df = data_df[data_df['codon_seq'].isin(CODONS)]
        filtered_len = len(data_df)

        # Check if invalid codons were filtered out
        if filtered_len < unfiltered_len:
            raise ValueError('Invalid codons filtered out of dataset.')

        # Get codon frequencies for each feature (with a pseudocount)
        start_codon_freqs, start_codons =
            get_feature_codon_freqs(data_df, 'START', codons=start_codons)
        sense_codon_freqs, sense_codons =
            et_feature_codon_freqs(data_df, 'ORF', codons=sense_codons)
        stop_codon_freqs, stop_codons =
            get_feature_codon_freqs(data_df, 'STOP', codons=stop_codons)

        return start_codons, sense_codons, stop_codons

    @staticmethod
    def set_probabilities(data_df,
                          model_states,
                          len_5UTR=None,
                          len_3UTR=None,
                          len_orf=None,
                          len_uorf=None,
                          len_dorf=None):
        """
        Set the probability of transitioning from each state to each other state
        Args:
            data_df: pandas DataFrame with all annotation info
            model_states: States object contatining all state info for the
                current model instance
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
            p_trans: the transition probability matrix
        Raises:

        """
        # Unpack parameters
        [alpha, beta, delta, gamma, epsilon] = model_states.parameters

        # Get frequency of 5'UTRs and 3'UTRs
        f_5UTR, f_3UTR = get_feature_freqs(data_df)

        # Get mean lengths of 5'UTRs, 3'UTRs, and ORFs
        len_5UTR, len_3UTR, len_orf, len_uorf, len_dorf =
            get_feature_lengths(data_df, len_5UTR, len_3UTR,
                len_orf, len_uorf, len_dorf)

        # Get start, sense, stop, and overlapping codon frequencies
        start_codons, sense_codons, stop_codons, \
            start_codon_freqs, sense_codon_freqs, stop_codon_freqs, \
            get_codon_freqs(data_df, model_states.start_codons,
                model_states.sense_codons, model_states.stop_codons):

        # Prepare the MxM transition matrix (add one to account for begin state)
        M = self.model_states.num_states
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
        for i in range(states_idx['start'][0]+1,
                       states_idx['start'][-1]+1, 3):
            codon = get_codon(i-1, states) # Sequence of this codon

            # Prob of transitioning from begin to nt1
            p_trans[0][i] = (1-f_5UTR) * start_codon_freqs[codon]

            # Prob of transitioning from 5UTR to nt1
            p_trans[states_idx['5UTR']+1][i] = \
                (1/len_5UTR) * start_codon_freqs[codon] * (1-delta)

            # Prob of transitioning from 3UTR to nt1 (multiple ORFs)
            p_trans[states_idx['3UTR']+1][i] = \
                (len_3UTR-1)/len_3UTR * start_codon_freqs[codon] * (1-delta) * zeta

            # Prob of transitioning from nt1 to nt2 within this codon
            p_trans[i][i+1] = 1

            # Prob of transitioning from nt2 to nt3 within this codon
            p_trans[i+1][i+2] = 1

            # Prob of transitioning from nt3 to nt1 in the next SENSE codon
            for j in range(states_idx['sense'][0]+1,
                           states_idx['sense'][-1]+1, 3):
                next_codon = get_codon(j-1, states) # Sequence of this codon
                p_trans[i+2][j] = sense_codon_freqs[next_codon]

        # For each SENSE codon row of the transition matrix, update the values
        for i in range(states_idx['sense'][0]+1,
                       states_idx['sense'][-1]+1, 3):
            codon = get_codon(i-1, states) # Sequence of this codon

            # Prob of transitioning from nt1 to nt2 within this codon
            p_trans[i][i+1] = 1

            # Prob of transitioning from nt2 to nt3 within this codon
            p_trans[i+1][i+2] = 1

            # Prob of transitioning from nt3 to nt1 in the next SENSE codon
            for j in range(states_idx['sense'][0]+1,
                           states_idx['sense'][-1]+1, 3):
                next_codon = get_codon(j-1, states) # Sequence of this codon
                p_trans[i+2][j] = \
                    (len_orf-1)/len_orf * sense_codon_freqs[next_codon] * (1-alpha)

            # Prob of transitioning from nt3 to nt1 in the next STOP codon
            for j in range(states_idx['stop'][0]+1, states_idx['stop'][-1]+1, 3):
                next_codon = get_codon(j-1, states) # Sequence of this codon
                p_trans[i+2][j] = \
                    1/len_orf * stop_codon_freqs[next_codon] * (1-gamma)

            # Prob of transitioning from nt3 to nt1 in the next SCR codon
            if gamma > 0:
                for j in range(states_idx['stop_SCR'][0]+1,
                               states_idx['stop_SCR'][-1]+1, 3):
                    next_codon = get_codon(j-1, states) # Sequence of this codon
                    p_trans[i+2][j] = \
                        1/len_orf * stop_codon_freqs[next_codon] * gamma

            # Prob of transitioning from nt3 to X1
            if alpha > 0:
                p_trans[i+2][states_idx['X1']+1] = \
                    (len_orf-1)/len_orf * alpha

            # Prob of transitioning from X1 to nt1 in this codon
            if alpha > 0:
                p_trans[states_idx['X1']+1][i] = \
                    sense_codon_freqs[codon] * (1-beta)

            # Prob of transitioning from X2 to nt1 in this codon
            if beta > 0:
                p_trans[states_idx['X2']+1][i] = sense_codon_freqs[codon]

        # For each STOP codon row of the transition matrix, update the values
        for i in range(states_idx['stop'][0]+1,
                       states_idx['stop'][-1]+1, 3):
            codon = get_codon(i-1, states) # Sequence of this codon

            # Prob of transitioning from nt1 to nt2 within this codon
            p_trans[i][i+1] = 1

            # Prob of transitioning from nt2 to nt3 within this codon
            p_trans[i+1][i+2] = 1

            # Prob of transitioning from nt3 to 3UTR
            p_trans[i+2][states_idx['3UTR']+1] = f_3UTR

            # Prob of transitioning from nt3 to end
            p_trans[i+2][0] = (1-f_3UTR)


        ################ SCR states
        # For each SCR codon row of the transition matrix, update the values
        if gamma > 0:
            for i in range(states_idx['stop_SCR'][0]+1,
                           states_idx['stop_SCR'][-1]+1, 3):
                codon = get_codon(i-1, states) # Sequence of this codon

                # Prob of transitioning from nt1 to nt2 within this codon
                p_trans[i][i+1] = 1

                # Prob of transitioning from nt2 to nt3 within this codon
                p_trans[i+1][i+2] = 1

                # Prob of transitioning from nt3 to nt1 in the next SENSE codon
                for j in range(states_idx['sense'][0]+1,
                               states_idx['sense'][-1]+1, 3):
                    next_codon = get_codon(j-1, states) # Sequence of this codon
                    p_trans[i+2][j] = sense_codon_freqs[next_codon]


        ################ PRF states
        if alpha > 0 and beta > 0:
            # Prob of transitioning from X1 to X2
            p_trans[states_idx['X1']+1][states_idx['X2']+1] = beta


        ################ uORF states
        if delta > 0:
            # For each START codon row of the transition matrix, update the values
            for i in range(states_idx['start_uORF'][0]+1, \
                           states_idx['start_uORF'][-1]+1, 3):
                codon = get_codon(i-1, states) # Sequence of this codon

                # Prob of transitioning from 5UTR to nt1
                p_trans[states_idx['5UTR']+1][i] = \
                    start_codon_freqs[codon] * delta

                # Prob of transitioning from nt1 to nt2 within this codon
                p_trans[i][i+1] = 1

                # Prob of transitioning from nt2 to nt3 within this codon
                p_trans[i+1][i+2] = 1

                # Prob of transitioning from nt3 to nt1 in the next SENSE codon
                for j in range(states_idx['sense_uORF'][0]+1, \
                               states_idx['sense_uORF'][-1]+1, 3):
                    next_codon = get_codon(j-1, states) # Sequence of this codon
                    p_trans[i+2][j] = sense_codon_freqs[next_codon]

            # For each SENSE codon row of the transition matrix, update the values
            for i in range(states_idx['sense_uORF'][0]+1, \
                           states_idx['sense_uORF'][-1]+1, 3):
                codon = get_codon(i-1, states) # Sequence of this codon

                # Prob of transitioning from nt1 to nt2 within this codon
                p_trans[i][i+1] = 1

                # Prob of transitioning from nt2 to nt3 within this codon
                p_trans[i+1][i+2] = 1

                # Prob of transitioning from nt3 to nt1 in the next SENSE codon
                for j in range(states_idx['sense_uORF'][0]+1, \
                               states_idx['sense_uORF'][-1]+1, 3):
                    next_codon = get_codon(j-1, states) # Sequence of this codon
                    p_trans[i+2][j] = \
                        (len_uorf-1)/len_uorf * sense_codon_freqs[next_codon]

                # Prob of transitioning from nt3 to nt1 in the next STOP codon
                for j in range(states_idx['stop_uORF'][0]+1, \
                               states_idx['stop_uORF'][-1]+1, 3):
                    next_codon = get_codon(j-1, states) # Sequence of this codon
                    p_trans[i+2][j] = \
                        1/len_uorf * stop_codon_freqs[next_codon]

            # For each STOP codon row of the transition matrix, update the values
            for i in range(states_idx['stop_uORF'][0]+1, \
                           states_idx['stop_uORF'][-1]+1, 3):
                codon = get_codon(i-1, states) # Sequence of this codon

                # Prob of transitioning from nt1 to nt2 within this codon
                p_trans[i][i+1] = 1

                # Prob of transitioning from nt2 to nt3 within this codon
                p_trans[i+1][i+2] = 1

                # Prob of transitioning from nt3 to 5UTR
                p_trans[i+2][states_idx['5UTR']+1] = 1


        ################ dORF states
        if delta > 0:
            # For each START codon row of the transition matrix, update the values
            for i in range(states_idx['start_dORF'][0]+1, \
                           states_idx['start_dORF'][-1]+1, 3):
                codon = get_codon(i-1, states) # Sequence of this codon

                # Prob of transitioning from 3UTR to nt1
                p_trans[states_idx['3UTR']+1][i] = \
                    start_codon_freqs[codon] * delta

                # Prob of transitioning from nt1 to nt2 within this codon
                p_trans[i][i+1] = 1

                # Prob of transitioning from nt2 to nt3 within this codon
                p_trans[i+1][i+2] = 1

                # Prob of transitioning from nt3 to nt1 in the next SENSE codon
                for j in range(states_idx['sense_dORF'][0]+1, \
                               states_idx['sense_dORF'][-1]+1, 3):
                    next_codon = get_codon(j-1, states) # Sequence of this codon
                    p_trans[i+2][j] = sense_codon_freqs[next_codon]

            # For each SENSE codon row of the transition matrix, update the values
            for i in range(states_idx['sense_dORF'][0]+1, \
                           states_idx['sense_dORF'][-1]+1, 3):
                codon = get_codon(i-1, states) # Sequence of this codon

                # Prob of transitioning from nt1 to nt2 within this codon
                p_trans[i][i+1] = 1

                # Prob of transitioning from nt2 to nt3 within this codon
                p_trans[i+1][i+2] = 1

                # Prob of transitioning from nt3 to nt1 in the next SENSE codon
                for j in range(states_idx['sense_dORF'][0]+1, \
                               states_idx['sense_dORF'][-1]+1, 3):
                    next_codon = get_codon(j-1, states) # Sequence of this codon
                    p_trans[i+2][j] = \
                        (len_dorf-1)/len_dorf * sense_codon_freqs[next_codon]

                # Prob of transitioning from nt3 to nt1 in the next STOP codon
                for j in range(states_idx['stop_dORF'][0]+1,
                               states_idx['stop_dORF'][-1]+1, 3):
                    next_codon = get_codon(j-1, states) # Sequence of this codon
                    p_trans[i+2][j] = 1/len_dorf * stop_codon_freqs[next_codon]

            # For each STOP codon row of the transition matrix, update the values
            for i in range(states_idx['stop_dORF'][0]+1, \
                           states_idx['stop_dORF'][-1]+1, 3):
                codon = get_codon(i-1, states) # Sequence of this codon

                # Prob of transitioning from nt1 to nt2 within this codon
                p_trans[i][i+1] = 1

                # Prob of transitioning from nt2 to nt3 within this codon
                p_trans[i+1][i+2] = 1

                # Prob of transitioning from nt3 to 3UTR
                p_trans[i+2][states_idx['3UTR']+1] = 1

        return p_trans


        def transition_probs_rev(self, model_states):
            """Calculate the the reverse transition probabilities for generating a
                sequence backwards
            Args:
                model_states: States object contatining all state info for the
                    current model instance
            Returns:
                p_trans_rev: the reverse transition probability matrix
            Raises:
                ValueError: Could not generate reverse transition matrix
            """
            # Calculate the stationary distribution (pi)

            try:
                # Calculate the eigenvector for the transpose of the transition probs
                w, v = np.linalg.eig(self.dense_transitions.T)

                # Find the first eigenvalue that is approximately 1
                w1 = int(np.where(math.isclose(w, 1, abs_tol=0.0001))[0])

                # Get the eigenvector corresponding to an eigenvalues of 1
                pi = np.real(v)[:,w1]

                # Normalize the eigenvector
                pi = pi/pi.sum()
            except:
                raise ValueError('Could not generate reverse transition matrix.')

            # Calcualte the backward transition probs
            M = model_states.num_states
            p_trans_rev = np.zeros([M,M])
            for j in range(M):
                for k in range(M):
                    p_trans_rev[j,k] = pi[k] / pi[j] * p_trans[k,j]
            p_trans_rev = p_trans_rev/p_trans_rev.sum(axis=1, keepdims=True)

            return p_trans_rev



class Emissions():
    """Emission probabilities class for an HMM"""

    def __init__(self,
                 pointers,
                 nt_probabilities,
                 rho_probabilities,
                 riboseq_ranges):
        """
        Construct an Emissions instance
        Args:
            pointers: pointers from each state to the correct emission
                probabilities column
            probabilities: corresponding emissions probabilities are stored in
                probabilities[pointers[:,s]]
        Returns:

        Raises:

        """
        self.pointers = pointers
        self.nt_probabilities = nt_probabilities
        self.rho_probabilities = rho_probabilities
        self.riboseq_ranges = riboseq_ranges


class ORFeusEmissions(Emissions):

    def __init__(self,
                 data_df,
                 model_states,
                 num_bins,
                 min_coverage=-1,
                 max_coverage=np.inf,
                 pool=False,
                 fit=False):

        # Generate a list of state pointers (indices)
        M = self.model_states.num_states
        pointers = np.arange(M, dtype=np.uint32)

        # Calculate riboseq and nt emission probabilities for each state
        riboseq_ranges = riboseq_bins(data_df, num_bins)
        rho_probabilities = set_riboseq_probabilities(data_df,
                                                      model_states,
                                                      riboseq_ranges,
                                                      min_coverage,
                                                      max_coverage,
                                                      pool,
                                                      fit)
        nt_probabilities = set_nt_probabilities(model_states)

        # Instantiate
        super(ORFeusEmissions, self).__init__(pointers,
                                              nt_probabilities,
                                              rho_probabilities,
                                              riboseq_ranges)

    @property
    def num_bins(self):
        """Number of bins"""
        return self.num_bins

    @staticmethod
    def riboseq_bins(data_df, num_bins):
        """
        Fit a distribution to the observed riboseq values for each state
        Args:
            data_df: pandas DataFrame with all riboseq info
            num_bins: int number of bins to group the riboseq data into
        Returns:
            riboseq_ranges: array of riboseq emission bin ranges

        """
        # List of ranges for discretizing riboseq observations
        min_reads = np.nanmin(data_df['norm_reads'])
        max_reads = np.nanmax(data_df['norm_reads'])

        # Create R-1 discrete bins for non-zero values
        riboseq_ranges = np.linspace(min_reads, max_reads, num=num_bins)

        # Add a bin for zeros (dummy lower boundary)
        riboseq_ranges[0] = 0
        riboseq_ranges = np.insert(riboseq_ranges, 0, -.0001) # Add a bin for zeros (dummy lower boundary)

        return riboseq_ranges

    @staticmethod
    def fit_riboseq_emissions(df,
                              states,
                              states_idx,
                              riboseq_ranges,
                              pool=False):
        """
        Fit a distribution to the frequency of observed riboseq values for
            each state
        Args:
            df: pandas DataFrame with all riboseq info
            states: list of state names
            states_idx: dictionary mapping state type to
                state indices (1-indexed)
            riboseq_ranges: array of riboseq emission bin ranges
            pool: boolean indicating whether to pool all codons of a given type
                (start, stop, sense) when calculating riboseq emissions
        Returns:
            p_emit: the riboseq emission probability matrix

        """
        # Isolate state labels
        df['nt_pos'].fillna(-1, inplace=True)
        df_states = df[['state','codon_type','nt_pos']].drop_duplicates()

        # Update SENSE states (aggregate of all SENSE codon states if pool)
        if pool:
            df_grouped = df.groupby(['codon_type','nt_pos']) \
                           .agg({'log_reads': lambda x: x.dropna().tolist(),
                                 'norm_reads': lambda x: x.dropna().tolist()})
            df_grouped = df_states.join(df_grouped,
                                        on=['codon_type','nt_pos'],
                                        how='left')

        # Update START and STOP states
        # (aggregate all START or STOP codon states)
        else:
            df_grouped1 = df.groupby(['state']) \
                            .agg({'log_reads': lambda x: x.dropna().tolist(),
                                  'norm_reads': lambda x: x.dropna().tolist()})
            df_grouped2 = df.groupby(['codon_type','nt_pos']) \
                            .agg({'log_reads': lambda x: x.dropna().tolist(),
                                  'norm_reads': lambda x: x.dropna().tolist()})
            df_grouped1 = df_states.join(df_grouped1,
                                         on='state',
                                         how='left')
            df_grouped2 = df_states.join(df_grouped2,
                                         on=['codon_type','nt_pos'],
                                         how='left')

            df_grouped1 = df_grouped1[~df_grouped1['codon_type'] \
                                     .isin(['START','STOP'])]
            df_grouped2 = df_grouped2[df_grouped2['codon_type'] \
                                     .isin(['START','STOP'])]
            df_grouped = pd.concat([df_grouped1, df_grouped2])

        # Fit a log normal distribution to the nonzero reads
        df_grouped['p'] = df_grouped.apply(lambda row: \
                                     ss.norm.fit(row['log_reads']),
                                     axis=1)

        # Calculate the the fraction of zero reads
        df_grouped['q'] = df_grouped.apply(lambda row: \
                                     float((len(row['norm_reads']) -
                                     np.count_nonzero(row['norm_reads'])) /
                                     len(row['norm_reads'])),
                                     axis=1)

        # Make sure all states are in order
        df_grouped.set_index('state', inplace=True)
        df_grouped = df_grouped.reindex(states)

        # Keep only these parameters for each state
        p = df_grouped['p'].tolist()
        q = df_grouped['q'].tolist()

        # Set representative emission values (mean each bin greater than zero)
        emit = np.mean([riboseq_ranges[:-1], riboseq_ranges[1:]], axis=0)

        # Discretize the emissions
        M = len(states)
        R = len(riboseq_ranges)-1
        p_emit = np.zeros([M,R])

        # Skip altORF states for now
        for i in (states_idx['5UTR'] + states_idx['ORF'] + states_idx['3UTR']):

            # Add the zero emissions
            if np.any(np.isnan(q[i])):
                p_emit[i,0] = None
            else:
                p_emit[i,0] = q[i]

            # Add the nonzero emissions
            for j in range(len(emit)-1):
                if np.any(np.isnan(p[i])):
                    p_emit[i,j+1] = None
                else:
                    p_emit[i,j+1] = ss.norm(*p[i]).pdf(emit[j]) * (1-q[i])

        return p_emit

    @staticmethod
    def nofit_riboseq_emissions(df,
                                states,
                                states_idx,
                                riboseq_ranges,
                                pool=False):
        """
        Calculate the frequency observed riboseq values for each state
        Args:
            df: pandas DataFrame with all riboseq info
            states: list of state names
            states_idx: dictionary mapping state type to
                state indices (1-indexed)
            riboseq_ranges: array of riboseq emission bin ranges
            pool: boolean indicating whether to pool all codons of a given type
                (start, stop, sense) when calculating riboseq emissions
        Returns:
            p_emit: the riboseq emission probability matrix

        """
        # Group the log riboseq reads by range
        # (include the upper limit of the range)
        df['riboseq_ranges'] = pd.cut(df['norm_reads'],
                                        riboseq_ranges,
                                        right=True)

        # Get an index of all states and log read ranges
        idx = pd.MultiIndex \
                .from_product([states, df['riboseq_ranges'].cat.categories],
                              names=['state', 'riboseq_ranges'])

        # For each state, count the reads in each range
        df = df.groupby(['state', 'riboseq_ranges']) \
               .size()

        # Reset the row names to make sure ALL log reads ranges are included
        # (fill in zeros for any missing ranges)
        df = df.reindex(index=idx, fill_value=0) \
               .reset_index()
        df.columns = ['state', 'riboseq_ranges', 'counts'] # Rename columns

        # Pivot to a MxR matrix of counts for each state
        df = df.pivot(index='state',
                      columns='riboseq_ranges',
                      values='counts')

        # Reorder the states
        df = df.reindex(states)

        # Emission prob is the frequency of counts in each state
        p_emit = df.to_numpy()

        # Update SENSE states (mean of all SENSE codon states if pool)
        if pool:
            for nt in [0,1,2]:
                sum_sense = \
                    p_emit[nt+states_idx['sense'][0]:states_idx['sense'][-1]:3] \
                    .sum(axis=0)
                p_emit[nt+states_idx['sense'][0]:states_idx['sense'][-1]:3] \
                    = sum_sense

        # Normalize to make sure the probs for each state sum to 1
        p_emit = p_emit / p_emit.sum(axis=1, keepdims=True)

        return p_emit

    @staticmethod
    def set_riboseq_probabilities(data_df,
                                  model_states,
                                  riboseq_ranges,
                                  min_coverage=-1,
                                  max_coverage=np.inf,
                                  pool=False,
                                  fit=False):
        """
        Calculate the probability of observing observing each range of riboseq
            values in each state
        Args:
            data_df: pandas DataFrame with all riboseq info
            model_states: States object contatining all state info for the
                current model instance
            riboseq_ranges: array of riboseq emission bin ranges
            min_coverage: (optional) int minimum mean reads per transcript
            max_coverage: (optional) int maximum mean reads per transcript
            pool: boolean indicating whether to pool all codons of a given type
                (start, stop, sense) when calculating riboseq emissions
            fit: boolean indicating whether to fit a log-normal distribution to
                the observed non-zero values when calculating riboseq emissions
        Returns:
            p_emit: the riboseq emission probability matrix
        Raises:

        """
        # Filter down to states that are in the list of states
        df = data_df[data_df['state'].isin(model_states.states)]

        # Filter down to transcripts above min coverage and below max coverage
        df = df[(df['mean_reads']>=min_coverage) & (df['mean_reads']<=max_coverage)]

        # Calculate the emission probabilities from the observed riboseq data
        # for all canonical states
        if fit:
            p_emit = fit_riboseq_emissions(df,
                                           model_states.states,
                                           model_states.states_idx,
                                           riboseq_ranges,
                                           pool)
        else:
            p_emit = nofit_riboseq_emissions(df,
                                           model_states.states,
                                           model_states.states_idx,
                                           riboseq_ranges,
                                           pool)

        # Update START states (mean of all START codon states)
        for nt in [0,1,2]:
            sum_start = p_emit[nt+states_idx['start'][0]:states_idx['start'][-1]:3] \
                        .sum(axis=0)
            p_emit[nt+states_idx['start'][0]:states_idx['start'][1]:3] \
                    = sum_start
            if 'start_uORF' in states_idx:
                p_emit[nt+states_idx['start_uORF'][0]:states_idx['start_uORF'][-1]:3] \
                    = sum_start
            if 'start_dORF' in states_idx:
                p_emit[nt+states_idx['start_dORF'][0]:states_idx['start_dORF'][-1]:3] \
                    = sum_start

        # Update STOP states (mean of all STOP codon states)
        for nt in [0,1,2]:
            sum_stop = p_emit[nt+states_idx['stop'][0]:states_idx['stop'][-1]:3] \
                       .sum(axis=0)
            p_emit[nt+states_idx['stop'][0]:states_idx['stop'][-1]:3] \
                    = sum_stop
            if 'stop_uORF' in states_idx:
                p_emit[nt+states_idx['stop_uORF'][0]:states_idx['stop_uORF'][-1]:3] \
                    = sum_stop
            if 'stop_dORF' in states_idx:
                p_emit[nt+states_idx['stop_dORF'][0]:states_idx['stop_dORF'][-1]:3] \
                    = sum_stop
            if 'stop_SCR' in states_idx:
                p_emit[nt+states_idx['stop_SCR'][0]:states_idx['stop_SCR'][-1]:3] \
                    = sum_stop

        # Add uORF and dORF states
        if 'sense_uORF' in states_idx:
            p_emit[states_idx['sense_uORF'][0]:states_idx['sense_uORF'][-1]] = \
                p_emit[states_idx['sense'][0]:states_idx['sense'][-1]]
        if 'sense_dORF' in states_idx:
            p_emit[states_idx['sense_dORF'][0]:states_idx['sense_dORF'][-1]] = \
            p_emit[states_idx['sense'][0]:states_idx['sense'][-1]]

        # Add PRF states
        mean_orf = p_emit[states_idx['sense'][0]:states_idx['sense'][-1]].mean(axis=0)
        if 'X1' in states:
            p_emit[states_idx['X1']] = mean_orf # X1
            if 'X2' in states:
                p_emit[states_idx['X2']] = mean_orf # X2

        # Replace missing states
        for row in np.where(~p_emit.any(axis=1))[0]:
            print('Emissions missing for ' + states[row])
            p_emit[row] = mean_orf

        # Add a pseudocount to all bins so there are no zero prob emission values
        p_emit += 1e-10

        # Normalize to make sure the probs for each state sum to 1
        p_emit = p_emit / p_emit.sum(axis=1, keepdims=True)

        return p_emit

    @staticmethod
    def set_nt_probabilities(model_states):
        """
        Calculate the probability of observing each nucleotide in each state
        Args:
            model_states: States object contatining all state info for the
                current model instance
        Returns:
            p_emit: the nucleotide emission probability matrix,
                i.e. if the state is ATG1, the prob of A is 1 and the prob of all
                other nucleotides is 0, and if the state is ATG2, the prob of T is
                1 and the prob of all other nucleotides is 0 (note that this array
                has one row per nucleotide, in the same order as the NUCLEOTIDES
                array)
        """
        # Prepare the nucleotide emission probabilities matrix
        M = self.model_states.num_states
        N = len(NUCLEOTIDES)
        p_emit = np.zeros((M,N)) # MxN matrix

        # Get a list of noncodon states (can be any nt)
        noncodon_states = [model_states.states_idx['5UTR'],
                           model_states.states_idx['3UTR']]
        if 'X1' in states:
            noncodon_states.append(model_states.states_idx['X1'])
        if 'X2' in states:
            noncodon_states.append(model_states.states_idx['X2'])

        # Iterate through row for each possible observed nt
        for i in range(N):

            # For each possible state
            for s in range(M):

                if s in noncodon_states:
                    # Any nt could be observed, so set value to 1/4
                    p_emit[s, i] = 1/4

                else:
                    # Only the nt at this position in this codon can be observed
                    codon = get_codon(s, model_states.states)
                    nt_pos = get_nt(s, model_states.states)

                    # If this nt is in this state, change the value to 1
                    if NUCLEOTIDES[i] == codon[nt_pos]:
                        p_emit[s, i] = 1

        return p_emit

    @staticmethod
    def logdotexp(A, B):
        """
        Code inspiration: https://stackoverflow.com/questions/23630277/numerically-stable-way-to-multiply-log-probability-matrices-in-numpy
        Given matrices A (one-hot encoded) and B (log space), calculate the
        dot product computed in logspace using the logsumexp function such that
        the log values of A are multiplied by B and then summed (in linear space)
        Args:
            A: numpy array (one-hot encoded)
            B: numpy array (log space)
        Returns:
            C: numpy array resulting from the dot product of A and B

        """
        max_B = np.max(A)
        C = np.log(np.dot(A, np.exp(B - max_B)))
        C += max_B

        return C

    @staticmethod
    def one_hot_nt(nt_seq):
        """
        Generate the one-hot encoding for this nucleotide sequence
        Args:
            nt_seq: the nucleotide sequence
        Returns:
            one_hot_nt: the one-hot-encoded matrix for this nucleotide sequence

        """
        # Length of sequence
        L = len(nt_seq)

        # Number of nucleotides
        N = len(NUCLEOTIDES)

        # Convert the sequence to numbers (A=0, C=1, G=2, T=3)
        one_hot_nt = np.zeros((L,N))
        for i,nt in enumerate(nt_seq):
            if nt in NUCLEOTIDES:
                one_hot_nt[i, NUCLEOTIDES.index(nt)] = 1
            elif nt=='N': # Any nucleotide
                one_hot_nt[i, :] = np.ones(N)
            elif nt=='R': # Purine
                one_hot_nt[i, NUCLEOTIDES.index('A')] = 1
                one_hot_nt[i, NUCLEOTIDES.index('G')] = 1
            elif nt=='Y': # Pyrimidine
                one_hot_nt[i, NUCLEOTIDES.index('C')] = 1
                one_hot_nt[i, NUCLEOTIDES.index('T')] = 1
            else:
                print('Unexpected character in sequence: %s' % i)

        return one_hot_nt

    @staticmethod
    def one_hot_riboseq(rho_seq, riboseq_ranges):
        """
        Generate the one-hot encoding for this rho sequence
        Args:
            rho_seq: the rho sequence
        Returns:
            one_hot_rho: the one-hot-encoded matrix for this rho sequence

        """
        # Length of sequence
        L = len(rho_seq)

        # Number of discretized riboseq ranges
        R = len(riboseq_ranges)-1

        # Convert the riboseq sequence to discretized ranges
        # Include the upper limit of the range and shift to be zero-indexed
        discrete_rho = np.digitize(rho_seq, riboseq_ranges, right=True) - 1

        # For anything beyond the max observed value,
        # assign it to the uppermost bin
        discrete_rho[discrete_rho >= R] = R-1

        # Create a one-hot encoding for the sequence
        one_hot_rho = np.eye(R)[np.array(discrete_rho)]

        return one_hot_rho

    def log_probabilities(self, nt_seq, rho_seq):
        """
        Generate the log emission probabilities at each position of a sequence
        Note: Returns the emission probabilities at each sequence position as
        an L x M matrix. This allows matrix addition down the line, since the
        forward and backward matrices are L x M
        Args:
            nt_seq: the nucleotide sequence
            rho_seq: the rho sequence
        Returns:
            one_hot_nt: the one-hot-encoded matrix for this nucleotide sequence
            one_hot_rho: the one-hot-encoded matrix for this rho sequence
            log_emit_seq: the total emission probabilities at each position for
                this sequence (combined nucleotide and rho emissions)
        """
        # Calculate the nucleotide emissions for this sequence
        one_hot_nt = one_hot_nt(nt_seq, NUCLEOTIDES)
        log_emit_nt = np.log(self.nt_probabilities)
        log_emit_nt_seq = logdotexp(one_hot_nt, log_emit_nt.T)

        # Create a one-hot encoding for the sequence
        one_hot_rho = one_hot_riboseq(rho_seq, self.riboseq_ranges)
        log_emit_rho = np.log(self.rho_probabilities)
        log_emit_rho_seq = logdotexp(one_hot_rho, log_emit_rho.T)

        # Calculate the total emissions for this sequence
        log_emit_seq = log_emit_nt_seq + log_emit_rho_seq

        return one_hot_nt, one_hot_rho, log_emit_seq



# Inline function to determine the best previous state
@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void best_prev_state(int state,
                                 int pos,
                                 double [::1] current_viterbi,
                                 double [::1] previous_viterbi,
                                 unsigned int [:, ::1] viterbi_pointers,
                                 unsigned int [::1] emissions_pointers,
                                 double [:, ::1] log_emissions,
                                 unsigned int [::1] transitions_states,
                                 unsigned int [::1] transitions_pointers,
                                 double [::1] log_transitions) nogil:
    """
    Inline function to determine the best previous state
    Args:
        state: current state
        pos: current position in the input sequence
        current_viterbi: current viterbi variables
        previous_viterbi: previous viterbi variables
        viterbi_pointers: back tracking viterbi path pointers
        emissions_pointers: emission pointers
        log_emissions: log emission probabilities (for the input sequence)
        transitions_states: transition states
        transitions_pointers: transition pointers
        log_transitions: log transition probabilities
    Returns:

    """
    # Define variables
    cdef unsigned int prev_state, pointer
    cdef double density, transition_prob

    # Reset the current viterbi variable
    current_viterbi[state] = -INFINITY

    # Get the log emission probability for each state,
    # given the observed value at this position
    log_emission = log_emissions[pos, emissions_pointers[state]]

    # Iterate over all possible previous states
    for pointer in range(transition_pointers[state], \
                         transition_pointers[state + 1]):

        # Get the previous state
        prev_state = transitions_states[pointer]

        # Weight the previous state with the transition probability
        # and the current emission probability density
        transition_prob = previous_viterbi[prev_state] + \
                          log_transitions[pointer] + log_emission

        # If this transition probability is greater than the current one,
        # overwrite it and save the previous state in the current pointers
        if transition_prob > current_viterbi[state]:

            # Update the transition probability
            current_viterbi[state] = transition_prob

            # Update the back tracking pointers
            pointers[pos, state] = prev_state


class HiddenMarkovModel(object):
    """Hidden Markov Model"""

    def __init__(self,
                 states,
                 transitions,
                 emissions,
                 num_threads=1):
        """
        Construct a new Hidden Markov Model
        Args:
            states: states instance for this HMM
            transitions: transitions matrix instance for this HMM
            emissions: emissions matrix instance for this HMM
            num_threads: int number of threads for parallel Viterbi
        Returns:

        """
        self.states = states
        self.transitions = transitions
        self.emissions = emissions
        self.num_threads = num_threads


    @cython.cdivision(True)
    @cython.boundscheck(False)
    @cython.wraparound(False)
    def viterbi(self, nt_seq, rho_seq):
        """
        Determine the best path with the viterbi algorithm
        Args:
            nt_seq: the nucleotide sequence
            rho_seq: the rho sequence
        Returns:
            path: viterbi path
            log_probability: total log probability of viterbi path
        """
        cdef unsigned int L = len(nt_seq)
        cdef unsigned int M = self.states.num_states

        # Transitions
        transitions = self.transitions
        cdef unsigned int [::1] transitions_states = transitions.states
        cdef unsigned int [::1] transitions_pointers = transitions.pointers
        cdef double [::1] log_transitions = transitions.log_probabilities

        # Emissions
        emissions = self.emissions
        cdef unsigned int [::1] emissions_pointers = emissions.pointers
        cdef double [:, ::1] log_emissions =
            emissions.log_probabilities(nt_seq, rho_seq)

        # Current viterbi scores
        cdef double [::1] current_viterbi = np.empty(M, dtype=np.float)

        # Previous viterbi scores (initial transitions)
        cdef double [::1] previous_viterbi = log_transitions[:,0].copy()

        # Viterbi back-tracking pointers
        cdef unsigned int [:, ::1] viterbi_pointers = np.empty((L, M),
                                                          dtype=np.uint32)
        # Define counters
        cdef int state, pos
        cdef unsigned int prev_state, pointer, num_threads = self.num_threads
        cdef double transition_prob

        # Iterate over all positions of the input sequence
        for pos in range(L):

            # Search for the best transition (in parallel)
            if num_threads == 1:
                # For 1 thread, range() is faster than prange()
                for state in range(M):
                    best_prev_state(state,
                                    pos,
                                    current_viterbi,
                                    previous_viterbi,
                                    viterbi_pointers,
                                    emissions_pointers,
                                    log_emissions,
                                    transitions_states,
                                    transitions_pointers,
                                    log_transitions)
            else:
                for state in prange(M, nogil=True,
                                    schedule='static',
                                    num_threads=num_threads):
                    best_prev_state(state,
                                    pos,
                                    current_viterbi,
                                    previous_viterbi,
                                    viterbi_pointers,
                                    emissions_pointers,
                                    log_emissions,
                                    transitions_states,
                                    transitions_pointers,
                                    log_transitions)

            # Overwrite the old states with the current ones
            previous_viterbi[:] = current_viterbi

        # Get the final best state
        state = np.asarray(current_viterbi).argmax()

        # Set the path probability to that of the best state
        log_probability = current_viterbi[state]

        # Most probable viterbi path
        path = np.empty(L, dtype=np.uint32)

        # Track the path backwards
        for pos in range(L -1, -1, -1):
            # Save the state in the path
            path[pos] = state
            # Fetch the next previous one
            state = viterbi_pointers[pos, state]

        # Return the viterbi path and its total probability
        return path, log_probability

# Alias
HMM = HiddenMarkovModel
