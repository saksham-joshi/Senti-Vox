from typing import overload, Dict, List
from googletrans import LANGCODES, Translator
from pydantic import BaseModel
from asyncio import run as async_run
from json import load