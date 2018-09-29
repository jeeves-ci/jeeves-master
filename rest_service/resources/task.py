from rest_service import responses
from rest_service.rest_decorators import (with_params,
                                          with_storage,
                                          jwt_required)
from rest_service.exceptions import WorkflowNotFound
from rest_service.resources.resource import JeevesResource

from flask_restful import marshal_with
from flask_restful_swagger import swagger


class Task(JeevesResource):

    @swagger.operation(
        responseClass='{0}'.format(responses.Task.__name__),
        nickname="get",
        notes="Returns a task by it's ID"
    )
    @with_storage
    @jwt_required
    @with_params
    @marshal_with(responses.Task.response_fields)
    def get(self,
            workflow_id=None,
            task_id=None,
            storage=None,
            user=None,
            **kwargs):
        workflow = storage.workflows.get(workflow_id=workflow_id,
                                         tenant_id=user.tenant_id)
        if workflow is None:
            raise WorkflowNotFound('Workflow with ID {} not found'
                                   .format(workflow_id))
        return storage.tasks.get(task_id=task_id, **kwargs)
