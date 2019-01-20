rm(list = ls())
setwd("~/2017.2.27 GSE41258")
library(affy)
library(limma)
library(hgu133a.db)
library(annotate)
data.raw <- ReadAffy()
sampleNames(data.raw)
a <- read.csv("GSE41258  分组信息.csv",header=TRUE)
treatment <- a[3]
treatment <- as.matrix(treatment)
treatment1 <- as.character(treatment)
head(treatment1)
treatment2 <- factor(treatment1)
treatment2
eset.rma <- rma(data.raw)
eset.rma.log2 <- exprs(eset.rma)
eset.rma.log2 <- eset.rma.log2
head(eset.rma.log2)
hist(eset.rma.log2)
boxplot(eset.rma.log2)
data.mas5calls <- mas5calls(data.raw)
eset.mas5calls <- exprs(data.mas5calls)
head(eset.mas5calls)
AP <- apply(eset.mas5calls,1,function(x)any(x=="P"))
present.probes <- names(AP[AP])
results.present <- eset.rma.log2[present.probes,]
probeset=rownames(results.present)
Symbol <- getSYMBOL(probeset,"hgu133a")
a=cbind.data.frame(Symbol,results.present)
a=a[!is.na(a[,1]),]
geneSymbols=a[,1]
a=a[,-1]
a=apply(a,2,as.numeric)
rownames(a)=geneSymbols
head(a)
aaverage<-avereps(as.matrix(a))
design1 <- model.matrix(~0 + treatment2)
design1
colnames(design1) <- c("N","T")
cntrast.matrix1 <- makeContrasts(T-N,levels = design1)
cntrast.matrix1
fit1 <- lmFit(aaverage,design1)
fit1 <- contrasts.fit(fit1, cntrast.matrix1)
fit12 <- eBayes(fit1)
dif1 <- topTable(fit12,coef = 1,n=nrow(fit12))
head(dif1)
write.csv(dif1,"GSE41258 2017.2.27 DE.csv")
