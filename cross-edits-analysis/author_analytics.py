'''
    Copyright 2020 Google LLC

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Date: 6/11/2020
    Author: Haoran Fei
    Script to perform author-specific analytics, as outlined in part II of Preliminary Data
    Analysis Planning.

'''

import sys
import getopt
#import pandas as pd
import matplotlib.pyplot as plt
import engine
import os


def main(argv): 
    '''Main routine to load files, compute aggregate statistics, per-author statistics and
    sliding window analysis.'''

    author_analysis_engine = engine.Engine()
    author_analysis_engine.get_command_line_input(argv)
    author_analysis_engine.set_key("author", "author")
    author_analysis_engine.open_log_file()
    author_analysis_engine.display_aggregate_stats()
    #author_analysis_engine.iterate_per_key(author_analysis_engine.display_per_group_stats)
    #author_analysis_engine.iterate_per_key(author_analysis_engine.plot_evolution_across_time)
    author_analysis_engine.iterate_per_key(author_analysis_engine.sliding_window_analysis)

    authors_with_non_zero_scores = []
    means = dict()
    medians = dict()
    columns = author_analysis_engine.columns_to_count

    for column in columns:
        means[column] = []
        medians[column] = []

    def compute_mean_and_median_non_zero(group, group_key, index):
        # Get the edits with non-zero ores score for time-series analysis
        non_zero_authors = group.loc[group["ores_damaging"] != 0].copy()
        non_zero_count = non_zero_authors.shape[0]
        if non_zero_count != 0:
            authors_with_non_zero_scores.append(group_key)
            for column in columns:
                means[column].append(group[column].mean())
                medians[column].append(group[column].median())

    author_analysis_engine.iterate_per_key(compute_mean_and_median_non_zero)

    # Distribution of mean and median scores across authors
    fig, axes = plt.subplots(2, len(columns))
    fig.set_size_inches(37, 21)
    for i in range(len(columns)):
        axes[0][i].hist(means[columns[i]], bins=50)
        axes[0][i].set_title("Mean of {} across all authors".format(columns[i]))
        axes[1][i].hist(medians[columns[i]], bins=50)
        axes[1][i].set_title("Median of {} across all authors".format(columns[i]))
    plt.savefig("./graphs/aggregate/Mean_median_all_authors_all_columns_no_zero.png")
    plt.close()

    author_analysis_engine.cleanup()

if __name__ == "__main__":
    main(sys.argv[1:])