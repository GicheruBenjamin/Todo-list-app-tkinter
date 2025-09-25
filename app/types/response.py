# app/types/response.py
"""
Response type.
Alias type of every response in the app.
config , db , repo and services
"""
from dataclasses import dataclass

@dataclass
class Response:
    status: bool
    message : str
    data : any