from .imports import *

class SentiVox: 

    class Config :
        APP_NAME     :  str = "Senti-Vox API"
        APP_DESC     :  str = ""
        APP_VERSION  :  str = "1.0.0"

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
        API_KEY      = "api-key"
        COMMENT      = "comment"
        COMMENT_LIST = "comment-list"
        LANG         = "lang"
        SENTIMENT    = "sentiment"
        POS_SCORE    = "positive-score"
        NEG_SCORE    = "negative-score"
        POL_SCORE    = "polarity-score"
        SUB_SCORE    = "subjectivity-score"
        KEYWORDS     = "keywords"
        UNID_WORDS   = "unidentified-words"
        POS_WORDS    = "positive-words"
        NEG_WORDS    = "negative-words"

    
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
    
    class Calculation :

        #====================| This is the score that determines if a given text is positive or negative in nature.
        # Range is from -1 to +1.
        @staticmethod
        def calculate_polarity_score(__positive_score : int, __negative_score : int) -> float :
            return round((__positive_score - __negative_score)/(0.000001+ __positive_score+__negative_score),3)
        
        #====================| This is the score that determines if a given text is objective or subjective.
        # Range is from 0 to +1.
        @staticmethod
        def calculate_subjectivity_score(__positive_score : int, __negative_score : int, __total_word_analyzed : int) -> float :
            return round((__positive_score+__negative_score)/(__total_word_analyzed),3) if __total_word_analyzed != 0 else (__positive_score+__negative_score)
    

    class Translator :

        @staticmethod
        async def translateToEnglish( __text : str , __src_lang : str ) :
            
            async with Translator() as translator :

                if __src_lang == "detect" : return await translator.translate( __text )

                else : return await translator.translate(text=__text, src=__src_lang, dest="en" )



        @staticmethod
        async def translateListToEnglish( __textlist : list[str], __src_lang : str ) :

            async with Translator() as translator :

                if __src_lang == "detect" : return await translator.translate(text=__textlist, dest="en")

                else : return await translator.translate(text=__textlist, dest="en", src=__src_lang)

        ## To call these functions
        ## asyncio.run(translateToEnglish())
    
    STOPWORDS_SET : set = set()
    POS_WORDS_SET : set = set()
    NEG_WORDS_SET : set = set()
    
    @staticmethod
    def loadWordFiles() -> None :
        with open("Analyzer/dataset/data.json") as word_file :
            dt = load(word_file)
            SentiVox.STOPWORDS_SET = set(dt['stop-words'])
            SentiVox.POS_WORDS_SET = set(dt['pos-words'])
            SentiVox.NEG_WORDS_SET = set(dt['neg-words'])