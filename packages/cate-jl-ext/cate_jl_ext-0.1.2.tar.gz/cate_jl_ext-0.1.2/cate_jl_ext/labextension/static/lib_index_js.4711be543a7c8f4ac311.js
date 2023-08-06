"use strict";
(self["webpackChunkcate_jl_ext"] = self["webpackChunkcate_jl_ext"] || []).push([["lib_index_js"],{

/***/ "./lib/api.js":
/*!********************!*\
  !*** ./lib/api.js ***!
  \********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "callAPI": () => (/* binding */ callAPI),
/* harmony export */   "getCateAppUrl": () => (/* binding */ getCateAppUrl),
/* harmony export */   "getServer": () => (/* binding */ getServer),
/* harmony export */   "setLabInfo": () => (/* binding */ setLabInfo)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _util__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./util */ "./lib/util.js");



const API_NAMESPACE = "cate";
function getCateAppUrl(serviceUrl) {
    return `${serviceUrl}/app/?serviceUrl=${serviceUrl}`;
}
/**
 * Set lab information.
 */
async function setLabInfo(settings) {
    const request = {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            lab_url: settings.baseUrl
        })
    };
    return callAPI('labinfo', request, settings);
}
/**
 * Start Cate server and return, once it is ready to serve.
 */
async function getServer(hasServerProxy, settings) {
    const serverState = await startServer(settings);
    assertServerStateOk(serverState);
    const serverPort = serverState.port;
    const serverUrl = (hasServerProxy
        && settings.baseUrl.indexOf("localhost") == -1
        && settings.baseUrl.indexOf("127.0.0.1") == -1)
        ? `${settings.baseUrl}proxy/${serverPort}`
        : `http://localhost:${serverPort}`;
    const fetchServerInfo = async () => {
        const serverState = await getServerState();
        assertServerStateOk(serverState);
        const response = await fetch(serverUrl);
        if (!response.ok) {
            throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response);
        }
        return response.json();
    };
    console.debug('Trying to connect to', serverUrl);
    const serverResponse = await (0,_util__WEBPACK_IMPORTED_MODULE_2__.callUntil)(fetchServerInfo, 10000, 10);
    console.debug('Cate server response:', serverResponse);
    return {
        url: serverUrl,
        state: serverState,
        response: serverResponse,
    };
}
function assertServerStateOk(serverState) {
    console.debug("cate-jl-ext server state:", serverState);
    if (serverState.status === "running") {
        return; // Ok!
    }
    if (serverState.status === "sleeping"
        || serverState.status === "disk-sleep") {
        console.warn("Cate server in sleeping state:", serverState);
        return; // Ok!
    }
    let message = "Cate server could not be started or terminated unexpectedly. ";
    if (typeof serverState.stderr === "string") {
        message += `Message: ${serverState.stderr}. `;
    }
    if (typeof serverState.returncode === "number") {
        message += `Exit code ${serverState.returncode}. `;
    }
    // noinspection SuspiciousTypeOfGuard
    if (typeof serverState.status === "string") {
        message += `Status: ${serverState.status}. `;
    }
    if (Array.isArray(serverState.cmdline)) {
        message += `Command-line: "${serverState.cmdline.join(" ")}". `;
    }
    throw new _util__WEBPACK_IMPORTED_MODULE_2__.UnrecoverableError(message);
}
/**
 * Start Cate server.
 */
async function startServer(settings) {
    return callAPI('server', { method: "PUT" }, settings);
}
/**
 * Get Cate server state.
 */
async function getServerState(settings) {
    return callAPI('server', { method: "GET" }, settings);
}
/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @param settings Server connection settings
 * @returns The response body interpreted as JSON
 */
async function callAPI(endPoint = '', init = {}, settings) {
    settings = settings || _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, API_NAMESPACE, endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.warn('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _api__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./api */ "./lib/api.js");








const ERROR_BOX_TITLE = "Cate JupyterLab Extension";
async function activate(app, settingRegistry, palette, launcher, restorer) {
    console.debug("Activating JupyterLab extension cate-jl-ext:");
    console.debug("  ISettingRegistry:", settingRegistry);
    console.debug("  ICommandPalette:", palette);
    console.debug("  ILauncher:", launcher);
    console.debug("  ILayoutRestorer:", restorer);
    console.debug("  baseUrl:", _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getBaseUrl());
    console.debug("  wsUrl:", _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getWsUrl());
    console.debug("  shareUrl:", _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getShareUrl());
    console.debug("  treeUrl:", _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getTreeUrl());
    const serverSettings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_4__.ServerConnection.makeSettings();
    // console.debug("  serverSettings:", serverSettings);
    let hasServerProxy = false;
    try {
        const labInfo = await (0,_api__WEBPACK_IMPORTED_MODULE_7__.setLabInfo)(serverSettings);
        hasServerProxy = !!labInfo.has_proxy;
    }
    catch (error) {
        await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_5__.showErrorMessage)(ERROR_BOX_TITLE, error);
        return;
    }
    if (settingRegistry !== null) {
        let settings;
        try {
            settings = await settingRegistry.load(plugin.id);
            console.debug("cate-jl-ext settings loaded:", settings.composite);
        }
        catch (error) {
            console.error("Failed to load settings for cate-jl-ext.", error);
        }
    }
    let widget = null;
    let tracker = null;
    // Add an application command
    const commandID = "cate:openCateApp";
    app.commands.addCommand(commandID, {
        label: "Cate App",
        iconClass: (args) => (args["isPalette"] ? "" : "cate-icon"),
        execute: async () => {
            if (widget === null || widget.isDisposed) {
                console.debug("Creating new JupyterLab widget cate-jl-ext");
                let serverStatus;
                try {
                    // TODO (forman): show indicator while starting server
                    serverStatus = await (0,_api__WEBPACK_IMPORTED_MODULE_7__.getServer)(hasServerProxy, serverSettings);
                }
                catch (error) {
                    console.error("Argh:", error);
                    await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_5__.showErrorMessage)(ERROR_BOX_TITLE, error);
                    return;
                }
                let cateAppUrl = (0,_api__WEBPACK_IMPORTED_MODULE_7__.getCateAppUrl)(serverStatus.url);
                console.debug("cateAppUrl:", cateAppUrl);
                // Create a blank content widget inside a MainAreaWidget
                const content = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.Widget();
                const iframe = document.createElement('iframe');
                iframe.style.position = "absolute";
                iframe.style.width = "100%";
                iframe.style.height = "100%";
                iframe.style.border = "none";
                iframe.src = cateAppUrl;
                content.node.appendChild(iframe);
                widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_5__.MainAreaWidget({ content });
                widget.id = "cate-app";
                widget.title.label = "Cate App";
                widget.title.closable = true;
            }
            if (tracker !== null && !tracker.has(widget)) {
                // Track the state of the widget for later restoration
                tracker.add(widget).then(() => {
                    console.debug('JupyterLab widget cate-jl-ext stored!');
                });
            }
            if (!widget.isAttached) {
                // Attach the widget to the main work area if it's not there
                app.shell.add(widget, "main");
            }
            // Activate the widget
            app.shell.activateById(widget.id);
        }
    });
    if (palette !== null) {
        // Add the command to the palette.
        palette.addItem({
            command: commandID,
            category: "Other"
        });
    }
    if (launcher !== null) {
        // Add the command to the launcher.
        launcher.add({
            command: commandID,
            category: "Other",
            rank: 0
        });
    }
    if (restorer !== null) {
        // Track and restore the widget state
        tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_5__.WidgetTracker({
            namespace: "cate"
        });
        restorer.restore(tracker, {
            command: commandID,
            name: () => "cate"
        }).then(() => {
            console.debug('JupyterLab widget cate-jl-ext restored!');
        });
    }
    console.log('JupyterLab extension cate-jl-ext is activated!');
}
/**
 * Initialization data for the cate-jl-ext extension.
 */
const plugin = {
    id: "cate-jl-ext:plugin",
    autoStart: true,
    optional: [
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__.ISettingRegistry,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_5__.ICommandPalette,
        _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__.ILauncher,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer
    ],
    activate
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/util.js":
/*!*********************!*\
  !*** ./lib/util.js ***!
  \*********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "UnrecoverableError": () => (/* binding */ UnrecoverableError),
/* harmony export */   "callUntil": () => (/* binding */ callUntil)
/* harmony export */ });
/*
 * The MIT License (MIT)
 *
 * Copyright (c) 2019-2023 by the Cate development team and contributors.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to
 * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
 * of the Software, and to permit persons to whom the Software is furnished to do
 * so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */
/**
 * Throw this error, if you want `callUntil()` to exit immediately.
 */
class UnrecoverableError extends Error {
    constructor(message, error) {
        super(message);
        this.error = error;
    }
}
/**
 * Call asynchronous function `fetchValue` until it returns a value without throwing an exception.
 * If it throws an exception, it will be executed after a delay of `timeout / maxCount`.
 * This is repeated until `maxCount` is reached or a `UnrecoverableError` is thrown.
 * Eventually, the last exception will be thrown.
 *
 * @param fetchValue The asynchronous function to be called.
 * @param timeout Overall timeout in milliseconds.
 * @param maxCount Maximum number of failures.
 */
async function callUntil(fetchValue, timeout, maxCount) {
    const delay = timeout / maxCount;
    const handler = (resolve, reject, count) => {
        console.debug(`Fetching ${fetchValue.name}() (attempt ${count}/${maxCount})`);
        fetchValue()
            .then(value => {
            resolve(value);
        })
            .catch(error => {
            if (error instanceof UnrecoverableError) {
                reject(error.error || error);
            }
            else if (count >= maxCount) {
                reject(error);
            }
            else {
                delayedHandler(resolve, reject, count + 1);
            }
        });
    };
    const delayedHandler = (resolve, reject, count) => {
        setTimeout(() => handler(resolve, reject, count), delay);
    };
    return new Promise((resolve, reject) => delayedHandler(resolve, reject, 1));
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.4711be543a7c8f4ac311.js.map