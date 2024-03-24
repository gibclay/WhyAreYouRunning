from gpsystem import GPSystem
from readers.argreader import ArgReader


argreader = ArgReader("args.txt")
args = argreader.get_all()
start_seed = args["random_gp"]
  
for x in range(10):
  gpsystem = GPSystem("args.txt", seed=start_seed+x)
  gpsystem.run()
