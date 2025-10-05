library(nflfastR)
library(tidyverse)

pbp <- load_pbp(2024)


# get QBs
load_player_stats(2024) |> 
  filter(position == 'QB') |> 
  group_by(player_id, player_name) |> 
  summarize() -> qb_table

players <- load_player_stats(2024)


# note when rusher's position is QB

# getting qb-play stats
pbp |> 
  mutate(air_yards = if_else(complete_pass == 1, air_yards, 0)) |> 
  mutate(qb_rush = rusher_id %in% qb_table$player_id) |> 
  # note if a qb rush

  # filtering to qb-important plays
  filter(
    play == 1,
    qb_kneel != 1,
    !(play_type %in% c('extra_point', 'field_goal', 'kickoff', 'no_play', 'punt', 'qb_kneel', 'qb_spike')),

    (id %in% qb_table$player_id),
    # the qb was either the passer or rusher
  ) |> 
  
  # creating columns
  mutate(
    home = home_team == posteam,
  ) |> 
  
  
  select(
    # selecting qb id
    id,
    game_id,
    
    # selecting columns needed for filters
    pass,
    rush,
    down,
    season_type,
    home,
    qb_scramble,
    
    # granularity
    pass_attempt, # validate difference between pass column
    qb_dropback,
    
  # selecting the result stats
    yards_gained,
    air_yards,
    rushing_yards,
    pass_touchdown,
    rush_touchdown,
    touchdown,
    interception,
    sack,
    qb_hit,
    qb_epa,
    epa,
    wpa,
    complete_pass,
    # fumbles later?
    success, # maybe with other definitions too?
    first_down,
  ) |> 
  
  # creating filters
  mutate(
    all_downs = T,
    third_down = down == 3,
    third_or_fourth_down = down %in% c(3, 4),
  ) -> qb_plays


# negative yards for non-completions are all sacks
filters <- c('all_downs', 'third_down', 'third_or_fourth_down')

for (i in 1:length(filters)){
  # filter rows to only the scenarios described in filters
  print(filters[i]) # current cilter
  
  qb_plays |> 
    group_by(id, qb_dropback, pass_attempt, game_id, complete_pass) |> # group by rate metrics
    filter(.data[[filters[i]]] == TRUE) |>  # filter all plays
    
    # get raw total result values
    summarize(count = n(),
              yards = sum(yards_gained),
              air_yards = sum(air_yards, na.rm=T),
              rushing_yards = sum(rushing_yards, na.rm=T),
              touchdowns = sum(touchdown),
              interceptions = sum(interception),
              sacks = sum(sack),
              # qbr?
              epa = sum(epa),
              wpa = sum(wpa),
              qb_hits = sum(qb_hit),
              successes = sum(success),
              ten_plus = sum(yards_gained >= 10),
              twenty_plus = sum(yards_gained >= 20),
              thirty_plus = sum(yards_gained >= 30),
              first_downs = sum(first_down),
              .groups="drop_last"
              
    ) |> 
    left_join(qb_table, by=c('id' = 'player_id')) |>
    relocate(player_name, id, game_id) |> 
    group_by(qb_dropback, pass_attempt, game_id, complete_pass) -> qb_stats_long
  
  levels <- as.character(groups(qb_stats_long)) # columns needed for rate metrics
  # indicate result columns as defined above
  results <- c('yards', 'air_yards', 'rushing_yards', 'touchdowns', 'interceptions', 'sacks', 'epa', 'wpa', 'qb_hits', 'successes', 'ten_plus', 'twenty_plus', 'thirty_plus', 'first_downs')
  for(ii in 1:length(levels)) { # create rate based stats 
    for(iii in 1:length(results)){ # get a rate for each stat result
      
      
      colname = paste(results[iii], "per", levels[ii], filters[i], sep="_")
      
      
      if(is.numeric(qb_stats_long[[levels[ii]]])) {
        
        # for numeric result stats group by the rate and 
        # summarize result metric
        # noting what filter is applied
        qb_stats_long |> 
          group_by(player_name, id, .data[[levels[ii]]]) |> 
          
          summarize(
            !!colname := sum(.data[[results[iii]]]) / sum(count),
            .groups="drop_last"
          ) |> 
          ungroup() |> 
          filter(.data[[levels[ii]]] == 1) |> 
          select(-levels[ii]) -> temp
        
        # join newly created columns to working table
        if (!(colname %in% colnames(qb_table))) { # don't want to add name every time
          qb_table <- qb_table |> 
            left_join(y = temp,
                      by=c('player_name', 'player_id' = 'id'))
        }
        
      } else {
        # for team results, 
        qb_stats_long |> 
          ungroup() |> 
          group_by(player_name, id, .data[[levels[ii]]]) |> 
          
          summarize(
            !!colname := sum(.data[[results[iii]]]),
            .groups="drop_last"
          ) |> 
          group_by(player_name, id) |> 
          summarize(!!colname := mean(.data[[colname]])  ,          
                    .groups="drop_last"
          ) -> temp
        
        if (!(colname %in% colnames(qb_table))) {
          qb_table <- qb_table |> 
            left_join(y = temp,
                      by=c('player_name', 'player_id' = 'id'))
        }
      }
    }  
  }
  
  
}

negative_results <- c('sack', 'interceptions', 'qb_hits', 'fumble')

# getting totals
players |> 
  filter(position == 'QB',
         season_type == 'REG') |> 
  group_by(player_id) |> 
  summarize(across(where(is.numeric), \(x) sum(x, na.rm = T)), games=n()) |> 
  select(
    player_id,
    games,
    completions,
    attempts, 
    passing_yards, 
    passing_tds, 
    interceptions,
    sacks, 
    sack_yards, 
    sack_fumbles,
    sack_fumbles_lost, 
    passing_first_downs,
    passing_epa,
    carries,
    rushing_yards,
    rushing_tds,
    rushing_fumbles,
    rushing_fumbles_lost,
    rushing_first_downs,
    rushing_epa,
    fantasy_points
  ) |> 
  right_join(qb_table,
             by="player_id") |> 
  select(player_name, everything()) -> final_stats

  
# evaluate if that's enough stats
all_stats_ranked <-
  # get stat rankings
  final_stats |> 
  mutate(across(-c(player_name, player_id), ~ rank(.))) |> 
  # reverse ranks for negative stats
  mutate(across(matches(paste(negative_results, collapse='|')), ~ . * -1 + max(.)))
  
library(ggthemes)

# get every players average ranking per stat
all_stats_ranked |> 
  filter(games > 30) |> 
  pivot_longer(cols=-c(player_name, player_id),
               names_to="name",
               values_to="rank") |> 
  group_by(player_name, player_id) |> 
  summarize(avg_rank = mean(rank)) |> 
  
  # plot histogram of average ranks
  
  ggplot(
    mapping=aes(x=avg_rank)
  ) + 
  geom_histogram(binwidth=4,
                 fill='steelblue',
                 color='white') + 
  geom_hline(yintercept=0) + 
  labs(y = "", x = "Average Rank", title = "QB Average Statistical Ranking",
       subtitle = "Excluding Bottom 30 in Games Played") + 
  theme_pander()


all_stats_ranked |> 
  filter(games > 30) |> 
  pivot_longer(cols=-c(player_name, player_id),
               names_to="name",
               values_to="rank") |> 
  group_by(player_name, player_id) |> 
  summarize(top_ranks = quantile(rank, .1),
            bottom_ranks = quantile(rank, .9)) |> 
  pivot_longer(cols=-c(player_name, player_id),
               names_to='name',
               values_to='rank') |> 
  
  # plot histogram of average ranks
  ggplot(
    mapping=aes(x=rank, fill=name)
  ) + 
  geom_histogram(binwidth=4,
                 color='white') + 
  geom_hline(yintercept=0) + 
  labs(y = "", x = "Rank", title = "All Quarterbacks' Best Stats vs\nAll Quarterbacks' Worst Stats",
       subtitle = "Excluding Bottom 30 in Games Played",
       fill="") + 
  scale_fill_discrete(
    name = "", 
    labels = c("Bottom 10%", "Top 10%"), 
  ) +
  theme_pander()


# get best and worst quarterback by average stat rank
all_stats_ranked |> 
  filter(games > 30) |> 
  pivot_longer(cols=-c(player_name, player_id),
               names_to="name",
               values_to="rank") |> 
  group_by(player_name, player_id) |> 
  summarize(average_rank = mean(rank)) |> 
  arrange(desc(average_rank)) |>
  ungroup() |> slice(c(1, n())) |> pull(player_id) -> best_and_worst

all_stats_ranked |> 
  filter(player_id %in% best_and_worst) -> best_worst_ranks

overlap_stats <- names(best_worst_ranks)[best_worst_ranks[1,] < best_worst_ranks[2,]]

final_stats |> 
  filter(player_id %in% best_and_worst) |> 
  select(player_name, overlap_stats)


best_ranks <- best_worst_ranks[1, -c(1, 2)]

all_stats_ranked |> 
 filter(games > 30) |> 
 pivot_longer(cols=-c(player_name, player_id),
              names_to="name",
              values_to="rank") |> 
 group_by(player_name, player_id) |> 
 summarize(average_rank = mean(rank)) -> mean_ranks 


mean_ranks |> pull(average_rank) |> quantile(0:9 / 10, names=F) -> quantiles
closest_idxs <- sapply(quantiles, function(q) which.min(abs(mean_ranks$average_rank - q)))

mean_ranks[closest_idxs,'percentile'] <- 0:9 * 10

mean_ranks |> 
  filter(!is.na(percentile)) |> 
  arrange(percentile) |> 
  left_join(all_stats_ranked, by=c('player_name', 'player_id')) -> all_stats_percentiles
  
overlaps <- rep(0, nrow(all_stats_percentiles))
overlap_percent <- rep(0, nrow(all_stats_percentiles))
for (i in 1:nrow(all_stats_percentiles)) {
  overlap_stats <- sum(best_ranks < all_stats_percentiles[i,-c(1:4)])
  t <- length(best_ranks)  

  overlaps[i] <- overlap_stats
  overlap_percent [i] <- overlap_stats / t
}
all_stats_percentiles$overlap <- overlaps
all_stats_percentiles$overlap_percent <- overlap_percent
all_stats_percentiles |> 
  select(player_name, percentile, overlap, overlap_percent) -> dat

dat |> 
  ggplot(mapping=aes(x=percentile, y=overlap)) + 
  geom_col(fill='steelblue',color='white') + 
  geom_hline(yintercept=0) + 
  labs(y = "Number of Stats Ranked Higher Than Josh Allen", x = "Percentile", 
       title = "QBs of Every Percentile Have Stats Greater than Best QB",
       subtitle = "Excluding Bottom 30 in Games Played") + 
  theme_pander()


# renaming stats for LLM readability
final_stats |> 
  mutate(player_id = as.integer(substring(player_id, 4))) |> 
  rename_with(function(x) sub('_id', '', x), .cols=-player_id) |> 
  rename_with(function(x) sub('_all_downs', '', x)) |> 
  rename(rushes='carries') |> 
  select(where(~ any(.x != 0 & !is.na(.x)))) |> # remove all NA columns like interceptions per complete pass
  select(-player_name) -> final_final_stats

final_final_stats |> 
  ggplot(mapping=aes(x=games)) + 
  geom_histogram()

final_final_stats |> 
  filter(games >= 4, attempts >=150) |> nrow()

  write.csv(final_final_stats, 'quarterback_stats.csv', row.names=F)
