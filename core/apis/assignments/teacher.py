from flask import Blueprint
from marshmallow import ValidationError

from core.apis import decorators
from core.apis.responses import APIResponse
from core import db
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentGradeSchema

teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments/', methods=["GET"], strict_slashes=False)
@decorators.auth_principal
def lists_assignments(p):
    teacher_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    teacher_assignments_dump = AssignmentSchema().dump(teacher_assignments, many=True)
    return APIResponse.respond(data=teacher_assignments_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignment(princi, incoming_payload):
    assignment_grade_payload = AssignmentGradeSchema().load(incoming_payload)
    if assignment_grade_payload.grade not in ['A', 'B', 'C', 'D']:
        raise ValidationError("ValidationError")
    submit_grade = Assignment.grade_assignment(
        _id=assignment_grade_payload.id,
        grade=assignment_grade_payload.grade,
        p=princi
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(submit_grade)
    return APIResponse.respond(data=graded_assignment_dump)
