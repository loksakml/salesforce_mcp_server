from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import httpx
import json

load_dotenv()
mcp = FastMCP("salesforce-mcp")
instance_url = os.getenv('SF_INSTANCE_URL')
sf_access_token = os.getenv('SF_ACCESS_TOKEN')


def get_profile_id(profile_name: str):
    url = f"{instance_url}/services/data/v62.0/query/?q=SELECT+Id+FROM+Profile+WHERE+Name='{profile_name}'"
    headers = {
        "Authorization": f"Bearer {sf_access_token}",
        "Content-Type": "application/json"
    }
    response = httpx.get(url, headers=headers)
    print(response.json()['records'][0]['Id'])
    return response.json()['records'][0]['Id']


@mcp.prompt()
def user_creation_prompt(lname: str, fname: str, email: str, profile_name: str):
    """
    Prompt used to create a new user in Salesforce.
    """
    return f"Create a new user in Salesforce with the following details: \n First Name: {fname} \n Last Name: {lname} \n Email: {email} \n Profile Name: {profile_name}"

@mcp.tool()
def create_user(lname: str, fname: str, email: str, profile_name: str):
    """
    Create a new user in Salesforce. Profile must be a valid Salesforce profile name:
        - Analytics Cloud Integration User
        - Analytics Cloud Security User
        - Anypoint Integration
        - Authenticated Website
        - Authenticated Website
        - B2B Reordering Portal Buyer Profile
        - Chatter External User
        - Chatter Free User
        - Chatter Moderator User
        - Contract Manager
        - Cross Org Data Proxy User
        - Custom: Marketing Profile
        - Custom: Sales Profile
        - Custom: Support Profile
        - Customer Community Login User
        - Customer Community Plus Login User
        - Customer Community Plus User
        - Customer Community User
        - Customer Portal Manager Custom
        - Customer Portal Manager Standard
        - Einstein Agent User
        - External Apps Login User
        - External Identity User
        - Force.com - App Subscription User
        - Force.com - Free User
        - Gold Partner User
        - High Volume Customer Portal
        - High Volume Customer Portal User
        - Identity User
        - Marketing User
        - Minimum Access - API Only Integrations
        - Minimum Access - Salesforce
        - Partner App Subscription User
        - Partner Community Login User
        - Partner Community User
        - Read Only
        - Salesforce API Only System Integrations
        - Silver Partner User
        - Solution Manager
        - Standard Platform User
        - Standard User
        - System Administrator
        - Work.com Only User
    Args:
        lname: Last name of the user
        fname: First name of the user
        email: Email of the user
        profile_name: Profile name of the user
    """

    url = f"{instance_url}/services/data/v62.0/sobjects/User"
    headers = {
        "Authorization": f"Bearer {sf_access_token}",
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
        #"ProfileId": "00egK000001FWf0", 
        "ProfileId": get_profile_id(profile_name), 
        "IsActive": True
    }

    response = httpx.post(url, headers=headers, json=data)
    return response.json()

if __name__ == "__main__":
    mcp.run(transport="stdio")
    #create_user("abi", "test9", "abitest9@example.com", "Chatter Free User")