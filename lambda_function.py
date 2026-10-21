import boto3

s3 = boto3.client("s3")

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    file_size = event['Records'][0]['s3']['object']['size']
    file_name = file_key.split("/")[-1]

    print("New file:", file_key, "Size:", file_size)

    # ignore the raw/ folder marker
    if file_key.endswith("/"):
        print("Folder marker, ignored")
        return {'statusCode': 200, 'body': 'ignored'}

    required = {
        "olist_orders_dataset.csv": ["order_id", "customer_id", "order_status", "order_purchase_timestamp"],
        "olist_customers_dataset.csv": ["customer_id", "customer_unique_id", "customer_city", "customer_state"],
        "olist_products_dataset.csv": ["product_id", "product_category_name"],
        "olist_order_items_dataset.csv": ["order_id", "order_item_id", "product_id", "price", "freight_value"],
    }

    reason = ""

    # check extension
    if not (file_name.endswith(".csv") or file_name.endswith(".json")):
        reason = "wrong file extension"

    # check empty
    elif file_size == 0:
        reason = "file is empty"

    # check expected name
    elif file_name not in required:
        reason = "file name is not one of the 4 expected files"

    # check required columns
    else:
        response = s3.get_object(Bucket=bucket_name, Key=file_key, Range="bytes=0-4095")
        text = response["Body"].read().decode("utf-8-sig")
        header = text.split("\n")[0].strip()
        columns = [c.strip().strip('"') for c in header.split(",")]
        missing = [c for c in required[file_name] if c not in columns]
        if missing:
            reason = f"missing columns {missing}"

    if reason == "":
        print(f"VALID: {file_name}")
        return {'statusCode': 200, 'body': 'VALID'}

    print(f"INVALID: {file_name} - {reason}")
    s3.copy_object(Bucket=bucket_name, CopySource={"Bucket": bucket_name, "Key": file_key}, Key=f"rejected/{file_name}")
    s3.delete_object(Bucket=bucket_name, Key=file_key)
    print(f"Moved to rejected/{file_name}")
    return {'statusCode': 200, 'body': 'INVALID'}