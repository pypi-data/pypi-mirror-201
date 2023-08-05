import requests
import json
from airbyte_cdk.models import AirbyteConnectionStatus,Status

class Destination3TLIPFS:
    """
    destination connector for IPFS as destination .
    This function is used to initialize a IPFSdestination object and is called when creating an instance of this class.
    Configuration parameters in json format:
    
    """

    def __init__(self, config: dict, clientSelf):
        self.clientSelf = clientSelf
        self.APIBaseURL = config["APIBaseURL"]


    def get3TLToken(self,email,password):
        try:
            params = {'email':email,'password':password}
            api= self.APIBaseURL +"getToken"
            resp = requests.get(api,params=params,verify=False) 
            if resp.status_code != 200:
                return "authentication failed"
            else :
                return resp.text

        except Exception as e:
            self.clientSelf.logError(self.clientSelf.step, f"Failed to authenticate: {str(e)}")


    def check(self):
  
  
        """
        This check3TL() function is used to check if the url  connection is successful.
        It attempts to connect to the IPFS url provided by user  and prints a success message if successful.
        this method requires 3tl  token 
        """
        try:

            f = requests.get(self.APIBaseURL)
            if f.status_code == 200 :
                self.clientSelf.logInfo(self.clientSelf.step, 'check IPFS node connection successful')
                return AirbyteConnectionStatus(status=Status.SUCCEEDED)
            else :
                self.clientSelf.logError(self.clientSelf.step, f"Failed to load IPFS url provided: {str(f._content)}")
                return AirbyteConnectionStatus(status=Status.FAILED,message=str(f._content))
            
        except Exception as e:
            self.clientSelf.logError(self.clientSelf.step, f"Failed to load IPFS url provided: {str(e)}")

   
    def write(self,path, myFiles,token):
        """
        This function is used to write data  on the IPFS node. It takes in the file object . 
        It tries to uploade file on private 3TL IPFS node and return output object with file ,hash, uploaded size and url to access it .
        """
        
        try:
            headers={'Authorization':f"Bearer {token}"}
            api =str(self.APIBaseURL) + "uploadfiletoipfs"
            if path :         
                newURL = api + "?dir_path=" + str(path)
            else :
                newURL = api
            x = requests.post(newURL, files =myFiles,headers=headers)
                 
            if x.status_code == 200:
                self.clientSelf.logInfo(self.clientSelf.step, 'IPFS  connection successful')
                
                outputContent = json.loads(x.content)
                hea = str(self.APIBaseURL).split(':',2)
                finalURL= 'http:' + str(hea[1]) + ':8080/ipfs/' + str(outputContent['Hash'])
                finalOutput= {'name':outputContent['Name'],'Hash':outputContent['Hash'],'Size':outputContent['Size'],'URL':finalURL}
                self.clientSelf.logInfo(self.clientSelf.step, str(finalOutput))
                return  finalOutput
            else : 
                self.clientSelf.logError(self.clientSelf.step, f"Failed to load IPFS url provided: {str(x._content)}")
                return x.content
            
        except Exception as e:
            self.clientSelf.logError(self.clientSelf.step, f"Failed to load IPFS url provided: {str(e)}")
  