rm(list = ls())
setwd("~/2017.2.27 GSE41258")
library(affycoretools)
library(affy)
data.raw <- ReadAffy()
summary(data.raw)
sampleNames(data.raw)
a <- read.csv("GSE41258 分组信息.csv",header=TRUE)
a <- a[3]
a <- as.matrix(a)
a <- paste(a,1:90,sep = "-")
head(a)
sampleNames(data.raw) <- a
sampleNames(data.raw)
eset.rma <- rma(data.raw)
eset.rma.log2 <- exprs(eset.rma)
hist(eset.rma.log2)
boxplot(eset.rma.log2)
person_cor <- cor(eset.rma.log2)
dist.lower <- as.dist(1-person_cor)
hc <- hclust(dist.lower,"ave")
plot(hc,cex=0.6)



#以下步骤进行 1.RLE 2.NUSE
library(RColorBrewer)
library(affyPLM)
Pset <- fitPLM(data.raw)
colors <- rainbow(90)
Mbox(Pset,ylim=c(-0.6,0.6),col=colors,main="GSE41258  RLE ",las=3)
boxplot(Pset,ylim=c(0.95,1.4),col=colors,main="GSE41258 NUSE ",las=3)



#以下步骤进行RNA降解图
data.deg <- AffyRNAdeg(data.raw)
plotAffyRNAdeg(data.deg,col=colors)
legend("topleft",rownames(pData(data.raw)),col=colors,,lwd=1,inset = 0.03,cex=0.2)


