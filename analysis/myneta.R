"
myNeta
Gaurav Sood							    	

"

# for nona
library(goji)

setwd(githubdir)
setwd("indian-politician-bios/")
setwd("dev")

# Read in data
netas <- read.csv("india-mps-all-states.csv")

# Clean Income cols
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

income_cols <- c("self_total_income", "spouse_total_income", "self_movable_assets_totals", "spouse_movable_assets_totals", 
	"self_immovable_assets_totals", "spouse_immovable_assets_totals", "self_liabilities_totals", "spouse_liabilities_totals")

netas[,income_cols] <- lapply(netas[,income_cols], clean_income)

# Total Income
netas$total_income  <- netas$self_total_income + netas$spouse_total_income
netas$total_movable <-  netas$self_movable_assets_totals + netas$spouse_movable_assets_totals
netas$total_immmovable <- netas$self_immovable_assets_totals + netas$spouse_immovable_assets_totals
netas$total_liabilities <- netas$self_liabilities_totals + netas$spouse_liabilities_totals
netas$total_net <- netas$total_movable + netas$total_immmovable - netas$total_liabilities

netas$prop_income   <- ifelse(netas$total_income==0, NA, netas$spouse_total_income/netas$total_income)
netas$prop_movable  <- ifelse(netas$total_movable==0, NA, netas$spouse_movable_assets_totals/netas$total_movable) 
netas$prop_immovable <- ifelse(netas$total_immmovable==0, NA, netas$spouse_immovable_assets_totals/netas$total_immmovable) 
netas$prop_liabilities <- ifelse(netas$total_liabilities==0, NA, netas$spouse_liabilities_totals/netas$total_liabilities) 
netas$prop_net <-  ifelse(netas$total_net==0, NA, (netas$spouse_movable_assets_totals + netas$spouse_immovable_assets_totals- netas$spouse_liabilities_totals)/netas$total_net)
