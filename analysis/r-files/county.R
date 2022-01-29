# This script plots the column graphic of the county frequency.

source("source.R")

olx %>%
  count(municipio) %>%
  filter(!is.na(municipio)) %>% 
  top_n(10, n) %>%
  mutate(municipio = forcats::fct_reorder(municipio, n)) %>% 
  ggplot() +
  geom_col(aes(x = municipio, y = n, fill = municipio), show.legend = FALSE) +
  geom_label(aes(x = municipio, y = n/2, label = n)) +
  coord_flip()

ggsave("county-frequency")
