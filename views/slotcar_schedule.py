import uvicorn
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import HTMLResponse

router = APIRouter()     #change to router next step


def generate_html_response():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return html_content


@router.get("/items/", response_class=HTMLResponse)
async def read_items():
    html_stuff = generate_html_response()
    return HTMLResponse(content=html_stuff, status_code=200)

