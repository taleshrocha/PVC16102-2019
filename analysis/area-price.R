library(readr)
library(dplyr)
library(forcats)
library(ggplot2)
library(patchwork)

# This file plots the point graphic of the area per price of the houses

olx <- readr::read_csv("olx-data.csv")

olx %>%
  mutate(valor = preco/area) %>%
  filter(preco <= 250000) %>%
  ggplot() +
  geom_point(aes(x = area, y = preco, color = valor)) + 
  xlim(40, 90) +
  scale_y_continuous(breaks = seq(0, 500000, 50000)) +
  scale_color_gradient(low = "green", high = "red")

ggsave(
filename = "images/area-price.png",
plot = last_plot(),
device = NULL,
path = NULL,
scale = 1,
width = NA,
height = NA,
units = c("in", "cm", "mm", "px"),
dpi = 300,
limitsize = TRUE,
bg = NULL,
)
