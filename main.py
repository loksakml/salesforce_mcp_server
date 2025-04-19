from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import httpx
import json

load_dotenv()
mcp = FastMCP("salesforce-mcp")

@mcp.tool()
def create_user(lname: str, fname: str, username: str, email: str):
    """
    Create a new user in Salesforce.

    Args:
        lname: Last name of the user
        fname: First name of the user
        email: Email of the user
    """
    url = "https://orgfarm-a7790e458a-dev-ed.develop.my.salesforce.com/services/data/v62.0/sobjects/User"
    headers = {
        "Authorization": f"Bearer {os.getenv('SF_ACCESS_TOKEN')}",
        "Content-Type": "application/json"
    }
    data = {
        "Username": f"{email}.mcppoc",
        "FirstName": fname,
        "LastName": lname,
        "Alias": f"{fname[:3]}{lname[0]}",
        "Email": email,
        "TimeZoneSidKey": "America/Los_Angeles",
        "LocaleSidKey": "en_US",
        "EmailEncodingKey": "UTF-8",
        "LanguageLocaleKey": "en_US",
        "ProfileId": "00egK000001FWf0", 
        "IsActive": True
    }

    response = httpx.post(url, headers=headers, json=data)
    return response.json()

if __name__ == "__main__":
    mcp.run(transport="stdio")
