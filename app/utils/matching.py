import string
# from pydantic import BaseModel
# from app.db import db
from app.models import (Bio, CurrentLocation, Education, Mentee, Mentor, 
                        MentorDetails, MenteeDetails, Match, Group, MatchMentee,
                        Occupation)
from app.utils.array import find_common_element
from typing import List, Optional
from underthesea import word_tokenize, pos_tag
from FlagEmbedding import BGEM3FlagModel
from sklearn.metrics.pairwise import cosine_similarity
import datetime
import uuid
import math

vietnamese_stopwords = set([
    "có", "của", "trong", "các", "được", "đến", "và", "nhiều", "này", "một",
    "chỉ", "đó", "sẽ", "số", "để", "đã", "ở", "những", "vào", "qua", "đi",
    "không", "là", "ra", "mà", "khi", "rằng", "từ", "năm", "rất", "hay", "tại",
    "sau", "bị", "đều", "vẫn", "lần", "như", "đồng", "mình", "còn", "xảy", "đợt",
    "theo", "hiện", "tuy nhiên", "10", "gì", "tới", "lại", "về", "2"
])

def calculateMatchingRate(mentee:Mentee, mentor:Mentor):
    total_points = 0
    # Accessing attributes using dict[key]
    if (mentee.education.major == mentor.occupation.industry):
        total_points += 2
        
    # Assuming find_common_element is a helper function you've defined
    wanted_fields = find_common_element(mentee.mentee.industries, mentor.mentor.industries)
    total_points += len(wanted_fields) * 1
    
    wanted_soft_skills = find_common_element(mentee.mentee.softSkills, mentor.mentor.softSkills)
    total_points += len(wanted_soft_skills) * 2   
        
    if(mentee.gender == mentor.gender):
        total_points += 1
    
    if(mentee.education.currentSchoolYear == mentor.mentor.preferredMenteeCollegeYear):
        total_points += 1 

    selfintro_similarity_score = calculateSelfIntroScore(mentee, mentor)
    total_points += selfintro_similarity_score
    
    return total_points
    


def extract_selfintro(mentee:Mentee, mentor:Mentor): 
    mentee_selfintro = mentee.bio.selfIntroduction
    mentor_selfintro = mentor.bio.selfIntroduction
    return mentee_selfintro, mentor_selfintro

def clean_and_tokenize(mentee_intro, mentor_intro):
    mentee_intro = mentee_intro.lower()
    mentor_intro = mentor_intro.lower()

    mentee_tokenized = word_tokenize(mentee_intro)
    mentor_tokenized = word_tokenize(mentor_intro)

    mentee_tokenized = [word for word in mentee_tokenized if word not in string.punctuation]
    mentor_tokenized = [word for word in mentor_tokenized if word not in string.punctuation]
    
    filtered_mentee = [word for word in mentee_tokenized if word not in vietnamese_stopwords]
    filtered_mentor = [word for word in mentor_tokenized if word not in vietnamese_stopwords]

    pos_tags_mentee = pos_tag(' '.join(filtered_mentee))
    pos_tags_mentor = pos_tag(' '.join(filtered_mentor))

    lemmatized_mentee = [word for word, pos in pos_tags_mentee]
    lemmatized_mentor = [word for word, pos in pos_tags_mentor]

    return lemmatized_mentee, lemmatized_mentor

def semantic_similarity(cleaned_mentee, cleaned_mentor):
    model = BGEM3FlagModel('BAAI/bge-m3',  
                       use_fp16=True) # Setting use_fp16 to True speeds up computation with a slight performance degradation
    embeddings_1 = model.encode(cleaned_mentee, 
                            batch_size=12, 
                            max_length=6000, # If you don't need such a long length, you can set a smaller value to speed up the encoding process.
                            )['dense_vecs']
    embeddings_2 = model.encode(cleaned_mentor)['dense_vecs']
    similarity_matrix = cosine_similarity(embeddings_1, embeddings_2)
    return similarity_matrix

def calculateSelfIntroScore(mentee:Mentee, mentor:Mentor): 
    mentee_intro, mentor_intro = extract_selfintro(mentor, mentee)
    print(f"Mentee Intro: {mentee_intro}")
    print(f"Mentor Intro: {mentor_intro}")

    cleaned_mentee, cleaned_mentor= clean_and_tokenize(mentee_intro, mentor_intro)
    print(f"Cleaned/Tokenized Mentee Intro: {cleaned_mentee}")
    print(f"Cleaned/Tokenzied Mentor Intro: {cleaned_mentor}")

    semantic_score_matrix = semantic_similarity(cleaned_mentee, cleaned_mentor)

    # make vector into score
    semantic_score = float(cosine_similarity(
        [semantic_score_matrix.mean(axis=1)],
        [semantic_score_matrix.mean(axis=0)]
    )[0][0])
    print(f"Semantic Score (Cos Similarity): {semantic_score}")

    return semantic_score

    
#  Read list of mentees and mentors from mentor.json and mentee.json
#  Generate a match with the mentees and mentors

def generateGroup(mentees, mentors, matchName:Optional[str] = None):
    groups:List[Group] = []
    candidates = []
    

    max_group_size = math.ceil(len(mentees) / len(mentors))



    print("max_gr_sz",max_group_size)
    for mentor in mentors:
        for mentee in mentees:
            score = calculateMatchingRate(mentee, mentor)
            candidates.append({
                "mentee": mentee,
                "mentor": mentor,
                "score": score
            })
    
    candidates.sort(key=lambda x: x["score"], reverse=True)
    unmatched_mentees = mentees.copy()
    target_mentor = 0
    
    while len(unmatched_mentees) > 0:
        group:Group = {
            "id":target_mentor,
            "mentorId": mentors[target_mentor]["id"],
            "mentees": [],
        }
        for candidate in candidates:
            if candidate["mentor"] == mentors[target_mentor] and candidate["mentee"] in unmatched_mentees and len(group['mentees']) < max_group_size:
                new_match_mentee:MatchMentee = {
                    "menteeId": candidate["mentee"]["id"],
                    "menteeName": candidate["mentee"]["fullName"],
                    "matchRate": candidate["score"]
                }
                group["mentees"].append(new_match_mentee)
                unmatched_mentees.remove(candidate["mentee"])
                candidates.remove(candidate)
        groups.append(group)
        target_mentor += 1
        target_mentor = target_mentor % len(mentors)
        
    new_match:Match = {
        "uid": str(uuid.uuid4()),
        "createdAt": str(datetime.datetime.now()),
        "groups": groups,
        "matchName": matchName if matchName else "Match " + str(datetime.datetime.now())
    }
    
    
    
    
    return new_match        
            

if __name__ == "__main__": 
    # my_current_location = CurrentLocation("USA")
    # my_occupation = Occupation("Employed", "UCSD")
    # my_mentor_details = MentorDetails(["SWE", "ECE"], ["Leadership", "Nice"], 3, "Junior", "Female")
    # my_mentee_details = MentorDetails(["SWE", "ECE"], ["Leadership", "Nice"], 3, "Junior", "Female")
    # my_mentor_bio = Bio("Tôi đang học lập trình Python và tìm hiểu cách xử lý ngôn ngữ tự nhiên.", 
    #                     "I love books", ["Watching Movies", "Playing games"], "Harry Potter",
    #                     "Harry Potter")
    


    # belma = Mentor("0", "0", "Belma Bajramovic", "0", "a@gmail.com", "female", "hometown", 
    #                my_current_location, 5, my_occupation, my_mentor_details, my_mentor_bio)
    # kobe = Mentee("0", "0", "Kobe Yang", "0", "a@gmail.com", "male", "hometown", 
    #                my_current_location, 5, my_occupation, my_mentee_details, my_mentor_bio)
    
    # Current location for both
    my_current_location = CurrentLocation(province="USA", district="California")

    # Occupation details
    my_occupation = Occupation(
        employmentStatus="Employed",
        companyName="UCSD",
        position="Research Assistant",
        employmentLevel="Intern",
        yearsOfExperience=1,
        industry="Education"
    )

    # Mentor-specific details
    my_mentor_details = MentorDetails(
        industries=["SWE", "ECE"],
        softSkills=["Leadership", "Empathy"],
        preferredNumberOfMentees=3,
        preferredMenteeCollegeYear="Junior",
        preferredMenteeGender="Female"
    )

    # Mentee-specific details
    my_mentee_details = MenteeDetails(
        industries=["SWE", "ECE"],
        softSkills=["Leadership", "Empathy"],
        preferredMentorGender="Female",
        preferredForeignMentor=False,
        preferredMentorType="Career guidance"
    )

    # Bio
    my_bio = Bio(
        selfIntroduction="Tôi đang học lập trình Python và tìm hiểu cách xử lý ngôn ngữ tự nhiên.",
        favoriteQuote="I love books",
        hobbies=["Watching Movies", "Playing Games"],
        favoriteBook="Harry Potter",
        favoriteMovie="Harry Potter"
    )

    # Education for mentee
    my_education = Education(
        currentSchool="UC San Diego",
        major="Computer Engineering",
        currentSchoolYear="Junior",
        latestGPA=3.8
    )

    # Mentor object
    belma = Mentor(
        id="1",
        uuid="uuid-belma",
        fullName="Belma Bajramovic",
        phoneNumber="1234567890",
        email="belma@gmail.com",
        gender="female",
        homeTown="Sarajevo",
        currentLocation=my_current_location,
        birthYear=2003,
        occupation=my_occupation,
        mentor=my_mentor_details,
        bio=my_bio
    )

    # Mentee object
    kobe = Mentee(
        id="2",
        uuid="uuid-kobe",
        fullName="Kobe",
        phoneNumber="0987654321",
        email="kobe@gmail.com",
        gender="male",
        homeTown="Hanoi",
        currentLocation=my_current_location,
        birthYear=2004,
        education=my_education,
        occupation=my_occupation,
        mentee=my_mentee_details,
        bio=my_bio
    )

    score = calculateMatchingRate(kobe, belma)
    print(f"Final Score: {score}")
    

