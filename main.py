import uvicorn

if __name__ == "__main__":

    uvicorn.run(
        'config:app',
        host="0.0.0.0",
        port=443,
        ssl_keyfile="/etc/letsencrypt/live/parsllm.ir/privkey.pem",
        ssl_certfile="/etc/letsencrypt/live/parsllm.ir/fullchain.pem"
    )