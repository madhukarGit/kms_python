
import boto3
import base64

key_id = 'de83a94e-a9b2-4253-9d1b-52d3d6edd529'

def kms_encrpyt():
  session = boto3.Session()
  clint = session.client("kms")
  encryption_result = clint.encrypt(KeyId=key_id,Plaintext = "hello")
  blob = encryption_result['CiphertextBlob']
  result = base64.b64encode(blob)
  
  decrypt = clint.decrypt(CiphertextBlob = base64.b64decode(result))
  print(decrypt['Plaintext'])

  
  
kms_encrpyt()