library(reshape2)
library(ggplot2)
library(gplots)
library(dplyr)
library(stringr)

# Plot a matrix of user similarity




filename <- '../outputs/adjacency.csv'
df <- read.table(filename, sep = ',')
names(df) <- c("from", "to")
df$similarity <- 1
M <- acast(df, from~to, fill = 0)

filename <- '../outputs/similarities.csv'
df <- read.table(filename, sep = ',', header = TRUE)
names(df) <- c("from", "to", "similarity")
M <- acast(df, from~to)


# Remove users with too few followers
users <- unique(df$from)

# Get user-userid dictionary
usernames <- list()
for(uid in list.files('../screen_names/')){
  fname <- paste0("../screen_names/", uid)
  name <- scan(fname, what = character())
  usernames[[name]] <- uid
}

# Select users with more than N followers
popular_users <- c()
users <- as.character(users)
for(user in users){
  uid <- usernames[[user]]
  cat(user, uid)
  fname <- paste0('../followers/', uid)
  if(file.exists(fname)){
    followers <- scan(fname, sep = ',', what = character())
    if(length(followers)>4000){
      popular_users <- c(popular_users, user)
    }
  }
}

# Filter df to keep only selected users
idx <- (df$from %in% popular_users) & (df$to %in% popular_users)
df <- df[idx,]

# Get an ordering where users are already clustered 
res <- heatmap(M, Colv=F, scale='none')
rownames(M)[res$rowInd]
df$from <- factor(df$from, levels = rownames(M)[res$rowInd])
df$to <- factor(df$to, levels = rownames(M)[res$rowInd])

# Plot
base_size <-  9
p <- ggplot(df, aes(x=to, y=from)) + 
  geom_tile(aes(fill = similarity), colour = "white") + 
  scale_fill_gradient(low = "white", high = "steelblue", na.value = 'red') +
  scale_x_discrete(expand = c(0, 0)) +
  scale_y_discrete(expand = c(0, 0)) +
  theme_bw()+
  theme(axis.text.x = element_text(angle = 45, size=base_size*1, hjust = 1, colour = "grey50"),
        axis.ticks = element_blank(),
        panel.grid.minor = element_blank(),
        legend.position = "none")
print(p)
