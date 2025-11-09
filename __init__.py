from typing_extensions import override

from comfy_api.latest import ComfyExtension, io

from .constants import KRITA_DOCUMENT_IO_TYPE, KRITA_SAVE_IMAGE_NODE_TYPE, KRITA_DOCUMENT_NODE_TYPE
from .krita_api import KritaApi
from .routes import define_routes


WEB_DIRECTORY = "."


api = KritaApi()
define_routes()


@io.comfytype(io_type=KRITA_DOCUMENT_IO_TYPE)
class KritaDocumentId:
    Type = str

    class Input(io.Input):
        def __init__(self, id: str, **kwargs):
            super().__init__(id, **kwargs)

    class Output(io.Output):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)


class KritaSaveImage(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id=KRITA_SAVE_IMAGE_NODE_TYPE,
            display_name="Save Image (as krita layer)",
            category="krita",
            is_output_node=True,
            inputs=[
                io.Image.Input(
                    id="image", 
                    display_name="image"
                ),
                KritaDocumentId.Input(
                    id="krita document"
                ),
                io.Combo.Input(
                    id="position",
                    options=["Top"],
                    display_name="position",
                    optional=False,
                    tooltip="Select the position where the image will be saved to in the layers docker.",
                    lazy=True,
                    default="Top",
                ),
            ],
        )

    @classmethod
    def execute(cls, image, position) -> io.NodeOutput: # type: ignore
        match position:
            case "Top":
                api.create_layer(image)

        return io.NodeOutput()


class KritaDocument(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id=KRITA_DOCUMENT_NODE_TYPE,
            display_name="Krita Document",
            category="krita",
            inputs=[
                io.Combo.Input(
                    id="document",
                    options=[],
                    display_name="document",
                    optional=False,
                    tooltip="Select a Krita document.",
                    lazy=True,
                ),
            ],
            outputs=[
                KritaDocumentId.Output()
            ]
        )

    @classmethod
    def execute(cls, document: str) -> io.NodeOutput: # type: ignore
        return io.NodeOutput(document)


class KritaExtension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [
            KritaSaveImage,
            KritaDocument,
        ]


async def comfy_entrypoint() -> ComfyExtension:
    return KritaExtension()
