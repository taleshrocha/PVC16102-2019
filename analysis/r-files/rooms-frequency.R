# This script plots the column graphic of the rooms frequency.

source("source.R")

olx %>%
  count(quartos) %>%
  filter(!is.na(quartos)) %>% 
  top_n(10, n) %>%
  #mutate(quartos = forcats::fct_reorder(quartos, n)) %>% 
  ggplot() +
  geom_col(aes(x = quartos, y = n, fill = quartos), show.legend = FALSE) +
  geom_label(aes(x = quartos, y = n/2, label = n)) +
  coord_flip()

ggsave("rooms-frequency")
