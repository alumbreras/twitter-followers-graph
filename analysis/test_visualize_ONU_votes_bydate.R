library(unvotes)
library(reshape2)
library(gplots)
library(dplyr)
library(ggplot2)
library(zoo)

# Set dataframe
df <- un_votes %>% select(rcid, country, vote) 

# Create a df dictionary rcid-date
df.dates <- un_roll_calls %>% select(rcid, date) %>% distinct(rcid, date) %>% arrange(date, rcid)
df.dates$rcid_sorted <- match(df.dates$rcid, unique(df.dates$rcid))
df.dates$date <- as.Date(df.dates$date)
df.dates$year <- format(as.yearmon(df.dates$date), "%Y")

df <-  merge(df, df.dates)
df$vote <- as.integer(df$vote)

# Drop countries with low activity (lots of NA)
top_countries <- names(sort(table(df$country), decreasing = TRUE))[1:75]
df <- df %>% filter(country %in% top_countries)

# Sort contries by similarity and use this to factor then accordingly
V <- acast(df, country~rcid, value.var = "vote", drop=FALSE)
names(dimnames(V)) <- c("country", 'rcid')
res <- heatmap.2(V)
df.positions <- data.frame(country = rownames(V)[res$rowInd], position=1:nrow(V))
df$country <- factor(df$country, levels = df.positions$country)


# Create a df dictionary rcid-issue
# df.issues <- un_roll_call_issues %>% select(rcid, issue) %>% distinct(rcid, issue) %>% arrange(issue, rcid)
# df.issues$rcid_sorted <- match(df.issues$rcid, unique(df.issues$rcid))
# df.dates <- df.issues 
# df <-  merge(df, df.dates, by="rcid")
# df$year <- NULL
# df$rcid_sorted.y <- NULL
# names(df)[5] <- "rcid_sorted"
# names(df)[6] <- "year"
# names(df.dates)[2] <- "year"


################################################################################
# Plot
################################################################################
df.V <- df

base_size <- 7
axis.text.y <- element_text(angle = 0, size=base_size*1, hjust = 1, colour = "black")
axis.text.x <- element_text(angle = 90, size=base_size*1, hjust = 1, colour = "grey50")

mytheme <- theme(
  axis.text.x   = axis.text.x,
  axis.text.y   = axis.text.y,
  axis.ticks.x  = element_blank(),
  axis.ticks.y  = element_blank(),
  panel.background = element_blank(),
  panel.grid.minor = element_blank(),
  panel.grid.major = element_blank(),
  legend.title = element_blank(),
  legend.key= element_rect(colour = "black"),
  aspect.ratio=1) 

  
  selected.breaks <- seq(1, max(df.V$rcid_sorted), by=150)
  selected.labels <- df.dates$year[selected.breaks]
  df.V$vote <- as.factor(df.V$vote)
  
  p <- ggplot(df.V, aes(x=rcid_sorted, y=country)) + 
    geom_tile(aes(fill = vote), colour = "white") + 
    scale_fill_manual(values=c("green", "blue", "red"), na.value = 'white',
                      labels = c("Yes", "Abstain", "No")) +
    scale_x_continuous(expand = c(0, 0), breaks=selected.breaks, 
                                         labels=selected.labels) +
    scale_y_discrete(expand = c(0, 0)) +
      theme_bw()  + ylab("") + xlab("votes") + mytheme +   coord_fixed()
  print(p)
  
  
  # Sorted by vote similarity
  

  
  # Plor for factor case
  df.positions <- data.frame(rcid = colnames(V)[res$colInd], position=1:ncol(V))
  df$rcid <- factor(df$rcid, levels = df.positions$rcid)
  df.V <- df
  
  selected.breaks <- levels(df.V$rcid)[seq(1, length(levels(df.V$rcid)), by=150)]
  selected.labels <- df.dates$year[selected.breaks]
  df.V$vote <- as.factor(df.V$vote)
  
  p <- ggplot(df.V, aes(x=rcid, y=country)) + 
    geom_tile(aes(fill = vote), colour = "white") + 
    scale_fill_manual(values=c("green", "blue", "red"), na.value = 'white',
                      labels = c("Yes", "Abstain", "No")) +
    scale_x_discrete(expand = c(0, 0), breaks=selected.breaks, labels=selected.labels) +
    scale_y_discrete(expand = c(0, 0)) +
    theme_bw()  + ylab("") + xlab("votes") +
    theme(
      axis.text.x   = element_blank(),
      axis.text.y   = axis.text.y,
      axis.ticks.x  = element_blank(),
      axis.ticks.y  = element_blank(),
      panel.background = element_blank(),
      panel.grid.minor = element_blank(),
      panel.grid.major = element_blank(),
      legend.title = element_blank(),
      legend.key= element_rect(colour = "black"),
      aspect.ratio=1) +
    coord_fixed()
  print(p)
p