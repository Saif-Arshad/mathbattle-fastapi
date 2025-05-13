from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
import random
import time
from typing import Dict, List, Optional

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],  # Allow Live Server origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Setup for socketio

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=["http://127.0.0.1:5500", "http://localhost:5500"],  # Allow Live Server origins
    ping_timeout=60,
    ping_interval=25,
    logger=True,
    engineio_logger=True
)
socket_app = socketio.ASGIApp(sio, app)

waiting_players: List[str] = []
active_games: Dict[str, Dict] = {}
player_rooms: Dict[str, str] = {}
#  Function for generating math question
def generate_math_question():
    """Generate a random math question."""
    operations = ['+', '-', '*']
    operation = random.choice(operations)
    if operation == '+':
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        answer = a + b
    elif operation == '-':
        a = random.randint(1, 100)
        b = random.randint(1, a)  #
        answer = a - b
    else:  # multiplication
        a = random.randint(1, 12)
        b = random.randint(1, 12)
        answer = a * b
    
    return {
        'question': f"{a} {operation} {b}",
        'answer': answer
    }

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")
    if sid in waiting_players:
        waiting_players.remove(sid)
    
    # Handle disconnection during game
    room = player_rooms.get(sid)
    if room and room in active_games:
        other_player = next((p for p in active_games[room]['players'] if p != sid), None)
        if other_player:
            await sio.emit('opponent_disconnected', room=other_player)
        del active_games[room]
    
    if sid in player_rooms:
        del player_rooms[sid]

@sio.event
async def join_queue(sid, data):
    player_name = data.get('name', 'Anonymous')
    waiting_players.append(sid)
    
    if len(waiting_players) >= 2:
        player1_sid = waiting_players.pop(0)
        player2_sid = waiting_players.pop(0)
        room = f"game_{int(time.time())}"
        
        active_games[room] = {
            'players': [player1_sid, player2_sid],
            'scores': {player1_sid: 0, player2_sid: 0},
            'start_time': time.time(),
            'current_question': generate_math_question()
        }
        
        player_rooms[player1_sid] = room
        player_rooms[player2_sid] = room
        
        await sio.enter_room(player1_sid, room)
        await sio.enter_room(player2_sid, room)
        
        await sio.emit('game_start', {
            'room': room,
            'question': active_games[room]['current_question']['question']
        }, room=room)

@sio.event
async def submit_answer(sid, data):
    room = player_rooms.get(sid)
    if not room or room not in active_games:
        return
    
    game = active_games[room]
    current_question = game['current_question']
    
    if int(data['answer']) == current_question['answer']:
        game['scores'][sid] += 1
        
        game['current_question'] = generate_math_question()
        
        await sio.emit('score_update', {
            'scores': game['scores'],
            'question': game['current_question']['question']
        }, room=room)
    else:
        await sio.emit('wrong_answer', room=sid)

@sio.event
async def game_over(sid):
    room = player_rooms.get(sid)
    if not room or room not in active_games:
        return
    
    game = active_games[room]
    scores = game['scores']
    
    max_score = max(scores.values())
    winners = [p for p, s in scores.items() if s == max_score]
    
    result = {
        'scores': scores,
        'winner': winners[0] if len(winners) == 1 else 'draw'
    }
    
    await sio.emit('game_results', result, room=room)
    
    for player_sid in game['players']:
        if player_sid in player_rooms:
            del player_rooms[player_sid]
    del active_games[room]

app.mount("/", socket_app) 