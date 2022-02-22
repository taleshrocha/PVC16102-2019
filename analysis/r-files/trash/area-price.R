# This script plots the point graphic of the area per price of the houses.

source("source.R")

olx %>%
  filter(preco <= 250000) %>%
  ggplot() +
  geom_point(aes(x = area, y = preco, color = preco/area, shape = politica), position = "jitter") + 
  geom_smooth(aes(x = area, y = preco), method = lm) +
  xlim(40, 90) +
  scale_y_continuous(breaks = seq(0, 500000, 50000)) +
  scale_color_gradient(low = "green", high = "red") +
  scale_shape_manual(values = c(0, 6)) +
  labs(
       x = "Área (m²)",
       y = "Preço (R$)",
       shape = "Política habitacional",
       color = "Preço/Área",
       title = "Área por preço"
  )

ggsave("../images/area-price.png")
