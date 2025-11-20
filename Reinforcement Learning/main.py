from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import save_log, reset_all_seats
from ai_rl_simple_recommender import SimpleRLSeatRecommender

app = FastAPI()

# Solve cross-origin issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the reinforcement learning recommender
rl_recommender = SimpleRLSeatRecommender()

# Seat recommendation interface (changed to GET)
@app.get("/api/recommend-seat-rl")
async def recommend_seat_rl(user_id: str):
    recommended_seat = rl_recommender.recommend()
    if recommended_seat == "No vacant seats":
        return {"code": 400, "msg": "No vacant seats"}
    # Storage Recommendation Log
    save_log({
        "user_id": user_id,
        "seat_id": recommended_seat,
        "operation_type": "recommend_rl",
        "user_preference": None
    })
    return {
        "code": 200,
        "msg": "Recommendation succeeded",
        "data": {"recommended_seat": recommended_seat}
    }

# Added: Reset all seats to available (for testing)
@app.post("/api/reset-seats")
async def reset_seats():
    reset_all_seats()
    return {"code": 200, "msg": "All seats reset to free"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)