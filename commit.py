import os

message = input("What you did?: ")

os.system("git add .")
print("git add .")
os.system("git commit -m \"" + message + "\"")
print("git commit -m " + message)
os.system("git push")
print("git push")
