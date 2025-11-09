import { app } from "../../../scripts/app.js";


(() => {
    const KRITA_DOCUMENT_NODE_TYPE = "KritaDocument";
    const KRITA_SAVE_IMAGE_NODE_TYPE = "KritaSaveImage";
    const DOCUMENT_NODE_DROPDOWN_LABEL = "document";
    const KRITA_DOCUMENT_GRAPH_USAGE_REFRESH_RATE = 300;
    const COMFY_TABS_CONTAINER_SELECTOR = ".workflow-tabs-container";
    const COMFY_ACTIVE_TAB_SELECTOR = ".p-togglebutton.p-component.p-togglebutton-checked .workflow-label";
    const KRITA_CUSTOM_IO_NODE_TYPES = [
        KRITA_SAVE_IMAGE_NODE_TYPE
    ];


    const kritaDocumentNodes = [];
    let baseUrl = null;
    let previousTabName = null;
    let previousUsedDocumentIdsInGraph = null;
    let previousSerializedNodes = null;


    const api = (() => {
        async function request(method, route, data) {
            if(baseUrl === null) baseUrl = wsToHttpBase(app.api.socket.url);

            const url = new URL(route, baseUrl).toString();
            
            const options = {
                method,
                headers: {
                    'Content-Type': 'application/json'
                },
            };

            if (data) options.body = JSON.stringify(data);
            const response = await fetch(url, options);
            if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`);

            const bodyText = await response.text();
            try {
                return JSON.parse(bodyText);
            }
            catch {
                return bodyText;
            }
        }

        return {
            get: (route) => request('GET', route),
            post: (route, data) => request('POST', route, data),
            put: (route, data) => request('PUT', route, data),
            delete: (route) => request('DELETE', route)
        };
    })();


    const extension = { 
        name: "Krita.WorkflowSync",
        async afterConfigureGraph() {
            await updateDocumentNodes();
            await setupAdditionalWebsocketRoutes();
            await setupWorkflowSynchronization();
        }
    };


    function setupAdditionalWebsocketRoutes() {
        app.api.socket.addEventListener('message', event => {
            const data = JSON.parse(event.data);
            switch(data.type) {
                case "krita::documents::update":
                    updateDocumentNodes(data.data.documents);
            }
        });
    }


    async function updateDocumentNodes(documentNames=null) {
        kritaDocumentNodes.slice(0, kritaDocumentNodes.length);
        const serializedNodes = app.graph.serialize().nodes;
        for(let i = 0; i < serializedNodes.length; i++) {
            const serializedNode = serializedNodes[i];
            if(serializedNode.type === KRITA_DOCUMENT_NODE_TYPE) {
                const node = app.graph._nodes[i];
                kritaDocumentNodes.push(node);
            }
        }

        if(documentNames === null) documentNames = (await api.get('/krita/documents')).documents;

        for(const documentNode of kritaDocumentNodes) {
            const dropdownWidget = documentNode.widgets.find(w => w.label === DOCUMENT_NODE_DROPDOWN_LABEL);
            if(!dropdownWidget) {
                console.warn("Could not find dropdown widget in krita document node.");
                continue;
            }

            const array = dropdownWidget.options.values;
            array.splice(0, array.length);
            documentNames.forEach(d => array.push(d));
            if(!documentNames.includes(dropdownWidget.value)) {
                dropdownWidget.value = null;
            }
            if(dropdownWidget.value == null && documentNames.length > 0) {
                dropdownWidget.value = documentNames[0]
            }
        }
    }

    async function setupWorkflowSynchronization() {
        await sendWorkflow();

        window.addEventListener("focus", () => sendWorkflow(true));

        (function asyncRecurse() {
            sendWorkflow();
            setTimeout(asyncRecurse, KRITA_DOCUMENT_GRAPH_USAGE_REFRESH_RATE);
        })();
    }


    async function sendWorkflow(skipCondition=false) {
        const tabGroupElement = document.querySelector(COMFY_TABS_CONTAINER_SELECTOR);
        const tabElements = tabGroupElement?.querySelector(COMFY_ACTIVE_TAB_SELECTOR);
        const tabName = tabElements?.innerHTML ?? previousTabName;
        if(!tabName) return;

        let documentIdObject = {};

        const serializedGraph = app.graph.serialize();
        const nodes = serializedGraph.nodes;

        for(const node of nodes) {
            if(node.type !== KRITA_DOCUMENT_NODE_TYPE) continue;

            const inputObject = node.inputs.find(i => i.name === DOCUMENT_NODE_DROPDOWN_LABEL);

            if(!inputObject) {
                console.warn("Could not find dropdown widget in krita document node.");
                continue;
            }
            
            const inputIndex = node.inputs.indexOf(inputObject);
            const value = node.widgets_values[inputIndex];
            documentIdObject[value] = null;
        }

        const serializedNodes = [];
        for(const node of nodes) {
            if(!KRITA_CUSTOM_IO_NODE_TYPES.includes(node.type)) continue;
            serializedNodes.push(JSON.stringify({
                id: node.id,
                type: node.type,
                inputs: node.inputs,
                outputs: node.outputs,
                widgets_values: node.widgets_values,
            }));
        }
        const documentIds = Object.keys(documentIdObject);

        if(
            !skipCondition &&
            haveSameElements(previousUsedDocumentIdsInGraph, documentIds) && 
            haveSameElements(previousSerializedNodes, serializedNodes) &&
            (previousTabName === tabName)
        ) return;

        const requestData = {
            workflow: serializedGraph,
            name: tabName,
        };
        documentIds.forEach(id => api.put(`/krita/documents/${id}/workflow`, requestData));

        previousUsedDocumentIdsInGraph = documentIds;
        previousSerializedNodes = serializedNodes;
        previousTabName = tabName;
    }


    function haveSameElements(a, b) {
        return a?.length === b?.length && a?.every(v => b?.includes(v));
    }


    function wsToHttpBase(wsUrl) {
        const url = new URL(wsUrl);

        if (url.protocol === 'ws:') {
            url.protocol = 'http:';
        } else if (url.protocol === 'wss:') {
            url.protocol = 'https:';
        }

        if (url.pathname.endsWith('/ws')) {
            url.pathname = '/';
            url.search = '';
        }

        return url.origin + url.pathname;
    }


    app.registerExtension(extension);
})();
