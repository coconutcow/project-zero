from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import csv

app = FastAPI()
templates = Jinja2Templates(directory="templates")

languages = {
    "en": {
        "name": "Name",
        "age": "Age",
        "gender": "Gender",
        "male": "Male",
        "female": "Female",
        "other": "Other",
        "smoker": "Smoker",
        "submit": "Submit",
        "thankyou": "Thank you for submitting the form. Your information has been recorded."
    },
    "it": {
        "name": "Nome",
        "age": "Età",
        "gender": "Genere",
        "male": "Maschio",
        "female": "Femmina",
        "other": "Altro",
        "smoker": "Fumatore",
        "submit": "Invia",
        "thankyou": "Grazie per aver inviato il modulo. Le tue informazioni sono state registrate."
    }
}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/form", response_class=HTMLResponse)
async def form(request: Request, lang: str):
    form_text = languages.get(lang, languages["en"])
    return templates.TemplateResponse("form.html", {"request": request, "form_text": form_text})


@app.post("/submit")
async def submit(
    request: Request,
    lang: str,
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    smoker: bool = Form(False)
):
    data = [name, str(age), gender, str(smoker)]

    with open("patient_data.csv", mode="a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

    form_text = languages.get(lang, languages["en"])
    return templates.TemplateResponse("thankyou.html", {"request": request, "form_text": form_text, "lang": lang})
