import os

PATHS = {"in": "./data/fetched/followers/",
         "out": "./data/fetched/followees/",
         "names": "./data/fetched/screen_names/",
         "users": "./data/fetched/users/",
         "tracked": "./data/fetched/tracked/",
         "outputs": "./outputs/"}

for path in PATHS.values():
    if not os.path.exists(path):
        os.makedirs(path)