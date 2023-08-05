import requests
import json
from airbyte_cdk.models import AirbyteConnectionStatus,Status

class IPFSDestination:
    """
    destination connector for IPFS as destination .
    This function is used to initialize a IPFSdestination object and is called when creating an instance of this class.
    Configuration parameters in json format:
    
    """

    def __init__(self, config: dict, clientSelf):
        self.clientSelf = clientSelf
        self.APIBaseURL = config["APIBaseURL"]


    def check(self):
  
  
        """
        This check() function is used to check if the url  connection is successful.
        It attempts to connect to the IPFS url provided by user  and prints a success message if successful.
        """
        try:

            f = requests.get(self.APIBaseURL)
            if f.ok :
                self.clientSelf.logInfo(self.clientSelf.step, 'check IPFS node connection successful')
                return AirbyteConnectionStatus(status=Status.SUCCEEDED)
            else :
                self.clientSelf.logError(self.clientSelf.step, f"Failed to load IPFS url provided: {str(f._content)}")
                return AirbyteConnectionStatus(status=Status.FAILED,message=str(f._content))
            
        except Exception as e:
            self.clientSelf.logError(self.clientSelf.step, f"Failed to load IPFS url provided: {str(e)}")

   
    def write(self,path, myFiles):
        """
        This function is used to write data  on the IPFS node. It takes in the file object . 
        It tries to uploade file on  IPFS node and return output object with file ,hash, uploaded size and url to access it .
        """
        
        try:
            
            api =str(self.APIBaseURL)
            if path :         
                newURL = api + "?dir_path=" + str(path)
            else :
                newURL = api
            x = requests.post(newURL, files =myFiles)
                 
            if x.status_code == 200:
                self.clientSelf.logInfo(self.clientSelf.step, 'IPFS  connection successful')
                outputContent = json.loads(x.content)
                self.clientSelf.logInfo(self.clientSelf.step, str(outputContent))
                return  outputContent
            else : 
                self.clientSelf.logError(self.clientSelf.step, f"Failed to load IPFS url provided: {str(x._content)}")
                return x.content
            
        except Exception as e:
            self.clientSelf.logError(self.clientSelf.step, f"Failed to load IPFS url provided: {str(e)}")
  