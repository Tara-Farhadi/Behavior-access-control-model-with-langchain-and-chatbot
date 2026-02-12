# Import FastAPI
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from chain import get_qa_chain

# Create FastAPI app
app = FastAPI(
    title="PDF QA API",
    description="Ask questions about your PDFs",
    version="1.0"
)

# Mount the frontend folder to serve static files (CSS, JS)
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Create the chain once at startup
print("Initializing QA chain...")
chain = get_qa_chain()
print("QA chain ready!")

# Define request/response models
class Question(BaseModel):
    input: str

class Answer(BaseModel):
    output: str

# Create a simple endpoint
@app.post("/qa/invoke", response_model=Answer)
async def ask_question(question: Question):
    """Ask a question about your PDFs"""
    answer = chain.invoke({"input": question.input})
# Extract string from AIMessage if needed
    if hasattr(answer, 'content'):
        return Answer(output=answer.content)
    return Answer(output=str(answer))

# Root endpoint
@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)