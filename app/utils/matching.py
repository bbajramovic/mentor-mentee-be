from pydantic import BaseModel
from app.models import Mentee, Mentor
from app.utils.array import find_common_element



def calculateMatchingRate(mentee:Mentee, mentor:Mentor):
    total_points = 0
    
    if (mentee.education.major == mentor.occupation.industry):
        total_points += 2
        
    # Mutual field wanted to be mentor and can mentor
    wanted_fields = find_common_element(mentee.mentee.industries, mentor.mentor.industries)
    total_points += len(wanted_fields)*1
    
    wanted_soft_skills = find_common_element(mentee.mentee.softSkills, mentor.mentor.softSkills)
    total_points += len(wanted_soft_skills)*2   
        
    if(mentee.gender == mentor.gender):
        total_points += 1
    
    if(mentee.education.currentSchoolYear == mentor.mentor.preferredMenteeCollegeYear):
        total_points += 1 
    
  

def calculateMatching(mentees, mentors):
    mentor_match_mentee = []
    for mentor in mentors:
        mentees_of_mentor = []
        for mentee in mentees: 
            rate = calculateMatchingRate(mentee, mentor)
            result = {
                "match_rate": rate, 
                "mentee": mentee.id,
                "mentor": mentor.id,
                # TODO:
                # Maybe we want to add other field for preview! To save cost too. 
            }
            
            mentees_of_mentor.push(result)
        
        result = {
            "mentor": mentor.id,
            "name": mentor.fullName, 
            "mentees": mentees_of_mentor # TODO: Consider to reduce result by only top 5!
        }
        mentees_of_mentor.append(result)
    return mentor_match_mentee
            