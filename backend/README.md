# Energy Advisor Backend

## Setup

```bash
cd backend
pip install -r requirements.txt
export OPENAI_API_KEY=sk-your-key
uvicorn main:app --reload
```

## API

- `POST /api/auth/register` - Register
- `POST /api/auth/login` - Login
- `GET /api/devices` - List devices
- `POST /api/devices` - Create device
- `GET /api/readings` - Get readings
- `POST /api/simulate/start` - Start simulation
- `GET /api/recommendations` - AI recommendations
- `POST /api/chat` - AI chat
