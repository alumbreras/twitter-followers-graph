### Description
Fetch the followers of a user and the following relationship between them. Create a graph file with this graph.

###Usage

You are supposed to have a config.yml file in the same directory, with your keys to access the API. Such as:

    CONSUMER_KEY: 6it3IkPFI4RNIGhIci1w
    CONSUMER_SECRET: zGUE1bTucHcNn5IxFNyBP8dN2EvbrMtij5xuWHqcW0

Then there are three functions to be executed secuentially:

*  **    python followers.py -u johnsnow -f api_followers**

Fetches the followers of user and their followers as well. Store them into files. By storing them into files we can, at different executions, check whether the user had already been fetched and avoid unnecessary API calls. 

Due to the API rate limitations, we can only fetch the followers of 15 users in a 15 minutes window. Thus, for a user with 1000 followers it requires 1000 minutes to complete.

Nonetheless, the script can be stoped at any time and the final graph will contain only those followers whose followers have been fetched.

* **    python followers.py -u johnsnow -f api_screen_names**

Fetches the screen names of the followers and store them into files. It allows the final graph to contain the screen names and therefore Gephi can plot them instead of the user ids. 

If the screen name of a user is not fetched, the `graph()` function will assign its id as screen name. 

This is very cheap in terms of API calls since we can retrieve 100 screen names per call.

*  **python -u johnsnow -f graph**

Builds a graph file (graphML format) form the information stored in files (followers and screen names). The graph can be directly opened by Gephi.


### Once in Gephi

Once in Gephi, I recommend the following steps (I assume you know how to do this):

*  Remove the ego 'user' since it provides no information at all (every one is connected to it).

* Detect connected components. Remove nodes that are not in the biggest component. If they are in components of size 1, they may be bots. If they are in small components, they might be family, or isolated some group of people not related to the other ones. 

* For the vertices, show only  the 'name' attribute.

* Run the Force Atlas 2 layout algorithm. Then use expand, rotate, adjust labels to minimize overlapping.

* Detect modularity and PageRank. Make colors of vertices correspond to their modularity group. Make sizes of vertices correspond to PageRank.

* More fine-tunning until you like the result.

Have fun!

![ego alberto_lm](https://github.com/alumbreras/twitter-followers-graph/blob/master/outputs/alberto_lm.png) 
