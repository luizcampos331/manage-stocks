from dotenv import load_dotenv

load_dotenv()

from app.presentation.http.app import create_app  # noqa: E402

app = create_app()
