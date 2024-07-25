from pydantic import BaseModel
from typing import List, Optional

class CurrentLocation(BaseModel):
    province: str
    district: Optional[str] = None

class Education(BaseModel):
    currentSchool: str
    major: str
    currentSchoolYear: str
    latestGPA: float

class Occupation(BaseModel):
    employmentStatus: str
    companyName: Optional[str] = None
    position: Optional[str] = None
    employmentLevel: Optional[str] = None
    yearsOfExperience: Optional[int] = None
    industry: Optional[str] = None

class MenteeDetails(BaseModel):
    industries: List[str]
    softSkills: List[str]
    preferredMentorGender: str
    preferredForeignMentor: str

class Bio(BaseModel):
    selfIntroduction: str
    favoriteQuote: str
    hobbies: List[str]
    favoriteBook: str
    favoriteMovie: str


class MentorDetails(BaseModel):
    industries: List[str]
    softSkills: List[str]
    preferredNumberOfMentees: int
    preferredMenteeCollegeYear: str
    preferredMenteeGender: str

class Mentor(BaseModel):
    id: str
    uuid: str
    fullName: str
    phoneNumber: str
    email: str
    gender: str
    homeTown: str
    currentLocation: CurrentLocation
    birthYear: int
    occupation: Occupation
    mentor: MentorDetails
    bio: Bio
    
class Mentee(BaseModel):
    id: str
    uuid: str
    fullName: str
    phoneNumber: str
    email: str
    gender: str
    homeTown: str
    currentLocation: CurrentLocation
    birthYear: int
    education: Education
    occupation: Occupation
    mentee: MenteeDetails
    bio: Bio
    