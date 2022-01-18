def student_or_professor(user):
    try:
        return user.professor
    except:
        return user.student