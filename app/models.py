from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class UserProfileRequest(BaseModel):
    name: str = Field(default="Rahul Sharma", example="Rahul Sharma")
    dob: str = Field(default="16/05/1998", example="16/05/1998")
    birth_place: str = Field(default="Ahmedabad, Gujarat", example="Ahmedabad, Gujarat")
    birth_time: str = Field(default="08:30 AM", example="08:30 AM")
    accuracy: str = Field(default="Exact", example="Exact")
    language: str = Field(default="gu", example="gu")

class UserProfileResponse(BaseModel):
    user_id: str
    name: str
    dob: str
    birth_place: str
    birth_time: str
    zodiac_sign_en: str
    zodiac_sign_gu: str
    zodiac_sign_hi: str
    zodiac_symbol: str
    destiny_number: int

class RashifalResponse(BaseModel):
    sign_id: str
    sign_en: str
    sign_gu: str
    sign_hi: str
    symbol: str
    date_range: str
    date: str
    prediction_summary: str
    love_score: str
    career_score: str
    finance_score: str
    family_score: str
    health_score: str
    travel_score: str
    love_stars: int
    career_stars: int
    finance_stars: int
    family_stars: int
    health_stars: int
    travel_stars: int
    lucky_number: int
    lucky_color: str
    lucky_time: str

class KundliHouseDetail(BaseModel):
    house_number: int
    sign: str
    planets: List[str]
    description: str

class KundliResponse(BaseModel):
    lagna: str
    moon_sign: str
    sun_sign: str
    nakshatra: str
    current_dasha: str
    manglik_dosh: bool
    manglik_status: str
    houses: List[KundliHouseDetail]
    life_analysis: Dict[str, String] if False else Dict[str, Any]

class NumerologyNumberDetail(BaseModel):
    number: int
    title: str
    calculation: str
    meaning: str

class NumerologyResponse(BaseModel):
    mulank: NumerologyNumberDetail
    bhagyank: NumerologyNumberDetail
    namank: NumerologyNumberDetail
    soul_urge: Optional[NumerologyNumberDetail] = None
    personality: Optional[NumerologyNumberDetail] = None
    hidden_passion: Optional[NumerologyNumberDetail] = None
    lucky_numbers: List[int]
    lucky_colors: List[str]

class NumerologyChatRequest(BaseModel):
    numbers_data: Dict[str, Any]
    message: str
    language: str = "gu"

class PanditDetail(BaseModel):
    id: str
    name: str
    specialty: str
    category: str
    rating: float
    consultations: str
    is_online: bool
    expertise_list: List[str]

class ChatMessageRequest(BaseModel):
    user_id: Optional[str] = "user_101"
    pandit_name: str = "Pandit Aarav Ji"
    question: str
    language: str = "gu"
    kundli_data: Optional[Dict[str, Any]] = None

class ChatMessageResponse(BaseModel):
    reply: str
    timestamp: str
    sender: str

class PanchangResponse(BaseModel):
    date: str
    tithi: str
    nakshatra: str
    yoga: str
    karana: str
    sunrise: str
    sunset: str
    shubh_choghadiya: List[str]
    ashubh_choghadiya: List[str]
