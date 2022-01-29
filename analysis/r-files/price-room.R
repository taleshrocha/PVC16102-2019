# This file plots the box-plot graphic of the price per rooms.

source("source.R")

olx %>%
  ggplot() +
  geom_boxplot(aes(x = preco, y = quartos, color = quartos), show.legend = TRUE)

ggsave("price-room")
