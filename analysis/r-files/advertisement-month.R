# This script plots the column graphic of the advertisement per month.

source("source.R")

# TODO: This doesn't filter the year.
olx %>%
  count(mes) %>%
  filter(!is.na(mes)) %>% 
  top_n(10, n) %>%
  #mutate(mes = forcats::fct_reorder(mes, n)) %>% 
  ggplot() +
  geom_col(aes(x = mes, y = n, fill = mes), show.legend = FALSE) +
  geom_label(aes(x = mes, y = n/2, label = n)) +
  coord_flip() +
  labs(
       x = "Mês",
       y = "N° de anúncios",
       title = "N° de anúncios por mês"
  )

ggsave("../images/advertisement-month.png")
