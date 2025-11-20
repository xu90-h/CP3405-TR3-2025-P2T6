from fastapi import FastAPI
from db import save_log
from ai_rl_simple_recommender import SimpleRLSeatRecommender

app = FastAPI()
# Initialize simplified RL recommender
rl_recommender = SimpleRLSeatRecommender()

@app.post("/api/recommend-seat-rl")
async def recommend_seat_rl(user_id: str):
    recommended_seat = rl_recommender.recommend()
    if recommended_seat == "No vacant seats":
        return {"code": 400, "msg": "No vacant seats"}
    # Store log
    save_log({
        "user_id": user_id,
        "seat_id": recommended_seat,
        "operation_type": "recommend_rl",
        "user_preference": None
    })
    return {
        "code": 200,
        "msg": "Reinforcement learning recommendation succeeded",
        "data": {"recommended_seat": recommended_seat}
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)