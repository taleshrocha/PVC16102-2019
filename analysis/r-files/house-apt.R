# This script plots the column graphic of the house and apartment frequency.

source("source.R")

olx %>%
  count(categoria) %>%
  filter(!is.na(categoria)) %>% 
  top_n(10, n) %>%
  mutate(categoria = forcats::fct_reorder(categoria, n)) %>% 
  ggplot() +
  geom_col(aes(x = categoria, y = n, fill = categoria), show.legend = FALSE) +
  geom_label(aes(x = categoria, y = n/2, label = n)) +
  coord_flip()

ggsave("../images/house-apartment-frequency.png")
