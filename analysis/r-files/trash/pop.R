source("source.R")
library(ggpubr)

options(scipen = 9999)

mun <- olx %>%
  select(preco, municipio)

mun <- mun %>% 
  group_by(municipio) %>%
  summarise(preco_medio = round(mean(as.numeric(preco))))

mun %>%
  ggplot(aes(x = municipio, y = preco_medio)) +
  geom_segment(
               aes(x = municipio, xend = municipio, y = 0, yend = preco_medio),
               color = "lightgray"
               ) +
geom_point(aes(color = municipio), size = 3) +
scale_color_viridis_d() +
theme_pubclean() +
rotate_x_text(45)

ggsave("../images/pop.png")
