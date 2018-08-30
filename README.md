# Twitter tracker

## Egonets

### Description
Fetch the followers of a user and the following relationship between them. Create a graph file with this graph.

### Usage

You are supposed to have a config.yml file in the same directory, with your keys to access the API. Such as:

    CONSUMER_KEY: 6it3IkPFI4RNIGhIci1w
    CONSUMER_SECRET: zGUE1bTucHcNn5IxFNyBP8dN2EvbrMtij5xuWHqcW0

Then there are three functions to be executed secuentially:

*  **python followers.py -u johnsnow -f api_followers**

*  **python followers.py -u johnsnow -f api_followees**


Fetches the followers/followees of user and their followers as well. Store them into files. By storing them into files we can, at different executions, check whether the user had already been fetched and avoid unnecessary API calls. 

Due to the API rate limitations, we can only fetch the followers of 15 users in a 15 minutes window. Thus, for a user with 1000 followers it requires 1000 minutes to complete.

Nonetheless, the script can be stoped at any time and the final graph will contain only those followers whose followers have been fetched.

* **python followers.py -u johnsnow -f api_followers_names**

* **python followers.py -u johnsnow -f api_followees_names**

Fetches the screen names of the followers/followees and store them into files. It allows the final graph to contain the screen names and therefore Gephi can plot them instead of the user ids. 

If the screen name of a user is not fetched, the `graph()` function will assign its id as screen name. 

This is very cheap in terms of API calls since we can retrieve 100 screen names per call.

*  **python followers.py -u johnsnow -f graph_followers**

*  **python followers.py -u johnsnow -f graph_followees**


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



## Keyword Communities

Reproduces the social network of the users who tweeted a given keyword

A typical use case: :

* Use `stream_tracker` to track the twitter stream and get tweets containing the keyword.
   *  output: `tracked/keyword.txt`

* Use `participation` to query the API to download the followers of participants and
to create a the social graph to be read by Gephi, R, etc
   *  input: `tracked/keyword.json` (to get the participants)
   *  input: `followers/` (to get the relationship between participants)
   *  output: `followers/participantid` (one file per participant)
   *  output: `outputs/edges.csv` (from, to) and `vertices.csv` (screen_name, entry_time).


JSON files should be properly closed by hand (leading and ending brackets)

