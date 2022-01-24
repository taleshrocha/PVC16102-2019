library(readr)
library(dplyr)
library(forcats)
library(ggplot2)
library(patchwork)

# This file plots the column graphic of the county frequency.

olx <- readr::read_csv("olx-data.csv")

olx %>%
  count(mes) %>%
  filter(!is.na(mes)) %>% 
  top_n(10, n) %>%
  #mutate(mes = forcats::fct_reorder(mes, n)) %>% 
  ggplot() +
  geom_col(aes(x = mes, y = n, fill = mes), show.legend = FALSE) +
  geom_label(aes(x = mes, y = n/2, label = n)) +
  coord_flip()

ggsave(
filename = "images/county.png",
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
