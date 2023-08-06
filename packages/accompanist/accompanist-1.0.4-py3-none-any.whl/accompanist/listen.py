import sys
import time
import json
import csv
import datetime

import click
import boto3


@click.command(name="listen")
@click.option("--days", required=False, type=int)
@click.option("--start_time", required=False, type=int)
@click.option("--end_time", required=False, type=int)
@click.option("--action", required=False, default="BLOCK")
def listen(days, start_time, end_time, action):

    with open("config.json", mode="r") as f:
        config_dict = json.load(f)

    log_group = config_dict["log_group"]
    client = boto3.client("logs")

    if action == "BLOCK":
        query = 'fields @timestamp, @message | filter @message like "BLOCK" | sort @timestamp desc'
    elif action == "COUNT":
        query = 'fields @timestamp, @message | filter @message like /"action":"COUNT"/ | sort @timestamp desc'
    else:
        print("Error: action is empty or invalid")
        sys.exit()

    if days is not None:
        end_time = int(time.time())
        start_time = end_time - days * 24 * 3600

    start_query_response = client.start_query(
        logGroupName=log_group,
        startTime=start_time,
        endTime=end_time,
        queryString=query,
        limit=10000
    )

    response = None
    print("Started...")

    while response is None or response["status"] == "Running":
        time.sleep(3)
        print(" ... ... ... ")
        response = client.get_query_results(queryId=start_query_response["queryId"])
    print("Complete!")

    with open("waf-log-all.json", mode="w", encoding="utf-8") as f:
        json.dump(response, f, indent=4)

    with open("waf-log.csv", mode="w", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONE, lineterminator="\n", delimiter="\t")

        if action == "BLOCK":
            for i in range(len(response["results"])):
                message = json.loads(response["results"][i][1]["value"])
                row = str(message["timestamp"]) + "," + \
                    message["terminatingRuleId"] + "," + \
                    message["httpRequest"]["uri"] + "," + \
                    message["httpRequest"]["clientIp"] + "," + \
                    message["httpRequest"]["country"]
                writer.writerow([row])
        elif action == "COUNT":
            for i in range(len(response["results"])):
                message = json.loads(response["results"][i][1]["value"])
                for j in range(len(message["nonTerminatingMatchingRules"])):
                    row = str(message["timestamp"]) + "," + \
                        message["nonTerminatingMatchingRules"][j]["ruleId"] + "," + \
                        message["httpRequest"]["uri"] + "," + \
                        message["httpRequest"]["clientIp"] + "," + \
                        message["httpRequest"]["country"]
                    writer.writerow([row])
        else:
            print("Error: action is invalid")
            sys.exit()

    # Calc dates
    s_time = datetime.datetime.fromtimestamp(start_time)
    e_time = datetime.datetime.fromtimestamp(end_time)
    days = (e_time - s_time).days

    # Dump data for re-create report command, "again"
    previous = {
        "days": days,
        "web_acl": log_group,
        "mode": action
    }
    with open("previous_music.json", mode="w", encoding="utf-8") as f:
        json.dump(previous, f, indent=4)
