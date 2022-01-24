library(readr)
library(dplyr)
library(forcats)
library(ggplot2)
library(patchwork)

# This file plots the column graphic of the rooms frequency.

olx <- readr::read_csv("olx-data.csv")

olx %>%
  count(quartos) %>%
  filter(!is.na(quartos)) %>% 
  top_n(10, n) %>%
  #mutate(quartos = forcats::fct_reorder(quartos, n)) %>% 
  ggplot() +
  geom_col(aes(x = quartos, y = n, fill = quartos), show.legend = FALSE) +
  geom_label(aes(x = quartos, y = n/2, label = n)) +
  coord_flip()

ggsave(
filename = "images/rooms-freq.png",
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

# This file plots the boxplot graphic of the price pre rooms.

olx <- readr::read_csv("olx-data.csv")

olx %>%
  ggplot() +
  geom_boxplot(aes(x = preco, y = quartos, color = quartos), show.legend = TRUE)

ggsave(
filename = "images/price-rooms.png",
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
