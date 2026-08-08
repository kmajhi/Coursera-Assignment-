def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    enrollment, created = Enrollment.objects.get_or_create(
        user=user, course=course, defaults={'mode': 'honor'}
    )

    submission = Submission.objects.create(enrollment=enrollment)
    selected_choices = extract_answers(request)
    submission.choices.set(selected_choices)
    submission.save()

    return HttpResponseRedirect(
        reverse('onlinecourse:show_exam_result', args=(course.id, submission.id))
    )


def extract_answers(request):
    submitted_answers = []
    for key in request.POST:
        if key.startswith('choice'):
            choice_id = int(request.POST[key])
            submitted_answers.append(choice_id)
    return submitted_answers


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    selected_choices = submission.choices.all()

    total_score = 0
    possible_score = 0

    for lesson in course.lessons.all():
        for question in lesson.questions.all():
            possible_score += question.grade
            selected_ids = [c.id for c in selected_choices if c.question_id == question.id]
            if question.is_get_score(selected_ids):
                total_score += question.grade

    context = {
        'course': course,
        'grade': total_score,
        'total_score': total_score,
        'possible_score': possible_score,
        'choices': selected_choices,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
