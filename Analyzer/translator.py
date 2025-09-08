from googletrans import Translator
import asyncio

class SentivoxTranslator :

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