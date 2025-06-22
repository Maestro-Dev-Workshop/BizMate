from google.adk.runners import Runner
from google.genai import types
from google.adk.sessions import InMemorySessionService, DatabaseSessionService
from main.utils.db_conn import DB_URL
async def create_session(app_name, user_id, session_id, session_service,**kwargs):
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
        **kwargs
    )
    print(f"Session created: APP_NAME={app_name}, USER_ID={user_id}, SESSION_ID={session_id}")

    return session

async def get_session(app_name, user_id, session_id, session_service):
    session = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )

    return session

async def delete_session(app_name, user_id, session_id, session_service):
    session = await session_service.delete_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )

    return session


def create_runner(app_name, session_service, agent):
    runner = Runner(
        agent=agent,
        app_name=app_name,
        session_service=session_service,
    )

    return runner


async def reset_session(app_name, user_id, session_id, session_service, **kwargs):
    await get_session(app_name, user_id, session_id, session_service)
    await delete_session(app_name, user_id, session_id, session_service)
    return await create_session(app_name, user_id, session_id, session_service, **kwargs)


async def call_agent_async(query: str, runner, user_id, session_id):
    # print(f"\n>>> User Query: {query}")

    content = types.Content(role='user', parts=[types.Part(text=query)])
    final_response_text = "Agent did not produce a final response."

    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")
        print("\n\n")

        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            break

    return event.author,final_response_text


async def call_agent_async_system(query: str, runner, user_id, session_id):
    # print(f"\n>>> User Query: {query}")

    content = types.Content(role='model', parts=[types.Part(text=query)])
    final_response_text = ""

    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        print("System")
        print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")
        print("\n\n")
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            break

    return final_response_text

async def create_or_get_session(app_name, user_id, session_id, session_service, **kwargs):
    try:
        return await get_session(app_name, user_id, session_id, session_service)
    except Exception as e:
        return await create_session(app_name, user_id, session_id, session_service, **kwargs)



session_service = DatabaseSessionService(db_url=DB_URL)
# session_service = InMemorySessionService()