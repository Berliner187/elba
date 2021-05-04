import os


for item in os.listdir("."):
    if item.endswith(".py"):
        os.system("cp " + item + " ~/elba")

