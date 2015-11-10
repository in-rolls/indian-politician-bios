"
India MPs
Gaurav Sood							    	

"

# for nona
library(goji)

# Multiple gsub
mgsub <- function(pattern, replacement, x, ...) {
  if (length(pattern)!=length(replacement)) {
    stop("pattern and replacement do not have the same length.")
  }
  result <- x
  for (i in 1:length(pattern)) {
    result <- gsub(pattern[i], replacement[i], result, ...)
  }
  result
}

# Lok Sabha
# ~~~~~~~~~~~~

# Load data
lsabha <- read.csv("data/loksabha-out.csv")
names(lsabha) <- tolower(names(lsabha))
names(lsabha)[13] <- "nchild"
	
# Get sons and dots
temp <- mgsub(c("No.of Sons:", "\t\t\t\t\t\t\tÂ", "Â No.of Daughters:", "\t\t\t\t\t\t\t"), rep("",4), lsabha[,13])	
lsabha$sons <- as.numeric(sapply(strsplit(temp, " "), "[", 1))
lsabha$dots <- as.numeric(sapply(strsplit(temp, " "), "[", 2))

# High Sex-Selective Abortion States
highssa <- c("Punjab", "Haryana", "Jammu and Kashmir", "Gujarat")
lsabha$highssa <- lsabha$state.name %in% highssa


# Exploring data
sum(lsabha$dots)
sum(lsabha$sons)
sum(lsabha$dots)*1000/sum(lsabha$sons)
sum((lsabha$dots)[lsabha$highssa=='TRUE'])/	sum((lsabha$sons)[lsabha$highssa=='TRUE'])
sum((lsabha$dots)[lsabha$party.name=='Indian National Congress'])*1000/sum((lsabha$sons)[lsabha$party.name=='Indian National Congress'])
sum((lsabha$dots)[lsabha$party.name=='Bharatiya Janata Party'])*1000/sum((lsabha$sons)[lsabha$party.name=='Bharatiya Janata Party'])

with(lsabha[lsabha$spouse.name!="",], sum(sons, dots))/nrow(lsabha[lsabha$spouse.name!="",])

# Rajya Sabha Data
rsabha <- read.csv("data/rajyasabha-out.csv")
names(rsabha) <- tolower(names(rsabha))
names(rsabha)[13] <- "nchild"

# Get sons and dots
lstr <- sapply(strsplit(rsabha[,13], " "), length)
rsabha[lstr==3,13]

dots4 <- ifelse(lstr==4, sapply(strsplit(rsabha[,13], " "), "[", 1), NA)
dots2 <- ifelse(lstr==2, sapply(strsplit(rsabha[,13], " "), "[", 1), NA)
sons4 <- ifelse(lstr==4, sapply(strsplit(rsabha[,13], " "), "[", 3), NA)
sons3 <- ifelse(lstr==3, sapply(strsplit(rsabha[,13], " "), "[", 2), NA)

dots <- tolower(ifelse(is.na(dots4), dots2, dots4))
sons <- tolower(ifelse(is.na(sons4), sons3, sons4))

rsabha$dots <- nona(as.numeric(mgsub(c("one", "two", "three", "four", "five", "six", "seven"), 1:7, dots)))
rsabha$sons <- nona(as.numeric(mgsub(c("one", "two", "three", "four", "five", "six", "seven"), 1:7, sons)))
