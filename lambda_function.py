import telebot
import boto3
import os
import datetime
import json

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

        if command == '/ListBuckets':
            s3 = boto3.client('s3')
            response = s3.list_buckets()
            buckets = 'Bucket is:'
            for bucket in response['Buckets']:
                buckets = buckets + ' ' + bucket["Name"]
            bot.send_message(chat['id'], buckets)
            return RESPONSE_200
     #
     # 2nd method:
     #   if command == '/ListBuckets':
     #       s3 = boto3.resource('s3')
     #       buckets = 'Bucket is:'
     #       for bucket in s3.buckets.all():
     #           buckets = buckets + ' ' + bucket.name
     #       bot.send_message(chat['id'], buckets)
     #       return RESPONSE_200

        elif command == '/GetCurrentMonthlyCost':
            client = boto3.client('ce')
            todayDate  = datetime.date.today() 
            first_day_of_month = todayDate.replace(day=1)
            billing = client.get_cost_and_usage(
                TimePeriod={ 
                    "Start": str(first_day_of_month), 
                    "End": str(todayDate)},
                Granularity = 'MONTHLY', 
                Metrics = ["UnblendedCost",]
            )
            for r in billing['ResultsByTime']:
                str_amount=(r['Total']['UnblendedCost']['Amount'])

            str_amount = str_amount[:5] + ' usd'
            bot.send_message(chat['id'], str_amount)
            return RESPONSE_200


        elif command == '/GetCurrentMonthlyForecast':
            client = boto3.client('ce')
            todayDate  = datetime.date.today() 
            last_day_of_month = (todayDate.replace(day=1) + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)

            forecast = client.get_cost_forecast(
                TimePeriod={ 
                    "Start": str(todayDate), 
                    "End": str(last_day_of_month)},
                Metric = 'UNBLENDED_COST',
                #Granularity = 'DAILY'
                Granularity = 'MONTHLY'
            )
            forecast = forecast['Total']['Amount'][:5] + ' usd'
            bot.send_message(chat['id'], forecast)
            return RESPONSE_200


        elif command == '/help':
            bot.send_message(chat['id'], 'You can type this: /ListBuckets, /GetCurrentMonthlyCost, /GetCurrentMonthlyForecast, /help')
            return RESPONSE_200

        else:
            bot.send_message(chat['id'], "Hello. You can type /help to release help docs.")
            return RESPONSE_200

    else: 
        bot.send_message(chat['id'], "You not allowed.")
        return RESPONSE_200

    return RESPONSE_200
