# This file plots the box-plot graphic of the price per rooms.

source("source.R")

olx$quartos[olx$quartos == "--"] <- NA

olx %>%
  ggplot() +
  geom_boxplot(aes(x = preco, y = quartos, color = quartos), show.legend = TRUE) +
  labs(
       x = "Preço (R$)",
       y = "N° de quartos",
       #title = "Gráfico Boxplot",
       title = "Preço por N° de quartos"
  )

ggsave("../images/price-room.png")
