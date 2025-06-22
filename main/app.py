from pathlib import Path
import os
from main.utils.db_utils import cursor,db
from dotenv import load_dotenv
from main.customer_service.telegram_bot import CustomerServiceBot
from main.bizmate.bizmate_tg import BizMateBot
import asyncio
from main.utils.session_utils import session_service,reset_session


class BotManager:
    def __init__(self, session_service):
        self.bot_tokens = os.environ["BIZ_TOK"]
        self.session_service = session_service
        self.cs_tokens = self.get_cs_bot_token()
        self.bizmate_bot = BizMateBot(session_service)
        self.customer_service_bots = [
            CustomerServiceBot(session_service=session_service, token=token, business_id=id)
            for id, token in self.cs_tokens if token != ""
        ]
        self.all_bot = [self.bizmate_bot] + self.customer_service_bots
    
    async def start_bot(self, bot):
        await bot.run()

    async def add_bot(self):
        while True:
            db.commit()
            print("Checking for new customer service bots...")
            cursor.execute("SELECT id,tg_bot_token FROM business")
            new_bots = cursor.fetchall()
            print("New bots found:", new_bots)
            N_BOTS = len(self.cs_tokens) - 1
            for id, token in new_bots[N_BOTS:]:
                if token == "":
                    continue
                if (id, token) in self.cs_tokens:
                    continue
                print("Adding new bot with ID:", id, "and token:", token)
                new_bot = CustomerServiceBot(session_service=self.session_service, token=token, business_id=id)
                self.cs_tokens.append((id, token))
                asyncio.create_task(self.start_bot(new_bot))
            await asyncio.sleep(5)

    async def start_all(self):
        # tasks = [self.start_bot(bot) for bot in self.all_bot if bot != ""] + [self.add_bot()]
        for bot in self.all_bot:
            asyncio.create_task(self.start_bot(bot))
        await self.add_bot()

    def get_cs_bot_token(self):
        cursor.execute("SELECT id,tg_bot_token FROM business")
        return cursor.fetchall()
    

if __name__ == "__main__":
    bot_manager = BotManager(session_service)
    asyncio.run(bot_manager.start_all())

