from scalesim.scale_sim import scalesim
config_path='C:/Users/Madhur/Documents/IITD/COL-719/Project/Alexnet/Config/scale.cfg'
topo_path='C:/Users/Madhur/Documents/IITD/COL-719/Project/Alexnet/Config/alexnet.csv'
top='C:/Users/Madhur/Documents/IITD/COL-719/Project/Alexnet/Config/Output'
s = scalesim(save_disk_space=False, verbose=True,
              config=config_path,
              topology=topo_path
              )

s.run_scale(top_path=top)