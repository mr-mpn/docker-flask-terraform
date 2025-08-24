from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

# Read environment variables for table name and region
DYNAMO_TABLE = os.environ.get("DYNAMO_TABLE", "EightDigit")
AWS_REGION = os.environ.get("AWS_REGION", "eu-central-1")

# Create DynamoDB client using IAM role credentials (no keys needed)
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(DYNAMO_TABLE)

# Default entry if table is empty
DEFAULT_ENTRY = {
    "username": "test",
    "number": "12345678",
    "timestamp": datetime.utcnow().isoformat()
}

def get_latest_entry():
    """Fetch the latest entry from DynamoDB."""
    try:
        response = table.scan()
        items = response.get("Items", [])
        if not items:
            table.put_item(Item=DEFAULT_ENTRY)
            return DEFAULT_ENTRY
        latest = max(items, key=lambda x: x["timestamp"])
        return latest
    except ClientError as e:
        print("DynamoDB Error:", e)
        return DEFAULT_ENTRY

def save_entry(username, number):
    """Save a new entry to DynamoDB."""
    entry = {
        "username": username,
        "number": number,
        "timestamp": datetime.utcnow().isoformat()
    }
    table.put_item(Item=entry)
    return entry

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        digits = [request.form.get(f"digit{i}") for i in range(1, 9)]

        # Validate that all digits are present and numeric
        if username and all(d.isdigit() and len(d) == 1 for d in digits):
            number = "".join(digits)
            save_entry(username, number)
            return redirect(url_for("index"))

    latest_entry = get_latest_entry()
    return render_template("index.html", latest=latest_entry)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
