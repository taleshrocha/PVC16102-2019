# This script plots the column graphic of the advertisement per month.

source("source.R")

olx %>%
  filter(ano > 2019) %>%
  count(mes) %>%
  filter(!is.na(mes)) %>%
  top_n(12, n) %>%
  mutate(mes = factor(c("Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novenbro", "Dezembro"), levels = c("Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novenbro", "Dezembro"))) %>%
  ggplot() +
  geom_col(aes(x = mes, y = n, fill = mes), show.legend = FALSE) +
  scale_y_continuous(labels = scales::percent_format()) +
  geom_label(aes(x = mes, y = n/2, label = n)) +
  coord_flip() +
  scale_color_viridis_d() +
  theme(axis.title.x = element_blank(),axis.title.y = element_blank()) +
  theme_light(base_size=14) +
  labs(
       x = "Mês",
       y = "N° de anúncios",
       title = "Figura 1",
       subtitle = "N° de anúncios por mês"
  )

ggsave("../images/advertisement-month.png")
