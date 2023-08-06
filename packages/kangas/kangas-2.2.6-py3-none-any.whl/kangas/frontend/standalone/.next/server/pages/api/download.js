"use strict";
(() => {
var exports = {};
exports.id = 51;
exports.ids = [51];
exports.modules = {

/***/ 12781:
/***/ ((module) => {

module.exports = require("stream");

/***/ }),

/***/ 322798:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {


// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "Z": () => (/* binding */ config)
});

;// CONCATENATED MODULE: external "process"
const external_process_namespaceObject = require("process");
;// CONCATENATED MODULE: ./config.js

const localConfig = {
    apiUrl: `${external_process_namespaceObject.env.KANGAS_BACKEND_PROTOCOL || "http"}://${external_process_namespaceObject.env.KANGAS_BACKEND_HOST}:${external_process_namespaceObject.env.KANGAS_BACKEND_PORT}/datagrid/`,
    rootUrl: `${external_process_namespaceObject.env.KANGAS_FRONTEND_PROTOCOL || "http"}://${external_process_namespaceObject.env.KANGAS_FRONTEND_HOST}:${external_process_namespaceObject.env.PORT}${external_process_namespaceObject.env.KANGAS_FRONTEND_ROOT || ""}/`,
    rootPath: `${external_process_namespaceObject.env.KANGAS_FRONTEND_ROOT || ""}/`,
    defaultDecimalPrecision: 5,
    locale: "en-US",
    hideSelector: external_process_namespaceObject.env.KANGAS_HIDE_SELECTOR === "1",
    cache: true,
    prefetch: false,
    debug: false
};
/* harmony default export */ const config = (localConfig);


/***/ }),

/***/ 514812:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var stream__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(12781);
/* harmony import */ var stream__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(stream__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _config__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(322798);


const handler = async (req, res)=>{
    const query = new URLSearchParams(req.query);
    const result = await fetch(`${_config__WEBPACK_IMPORTED_MODULE_1__/* ["default"].apiUrl */ .Z.apiUrl}download?dgid=${query?.get("dgid")}`, {
        next: {
            revalidate: 100000
        }
    });
    const datagrid = await result.body;
    const passthrough = new stream__WEBPACK_IMPORTED_MODULE_0__.Stream.PassThrough();
    stream__WEBPACK_IMPORTED_MODULE_0___default().pipeline(datagrid, passthrough, (err)=>err ? console.error(err) : null);
    res.setHeader("Cache-Control", "max-age=604800");
    passthrough.pipe(res);
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (handler);


/***/ })

};
;

// load runtime
var __webpack_require__ = require("../../webpack-api-runtime.js");
__webpack_require__.C(exports);
var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
var __webpack_exports__ = (__webpack_exec__(514812));
module.exports = __webpack_exports__;

})();