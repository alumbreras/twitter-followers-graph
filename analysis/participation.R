library(dplyr)
library(jsonlite)
library(ggplot2)
library(anytime)
library(tm)
library(topicmodels)
library(slam)

keywords <- c('#pensionesdignas',
              '#Puigdemont1',
              '#ObjetivoPensiones',
              '#DEPPescaíto', 
              '#ObjetivoMujeres', 
              '#IzquierdaSalvados',
              '#feijóosalvados')

keywords <- c('#feijóosalvados')
keywords <- c('#Puigdemont1')

df <- data.frame()
for(keyword in keywords){
  fname <- paste0('../tracked/', keyword, '.json')
  
  # If file has comma at the end
  #data <- sprintf("[%s", paste(readLines(fname), collapse=""))
  #data <- paste(substr(data, 1, nchar(data)-1), ']')
  #df_ <- fromJSON(data)
  
  # If file has no comma at the end
  #df <-fromJSON(sprintf("[%s]", paste(readLines(fname), collapse="")))
  
  # If proper JSON file
  df_ <- fromJSON(fname)
  
  #df <-fromJSON(sprintf("%s", paste(readLines(fname), collapse="")))
  
  #df_$text <- NULL
  df_$keyword <- keyword
  cat("\nKeyword:", keyword)
  cat("\nNumber of tweets:", nrow(df_))
  cat("\nNumber of users", length(unique(df_$user)))
  
  
  df_$seconds <- df_$timestamp - min(df_$timestamp)
  df_$hours <- (df_$seconds - min(df_$seconds))/3600
  df_$date <- anytime(df_$timestamp)
  df_$ntweet <- 1:nrow(df_)
  df_$nusers <- cumsum(!duplicated(df_$user))
  df_$nusers_norm <- df_$nusers/length(unique(df_$user))
  df_$hours_norm <- df_$hours/max(df_$hours)
  
    
  df <- rbind(df, df_)
}

base_size=9
g <- ggplot(df, aes(x=hours, y=ntweet, group=keyword, color=keyword)) + geom_line() + 
    xlab('hora') + ylab('tweets')+
    theme_bw()
print(g)

g <- ggplot(df, aes(x=hours, y=nusers, group=keyword, color=keyword)) + geom_line() + 
  xlab('hora') + ylab('users')+
  theme_bw()
print(g)


# Normalized
g <- ggplot(df, aes(x=hours_norm, y=nusers_norm, group=keyword, color=keyword)) + geom_line() + 
  xlab('hora') + ylab('users')+
  theme_bw()
print(g)


# Cumsum of participations
df_ <- count(df, keyword, user) %>%
  arrange(keyword, n) %>% 
  group_by(keyword) %>% mutate(cum = cumsum(n)/sum(n), idx = 1:n(), perc_user = idx/n()) %>%  
  ungroup
g <- ggplot(df_, aes(x=perc_user, y=cum, group=keyword, color=keyword)) + geom_line() + 
  xlab('user') + ylab('% tweets')+
  theme_bw()
print(g)


###############################################################################
# Text Mining
###############################################################################
myCorpus <- Corpus(VectorSource(df$text))
myCorpus <- tm_map(myCorpus, content_transformer(tolower))
removeURL <- function(x) gsub("http[^[:space:]]*", "", x)
myCorpus <- tm_map(myCorpus, content_transformer(removeURL))
myCorpus <- tm_map(myCorpus, stripWhitespace)
myCorpusCopy <- myCorpus

tdm <- TermDocumentMatrix(myCorpus, control = list(weighting =
                                                     function(x)
                                                       weightTfIdf(x, normalize =
                                                                     FALSE)))
tdm <- TermDocumentMatrix(myCorpus)

findFreqTerms(tdm, lowfreq = 20)

dtm <- as.DocumentTermMatrix(tdm)

# remove empty docs
rowTotals <- slam::row_sums(dtm, na.rm = T)
dtm <- dtm[rowTotals> 0, ]  
lda <- LDA(dtm, k=8)
term <- terms(lda, 7)
term <- apply(term, MARGIN = 2, paste, collapse = ", ")

topics <- topics(lda)
topics <- data.frame(date=1:length(topics), topic=topics)
ggplot(topics, aes(date, fill = term[topic])) +
  geom_density(position = "stack")