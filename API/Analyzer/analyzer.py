from .base import *

class SentimentAnalyzer :

    @overload
    async def __init__(self, __comment : str , __lang : str ) :
        self.__initialize()
        
        if __lang == SentiVox.Lang.ENGLISH : 
            self.comment = __comment
        else : 
            self.comment = async_run(SentiVox.Translator.translateToEnglish(__comment, __lang))

    @overload
    async def __init__(self, __comment_list : Dict[str, List[str]]) :
        self.__initialize()
        self.comment = []


        for lang, lst in __comment_list.items() :
        
            if lang == SentiVox.Lang.ENGLISH :
                for i in lst : self.comment.append(i)
            else :
                translated_lst = async_run(SentiVox.Translator.translateListToEnglish(lst, lang))
                for i in translated_lst : self.comment.append(i)

    # declares /initializes class variables. Called by constructor before performing anything
    def __initialize(self) -> None :
        self.words : List[str] = []

    async def analyze( self ) :
        if self.comment is str :
            pass
        else :
            pass