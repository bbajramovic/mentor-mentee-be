from app.models import (
    Bio, CurrentLocation, Education, Mentee, MenteeDetails, 
    Mentor, MentorDetails, Occupation
)
from app.utils.group_assignment import generate_balanced_group
from app.utils.matching import calculateMatchingRate


if __name__ == "__main__":     
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
    
    generate_balanced_group(belma, kobe)

