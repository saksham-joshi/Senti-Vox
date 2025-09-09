from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from Analyzer.analyzer import *

from pydantic import BaseModel, ValidationError
import json
from Analyzer.analyzer import *