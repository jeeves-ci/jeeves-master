import json
import uuid


from rest_service import responses
from rest_service.exceptions import (JeevesServerError,
                                     WorkflowAlreadyExists,
                                     WorkflowNotFound)
from rest_service.rest_decorators import with_params, with_storage

from jeeves_commons.queue import publisher
from jeeves_commons.storage import utils as storage_utils
from jeeves_commons.dsl.validate import validate_workflow, ValidationError

from flask_restful import Resource, marshal_with, request


class Workflow(Resource):

    @with_storage
    @with_params
    @marshal_with(responses.Workflow.response_fields)
    def post(self, workflow_id=None, execute=True, storage=None, **kwargs):
        # Assign default UUID id
        if not workflow_id:
            workflow_id = str(uuid.uuid4())
        # Raise if workflow with id already exists
        elif storage.workflows.get(workflow_id):
            raise WorkflowAlreadyExists('Workflow with ID \'{}\' already '
                                        'exists.')
        data = json.loads(request.data)
        workflow = data['workflow']
        env = data.get('env', {})
        # Assert env type is dict
        if type(env) is not dict:
            raise JeevesServerError('Workflow env \'{}\' must be of a valid '
                                    'JSON format.'.format(env), 400)
        try:
            validate_workflow(workflow)
        except ValidationError as e:
            raise JeevesServerError(e.message, 400)

        # Create workflow and workflow tasks.
        workflow, tasks = storage_utils.create_workflow(storage,
                                                        workflow,
                                                        workflow_id,
                                                        env)
        if execute:
            storage.workflows.update(workflow_id,
                                     status='QUEUED')
            # queue all workflow tasks.
            for task_item in tasks:
                storage.tasks.update(task_item.task_id, status='QUEUED')
                publisher.send_task_message(task_item.task_id)
            storage.commit()
        return workflow, 201

    @with_storage
    @with_params
    @marshal_with(responses.Workflow.response_fields)
    def delete(self, workflow_id=None, storage=None, **kwargs):
        workflow = storage.workflows.get(workflow_id)
        if not workflow:
            raise WorkflowNotFound('Workflow with ID {0} does not exist.')
        if workflow.status == 'REVOKED':
            raise JeevesServerError('Workflow {0} already revoked.',
                                    404)
        publisher.revoke_workflow_manually(workflow)
        return workflow, 200
