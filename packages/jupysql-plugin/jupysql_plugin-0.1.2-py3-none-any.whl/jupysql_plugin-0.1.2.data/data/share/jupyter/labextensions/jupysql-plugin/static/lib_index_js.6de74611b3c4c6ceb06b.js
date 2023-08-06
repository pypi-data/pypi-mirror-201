"use strict";
(self["webpackChunkjupysql_plugin"] = self["webpackChunkjupysql_plugin"] || []).push([["lib_index_js"],{

/***/ "./lib/connector.js":
/*!**************************!*\
  !*** ./lib/connector.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CompletionConnector": () => (/* binding */ CompletionConnector)
/* harmony export */ });
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
// Modified from jupyterlab/packages/completer/src/connector.ts

/**
 * A multi-connector connector for completion handlers.
 */
class CompletionConnector extends _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__.DataConnector {
    /**
     * Create a new connector for completion requests.
     *
     * @param connectors - Connectors to request matches from, ordered by metadata preference (descending).
     */
    constructor(connectors) {
        super();
        this._connectors = connectors;
    }
    /**
     * Fetch completion requests.
     *
     * @param request - The completion request text and details.
     * @returns Completion reply
     */
    fetch(request) {
        return Promise.all(this._connectors.map((connector) => connector.fetch(request))).then((replies) => {
            const definedReplies = replies.filter((reply) => !!reply);
            return Private.mergeReplies(definedReplies);
        });
    }
}
/**
 * A namespace for private functionality.
 */
var Private;
(function (Private) {
    /**
     * Merge results from multiple connectors.
     *
     * @param replies - Array of completion results.
     * @returns IReply with a superset of all matches.
     */
    function mergeReplies(replies) {
        // Filter replies with matches.
        const repliesWithMatches = replies.filter((rep) => rep.matches.length > 0);
        // If no replies contain matches, return an empty IReply.
        if (repliesWithMatches.length === 0) {
            return replies[0];
        }
        // If only one reply contains matches, return it.
        if (repliesWithMatches.length === 1) {
            return repliesWithMatches[0];
        }
        // Collect unique matches from all replies.
        const matches = new Set();
        repliesWithMatches.forEach((reply) => {
            reply.matches.forEach((match) => matches.add(match));
        });
        // Note that the returned metadata field only contains items in the first member of repliesWithMatches.
        return { ...repliesWithMatches[0], matches: [...matches] };
    }
    Private.mergeReplies = mergeReplies;
})(Private || (Private = {}));


/***/ }),

/***/ "./lib/customconnector.js":
/*!********************************!*\
  !*** ./lib/customconnector.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CustomConnector": () => (/* binding */ CustomConnector)
/* harmony export */ });
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _keywords_json__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./keywords.json */ "./lib/keywords.json");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * A custom connector for completion handlers.
 */
class CustomConnector extends _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__.DataConnector {
    /**
     * Create a new custom connector for completion requests.
     *
     * @param options - The instatiation options for the custom connector.
     */
    constructor(options) {
        super();
        this._editor = options.editor;
        this._sessionContext = options.sessionContext;
    }
    /**
     * Fetch completion requests.
     *
     * @param request - The completion request text and details.
     * @returns Completion reply
     */
    fetch(request) {
        if (!this._editor) {
            return Promise.reject('No editor');
        }
        return new Promise((resolve) => {
            resolve(Private.completionHint(this._editor, this._sessionContext));
        });
    }
}
/**
 * A namespace for Private functionality.
 */
var Private;
(function (Private) {
    /**
     * Get a list of mocked completion hints.
     *
     * @param editor Editor
     * @returns Completion reply
     */
    function completionHint(editor, sessionContext) {
        // Find the token at the cursor
        const cursor = editor.getCursorPosition();
        const token = editor.getTokenForPosition(cursor);
        var newTokenList = _keywords_json__WEBPACK_IMPORTED_MODULE_1__.keywords;
        const completionList = newTokenList.filter((t) => t.value.startsWith(token.value.toUpperCase())).map((t) => t.value);
        // Remove duplicate completions from the list
        const matches = Array.from(new Set(completionList));
        return {
            start: token.offset,
            end: token.offset + token.value.length,
            matches,
            metadata: {},
        };
    }
    Private.completionHint = completionHint;
})(Private || (Private = {}));


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
/* harmony import */ var _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/completer */ "webpack/sharing/consume/default/@jupyterlab/completer");
/* harmony import */ var _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _connector__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./connector */ "./lib/connector.js");
/* harmony import */ var _customconnector__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./customconnector */ "./lib/customconnector.js");
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/codemirror */ "webpack/sharing/consume/default/@jupyterlab/codemirror");
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! underscore */ "webpack/sharing/consume/default/underscore/underscore");
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(underscore__WEBPACK_IMPORTED_MODULE_3__);




// for syntax highlighting


/**
 * The command IDs used by the console plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.invoke = 'completer:invoke';
    CommandIDs.invokeNotebook = 'completer:invoke-notebook';
    CommandIDs.select = 'completer:select';
    CommandIDs.selectNotebook = 'completer:select-notebook';
})(CommandIDs || (CommandIDs = {}));
/**
 * Initialization data for the extension.
 */
const extension = {
    id: 'completer',
    autoStart: true,
    requires: [_jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.ICompletionManager, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.INotebookTracker],
    activate: async (app, completionManager, notebooks) => {
        console.log('JupyterLab custom completer extension is activated!');
        // Modelled after completer-extension's notebooks plugin
        notebooks.widgetAdded.connect((sender, panel) => {
            var _a, _b;
            let editor = (_b = (_a = panel.content.activeCell) === null || _a === void 0 ? void 0 : _a.editor) !== null && _b !== void 0 ? _b : null;
            const session = panel.sessionContext.session;
            const sessionContext = panel.sessionContext;
            const options = { session, editor, sessionContext };
            const connector = new _connector__WEBPACK_IMPORTED_MODULE_4__.CompletionConnector([]);
            const handler = completionManager.register({
                connector,
                editor,
                parent: panel,
            });
            const updateConnector = () => {
                var _a, _b;
                editor = (_b = (_a = panel.content.activeCell) === null || _a === void 0 ? void 0 : _a.editor) !== null && _b !== void 0 ? _b : null;
                options.session = panel.sessionContext.session;
                options.sessionContext = panel.sessionContext;
                options.editor = editor;
                handler.editor = editor;
                const kernel = new _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.KernelConnector(options);
                const context = new _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.ContextConnector(options);
                const custom = new _customconnector__WEBPACK_IMPORTED_MODULE_5__.CustomConnector(options);
                handler.connector = new _connector__WEBPACK_IMPORTED_MODULE_4__.CompletionConnector([
                    kernel,
                    context,
                    custom
                ]);
            };
            // Update the handler whenever the prompt or session changes
            panel.content.activeCellChanged.connect(updateConnector);
            panel.sessionContext.sessionChanged.connect(updateConnector);
        });
        // Add notebook completer command.
        app.commands.addCommand(CommandIDs.invokeNotebook, {
            execute: () => {
                var _a;
                const panel = notebooks.currentWidget;
                if (panel && ((_a = panel.content.activeCell) === null || _a === void 0 ? void 0 : _a.model.type) === 'code') {
                    return app.commands.execute(CommandIDs.invoke, { id: panel.id });
                }
            },
        });
        // Add notebook completer select command.
        app.commands.addCommand(CommandIDs.selectNotebook, {
            execute: () => {
                const id = notebooks.currentWidget && notebooks.currentWidget.id;
                if (id) {
                    return app.commands.execute(CommandIDs.select, { id });
                }
            },
        });
        // Set enter key for notebook completer select command.
        app.commands.addKeyBinding({
            command: CommandIDs.selectNotebook,
            keys: ['Enter'],
            selector: '.jp-Notebook .jp-mod-completer-active',
        });
    },
};
// %%sql highlighting
class SqlCodeMirror {
    constructor(app, tracker, code_mirror) {
        var _a, _b;
        this.app = app;
        this.tracker = tracker;
        this.code_mirror = code_mirror;
        (_b = (_a = this.tracker) === null || _a === void 0 ? void 0 : _a.activeCellChanged) === null || _b === void 0 ? void 0 : _b.connect(() => {
            var _a;
            if (((_a = this.tracker) === null || _a === void 0 ? void 0 : _a.activeCell) !== null) {
                const cell = this.tracker.activeCell;
                if (cell !== null && (cell === null || cell === void 0 ? void 0 : cell.model.type) === 'code') {
                    const code_mirror_editor = cell === null || cell === void 0 ? void 0 : cell.editor;
                    const debounced_on_change = underscore__WEBPACK_IMPORTED_MODULE_3__.debounce(() => {
                        var _a;
                        // check for editor with first line starting with %%sql
                        const line = (_a = code_mirror_editor
                            .getLine(code_mirror_editor.firstLine())) === null || _a === void 0 ? void 0 : _a.trim();
                        if (line === null || line === void 0 ? void 0 : line.startsWith('%%sql')) {
                            code_mirror_editor.editor.setOption('mode', 'text/x-sql');
                        }
                        else {
                            code_mirror_editor.editor.setOption('mode', 'text/x-ipython');
                        }
                    }, 300);
                    code_mirror_editor.editor.on('change', debounced_on_change);
                    debounced_on_change();
                }
            }
        });
    }
}
function activate_syntax(app, tracker, code_mirror) {
    new SqlCodeMirror(app, tracker, code_mirror);
    console.log('SQLCodeMirror loaded.');
}
/**
 * Initialization data for the jupyterlabs_sql_codemirror extension.
 */
const extension_sql = {
    id: '@ploomber/sql-syntax-highlighting',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.INotebookTracker, _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.ICodeMirror],
    optional: [],
    activate: activate_syntax
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([extension, extension_sql]);


/***/ }),

/***/ "./lib/keywords.json":
/*!***************************!*\
  !*** ./lib/keywords.json ***!
  \***************************/
/***/ ((module) => {

module.exports = JSON.parse('{"keywords":[{"value":"ADD"},{"value":"ADD CONSTRAINT"},{"value":"ALL"},{"value":"ALTER"},{"value":"ALTER COLUMN"},{"value":"ALTER TABLE"},{"value":"AND"},{"value":"ANY"},{"value":"AS"},{"value":"ASC"},{"value":"BACKUP DATABASE"},{"value":"BETWEEN"},{"value":"CASE"},{"value":"CHECK"},{"value":"COLUMN"},{"value":"CONSTRAINT"},{"value":"CREATE"},{"value":"CREATE DATABASE"},{"value":"CREATE INDEX"},{"value":"CREATE OR REPLACE VIEW"},{"value":"CREATE TABLE"},{"value":"CREATE PROCEDURE"},{"value":"CREATE UNIQUE INDEX"},{"value":"CREATE VIEW"},{"value":"DATABASE"},{"value":"DEFAULT"},{"value":"DELETE"},{"value":"DESC"},{"value":"DISTINCT"},{"value":"DROP"},{"value":"DROP COLUMN"},{"value":"DROP CONSTRAINT"},{"value":"DROP DATABASE"},{"value":"DROP DEFAULT"},{"value":"DROP INDEX"},{"value":"DROP TABLE"},{"value":"DROP VIEW"},{"value":"EXEC"},{"value":"EXISTS"},{"value":"FOREIGN KEY"},{"value":"FROM"},{"value":"FULL OUTER JOIN"},{"value":"GROUP BY"},{"value":"HAVING"},{"value":"IN"},{"value":"INDEX"},{"value":"INNER JOIN"},{"value":"INSERT INTO"},{"value":"INSERT INTO SELECT"},{"value":"IS NULL"},{"value":"IS NOT NULL"},{"value":"JOIN"},{"value":"LEFT JOIN"},{"value":"LIKE"},{"value":"LIMIT"},{"value":"NOT"},{"value":"NOT NULL"},{"value":"OR"},{"value":"ORDER BY"},{"value":"OUTER JOIN"},{"value":"PRIMARY KEY"},{"value":"PROCEDURE"},{"value":"RIGHT JOIN"},{"value":"ROWNUM"},{"value":"SELECT"},{"value":"SELECT DISTINCT"},{"value":"SELECT INTO"},{"value":"SELECT TOP"},{"value":"SET"},{"value":"TABLE"},{"value":"TOP"},{"value":"TRUNCATE TABLE"},{"value":"UNION"},{"value":"UNION ALL"},{"value":"UNIQUE"},{"value":"UPDATE"},{"value":"VALUES"},{"value":"VIEW"},{"value":"WHERE"}]}');

/***/ })

}]);
//# sourceMappingURL=lib_index_js.6de74611b3c4c6ceb06b.js.map