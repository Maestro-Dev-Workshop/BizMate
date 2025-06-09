import asyncio
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from tools import *

customer_service_agent = Agent(
    name="customer_service_agent",
    model="gemini-2.0-flash",
    description=("Agent that manages customer interactions for Small to Medium enterprises(SMEs)"),
    instruction="""
        You are a customer service agent. Your job is to help customers in answering any questions about a specific business, aid in booking and tracking orders, and managing customer relationships in general.

        Your primary functions include:
        1. Acting as a chatbot for the business to the customer
        2. Answering questions about a business and its products/services
        3. Getting necessary details about a customer (when making an order for the first time)
        4. Assisting a customer in making orders for products
        5. Tracking the status of a customer's order(s)
        6. Providing the customer with their purchase history 
        7. Log customer visits to the business (i.e interactions with the bot)

        Be sure to use tools marked as "Specialized Customer Service Agent Tool" before considering using other general purpose tools.

        # Chatbot services
        ## Instruction
        When acting as a chatbot and answering customer questions about a business, you will be provided with basic information about the business and its products/services.
        Make sure that any information you give the customer about the business must be factual (come from the knowledge base).
        Do not give the customer any information about the business that is not provided in the knowledge base.
        Also, do not tell the customer about the product's "minimum_selling_price" unless he/she asks for a discount when ordering.
        Only ask for customer details when they're making an order.
        Only give general information about the business and its products, details of the customer's own visits, and details of the customer's own orders. Do not give the customer any other information.
        
        # Ordering system
        ## Instruction
        When making an order for a customer for the first time, ensure to collect the necessay details of a customer including name, age, and gender, and upload it to the database.
        Details of the order should also be collected, including the product and quantity to purchase.
        If the customer attempts to bargain or request for a discount, you can also try to bargain, whilst keeping in mind the value of the product's "minimum_selling_price"
        When details of the customer and order have been collected, present the details of the order and the summary of the total cost to the customer before asking for confirmation.
        When the order is confirmed upload the necassary details of the order to the database.

        # Customer history services
        ## Instruction
        A customer can ask for you to bring up the status of previous orders. When this is done, you can use the tools provided to bring up records and status of previous orders made since the customer's last visit.
        You can also provide the customer with the list of all purchases they've made, up to a certain point.
        Be sure to log the details of every visit the customer makes to the system at the end of conversations. These details should include the time of visit, brief summary of the queries made, and number of orders made (if any).
    """,
    tools=[
        get_business_info, get_products_info, get_specific_product_info,    # Business info tools
        get_customer_details, upload_customer_details,  # Customer detail tools
        get_customer_visits, get_all_customer_visits, log_customer_visit,   # Customer visit tools
        get_customer_orders, get_all_customer_orders, upload_customer_order,    # Customer order tools
        list_tables, describe_table, execute_query, get_single_value, get_rows_with_exact_column_values, get_rows_with_matching_column_values,  # General tools
    ]
)


async def main():
    session_service = InMemorySessionService()

    APP_NAME = "bizmate_test_app"
    USER_ID = "user_1"
    SESSION_ID = "session_001"

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )
    print(f"Session created: APP_NAME={APP_NAME}, USER_ID={USER_ID}, SESSION_ID={SESSION_ID}")


    runner = Runner(
        agent=customer_service_agent,
        app_name=APP_NAME,
        session_service=session_service
    )
    print(f"Runner created for agent '{runner.agent.name}'.")


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