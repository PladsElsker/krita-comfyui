from typing import Any, Dict, List
from pydantic import BaseModel


class StatusRequest(BaseModel):
    status: Dict[str, Any]
    sid: str


class Node(BaseModel):
    id: int
    type: str


class PrunedKritaWorkflow(BaseModel):
    name: str
    inputs: List[Node]
    outputs: List[Node]


class UpdateKritaWorkflowRequest(BaseModel):
    id: str
    workflow: PrunedKritaWorkflow


class UpdateKritaDocumentsRequest(BaseModel):
    documents: List[str]
