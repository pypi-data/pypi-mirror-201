#!/usr/bin/env python

# -----------------------------------------------------------------------------
# Gene coverage
# Author: Mary Richardson
# Date: 2023.03.20
# -----------------------------------------------------------------------------

import logging
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)



def count_gene_coverage(data_df,
                        coverage):
    """
    Compares the true and predicted paths to determine the accuracy of the
        prediction
    Args:
        data_df: pandas DataFrame of all annotated transcripts
        coverage: mean coverage per transcript (reads/nt)
    Returns:
        count: number of transcripts with the given coverage or higher
    Raises:

    """
    # Count the number of genes with at least the specified coverage
    count = len(data_df[data_df['mean_reads']>=coverage] \
                       ['transcript_id'].unique())

    return count


def plot_gene_coverage(data_df, coverages, file):
    """
    Compares the true and predicted paths to determine the accuracy of the
        prediction
    Args:
        data_df: pandas DataFrame of all annotated transcripts
        coverages: mean coverages per transcript (reads/nt)
        file: output file for plot
    Returns:

    Raises:

    """
    # Calculate the genes for each coverage
    coverages = np.insert(coverages,0,0)
    counts = [count_gene_coverage(data_df, coverage) for coverage in coverages]

    # Plot the results
    fig, ax = plt.subplots(figsize=(6,4))
    x = coverages
    y = counts

    print('Total genes: %i' % counts[0])
    for i in range(len(counts)):
        print('%f coverage genes: %i' % (coverages[i], counts[i]))

    ax.scatter(x, y, color=colors[0]) # Plot in grey

    # Label the axes
    plt.xlabel('Mean ORF coverage (footprints/nt)', fontsize=12)
    plt.ylabel('Number of genes', fontsize=12, rotation='vertical')
    plt.title('Number of genes\nwith sufficient coverage', fontsize=14, weight='bold')

    # Save the plot
    plt.tight_layout()
    plt.savefig(file)
