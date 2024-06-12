import uvicorn

if __name__ == "__main__":

    uvicorn.run(
        'config:app',
        host="0.0.0.0",
        # host='localhost',
        port=800,  
        # reload=True
        # ssl_keyfile="/etc/letsencrypt/live/yourdomain.com/privkey.pem",
        # ssl_certfile="/etc/letsencrypt/live/yourdomain.com/fullchain.pem"
    )