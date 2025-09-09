from imports import *

# Initialize FastAPI app
app = FastAPI(
    title= SentiVox.Config.APP_NAME,
    description= SentiVox.Config.APP_DESC,
    version= SentiVox.Config.APP_VERSION
)

# Dummy function to simulate sentiment analysis - replace with your actual analysis module
def analyze_sentiment(comment: str, lang: str) -> Dict:
    """
    This is a placeholder function for sentiment analysis.
    Replace this with your actual sentiment analysis module.
    """
    # Placeholder logic - replace with actual sentiment analysis
    return {
        "comment": comment,
        "language": lang,
        "sentiment": "positive",  # This should come from your analysis module
        "confidence": 0.85,       # This should come from your analysis module
        "processed": True
    }

def validate_api_key(api_key: str) -> bool:
    """
    Validate the API key. Replace this with your actual API key validation logic.
    """
    # Placeholder validation - replace with actual API key validation
    valid_keys = ["demo-key", "test-key", "your-api-key-here"]
    return api_key in valid_keys

@app.post("/analyze/single")
async def analyze_single_comment(data: SentiVox.Models.CommentAndLang):
    """
    Analyze sentiment for a single comment.
    
    Expected JSON format:
    {
        "api_key": "your-api-key",
        "comment": "Your comment text here",
        "lang": "en"
    }
    """
    try:
        # Validate API key
        if not validate_api_key(data.api_key):
            raise HTTPException(status_code=401, detail="Invalid API key")
        
        # Validate language
        supported_languages = [SentiVox.Lang.ENGLISH, SentiVox.Lang.HINDI]
        if data.lang not in supported_languages:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported language. Supported languages: {supported_languages}"
            )
        
        # Perform sentiment analysis
        result = analyze_sentiment(data.comment, data.lang)
        
        return {
            "status": "success",
            "message": "Sentiment analysis completed successfully",
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/analyze/batch")
async def analyze_comment_list(data: SentiVox.Models.CommentList):
    """
    Analyze sentiment for multiple comments in different languages.
    
    Expected JSON format:
    {
        "api_key": "your-api-key",
        "comment_list": {
            "en": ["comment1", "comment2"],
            "hi": ["comment3", "comment4"]
        }
    }
    """
    try:
        # Validate API key
        if not validate_api_key(data.api_key):
            raise HTTPException(status_code=401, detail="Invalid API key")
        
        # Process comments by language
        results = {}
        supported_languages = [SentiVox.Lang.ENGLISH, SentiVox.Lang.HINDI]
        
        for lang, comments in data.comment_list.items():
            if lang not in supported_languages:
                results[lang] = {
                    "error": f"Unsupported language: {lang}. Supported: {supported_languages}"
                }
                continue
                
            results[lang] = []
            for comment in comments:
                analysis_result = analyze_sentiment(comment, lang)
                results[lang].append(analysis_result)
        
        return {
            "status": "success",
            "message": "Batch sentiment analysis completed",
            "data": results,
            "total_processed": sum(len(comments) for comments in data.comment_list.values())
        }
    except Exception as excep:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(excep)}")

@app.get("/")
async def root():
    """
    Root endpoint with API information.
    """
    return SentiVox.Config.WELCOME_MESSAGE

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return SentiVox.Config.HEALTH_MESSAGE

# Handle 404 errors
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """
    Handle 404 Not Found errors.
    """
    return JSONResponse(
        status_code=404,
        content={
            "status": "error",
            "message": "Endpoint not found",
            "detail": f"The requested endpoint '{request.url.path}' does not exist",
            "available_endpoints": {
                "/": "GET - Root endpoint",
                "/analyze/single": "POST - Analyze single comment",
                "/analyze/batch": "POST - Analyze multiple comments",
                "/health": "GET - Health check",
                "/docs": "GET - API documentation"
            }
        }
    )

# Handle validation errors (when JSON data doesn't match models)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors when JSON data doesn't match the expected models.
    """
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Data format is incorrect",
            "detail": "The provided JSON data doesn't match the expected format",
            "errors": exc.errors(),
            "expected_formats": {
                "single_comment_analysis": {
                    "endpoint": "/analyze/single",
                    "method": "POST",
                    "format": {
                        "api_key": "string - Your API key",
                        "comment": "string - Comment text to analyze",
                        "lang": "string - Language code (en/hi)"
                    },
                    "example": {
                        "api_key": "your-api-key-here",
                        "comment": "This is a sample comment",
                        "lang": "en"
                    }
                },
                "batch_comment_analysis": {
                    "endpoint": "/analyze/batch",
                    "method": "POST",
                    "format": {
                        "api_key": "string - Your API key",
                        "comment_list": "object - Dictionary with language codes as keys and arrays of comments as values"
                    },
                    "example": {
                        "api_key": "your-api-key-here",
                        "comment_list": {
                            "en": ["comment1", "comment2"],
                            "hi": ["comment3", "comment4"]
                        }
                    }
                }
            }
        }
    )

# Handle general HTTP exceptions
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handle general HTTP exceptions.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)