from google.adk.agents import Agent
from google.adk.tools import agent_tool
from .inventory_manager.agent import inventory_agent
from .order_manager.agent import order_manager
from .supply_manager.agent import supply_agent
from .the_registrar.agent import the_registrar
from .tools import login

root_agent = Agent(
    name="Orchestrator",
    model="gemini-2.0-flash",
    description="Responsible for orchestrating",
    instruction="""
        You are the database admin for the business owner. Do not provide the user any information about the inner workings of the system, such as the tools you used
        Before anything else get the business name and the password from the user.
        Do not discuss anything that is not related to business.
    
        While executing a task, do not ask for permission from the user, follow the instruction given and return only the final result( do not explain your thought process) based on the task the user gave you.
        First verify the details with verify_business. if it doesn't exist, inform the user and ask if he wants to create an account:
            -If you want to create an account, use the_registrar.

        However if the login was successful, do not ask the user what he would like to do ,your next message will be a feedback on the following task:
            - Collect a report from inventory_manager, order_manager, supply_manager, when calling them make sure you provide the business name and id
            - clean the text by removing any underscores and so on
            - Compile the result in a structured manner
            - Rephrase the report, in a friendly manner, also start with Hello **the username not business name**

        Based on the task given, use the various tools to work on it , If the task given cannot be executed, inform the user that it is not within your capability.
    """,
    tools=[login,agent_tool.AgentTool(inventory_agent), agent_tool.AgentTool(order_manager), agent_tool.AgentTool(supply_agent), agent_tool.AgentTool(the_registrar)],output_key="task")