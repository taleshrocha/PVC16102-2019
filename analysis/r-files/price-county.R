# This script plots the box-plot of the price per county.

source("source.R")

# TODO: Put labels in the maximum, medium and minimum values.
olx %>%
  ggplot() +
  geom_boxplot(aes(x = preco, y = municipio, color = municipio), show.legend = FALSE) +
  scale_x_continuous(breaks = seq(0, 1000000, 100000)) +
  #xlim(0, 500000) +
  labs(
       x = "Preço (R$)",
       y = "Município",
       title = "Gráfico Boxplot",
       subtitle = "Município por preço"
  )

ggsave("../images/price-county.png", width=10)
