---
title: "Analyzing Assets by Spousal "
author: "Gaurav Sood"
date: "2015-12-10"
output: rmarkdown::html_vignette
---

### Netagiri: Spousal Income, Movable and Immovable Assets by Politician Gender  


```r
library(goji) # for nona
library(plyr) # for ddply
library(knitr) # knit2html("analysis/myneta.Rmd")
```


```r
#setwd(githubdir)
#setwd("indian-politician-bios/")
```

Read in data


```r
#netas <- read.csv("data/mynetas.csv")
```

Female Netas


```r
netas$female <- ifelse(netas$gender=="female", 1, 0)
```

# Clean Income cols


```r
clean_income <- function(income_col) {
	# income_col <- netas$spouse_liabilities_totals
	income_col <- tolower(income_col)
	income_col <- gsub("rs|,|~|lacs+|â|\\+|thou|crore| .+", "", income_col)
	income_col <- gsub("^\\s+|\\s+$", "", income_col)
	#income_col <- gsub("^[0-9]", "", income_col)
	income_col <- ifelse(income_col=="", NA, income_col)
	income_col <- ifelse(income_col=="nil", 0, income_col)
	as.numeric(income_col)
}

income_cols <- c("self_total_income", "spouse_total_income", "self_movable_assets_totals", "spouse_movable_assets_totals", "self_immovable_assets_totals", 
	"spouse_immovable_assets_totals", "self_liabilities_totals", "spouse_liabilities_totals")

netas[,income_cols] <- lapply(netas[,income_cols], clean_income)
```

Get variables for total income and spousal share of incomes


```r
netas$total_income  <- netas$self_total_income + netas$spouse_total_income
netas$total_movable <-  netas$self_movable_assets_totals + netas$spouse_movable_assets_totals
netas$total_immmovable <- netas$self_immovable_assets_totals + netas$spouse_immovable_assets_totals
netas$total_liabilities <- netas$self_liabilities_totals + netas$spouse_liabilities_totals
netas$total_net <- netas$total_movable + netas$total_immmovable - netas$total_liabilities

netas$prop_income   <- ifelse(netas$total_income==0, NA, netas$spouse_total_income/netas$total_income)
netas$prop_movable  <- ifelse(netas$total_movable==0, NA, netas$spouse_movable_assets_totals/netas$total_movable) 
netas$prop_immovable <- ifelse(netas$total_immmovable==0, NA, netas$spouse_immovable_assets_totals/netas$total_immmovable) 

# No Spouse Liabilities...tssk tssk
# netas$prop_liabilities <- ifelse(netas$total_liabilities==0, NA, netas$spouse_liabilities_totals/netas$total_liabilities) 
# netas$prop_net <-  ifelse(netas$total_net==0, NA, (netas$spouse_movable_assets_totals + netas$spouse_immovable_assets_totals- netas$spouse_liabilities_totals)/netas$total_net)
```

Spousal income, movable and immovable assets by gender


```r
# Try medians also has distribution of proportions is skewed. Ideally density or boxplot it.

# For female politicians, ~ 53% of income earned by income. For male politicians,  just 21% of income earned by wife.
ddply(netas, ~gender, summarise, mean=mean(prop_income, na.rm=T))
```

```
##   gender      mean
## 1 female 0.5288463
## 2   male 0.2133350
```

```r
# For female politicians, ~ 27% couple's movable assets owned by husband. When male, ~ 34% owned by wife (think gold)
ddply(netas, ~gender, summarise, mean=mean(prop_movable, na.rm=T))
```

```
##   gender      mean
## 1 female 0.2732189
## 2   male 0.3378002
```

```r
# For female politicians, ~ 41% of couple's immovable assets owned by husband. For male politicians, ~ 17% owned by wife.
ddply(netas, ~gender, summarise, mean=mean(prop_immovable, na.rm=T))
```

```
##   gender      mean
## 1 female 0.4119150
## 2   male 0.1724018
```
