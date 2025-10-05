import pandas as pd
import numpy as np

def find_negative_stats(df: pd.DataFrame):

    negative_values = ['sack', 'interception', 'qb_hit', 'fumble']
    colnames = []
    for val in negative_values:
        colnames.extend([colname for colname in df.columns if val in colname])
    return colnames


def normalize_data(df: pd.DataFrame):
    return (df - df.mean()) / (df.std())


def weighted_random(df:pd.DataFrame):
    # df is a dataframe with columns stat and norm_value
    stat_mask = (df['stat'].str.contains('per') - 1) * -1 + 1 # weight non 'per' columns 2 times as heavy
    values = np.array(df['norm_value'] * (stat_mask))
    weighted_dist = values / values.sum()
    return np.random.choice(a=df['stat'].to_numpy(), size=int(len(df['stat']) / 2), p=weighted_dist, replace=False)


def get_supporting_data(ids: list[int], names: list[str], data: pd.DataFrame) -> list[str, str]:

    # filter all data to qualified quarterbacks
    # my definition: >=4 games, >= 150 pass attempts

    # find stats the top qb is worst at, the bottom qb is best at
    # random select from subset (maybe favoring worst/best and stat simplicity)
    # provide stats and all qbs rankings and values to the prompt
    qualified = (
        data
        .loc[(data['games'] >= 4) & (data['attempts'] >= 150)]
    )
    qualified_numeric = qualified.drop(columns='player_id') # drop id column before standardization
    # nomalize data
    qualified_norm = normalize_data(qualified_numeric)
    qualified_norm = pd.concat([qualified['player_id'], qualified_norm], axis=1)

    negative_columns = find_negative_stats(qualified_norm)

    qualified_norm_melted = qualified_norm.melt(
        id_vars='player_id', var_name='stat', value_name='norm_value'
    )
    # reverse values for negative stats
    negative_column_mask = (
        qualified_norm_melted
        ['stat']
        .apply(lambda x: x in negative_columns)
        # go from 0 for postive stat 1 for negative stat
        # to -1 for negative stat 1 for positive stat
        * 2 # expand
        * -1 # shift
        + 1 # flip
    )

    qualified_norm_melted['norm_value'] = qualified_norm_melted['norm_value'] * negative_column_mask

    # find worst stats for best player
    best_players_worst_stats = (
        qualified_norm_melted
        .loc[
            qualified_norm_melted['player_id'] == ids[0]
        ]
        .sort_values('norm_value')
        .iloc[:10]
    )
    worst_players_best_stats = (
        qualified_norm_melted
        .loc[
            qualified_norm_melted['player_id'] == ids[-1]
        ]
        .sort_values('norm_value', ascending=False)
        .iloc[:10]
    )

    stats = list(weighted_random(best_players_worst_stats)) + list(weighted_random(worst_players_best_stats))

    # find all ranks for these stats
    # using melted becuase negative ranks will be accounted for
    stat_ranks = (
        qualified_norm_melted
        .query('stat in @stats')
        .pivot(
            columns='stat',
            values='norm_value', 
            index='player_id'
        )
        .rank(ascending=False, method='first')
        .reset_index()
        .query('player_id in @ids')
        .melt(
            id_vars='player_id',
            value_name='rank',
            var_name='stat'
        )
    )

    stat_values = (
        qualified
        .loc[
            qualified['player_id'].isin(ids), ['player_id'] + stats
        ]
        # melt back down to long format
        .melt(
            id_vars='player_id', 
            var_name='stat',
            value_name='value'
        )
    )

    supporting_stats = (
        pd.merge(
            stat_ranks, stat_values,
            how='inner',
            on=['player_id', 'stat']
        )
    )
    # add names
    supporting_stats['name'] = supporting_stats['player_id'].map(dict(zip(ids, names)))

    return render_data_as_md(supporting_stats)

def render_data_as_md(df:pd.DataFrame):
    tables = []
    for stat in df['stat'].unique():
        md = (
            df
            .loc[
                df['stat'] == stat,
                ['name', 'value', 'rank']
            ]
            .to_markdown(index=False)
        )
        tables.append((stat, md))
    return tables




def get_supporting_data_v2(ids: list[int], names: list[str], data: pd.DataFrame):
    # for bottom player, find what stats are better than each of the other players
    # random select from each list
    # same for top player
    return