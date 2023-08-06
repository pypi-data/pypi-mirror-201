import asyncio
import socketio

async def enviar_mensagem(message, server_address, port, event_name):
    sio = socketio.AsyncClient()

    @sio.event
    async def connect():
        print('Conexão estabelecida')

    @sio.event
    async def my_message():
        print('Mensagem recebida')
        await sio.emit(event_name, message)

    @sio.event
    async def disconnect():
        print('Desconectado do servidor')

    await sio.connect(f'http://{server_address}:{port}')
    await my_message()
    await sio.wait()

def notify(message, server_address, port, event_name):
    asyncio.run(enviar_mensagem(message, server_address, port, event_name))