import uvicorn
from pathlib import Path
import sys

if __name__ == "__main__":
    # Добавляем src в PYTHONPATH
    sys.path.insert(0, str(Path(__file__).parent))

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(Path(__file__).parent)]  # Для отслеживания изменений
    )
