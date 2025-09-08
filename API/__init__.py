from pydantic import BaseModel
from typing import Dict, List
from googletrans import LANGCODES


class SentiVox: 

    class Config :
        APP_NAME     :  str = "Senti-Vox API"
        APP_DESC     :  str = ""
        APP_VERSION  : str = "1.0.0"
        HEALTH_MESSAGE : dict = {
            "status": "healthy",
            "message": "SentiVox API is running successfully"
        }
        WELCOME_MESSAGE : dict = {
            "message": "Welcome to SentiVox API",
            "description": "Sentiment Analysis API for E-consultation module of Ministry of Corporate Affairs of India",
            "version": "1.0.0",
            "endpoints": {
                "/analyze/single": "POST - Analyze single comment",
                "/analyze/batch": "POST - Analyze multiple comments",
                "/health": "GET - Health check",
                "/docs": "GET - API documentation"
            }
        }

    # This class contains the keys which are used to extract data from the
    # JSON request coming from the user to the API
    class JsonKeys:
        API_KEY = "api-key"
        COMMENT = "comment"
        COMMENT_LIST = "comment-list"
        LANG = "lang"
    
    # This class contains the string of how to denote a language
    class Lang:
        DETECT  = "detect"
        ENGLISH = LANGCODES['english']
        HINDI   = LANGCODES['hindi']
        MARATHI = LANGCODES['marathi']
        BENGALI = LANGCODES['bengali']
        KANNADA = LANGCODES['kannada']
        GUJARATI = LANGCODES['gujarati']
        PUNJABI = LANGCODES['punjabi']
        TAMIL   = LANGCODES['tamil']
        TELUGU  = LANGCODES['telugu']
        SPANISH = LANGCODES['spanish']
        URDU    = LANGCODES['urdu']
        RUSSIAN = LANGCODES['russian']
        SANSKRIT = LANGCODES['sanskrit']

        
    
    # This class contains the models which requires
    class Models:
        class CommentAndLang(BaseModel):
            api_key: str
            comment: str  # contains the data which will be analysed
            lang: str     # specifies the language of the comment (e.g, English, Hindi, Spanish)
            
            class Config:
                json_schema_extra = {
                    "example": {
                        "api_key": "your-api-key-here",
                        "comment": "This is a sample comment for sentiment analysis",
                        "lang": "en"
                    }
                }
        
        class CommentList(BaseModel):
            api_key: str
            comment_list: Dict[str, List[str]]
            
            class Config:
                json_schema_extra = {
                    "example": {
                        "api_key": "your-api-key-here",
                        "comment_list": {
                            "detect" : [
                                "This is a Text",
                                "यह एक अच्छी पहल है"
                            ],
                            "en": [
                                "This is a great initiative",
                                "I support this policy",
                                "Needs more improvement"
                            ],
                            "hi": [
                                "यह एक अच्छी पहल है",
                                "मैं इस नीति का समर्थन करता हूं",
                                "और सुधार की जरूरत है"
                            ]
                        }
                    }
                }