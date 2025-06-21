from pathlib import Path
import os
from utils.db_utils import cursor
from dotenv import load_dotenv


from customer_service.telegram_bot import CustomerServiceBot
from bizmate.bizmate_tg import BizMateBot
import asyncio
from main.utils.session_utils import session_service
load_dotenv()




BZ_LOGS_FOLDER_PATH = Path(r"C:\Users\VICTUS\Documents\Python\Everything Data\Deep Learning\llm_projects\Bizmate\bizlogs")
CS_LOGS_FOLDER_PATH = Path(r"C:\Users\VICTUS\Documents\Python\Everything Data\Deep Learning\llm_projects\Bizmate\cslogs")

class BotManager:
    def __init__(self, session_service):
        self.bot_tokens = os.environ["BIZ_TOK"]
        self.session_service = session_service
        self.cs_tokens = self.get_cs_bot_token()
        self.bizmate_bot = BizMateBot(session_service,BZ_LOGS_FOLDER_PATH)
        self.customer_service_bots = [
            CustomerServiceBot(session_service=session_service, token=token, logs_folder_path=CS_LOGS_FOLDER_PATH, business_id=id)
            for id, token in self.cs_tokens
        ]
        self.all_bot = [self.bizmate_bot] + self.customer_service_bots
    
    async def start_bot(self, bot):
        await bot.run()

    async def add_bot(self):
        while True:
            cursor.execute("SELECT id,tg_bot_token FROM business")
            new_bots = cursor.fetchall()
            if len(self.cs_tokens) < len(new_bots):
                N_BOTS = len(self.cs_tokens) - 1
                for id, token in new_bots[N_BOTS:]:
                    new_bot = CustomerServiceBot(session_service=self.session_service, token=token, logs_folder_path=CS_LOGS_FOLDER_PATH, business_id=id)
                    self.customer_service_bots.append(new_bot)
                    self.all_bot.append(new_bot)
                    self.cs_tokens.append((id, token))
                    asyncio.create_task(self.start_bot(new_bot))
            await asyncio.sleep(5)

    async def start_all(self):
        tasks = [self.start_bot(bot) for bot in self.all_bot] + [self.add_bot()]
        await asyncio.gather(*tasks)

    def get_cs_bot_token(self):
        cursor.execute("SELECT id,tg_bot_token FROM business")
        return cursor.fetchall()
    

if __name__ == "__main__":
    bot_manager = BotManager(session_service)
    asyncio.run(bot_manager.start_all())