import asyncio
from main.database_manager.agent import orchestrator
from google.adk.agents import Agent
from main.session_utils import *
from tools import *

bizmate = Agent(
    name="bizmate",
    model="gemini-2.0-flash",
    description=("Agent that manages interact with Small to Medium enterprise(SME) Business Owners"),
    instruction="""
        You are a BizMate. Your job is to help SME owners in managing inventory, suppliers, suppliers inventory, customer order and supply order.

        Your primary functions include:
        1. Acting as a Personal Assistant(PA) for the business owner
        2. Answering questions about a business and its products/services
        3. Delegating tasks to subagent

        # PA services
        ## Instruction
        When acting as a PA for a business owner, you will be provided with the username and name of the person talking to you, if available.
        The price of all the products is in Naira.
        Make sure that any information you report to the business owner are be factual (come from the knowledge base).
        Do not give the owner any information that is not provided in the knowledge base such as details needed to register a business.
        If the owner telegram username is unavailable, be sure to ask for it immediately, and delegate the task to database manager to successfully register the business
        Otherwise use the provided telegram username to search for the owners business in the database.
        
        Once business registration was successful:
            - Proceed to log using log tool

            
        If the time difference exceeds 30mins:
            - Proceed to generate recent orders made since last login using get_recent_orders
            - log it
            
        
        # Management system
        ## Instruction
        When the owner requests for a management service, such as, adding items to inventory, updating supplier information, or fulfilling an order, delegate such tasks to the db_orchestrator providing the business name, id and the summary of the tasks at hand

        # Analytics services
        ## Instruction
        A business owner could ask for how well his business has been doing, delegate the task to analyzer  providing the business name, id and the summary of the tasks at hand

        # Sales Notification
             Extract the following .
            - Order ID
            - Customer ID
            - Customer Username
            - Quantity
            - Product name
            - Product brand
            - Date Ordered
            - Total Amount

            Then use the following information and draft the message:
            `Another sales made, **username** 
                **customer_username** bought the following:
                **order_details**
                Do you want to fulfill the order?`
            
            Then another message of containing the following:
            A user ordered the following:
            **all the order details**
            
            Your output should be in json format, with the following keys
            - message_to_owner: the message to the business owner
            - system_message: the message to the system
            - business_id: the id of the business

            The json output should be your only output, do not include any other text or explanation.
    """,
    tools=[get_business_details,log]
    ,sub_agents=[orchestrator]
)




async def call_agent_async(query: str, runner, user_id, session_id):
    # print(f"\n>>> User Query: {query}")

    content = types.Content(role='user', parts=[types.Part(text=query)])
    final_response_text = "Agent did not produce a final response."

    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        # print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            break

    return final_response_text

async def main():
    APP_NAME = "bizmate_test_app"
    USER_ID = "user_1"
    SESSION_ID = "session_001"

    session = await create_session(APP_NAME, USER_ID, SESSION_ID, session_service)
    runner = create_runner(APP_NAME, session_service)

    async def run_conversation():
        business_id = "1"
        customer_username = "blaze"
        initial_prompt = f"""
            This is a message from the business admin.
            The id of the business in the database is {business_id}. Use your tools to extract basic information about the business and its products.
            Ensure to greet the customer and provide a very brief description of the business, including the name and services offered.
            The telegram username of the customer you're currently serving is {customer_username}. Confirm if the customer already exists in the database before interacting.
            From now on you will be engaging with the customer.
        """
        initial_response = await call_agent_async(initial_prompt, runner, USER_ID, SESSION_ID)
        print(f">>> Agent: {initial_response}")

        running = True
        while running:
            user_query = input(">>> User: ")
            if user_query == "q":
                running = False
            else:
                response = await call_agent_async(user_query, runner, USER_ID, SESSION_ID)
                print(f">>> Agent: {response}")
    
    await run_conversation()

if __name__ == "__main__":
    asyncio.run(main())