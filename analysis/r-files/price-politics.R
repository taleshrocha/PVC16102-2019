source("source.R")
library(ggpubr)

options(scipen = 9999)

olx$preco <- strtoi(olx$preco)

mu <- olx %>%
  group_by(politica) %>%
  summarise(grp.mean = mean(preco))

olx %>%
  ggplot() +
  geom_histogram(aes(x = preco, color = politica, fill = politica, show.legend = FALSE), bins = 30, alpha = 0.4, position = "identity") +
  geom_vline(data = mu, aes(xintercept = grp.mean, color = politica), linetype = "dashed", show.legend = FALSE) +
  scale_x_continuous(breaks = seq(0, 1000000, 100000)) +
  theme_light(base_size=14) +
  theme(axis.title.x = element_blank(),axis.title.y = element_blank()) +
  rotate_x_text(45) +
  guides(fill = FALSE) +
  labs(
       x = "Preço (R$)",
       y = "Densidade",
       title = "Figura 3",
       subtitle = "Preço por política habitacional",
       color = "Política"
  )

ggsave("../images/price-politics.png")
