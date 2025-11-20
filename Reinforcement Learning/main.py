from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import save_log, reset_all_seats
from ai_rl_simple_recommender import SimpleRLSeatRecommender

app = FastAPI()

# 解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化强化学习推荐器
rl_recommender = SimpleRLSeatRecommender()

# 座位推荐接口（已改为GET）
@app.get("/api/recommend-seat-rl")
async def recommend_seat_rl(user_id: str):
    recommended_seat = rl_recommender.recommend()
    if recommended_seat == "No vacant seats":
        return {"code": 400, "msg": "No vacant seats"}
    # 存储推荐日志
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

# 新增：重置所有座位为空闲（用于测试）
@app.post("/api/reset-seats")
async def reset_seats():
    reset_all_seats()
    return {"code": 200, "msg": "All seats reset to free"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)