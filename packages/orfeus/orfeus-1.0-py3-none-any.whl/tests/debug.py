#!/usr/bin/env python

# HMM tests
# Author: Mary Richardson
# Date: 2020.01.08

import sys
import argparse
import numpy as np
import pandas as pd
import pickle as pk
import itertools as it
from scipy.special import logsumexp
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter as fmt
import seaborn as sns

from helper import convert_emissions
from algorithms import viterbi, forward, backward, score_path
from set_parameters import riboseq_emission_probs

# Customize plotting style
sns.set_style('white')
colors = ['#CA4B4C', '#F0BF1A', '#2E659D']
sns.set_palette(sns.color_palette(colors))

np.set_printoptions(threshold=sys.maxsize)



###########################
# Check parameters
###########################


def check_sums(p_emit, p_trans):
    '''
    Check that all probabilities sum to 1 where they should
    '''
    match = True # Default

    # Check that emission prob matrix rows except begin state sum to 1 (within some error here)
    if not (np.all(p_emit.sum(axis=1) > 0.99) and (np.all(p_emit.sum(axis=1) < 1.01))):
        print('Emission probability matrix rows don\'t sum to 1!')
        match = False

    # Check that transition prob matrix rows sum to 1
    if (np.all(p_trans.sum(axis=1) != 1)):
        print('Transition probability matrix rows don\'t sum to 1!')
        match = False

    return match



###########################
# Check HMM functions
###########################

def check_scores(log_emit_nx, log_trans,
                 prev_states_options, next_states_options
                 dec=5):
    '''
    Given an observed sequence x and parameters,
    Checks that at every column the product of the forward and backward algorithms summed over all states is equal
    to the total forward score and total backward score
    '''
    L = len(log_emit_nx)  # Length of observed sequence

    # Calculate the forward and backward scores at each position of the sequence
    F, F_score = forward(log_emit_nx, log_trans, prev_states_options, next_states_options)
    B, B_score = backward(log_emit_nx, log_trans, prev_states_options, next_states_options)

    # Check whether forward score equals backward score to start
    match = True # Default
    if (np.round(F_score, dec) != np.round(B_score, dec)):
        print('Forward and backward scores not equal!')
        match = False

    # Calculate the score at each position of the sequence
    for i in range(L):
        sequence_score = logsumexp(F[i,:] + B[i,:])
        if np.round(sequence_score, dec) != np.round(F_score, dec):
            print('The scores at each position of the sequence are not equal!')
            match = False

    # Return whether the forward score, backward score, and the score at each position match
    return match


def brute_test(log_emit_nx, log_trans,
               prev_states_options, next_states_options,
               dec=5):
    '''
    Given an observed sequence x and parameters,
    Enumerates all possible paths and checks that the sum over all paths is equal to the total
    forward score
    '''
    M = len(log_trans) - 1 # Number of states
    L = len(log_emit_nx)   # Length of observed sequence

    # Enumerate all possible hidden state paths for this sequence (M^L paths)
    # Compute the cartesian product of the possible states at each position in the sequence
    all_paths = list(it.product(range(M), repeat = L))

    # Compute the probability of each possible path
    path_scores = []
    for path in all_paths:
        path_score = score_path(path, log_emit_nx, log_trans)
        path_scores.append(path_score)

    # Sum the probability over all paths
    all_paths_score = logsumexp(path_scores)
    print('Sum over all paths:  ', all_paths_score)

    # Calculate the total score from the forward algorithm
    F, F_score = forward(log_emit_nx, log_trans, prev_states_options, next_states_options)
    print('Total forward score: ', F_score)

    # Check that the sum over all paths equals the total forward probability
    match = True # Default
    if (np.round(F_score, dec) != np.round(all_paths_score, dec)):
        print('The sum over all paths and the forward score are not equal!')
        match = False

    return match


def generation_test(log_emit_nt, log_emit, log_trans,
                    prev_states_options, next_states_options,
                    nts, riboseq_ranges, dec=5, suppress=True):
    '''
    Given parameters,
    Samples a sequence and calculates the viterbi path to check that the viterbi result
    is at least as probable as the true path but not greater than the forward and backward scores
    '''
    # Simulate a sequence
    n, x, true_path = simulate_seq(np.exp(log_emit_nt), np.exp(log_emit), np.exp(log_trans), nts, riboseq_ranges)

    # Generate the reformatted emission probabilities
    one_hot_n, one_hot_x, log_emit_nx = convert_emissions(n, x, log_emit_nt, log_emit, nts, riboseq_ranges)

    # Calculate the viterbi path
    viterbi_path, P = viterbi(log_emit_nx, log_trans, prev_states_options, next_states_options)

    # Calculate the score of the true path
    true_score = score_path(true_path, log_emit_nx, log_trans)
    print('True path score:      ', true_score)

    # Calculate the viterbi path score
    viterbi_score = score_path(viterbi_path, log_emit_nx, log_trans)
    print('Viterbi path score:   ', viterbi_score)

    # Calculate the total score from the forward algorithm
    F, F_score = forward(log_emit_nx, log_trans, prev_states_options, next_states_options)
    print('Total forward score:  ', F_score)

    # Calculate the total score from the backward algorithm
    B, B_score = backward(log_emit_nx, log_trans, prev_states_options, next_states_options)
    print('Total backward score: ', B_score)

    # Check that the forward and backward scores are equal
    match = True # Default
    if not np.round(F_score, dec) == np.round(B_score, dec):
        print('Forward and backward scores not equal!')
        match = False

    # Check that the forward and backward scores are at least as good as the viterbi score
    if not F_score >= viterbi_score and B_score >= viterbi_score:
        print('Forward and backward scores not at least as good as viterbi!')
        match = False

    # Check that the viterbi path is at least as probable as the actual path
    if not viterbi_score >= true_score:
        print('Viterbi score not at least as good as true score!')
        match = False

    return match


def main():

    # Accept command line arguments for input and output files
    parser = argparse.ArgumentParser(description='Test the model for the current dataset')

    parser.add_argument('nt_emissions_file', type=str,
                        help='nt emission probability file path')
    parser.add_argument('riboseq_emissions_file', type=str,
                        help='riboseq emission probability file path')
    parser.add_argument('transitions_file', type=str,
                        help='transition probability file path')
    parser.add_argument('transitions_rev_file', type=str,
                        help='reverse transition probability file path')
    parser.add_argument('constants_file', type=str,
                        help='constants file path')

    args = parser.parse_args()


    ###########################
    # Import initial transition and emission probabilities
    ###########################

    # Get the constants
    [nts, riboseq_ranges, states] = pk.load(open(args.constants_file, 'rb'))
    M = len(states)
    R = len(riboseq_ranges)-1

    # Get the initial parameters
    p_emit_nt = np.loadtxt(args.nt_emissions_file)
    p_emit = np.loadtxt(args.riboseq_emissions_file)
    p_trans = np.loadtxt(args.transitions_file)
    p_trans_rev = np.loadtxt(args.transitions_rev_file)

    # Log the initial parameters
    log_emit_nt = np.log(p_emit_nt)
    log_emit = np.log(p_emit)
    log_trans = np.log(p_trans)


    ###########################
    # Generate a test sequence
    ###########################

    # Simple test sequence (A=0, C=1, G=2, T=3)
    n = np.array(['A','T','G','T','T'])
    x = np.array([0,1,2,3,1])
    one_hot_n, one_hot_x, log_emit_nx = convert_emissions(n, x, log_emit_nt, log_emit, nts, riboseq_ranges)


    ###########################
    # Check parameters
    ###########################

    print('Check parameters:')
    print(check_sums(p_emit, p_trans))
    print()


    ###########################
    # Check scores
    ###########################

    # Test on simple case
    print('Check scores (simple sequence):')
    print(check_scores(log_emit_nx, log_trans))
    print()

    # Test on random sequence
    print('Check scores (simulated sequence):')
    for i in range(10):
        simulated_n, simulated_x, true_path = simulate_seq(p_emit_nt, p_emit, p_trans, nts, riboseq_ranges)
        one_hot_n, one_hot_x, simulated_log_emit_nx = convert_emissions(simulated_n, simulated_x, log_emit_nt, log_emit,
                                                            nts, riboseq_ranges)
        print(check_scores(simulated_log_emit_nx, log_trans))
    print()


    ###########################
    # Brute test
    ###########################

    # Test on simple case
    #print('Brute test (simple sequence):')
    #print(brute_test(log_emit_nx, log_trans))
    #print()

    # Test on random sequence (takes a LONG time)
    #simulated_n, simulated_x, true_path = simulate_seq(p_emit_nt, p_emit, p_trans, nts, riboseq_ranges)
    #one_hot_n, one_hot_x, simulated_log_emit_nx = convert_emissions(simulated_n, simulated_x, log_emit_nt, log_emit,
    #                                                    nts, riboseq_ranges)
    #print('Brute test (simulated sequence):')
    #print(brute_test(simulated_log_emit_nx, log_trans))
    #print()


    ###########################
    # Generation test
    ###########################

    print('Generation test:')
    for i in range(10):
        print(generation_test(log_emit_nt, log_emit, log_trans, nts, riboseq_ranges))
    print()


    ###########################
    # Baum-Welch test
    ###########################

    # Generate synthetic training data from known parameters
    train_id, train_n, train_x = [], [], []
    for i in range(1000):

        # Simulate a sequence
        simulated_n, simulated_x, true_path = simulate_seq(p_emit_nt, p_emit, p_trans, nts, riboseq_ranges)
        predict_frameshift(true_path, states)

        # Add it to the training data
        train_id.append('simulated %i' % i)
        train_n.append(simulated_n)
        train_x.append(simulated_x)

    # Save the simulated transcripts
    transcripts_file = 'tmp1.txt'
    pk.dump([train_id, train_n, train_x], open(transcripts_file, 'wb'))


    # Start from true parameters
    print('Baum-Welch test (starting from true parameters):')
    log_emit_nt_test = log_emit_nt
    log_emit_test  = log_emit
    log_trans_test = log_trans
    match, log_emit_nt_test, log_emit_test, log_trans_test, log_emit_nt_pred, log_emit_pred, log_trans_pred, ll  = test_baum_welch(transcripts_file, log_emit_nt, log_emit, log_trans,
                                 log_emit_nt_test, log_emit_test, log_trans_test,
                                 nts, riboseq_ranges)
    print_baum_welch(states,
           log_emit_nt, log_emit, log_trans,
           log_emit_nt_test, log_emit_test, log_trans_test,
           log_emit_nt_pred, log_emit_pred, log_trans_pred)
    print('final log likelihood: %f' % ll)
    print(match)
    print()


    # Set random parameters to start
    print('Baum-Welch test (starting from random parameters):')
    best_ll = -np.inf
    for _ in range(50): # Run from multiple random starting conditions

        p_emit_test = np.zeros((M,R))
        p_emit_test[np.nonzero(p_emit)] = 1
        for m in range(M):
            nonzero = np.transpose(p_emit_test[m].nonzero()).flatten()
            p = np.random.dirichlet(np.ones(len(nonzero)))
            for i,j in enumerate(nonzero):
                p_emit_test[m,j] = p[i]

        p_trans_test = np.zeros((M+1,M+1))
        p_trans_test[np.nonzero(p_trans)] = 1
        for m in range(M):
            nonzero = np.transpose(p_trans_test[m].nonzero()).flatten()
            p = np.random.dirichlet(np.ones(len(nonzero)))
            for i,j in enumerate(nonzero):
                p_trans_test[m,j] = p[i]

        log_emit_test = np.log(p_emit_test)
        log_trans_test = np.log(p_trans_test)

        match, log_emit_nt_test, log_emit_test, log_trans_test, log_emit_nt_pred, log_emit_pred, log_trans_pred, ll  = test_baum_welch(transcripts_file, log_emit_nt, log_emit, log_trans,
                                     log_emit_nt_test, log_emit_test, log_trans_test,
                                     nts, riboseq_ranges)


        if ll > best_ll:
            best_match = match
            best_log_emit_nt_test = log_emit_nt_test
            best_log_emit_test = log_emit_test
            best_log_trans_test = log_trans_test
            best_log_emit_nt_pred = log_emit_nt_pred
            best_log_emit_pred = log_emit_pred
            best_log_trans_pred = log_trans_pred
            best_ll = ll


    print_baum_welch(states,
           log_emit_nt, log_emit, log_trans,
           best_log_emit_nt_test, best_log_emit_test, best_log_trans_test,
           best_log_emit_nt_pred, best_log_emit_pred, best_log_trans_pred)
    print('final log likelihood: %f' % best_ll)
    print(best_match)
    print()



if __name__== "__main__":
    main()
