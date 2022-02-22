source("source.R")
library(ggpubr)

options(scipen = 9999)

olx$preco <- as.numeric(olx$preco)

mu <- olx %>%
  summarise(grp.mean = mean(preco), grp.des.pad = sqrt(var(preco)))

p1 <- olx %>%
  ggplot() +
  geom_density(aes(x = preco)) +
  geom_vline(data = mu, aes(xintercept = grp.mean), linetype = "dashed") +
  geom_vline(data = mu, aes(xintercept = grp.mean + grp.des.pad), linetype = "dashed", color = "#ba1a1a") +
  geom_vline(data = mu, aes(xintercept = grp.mean - grp.des.pad), linetype = "dashed", color = "#1d1aba") +
  scale_x_continuous(breaks = seq(0, 1000000, 100000)) +
  theme_light(base_size=14) +
  #geom_label(data = mu, aes(x = grp.mean, y = 0.000010, label = round(grp.mean)), size = 3, vjust = 0, hjust = -0.2) +
  scale_color_viridis_d() +
  theme(axis.title.x = element_blank(),axis.title.y = element_blank()) +
  rotate_x_text(45) +
  labs(
       x = "Preço (R$)",
       y = "Densidade",
       title = "Figura 3",
       subtitle = "Preço por política habitacional",
  )

ggsave("../images/desvio-padrao.png")
