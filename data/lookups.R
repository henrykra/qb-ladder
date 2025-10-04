library(nflfastR)

load_player_stats(2024) %>% 
  filter(position == 'QB') %>% 
  group_by(player_id, player_name, recent_team) %>% 
  summarize() %>%
  mutate(player_id = as.integer(substring(player_id, 4))) %>%
  distinct(player_id, .keep_all=T) %>%
  separate(player_name, into=c('first_initial', 'last_name'), sep='[.]', remove=F) %>%
  select(-first_initial, player_name) %>%
  rename(team='recent_team') -> qb_lnames

qb_lnames$first_name = c('Aaron', 'Joe', 'Josh', 'Matthew', 'Andy', 'Tyrod',
                        'Russell', 'Kirk', 'Geno', 'Teddy', 'Derek', 'Jimmy', 'Jameis', 
                        'Taylor', 'Marcus', 'Brandon', 'Carson', 'Dak', 'Jared', 'Jacoby',
                        'Nick', 'DeShaun', 'Caleb', 'Mitch', 'Patrick', 'Josh', 'Tim',
                        'Mike', 'Kyle', 'Mason', 'Lamar', 'Baker', 'Josh', 'Sam', 'Jake', 'Kyler', 
                        'Jared', 'Gardner', 'Drew', 'Daniel', 'Tyler', 'Tua', 'Jordan', 'Justin', 'Jalen',
                        'Joe', 'Davis', 'Kyle', 'Justin', 'Trevor', 'Mack', 'Trey', 'Sam',
                        'Chris', 'Skyler', 'Brock', 'Kenny', 'Bailey', 'Desmond', 'Malik', 'Tanner',
                        'Tyson', 'Tommy', 'Hendon', 'Aiden', 'Clayton', 'Dorian', 'Jake', 'Bryce',
                        'Will', 'C.J.', 'Anthony', 'Spencer', 'Joe', 'Bo', 'Drake', 'Jayden',
                        'Michael', 'Caleb')

qb_lnames |> mutate(player_name = paste(first_name, last_name, sep=' ')) -> qb_names

teams_colors_logos |> select(team_abbr, team_color, team_color2) -> team_colors

write.csv(team_colors, file='team_colors.csv', row.names=F)
write.csv(qb_names, file='qb_names.csv', row.names=F)
