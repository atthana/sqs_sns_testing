import boto3
import json
import uuid
import config

def publish_order():
    sns = boto3.client(
        'sns',
        region_name=config.AWS_REGION,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    )
    
    # จำลองข้อมูลออเดอร์
    order_data = {
        "order_id": str(uuid.uuid4()),
        "item": "Mechanical Keyboard",
        "quantity": 1,
        "customer_email": "q_electronics@hotmail.com"
    }

    # ส่งข้อความเข้า SNS
    response = sns.publish(
        TopicArn=config.SNS_TOPIC_ARN,
        Message=json.dumps(order_data),
        Subject="New Order Created by GR"
    )

    print(f"✅ สร้างออเดอร์สำเร็จ! Message ID: {response['MessageId']}")
    print(f"ข้อมูล: {order_data}")

if __name__ == '__main__':
    publish_order()