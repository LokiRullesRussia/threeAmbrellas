from fastapi import FastAPI
from pydantic import BaseModel
import math
# создание обьекта класса fastapi
app = FastAPI(title="Adaptive Access Control PDP")
# модель валидации данных
class AuthRequest(BaseModel):
    t:int
    d:int
    a:int
    c:int
# модель ответа
class AuthResponse(BaseModel):
    riskScore:float
    phase:str

def normalizeCommands(c: int) -> float:
    return 1 - math.exp(-0.5 * c)


# декоратор для пост запроса @app.post("/")
@app.post("/v1/authz")
def check(request: AuthRequest):
    c_norm = normalizeCommands(request.c)
    R = (0.5 * request.t +
     0.5 * request.d +
     0.8 * request.a +
     0.7 * c_norm +
     0.1 * request.t * request.d +
     0.1 * request.t * request.a +
     0.1 * request.d * request.a +
     0.3 * request.t * c_norm +
     0.3 * request.d * c_norm +
     0.4 * request.a * c_norm)
    if R <= 2:
        phase = "GREEN"
    elif R <= 6:
        phase = "GRAY"
    else:
        phase = "BLAC"

    return AuthResponse(riskScore=round(R, 3), phase=phase)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)