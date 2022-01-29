# This script plots the box-plot of the price per county.

source("source.R")

# TODO: Put labels in the maximum, medium and minimum values.

olx %>%
  filter(municipio == "Natal" | municipio == "Parnamirim") %>%
  filter(preco <= 500000) %>%
  ggplot(aes(x=municipio, y=preco, fill=municipio)) +
  geom_boxplot(show.legend = FALSE) +
  stat_summary(geom="text", fun=quantile,
               aes(label=sprintf("%1.1f", ..y..)),
               position=position_nudge(y=0.33), size=3.5
  ) +
  labs(
       x = "Município",
       y = "Preço (R$)",
       title = "Gráfico Boxplot",
       subtitle = "Preço por município"
  )

ggsave("../images/price-county.png")
