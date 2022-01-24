library(readr)
library(dplyr)
library(forcats)
library(ggplot2)
library(patchwork)

# This file plots the column graphic of the county frequency.

olx <- readr::read_csv("olx-data.csv")

olx %>%
  count(municipio) %>%
  filter(!is.na(municipio)) %>% 
  top_n(10, n) %>%
  mutate(municipio = forcats::fct_reorder(municipio, n)) %>% 
  ggplot() +
  geom_col(aes(x = municipio, y = n, fill = municipio), show.legend = FALSE) +
  geom_label(aes(x = municipio, y = n/2, label = n)) +
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
