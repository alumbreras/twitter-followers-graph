### Description
Fetch the followers of a user and the following relationship between them. Create a graph file with this graph.

###Usage

It is a simple script with no arguments. User name is to be provided by editint the script, as well as API keys.

There are three functions to be executed secuentially:

*  **api_followers('user')**

Fetches the followers of user and their followers as well. Store them into files. By storing them into files we can, at different executions, check whether the user had already been fetched and avoid unnecessary API calls. 

Due to the API rate limitations, we can only fetch the followers of 15 users in a 15 minutes window. Thus, for a user with 1000 followers it requires 1000 minutes to complete.

Nonetheless, the script can be stoped at any time and the final graph will contain only those followers whose followers have been fetched.

* **api_followers_screen_names('user')**

Fetches the screen names of the followers and store them into files. It allows the final graph to contain the screen names and therefore Gephi can plot them instead of the user ids. 

If the screen name of a user is not fetched, the `graph()` function will assign its id as screen name. 

This is very cheap in terms of API calls since we can retrieve 100 screen names per call.

*  **graph('user')**

Builds a graph file (graphML format) form the information stored in files (followers and screen names). The graph can be directly opened by Gephi.


### Once in Gephi

Once in Gephi, I recommend removing the ego 'user' since it provides no information at all (every one is connected to it).

Then you can run, for instance, the Force Atlas 2 layout algorithm. 

And then detect communities, make vertices sizes proportional to degree,  colors according to communities, and whatever you like.

Have fun!
