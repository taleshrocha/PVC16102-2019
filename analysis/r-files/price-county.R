# This script plots the box-plot of the price per county.

source("source.R")
library(Hmisc)

options(scipen = 9999)

olx %>%
  filter(municipio == "Natal" | municipio == "Parnamirim") %>%
  filter(strtoi(preco) <= 500000) %>%
  ggplot(aes(x=municipio, y=strtoi(preco), color=municipio)) +
  geom_violin(show.legend = FALSE, trim = FALSE) +
  theme_light(base_size=14) +
  geom_boxplot(width = 0.1) +
  scale_y_continuous(breaks = seq(0, 1000000, 50000)) +
  labs(
       x = "Município",
       y = "Preço (R$)",
       title = "Figura 2",
       subtitle = "Preço por município",
       color = "Município",
  )

ggsave("../images/price-county.png")
