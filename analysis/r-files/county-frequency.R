# This script plots the column graphic of the county frequency per advertisement.

source("source.R")

olx %>%
  count(municipio) %>%
  filter(!is.na(municipio)) %>% 
  top_n(11, n) %>%
  mutate(municipio = forcats::fct_reorder(municipio, n)) %>% 
  ggplot() +
  geom_col(aes(x = municipio, y = n, fill = municipio), show.legend = FALSE) +
  scale_y_continuous(labels = scales::percent_format()) +
  geom_label(aes(x = municipio, y = n/2, label = n)) +
  coord_flip() +
  theme_light(base_size=14) +
  scale_color_viridis_d() +
  labs(
       x = "Município",
       y = "N° de anúncios",
       title = "Figura 1",
       subtitle = "N° de anúncios por municípios"
  )

ggsave("../images/county-frequency.png")
