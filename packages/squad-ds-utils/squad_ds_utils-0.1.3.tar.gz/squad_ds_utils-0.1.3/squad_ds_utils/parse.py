from urllib.parse import urlparse


def infer_bucket_and_key(url):
    if "call-recordings" in url:
        bucket_object_key_path = urlparse(url).path
        splitted_bucket_object_key_path = bucket_object_key_path.split("/")
        bucket_name = splitted_bucket_object_key_path[1]
        object_key_path = "/".join(splitted_bucket_object_key_path[2:])
    elif "call-recs" in url:
        url_obj = urlparse(url)
        bucket_name = url_obj.netloc.split(".")[0]
        object_key_path = url_obj.path.lstrip("/")

    return (bucket_name, object_key_path)
