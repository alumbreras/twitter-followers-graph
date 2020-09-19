library(reshape2)
library(ggplot2)
library(gplots)
library(dplyr)
library(stringr)
library(yaml)
#TODO: show the ideal blocks, nowing each member's party.
# members sorted by party so that we can see which blocks are more dense
# and with less leaks to other blocks

# Plot a matrix of user similarity

# Spanish parliament
filename.sim <- '../outputs/similarity_diputados_out.csv'
filename.adj <- '../outputs/adjacency.csv'
filename.labels <- '../diputados_labeled.csv'

# badalona
filename.sim <- '../outputs/similarity_badalona_out.csv'
filename.adj <- '../outputs/adjacency-badalona_out.csv'
filename.labels <- '../badalona_labeled.csv'

# Catalan parliament
filename.sim <- '../outputs/similarity_parlamentcat_in.csv'
filename.adj <- '../outputs/adjacency-parlamentcat_out.csv'
filename.labels <- '../parlamentcat_labeled.csv'


# Load dataframe with users info
usernames <- list()
df.users <- data.frame()
for(user in list.files('../users/')){
  fname <- paste0("../users/", user)
  info <- yaml.load_file(fname)
  
  # preserve all fields but 'description'
  info[sapply(info, is.null)] <- NA
  info$description <- NULL
  info$url <- NULL
  info$location <- NULL
  info$created_at <- NULL
  info <- t(unlist(info, use.names=TRUE))
  
  df.users <- rbind(df.users, info)
}
df.users$followers_count <- as.numeric(as.character(df.users$followers_count))
df.users$friends_count <- as.numeric(as.character(df.users$friends_count))
df.users$favourites_count <- as.numeric(as.character(df.users$favourites_count))
df.users$statuses_count <- as.numeric(as.character(df.users$statuses_count))


df <- read.table(filename.sim, sep = ',', header = TRUE)
names(df) <- c("from", "to", "similarity")
M <- acast(df, from~to, drop=FALSE)

df <- read.table(filename.adj, sep = ',')
names(df) <- c("from", "to")
df$similarity <- 1
M <- acast(df, from~to, fill = 0, drop=FALSE)

# Leave only users in the matrix
users <- unique(df$from)
df.users <- filter(df.users, screen_name %in% unique(df$from))

# Add user labels
df.users_labeled <- read.table(filename.labels, sep = ',')
names(df.users_labeled) <- c("screen_name", "party")
df.users <- merge(df.users, df.users_labeled)
df.indegrees <- data.frame(screen_name=colnames(M), indegree = colSums(M))
df.users <- merge(df.users, df.indegrees)
#df.users <- merge(df.users, data.frame(screen_name=colnames(M), outdegree = rowSums(M)))

# remove users with few followers (for readability) 
df.users <- df.users %>% filter(followers_count>00)

# Filter df to keep only selected users
popular_users <- df.users$screen_name
idx <- (df$from %in% popular_users) & (df$to %in% popular_users)
df <- df[idx,]

# Get an ordering where users are already clustered 
res <- heatmap(M, Colv=F, scale='none')
rownames(M)[res$rowInd]
df$from <- factor(df$from, levels = rownames(M)[res$rowInd])
df$to <- factor(df$to, levels = rownames(M)[res$rowInd])


# Get order by followers
df.users <- df.users %>% arrange(-followers_count)
df$from <- factor(df$from, levels = df.users$screen_name)
df$to <- factor(df$to, levels = df.users$screen_name)

# Get order by followers among users
df.users <- df.users %>% arrange(-indegree)
df$from <- factor(df$from, levels = df.users$screen_name)
df$to <- factor(df$to, levels = df.users$screen_name)

# Get order by party, name
df.users <- df.users %>% arrange(party, screen_name)
df$from <- factor(df$from, levels = df.users$screen_name)
df$to <- factor(df$to, levels = df.users$screen_name)

# Store sorted matrix 
V <- acast(df, from~to, fill=0)
save(V, file="adjacency_parlamentcat_sorted.RData")


# Plot
base_size <-  6
p <- ggplot(df, aes(x=to, y=from)) + 
  geom_tile(aes(fill = similarity), colour = "white") + 
  scale_fill_gradient(low = "white", high = "steelblue", na.value = 'red') +
  scale_x_discrete(expand = c(0, 0)) +
  scale_y_discrete(expand = c(0, 0)) +
  theme_bw()+
  theme(axis.text.x = element_text(angle = 45, size=base_size*1, hjust = 1, colour = "grey50"),
        axis.text.y = element_text(size=base_size*1, hjust = 1, colour = "grey50"),
        axis.ticks = element_blank(),
        panel.grid.minor = element_blank(),
        legend.position = "none")
print(p)
