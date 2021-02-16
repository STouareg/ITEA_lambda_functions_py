import telebot
import boto3
import os
import datetime

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
    bot = telebot.TeleBot(TOKEN)

    command = message.get('text', '')
    if chat['id'] == int(ADMINCHAT):

        if command == '/listbucket':
            s3 = boto3.client('s3')
            response = s3.list_buckets()
            buckets = 'Bucket is:'
            for bucket in response['Buckets']:
                buckets = buckets + ' ' + bucket["Name"]
            bot.send_message(chat['id'], buckets)
            return RESPONSE_200
     #
     # 2nd method:
     #   if command == '/listbucket':
     #       s3 = boto3.resource('s3')
     #       buckets = 'Bucket is:'
     #       for bucket in s3.buckets.all():
     #           buckets = buckets + ' ' + bucket.name
     #       bot.send_message(chat['id'], buckets)
     #       return RESPONSE_200

        elif command == '/getcost':
            billing_client = boto3.client('ce')
        #    today = date.today() 
        #    yesterday = today - datetime.timedelta(days = 1) 
        #    str_today = str(today) 
        #    str_yesterday = str(yesterday)
            #first_day_of_month = TODAY.replace(day=1)
            #str_first_day_of_month = str(first_day_of_month)     
        #    billing = billing_client.get_cost_and_usage(
        #        TimePeriod={ 
        #            'Start': str_yesterday, 
        #            'End': str_today },
        #        Granularity='DAILY', 
        #        Metrics=['UnblendedCost',] 
        #    )
            bot.send_message(chat['id'], 'billing')
            return RESPONSE_200
        #


        elif command == '/help':
            bot.send_message(chat['id'], 'You can type this: /listbucket, /getcost, /help')
            return RESPONSE_200

        else:
            bot.send_message(chat['id'], "Hello. You can type /help to release help docs.")
            return RESPONSE_200

    else: 
        bot.send_message(chat['id'], "You not allowed.")
        return RESPONSE_200

    return RESPONSE_200
