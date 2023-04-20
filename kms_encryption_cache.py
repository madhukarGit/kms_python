
# Create an AWS KMS master key provider
#  The input is the Amazon Resource Name (ARN) 
#  of an AWS KMS key
import aws_encryption_sdk
from aws_encryption_sdk import CommitmentPolicy
import boto3

s3 = s3 = boto3.resource('s3',
    endpoint_url = 'https://s3.eu-central-1.wasabisys.com',
    aws_access_key_id = 'MY_ACCESS_KEY',
    aws_secret_access_key = 'MY_SECRET_KEY'
)

def encrypt_with_caching_client(kms_key_arn, max_age_in_cache, cache_capacity):
    """Encrypts a string using an &KMS; key and data key caching.

    :param str kms_key_arn: Amazon Resource Name (ARN) of the &KMS; key
    :param float max_age_in_cache: Maximum time in seconds that a cached entry can be used
    :param int cache_capacity: Maximum number of entries to retain in cache at once
    """
  
    # Security thresholds
    #   Max messages (or max bytes per) data key are optional
    MAX_ENTRY_MESSAGES = 100

    # Set up an encryption client with an explicit commitment policy. Note that if you do not explicitly choose a
    # commitment policy, REQUIRE_ENCRYPT_REQUIRE_DECRYPT is used by default.
    client = aws_encryption_sdk.EncryptionSDKClient(commitment_policy=CommitmentPolicy.REQUIRE_ENCRYPT_REQUIRE_DECRYPT)

    # Create a master key provider for the &KMS; key
    key_provider = aws_encryption_sdk.StrictAwsKmsMasterKeyProvider(key_ids=[kms_key_arn])

    # Create a local cache
    cache = aws_encryption_sdk.LocalCryptoMaterialsCache(cache_capacity)

    # Create a caching CMM
    caching_cmm = aws_encryption_sdk.CachingCryptoMaterialsManager(
        master_key_provider=key_provider,
        cache=cache,
        max_age=max_age_in_cache,
        max_messages_encrypted=MAX_ENTRY_MESSAGES,
    )
    return {"client":client,"caching_cmm":caching_cmm}
  

def encrypt_text(txt):
  encryption_context = {"purpose": "test"}
  my_data = "My plaintext data"
  encrypted_message, _header = txt["client"].encrypt(
        source=my_data, materials_manager=txt["caching_cmm"], encryption_context=encryption_context
  )
  with open("encrypt_kms.txt","wb") as binary_file:
    binary_file.write(encrypted_message)


def decrypt_data(txt,ciphertext):
  decrypted_plaintext, decryptor_header = txt["client"].decrypt(
        source=ciphertext, materials_manager=txt["caching_cmm"]
  )
  print(decrypted_plaintext.decode("utf-8"))
  
if __name__ == "__main__":
  # Create an encryption context
  kms_key_arn = "arn:aws:kms:us-east-1:436904145537:key/de83a94e-a9b2-4253-9d1b-52d3d6edd529"
  result = encrypt_with_caching_client(kms_key_arn,60.0,10) 
  cipherText = encrypt_text(result)
  with open("encrypt_kms.txt","rb") as text:
    resultEncode =  text.read()
    print(resultEncode)
    decrypt_data(result,resultEncode)
  

