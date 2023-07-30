# library rewritten by amorescam.t.me for claude.ai

import aiohttp
import requests
import json
import os
import uuid


class AIOclient:
    def __init__(self, cookie):
        self.cookie = cookie
        self.organization_id = self.get_organization_id()

    def get_organization_id(self):
        url = "https://claude.ai/api/organizations"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://claude.ai/chats",
            "Content-Type": "application/json",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Connection": "keep-alive",
            "Cookie": f"{self.cookie}",
        }

        response = requests.request("GET", url, headers=headers)
        res = json.loads(response.text)
        return res[0]["uuid"]

    def get_content_type(self, file_path):
        extension = os.path.splitext(file_path)[-1].lower()
        if extension == ".pdf":
            return "application/pdf"
        elif extension == ".txt":
            return "text/plain"
        elif extension == ".csv":
            return "text/csv"
        else:
            return "application/octet-stream"

    async def list_all_conversations(self):
        url = (
            f"https://claude.ai/api/organizations/{self.organization_id}/conversations"
        )

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://claude.ai/chats",
            "Content-Type": "application/json",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Connection": "keep-alive",
            "Cookie": f"{self.cookie}",
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, headers=headers) as response:
                return await response.json(content_type="text/html")

    async def send_message(self, prompt, conversation_id, attachment=None):
        url = "https://claude.ai/api/append_message"

        attachments = []
        if attachment:
            attachment_response = await self.upload_attachment(attachment)
            if attachment_response:
                attachments = [attachment_response]
            else:
                return {"Error: Invalid file format. Please try again."}

        # Ensure attachments is an empty list when no attachment is provided
        if not attachment:
            attachments = []

        payload = json.dumps(
            {
                "completion": {
                    "prompt": f"{prompt}",
                    "timezone": "Asia/Kolkata",
                    "model": "claude-2",
                },
                "organization_uuid": f"{self.organization_id}",
                "conversation_uuid": f"{conversation_id}",
                "text": f"{prompt}",
                "attachments": attachments,
            }
        )

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Accept": "text/event-stream, text/event-stream",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://claude.ai/chats",
            "Content-Type": "application/json",
            "Origin": "https://claude.ai",
            "DNT": "1",
            "Connection": "keep-alive",
            "Cookie": f"{self.cookie}",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers",
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(
                url, data=payload, raise_for_status=True
            ) as response:
                decoded_data = await response.text()
                data = decoded_data.strip().split("\n")[-1]
                answer = {"answer": json.loads(data[6:])["completion"]}["answer"]

        return answer

    async def delete_conversation(self, conversation_id):
        url = f"https://claude.ai/api/organizations/{self.organization_id}/chat_conversations/{conversation_id}"

        payload = json.dumps(f"{conversation_id}")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json",
            "Content-Length": "38",
            "Referer": "https://claude.ai/chats",
            "Origin": "https://claude.ai",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Connection": "keep-alive",
            "Cookie": f"{self.cookie}",
            "TE": "trailers",
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.delete(
                url, data=payload, raise_for_status=True
            ) as response:
                return response.status == 204

    async def chat_conversation_history(self, conversation_id):
        url = f"https://claude.ai/api/organizations/{self.organization_id}/chat_conversations/{conversation_id}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://claude.ai/chats",
            "Content-Type": "application/json",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Connection": "keep-alive",
            "Cookie": f"{self.cookie}",
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Error: {response.status} - {await response.text()}")

    async def generate_uuid(self):
        random_uuid = uuid.uuid4()
        random_uuid_str = str(random_uuid)
        return f"{random_uuid_str[:8]}-{random_uuid_str[8:12]}-{random_uuid_str[12:16]}-{random_uuid_str[16:20]}-{random_uuid_str[20:]}"

    async def create_new_chat(self):
        url = f"https://claude.ai/api/organizations/{self.organization_id}/chat_conversations"
        uuid = await self.generate_uuid()

        payload = json.dumps({"uuid": uuid, "name": ""})
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://claude.ai/chats",
            "Content-Type": "application/json",
            "Origin": "https://claude.ai",
            "DNT": "1",
            "Connection": "keep-alive",
            "Cookie": self.cookie,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload, headers=headers) as response:
                    return await response.json(content_type='text/html')
                

    async def reset_all(self):
        conversations = await self.list_all_conversations()

        for conversation in conversations:
            conversation_id = conversation["uuid"]
            await self.delete_conversation(conversation_id)
        return True

    async def upload_attachment(self, file_path):
        url = "https://claude.ai/api/convert_document"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://claude.ai/chats",
            "Origin": "https://claude.ai",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Connection": "keep-alive",
            "Cookie": f"{self.cookie}",
            "TE": "trailers",
        }

        file_name = os.path.basename(file_path)
        content_type = self.get_content_type(file_path)

        files = {
            "file": (file_name, open(file_path, "rb"), content_type),
            "orgUuid": (None, self.organization_id),
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=files, headers=headers) as response:
                return await response.json(content_type='text/html')

    async def rename_chat(self, title, conversation_id):
        url = "https://claude.ai/api/rename_chat"

        payload = json.dumps(
            {
                "organization_uuid": f"{self.organization_id}",
                "conversation_uuid": f"{conversation_id}",
                "title": f"{title}",
            }
        )
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json",
            "Referer": "https://claude.ai/chats",
            "Origin": "https://claude.ai",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Connection": "keep-alive",
            "Cookie": f"{self.cookie}",
            "TE": "trailers",
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(url, data=payload) as response:
                return response.status == 200
