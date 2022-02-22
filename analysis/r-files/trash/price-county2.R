# This script plots the box-plot of the price per county.

source("source.R")

# Faceta; estratificar;N de quartos; fecity_grade

olx %>%
  filter(strtoi(quartos) > 0) %>%
  ggplot(aes(x=municipio, y=strtoi(preco), color=municipio)) +
  geom_boxplot(show.legend = FALSE) +
  coord_flip() +
  facet_grid(~quartos)
  labs(
       x = "Município",
       y = "Preço (R$)",
       title = "Gráfico Boxplot",
       subtitle = "Preço por município"
  )

ggsave("../images/price-county2.png", width=18)
