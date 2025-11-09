from .comfy_websocket import ComfyWebsocket
from .comfy_api import ComfyApi
from .models import StatusRequest, UpdateKritaWorkflowRequest


def define_commands(comfy_ws: ComfyWebsocket, comfy_api: ComfyApi):
    @comfy_ws.handler("status")
    def status_statement(data: dict):
        status_request = StatusRequest.model_validate(data)
        comfy_ws.sid = status_request.sid
        comfy_api.update_documents()

    @comfy_ws.handler("krita::workflow::update")
    def update_workflow(data: dict):
        workflow_request = UpdateKritaWorkflowRequest.model_validate(data)
