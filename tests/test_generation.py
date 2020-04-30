import sys
import os
import random
def gen():
    name=str(1+len(os.listdir()))+'.csv'
    ware_house=[28.545181,77.1926]
    depotNum=random.randint(5,20)
    vehicleNum=random.randint(1,10)
    file_f=open(name,'w')
    file_output="lat_w,long_w,lat_d,long_d,cap_d,id_d,cap_v,id_v\n"
    cur=0
    for i in range(depotNum):
        lat=ware_house[0]+((random.random()*(2)-1)*(0.4)) # lat+-0.4 0.4 change in latitude corrosponds to around 44.4 km
        lon=ware_house[1]+((random.random()*(2)-1)*(0.4))
        cap=random.randint(0,100)
        file_output+=(str(ware_house[0])+','+str(ware_house[1])+','+str(lat)+','+str(lon)+','+str(cap)+','+str(i))
        if (cur<vehicleNum):
            cap_v=random.randint(0,100)
            file_output+=','+str(cap_v)+','+str(cur)
            cur+=1
        else :
            file_output+=',x,x'
        file_output+='\n'
    
    for cur in range(cur,vehicleNum):
        file_output+=('x')+','+'x'+','+'x'+','+'x'+','+'x'+','+'x'
        cap_v=random.randint(0,100)
        file_output+=','+str(cap_v)+','+str(cur)
        file_output+='\n'
    file_f.write(file_output)
    file_f.close()

if __name__=='__main__':
    n=int(sys.argv[1])
    for i in range(n):
        gen()
