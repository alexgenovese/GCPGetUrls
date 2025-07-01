from google.cloud import storage


def is_hidden_or_temp(filename):
    # File nascosti (iniziano con .) o temporanei (iniziano con ~ o finiscono con .tmp/.temp)
    basename = filename.split('/')[-1]
    if basename.startswith('.') or basename.startswith('~'):
        return True
    if basename.lower().endswith(('.tmp', '.temp')):
        return True
    return False

def list_gcs_folder_urls(bucket_name, folder_prefix, key_path, output_file):
    storage_client = storage.Client.from_service_account_json(key_path)
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=folder_prefix)
    
    urls = []
    for blob in blobs:
        if is_hidden_or_temp(blob.name):
            continue
        url = f"https://storage.googleapis.com/{bucket_name}/{blob.name}"
        urls.append(url)
    
    # Salva gli URL su file
    with open(output_file, 'w') as f:
        for url in urls:
            f.write(url + '\n')
    print(f"Salvati {len(urls)} URL in {output_file}")

# Esempio di utilizzo
bucket_name = "tryonyou"
folder_prefix = "xprocess/generated-retro/"  # Assicurati di includere la barra finale se necessario
key_path = "./google-storage-auth.json"
output_file = "urls.txt"

list_gcs_folder_urls(bucket_name, folder_prefix, key_path, output_file)
