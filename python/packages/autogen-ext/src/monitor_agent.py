import asyncio
import sqlite3
from playwright.async_api import async_playwright

class WhatsAppChatLogger:
    def __init__(self, contact_name: str, db_path: str = "messages.db"):
        self.contact_name = contact_name
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.page = None
        self.context = None

    async def setup_database(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                sender TEXT,
                message TEXT
            )
        ''')
        self.conn.commit()

    async def launch_browser(self):
        self.playwright = await async_playwright().start()
        browser = await self.playwright.chromium.launch(headless=False)
        self.context = await browser.new_context(storage_state="whatsapp_auth.json")  # You can pre-login and save auth
        self.page = await self.context.new_page()
        await self.page.goto("https://web.whatsapp.com")
        print("Please scan QR or wait for session to load...")

        # Wait for WhatsApp Web to load
        await self.page.wait_for_selector("div[role='textbox']", timeout=180000)

    async def open_chat(self):
        # Click the search bar
        search_box_selector = "div[contenteditable='true'][data-tab='3']"  # May vary; inspect element to update
        await self.page.click(search_box_selector)
        await self.page.fill(search_box_selector, self.contact_name)
        await asyncio.sleep(1)

        # Click on the chat from the list
        contact_selector = f"span[title='{self.contact_name}']"
        await self.page.click(contact_selector)
        await asyncio.sleep(1)

    async def extract_messages(self):
        # Placeholder: You must inspect and update these selectors to extract sender, timestamp, and message
        message_selector = "div.selectable-text.copyable-text"  # general message selector
        elements = await self.page.query_selector_all(message_selector)

        messages = []
        for el in elements[-20:]:  # only check the latest 20 messages
            text = await el.inner_text()
            # Placeholder parsing - you must extract sender and timestamp accurately based on WhatsApp DOM
            sender = "UNKNOWN"
            timestamp = "NOW"

            messages.append((timestamp, sender, text))
        return messages

    async def store_new_messages(self, new_messages):
        for timestamp, sender, message in new_messages:
            self.cursor.execute(
                "INSERT INTO messages (timestamp, sender, message) VALUES (?, ?, ?)",
                (timestamp, sender, message)
            )
        self.conn.commit()

    async def monitor_chat(self, interval: float = 5.0):
        seen = set()
        while True:
            messages = await self.extract_messages()
            new = []
            for msg in messages:
                if msg not in seen:
                    new.append(msg)
                    seen.add(msg)
            if new:
                await self.store_new_messages(new)
            await asyncio.sleep(interval)

    async def run(self):
        await self.setup_database()
        await self.launch_browser()
        await self.open_chat()
        await self.monitor_chat()

    async def close(self):
        await self.context.storage_state(path="whatsapp_auth.json")
        await self.playwright.stop()
        self.conn.close()
