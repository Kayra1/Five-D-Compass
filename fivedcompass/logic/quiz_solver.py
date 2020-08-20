from ..models import Quiz, Question

def quiz_solver(quiz_id, answer_string):
    
    quiz_questions = Quiz.objects.get(id=quiz_id).question_set.all()
    answer_list = answer_string.split(',')

    resultDict = {}

    for question in quiz_questions:
        # Extract the dimension
        direction = getattr(question, 'dimension')
        magnitude = int(answer_list[0]) - 3    # - 3 so the scale is [-2,2]
        answer_list.pop(0)

        # Multiply the value by the answer
        vector = direction / abs(direction) * magnitude 

        # Add the value to the dict
        if f'{abs(direction)}' in resultDict:
            resultDict[f'{abs(direction)}'] += vector
        else:
            resultDict.update({f'{abs(direction)}': vector})

    return resultDict