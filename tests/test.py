import os
import requests

def sol():
    name=[i for i in os.listdir() if i.endswith('.csv')]
    for i in name:
        response=requests.post('https://vehicleroutingproblem.herokuapp.com/handleUpload',files=dict(datax=open(i,'r')))
        file_output=open(i[:-4]+'.txt','w')
        file_output.write(response.content.decode('utf-8'))
        file_output.close()
    return
if __name__=='__main__':
    sol()
