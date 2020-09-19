library(igraph)

e <- read.csv("../edges.csv", header=FALSE)
names(e) <- c("from", "to")

v <- read.csv("../vertices.csv", header=FALSE)
names(v) <- c("name", "timestamp")

mask1 <- e$from %in% v$name
mask2 <- e$to %in% v$name
mask <- mask1 & mask2
e <- e[mask,]
g <- graph.data.frame(e, vertices = v)
g <- delete.vertices(g, V(g)[degree(g)==0])

la <- layout_with_fr(g)
g <- add_layout_(g, in_circle(), component_wise())
memberships.eigen <- cluster_leading_eigen(as.undirected(g))$membership 

indegrees <- degree(g, mode="in")
q_degree <- quantile(indegrees, 0.9)

V(g)$label.cex <- ifelse(degree(g, mode="in")>0, 1+0.5*tanh(indegrees-q_degree), 0)
V(g)$name[degree(g, mode="in")<10] = ""

# Size proportional to degree
V(g)$size <- 1+0.5*tanh(indegrees-q_degree)

plot(g,
     layout = la, 
     vertex.color = memberships.eigen,
     edge.width = 0.2, 
     edge.arrow.size=0.02,
     asp=9/16,
     margin=-0.15)

