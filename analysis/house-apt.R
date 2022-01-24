library(readr)
library(dplyr)
library(forcats)
library(ggplot2)
library(patchwork)

# This file plots the column graphic of the house and apt frequency.

olx <- readr::read_csv("olx-data.csv")

olx %>%
  count(categoria) %>%
  filter(!is.na(categoria)) %>% 
  top_n(10, n) %>%
  mutate(categoria = forcats::fct_reorder(categoria, n)) %>% 
  ggplot() +
  geom_col(aes(x = categoria, y = n, fill = categoria), show.legend = FALSE) +
  geom_label(aes(x = categoria, y = n/2, label = n)) +
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

olx %>% 
  filter(!is.na(categoria)) %>% 
  group_by(mes, categoria) %>% 
  summarise(num_cat = n()) %>% 
  ggplot() +
  geom_line(aes(x = mes, y = num_cat, color = categoria, group = 0))
  #scale_color_discrete(labels = c("Casa", "Apartamento"))

imdb %>% 
  filter(!is.na(cor)) %>% 
  group_by(ano, cor) %>% 
  summarise(num_filmes = n()) %>% 
  ggplot() +
  geom_line(aes(x = ano, y = num_filmes, color = cor))
  #scale_color_discrete(labels = c("Preto e branco", "Colorido"))
