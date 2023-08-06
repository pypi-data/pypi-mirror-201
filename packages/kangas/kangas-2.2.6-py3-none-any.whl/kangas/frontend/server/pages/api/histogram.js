"use strict";
(() => {
var exports = {};
exports.id = 72;
exports.ids = [72];
exports.modules = {

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

/***/ 553445:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _config__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(322798);

const handler = async (req, res)=>{
    const { endpoint , ...query } = req.query;
    const queryString = new URLSearchParams(query).toString();
    const result = await fetch(`${_config__WEBPACK_IMPORTED_MODULE_0__/* ["default"].apiUrl */ .Z.apiUrl}histogram?${queryString}`, {
        next: {
            revalidate: 100000
        }
    });
    const json = await result.json();
    res.setHeader("Cache-Control", "max-age=604800");
    res.send(json);
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (handler);


/***/ })

};
;

// load runtime
var __webpack_require__ = require("../../webpack-api-runtime.js");
__webpack_require__.C(exports);
var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
var __webpack_exports__ = (__webpack_exec__(553445));
module.exports = __webpack_exports__;

})();