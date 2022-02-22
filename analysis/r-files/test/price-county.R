#source("../source.R")
library(tidyverse)

#olx$quartos[olx$quartos == "--"] <- NA

olx <- readr::read_csv("../../olx-data.csv")

olx %>%
  ggplot() +
  geom_bar(aes(x = preco, fill = municipio), show.legend = TRUE, stat = "bin") +
  labs(
       x = "Preço (R$)",
       y = "N° de municipios",
       #title = "Gráfico Boxplot",
       title = "Preço por municipios"
  )

ggsave("../../images/test-price-room.png")
