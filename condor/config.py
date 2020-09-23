import os

dir_path = os.path.dirname(os.path.realpath(__file__))
PATHS = {"in": f"{dir_path}/data/fetched/followers/",
         "out": f"{dir_path}/data/fetched/followees/",
         "names": f"{dir_path}/data/fetched/screen_names/",
         "users": f"{dir_path}/data/fetched/users/",
         "tracked": f"{dir_path}/data/fetched/tracked/",
         "outputs": f"{dir_path}/outputs/"}

print(PATHS)
for path in PATHS.values():
    if not os.path.exists(path):
        os.makedirs(path)