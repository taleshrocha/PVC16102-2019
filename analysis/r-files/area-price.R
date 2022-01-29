# This script plots the point graphic of the area per price of the houses.

source("source.R")

olx %>%
  mutate(valor = preco/area) %>%
  filter(preco <= 250000) %>%
  ggplot() +
  geom_point(aes(x = area, y = preco, color = valor), show.legend = FALSE) + 
  xlim(40, 90) +
  scale_y_continuous(breaks = seq(0, 500000, 50000)) +
  scale_color_gradient(low = "green", high = "red") +
  labs(
       x = "Área (m²)",
       y = "Preço (R$)",
       #color = "",
       title = "Gráfico de dispersão",
       subtitle = "Área por preço"
  )

ggsave("area-price")
