import telebot
import boto3
import os

RESPONSE_200 = {
      "statusCode" : 200,
      "headers"    : {},
      "body"       : ""
    }

def lambda_handler(event, context):

    update = telebot.types.JsonDeserializable.check_json(event["body"])
    TOKEN     = os.environ['BOT_TOKEN']
    ADMINCHAT = os.environ['ADMIN']

    message = update.get('message')
    if not message:
        return RESPONSE_200

    chat = message.get('chat')
    user = message.get('from')

    bot = telebot.TeleBot(TOKEN)

    command = message.get('text', '')
    if chat['id'] == int(ADMINCHAT):

     #  if command == '/listbucket':
     #      s3 = boto3.client('s3')
     #      response = s3.list_buckets()
     #      for bucket in response['Buckets']:
     #          print(f'  {bucket["Name"]}')

        if command == '/listbucket':
            s3 = boto3.resource('s3')
            buckets = 'Bucket is:'
            for bucket in s3.buckets.all():
                buckets = buckets + ' ' + bucket.name
            bot.send_message(chat['id'], buckets)
            return RESPONSE_200

        elif command == '/help':
            bot.send_message(chat['id'], 'You can type this: /listbucket, /help')
            return RESPONSE_200

        else:
            bot.send_message(chat['id'], "Hello. You can type /help to release help docs.")

    else: 
        bot.send_message(chat['id'], "You not allowed.")

    return RESPONSE_200
