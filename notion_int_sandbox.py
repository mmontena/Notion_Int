import os
from pprint import pprint
from datetime import datetime, timezone
import json
from notion_client import Client

# Set the Notion API token
os.environ["NOTION_TOKEN"] = "secret_key" # Enter your own API token for use
os.environ["DATABASE_ID"] = "database_id" # Enter the database id you plan to edit

def getData(query_response):
    results = query_response["results"]
    return results

def makeUpdate(results, entry):

    print("""\n1. URL
             \n2. Title
             \n3. Date Test""")
    
    ans = str(input("\nSelect the options youd like to update (EX: 1,3 or 2 or 0 to quit): "))
    data = results[entry]["properties"]
    while True:
        if '1' in ans or '2' in ans or '3' in ans or '0' in ans:
            if '1' in ans:
                url = input("Please enter the URL youd like to add: ")
                data["URL"]["title"][0]["text"]["content"] = url
            if '2' in ans:
                title = input("Please enter the Title youd like to add: ")
                data["Title"]["rich_text"][0]["text"]["content"] = title
            if '3' in ans:
                date = input("Please enter the Date Test youd like to add: ")
                data["Date Test"]["date"]["start"] = date
            break
        else:
            ans = input("\nThe option you selected is invalid, please enter a different value or '0' to quit: ")
    
    return data

def addPage(results):
    data = requestData(results)
    parentInfo = {"database_id": os.environ["DATABASE_ID"]}
    notion.pages.create(parent=parentInfo, properties=data)

def requestData(results): #FIX
    try:
        data = results[0]["properties"]
    except:
        data = {"Title": {"rich_text": [{"text": {"content": "Test Title"}}]},"Date Test": {"date": {"start": "2023-10-18","end": None,"time_zone": None}},"URL": {"title": [{"text": {"content": "Test URL"}}]}}
                                         
    data["URL"]["title"][0]["text"]["content"] = input("Please provide a URL: ")
    data["Title"]["rich_text"][0]["text"]["content"] = input("Please provide a Title: ")
    data["Date Test"]["date"]["start"] = datetime.now().astimezone(timezone.utc).isoformat()

    return data

def sendUpdate(results, entry):
    pageID = results[entry]["id"]
    data = makeUpdate(results, entry)
    notion.pages.update(page_id=pageID, properties=data)

def removePage(results, entry):
    notion.blocks.delete(block_id=results[entry]['id'])

def readPage(results, entry):
    props = results[entry]["properties"]
    url = props["URL"]["title"][0]["text"]["content"]
    title = props["Title"]["rich_text"][0]["text"]["content"]
    date = props["Date Test"]["date"]["start"]
    date = datetime.fromisoformat(date)
    print("\nHere is the data requested:")
    print("\n  URL: " + str(url))
    print("\n  Title: " + str(title))
    print("\n  Date: " + str(date))

def doStuff():
    query_response = notion.databases.query(database_id=os.environ["DATABASE_ID"])
    numEntries = len(query_response["results"])

    print("""\n1. Adding Data to Database
             \n2. Updating a Database Entry
             \n3. Removing a Database Entry
             \n4. Read a Database Entry\n""")

    ans = input("What you doing here?: ")
    results = getData(query_response)
    acceptableAns = '0 1 2 3 4'

    if '0' in ans and len(ans) == 1:
        return ans
    
    elif (ans in acceptableAns) and len(ans) == 1:
        if '1' in ans:
            addPage(results)
        elif numEntries > 0:
            entry = int(input("Please enter the entry index youd like to update (Entries are 1-"+ str(numEntries)+"): ")) - 1
            if '2' in ans:
                sendUpdate(results, entry)
            elif '3' in ans:
                removePage(results, entry)
            elif '4' in ans:
                readPage(results, entry)
        else:
            print("Sorry, cannot update or remove entries since there are none")
    else:
        print("Please provide a valid answer")

    return ans

def main():
    # Create a Notion client
    global notion
    notion = Client(auth=os.environ["NOTION_TOKEN"])
    while True:
        ans = doStuff()
        if ans == '0':
            break

main()


