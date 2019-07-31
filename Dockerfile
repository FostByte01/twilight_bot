FROM python:3.7

RUN pip install discord.py aiohttp 

COPY . .

CMD ["python", "main.py"]
