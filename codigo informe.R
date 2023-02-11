# cargar datos # 

library(readxl)
datos <- read_excel("C:/Users/pc/Downloads/DATOS CORREGIDOS.xlsx", 
                    sheet = "Para comparar")
attach(datos)

## Producto-Hectarias-Produccion ##
anova <- aov(datos$PRODUCCIÓN~PRODUCTO+HECTÁREAS)
summary(anova)
TukeyHSD(anova)

boxplot(datos$HECTÁREAS~datos$PRODUCTO, xlab = "Productos", ylab = "Hectarias")

## Producción-corregimiento #

anova2 <- aov(datos$PRODUCCIÓN~datos$MUNICIPIO+datos$PRODUCTO)
summary(anova2)
TukeyHSD(anova2)

boxplot(datos$PRODUCCIÓN~datos$MUNICIPIO, xlab = "Corregimiento", ylab = "Producción")

