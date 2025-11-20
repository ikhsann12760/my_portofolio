from flask import Flask, jsonify

def handler(event, context):
    return {
        "statusCode": 200,
        "body": jsonify({"message": "Hello from Flask!"})
    }