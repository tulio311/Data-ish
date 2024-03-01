# Función para graficar contornos de cualquier verosilitud relativa
plotRelative<-function(l, aG, bG, xL, xR, yL, yR, levels, n, xlab="", 
                       ylab="", main="Contornos de verosimilitud relativa"){
  x_vec = seq(from = xL, to = xR, length.out = n)
  y_vec = seq(from = yL, to = yR, length.out = n)
  R<-function(a, b){
    return(exp(l(a, b) - l(aG, bG)))
  }
  Rmat = matrix(nrow = n, ncol = n)
  for(i in 1:n){
    for(j in 1:n){
      Rmat[i, j] = R(x_vec[i], y_vec[j])
    }
  }
  contour(x_vec,y_vec,Rmat,level=levels,xlab=xlab,ylab=ylab,main=main)
}



# logverosimilitud
logver <- function(a,b){
  return((a-1)*t2 - (t1 / b) - n*log(gamma(a)) - a*n*log(b) )
}


# logverosimilitud perfil de alpha
logverPa <- function(a){
  return((a-1)*t2 - a*n - n*log(gamma(a)) - a*n*log(t1 / (a*n)))
}


# verosimilitud perfil relativa de alpha
verPRa <- function(a){
  return(exp(logverPa(a) - logverPa(emv[1])))
}


# Función para la gráfica PP
pp_plot = function(X, ag, bg, confidence){
  X = pgamma(sort(X), ag, bg)
  print(sort(X))
  print(X)
  Y = seq(1/(n+1), 1, length.out = n)
  # puntos de la muestra
  plot(Y, X,
       main = "Gráfica PP",
       xlab = "Probabilidades teóricas",
       ylab = "Probabilidades empíricas",
       pch = 19,
       cex = 0.5)
  # identidad
  abline(a = 0, b = 1, col = "red", lwd = 2)
  # bandas de confianza
  points(qbeta((1 - confidence)/2, 1:n, n + 1 - 1:n), Y,
         type = "l",
         lty = 2)
  points(qbeta((1 + confidence)/2, 1:n, n + 1 - 1:n), Y,
         type = "l",
         lty = 2)
}

--------------------------------------------------------------------

# Función para cálculo de EMV de cualquier distribución de
# dos parámetros de manera numérica

# Densidad Gamma 
ddist <- function(x,a,b){
  return( (x**(a - 1) * exp(-x / b)) /  (gamma(a)* b**a) )
}

emvdist <- function(vec, X, ddist){
  # Tenemos que optimizar con el negativo de la logverosimilitud
  lvneg <- function(vec, X, ddist){
    lv <- sum(log(ddist(X, vec[1], vec[2])))
    return(-1*lv)
  }
  # Se encuentan los emv optimizando con el método Nelder-Mead, se tiene
  # que mandar el negativo de la logverosimilitud
  emv <- optim(vec, lvneg, X = X, ddist = ddist)$par
  return(emv)
}

X <- c(39.37, 32.39, 68.32, 71.26, 46.41, 42.77, 48.29, 50.98, 46.19, 70.35, 83.39, 63.46, 30.49, 54.23, 39.07, 67.13, 63.2, 34.49, 33.22, 47.41, 36.43, 36.74, 86.26)
t1 <- sum(X)
t2 <- log(prod(X))
n <- 23

# Suma de cuadrados
sc <- sum(X**2)

# Estimadores de momentos
bgm <- (sc - (t1**2 / n)) / t1
agm <- t1 / (n*bgm)

emv <- emvdist(c(agm,bgm), X, ddist)


# Gráfica para los contornos de verosimilitud
plotRelative(logver , emv[1], emv[2], 3, 22, 2, 12, c(0.05,0.15, 0.25, 0.5), 1000)
points(emv[1],emv[2], type = "p",pch = 8, col = "red")
legend("bottomright", legend=expression(paste("(", hat(alpha),"," ,hat(beta),")")),
       pch = 8, col = "red") 

# Gráfica PP
pp_plot(X, emv[1], 1/emv[2], 0.95)

# Verosimilitud perfil relativa de alpha
plot.function(x = function(t) verPRa(t),
              from = 1,
              to = 25, lwd = 2.5,
              col = "springgreen3",
              main = "Verosimilitud perfil de alpha",
              ylab = "perfil",
              xlab = "Valores")

