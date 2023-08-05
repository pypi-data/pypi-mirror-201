"use strict";
(self["webpackChunkipyniivue"] = self["webpackChunkipyniivue"] || []).push([["lib_widget_js"],{

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ ((__unused_webpack_module, exports) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.stringToArrayBuffer = exports.arrayBufferToString = exports.arrayBufferToBase64 = void 0;
//https://stackoverflow.com/a/9458996
function arrayBufferToBase64(buffer) {
    let binary = '';
    const bytes = new Uint8Array(buffer);
    const len = bytes.byteLength;
    for (let i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return btoa(binary);
}
exports.arrayBufferToBase64 = arrayBufferToBase64;
//https://developer.chrome.com/blog/how-to-convert-arraybuffer-to-and-from-string/
function arrayBufferToString(buffer) {
    const bytes = new Uint8Array(buffer);
    return String.fromCharCode.apply(null, [...bytes]);
}
exports.arrayBufferToString = arrayBufferToString;
function stringToArrayBuffer(str) {
    const buf = new ArrayBuffer(str.length);
    const bufView = new Uint8Array(buf);
    for (let i = 0, strLen = str.length; i < strLen; i++) {
        bufView[i] = str.charCodeAt(i);
    }
    return buf;
}
exports.stringToArrayBuffer = stringToArrayBuffer;


/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


// Copyright (c) Niivue
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


// Copyright (c) Niivue
// Distributed under the terms of the Modified BSD License.
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.NiivueView = exports.NiivueModel = void 0;
// Much of the structure and many of the functions/classes in this file
// are from https://github.com/martinRenou/ipycanvas. NiivueModel is based off of  CanvasModel and NiivueView is based off of CanvasView.
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
const niivue = __importStar(__webpack_require__(/*! @niivue/niivue */ "webpack/sharing/consume/default/@niivue/niivue/@niivue/niivue"));
const utils_1 = __webpack_require__(/*! ./utils */ "./lib/utils.js");
const setters = [
    'saveScene',
    'addVolumeFromUrl',
    'removeVolumeByUrl',
    'setCornerOrientationText',
    'setRadiologicalConvention',
    'setMeshThicknessOn2D',
    'setSliceMosaicString',
    'setSliceMM',
    'setHighResolutionCapable',
    'addVolume',
    'addMesh',
    'drawUndo',
    'loadDrawingFromUrl',
    'drawOtsu',
    'removeHaze',
    'saveImage',
    'setMeshProperty',
    'reverseFaces',
    'setMeshLayerProperty',
    'setPan2Dxyzmm',
    'setRenderAzimuthElevation',
    'setVolume',
    'removeVolume',
    'removeVolumeByIndex',
    'removeMesh',
    'removeMeshByUrl',
    'moveVolumeToBottom',
    'moveVolumeUp',
    'moveVolumeDown',
    'moveVolumeToTop',
    'setClipPlane',
    'setCrosshairColor',
    'setCrosshairWidth',
    'setDrawingEnabled',
    'setPenValue',
    'setDrawOpacity',
    'setSelectionBoxColor',
    'setSliceType',
    'setOpacity',
    'setScale',
    'setClipPlaneColor',
    'loadDocumentFromUrl',
    'loadVolumes',
    'addMeshFromUrl',
    'loadMeshes',
    'loadConnectome',
    'createEmptyDrawing',
    'drawGrowCut',
    'setMeshShader',
    'setCustomMeshShader',
    'updateGLVolume',
    'setColorMap',
    'setColorMapNegative',
    'setModulationImage',
    'setFrame4D',
    'setInterpolation',
    'moveCrosshairInVox',
    'drawMosaic',
];
class NiivueModel extends base_1.DOMWidgetModel {
    constructor() {
        super(...arguments);
        this.currentProcessing = Promise.resolve();
    }
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: NiivueModel.model_name, _model_module: NiivueModel.model_module, _model_module_version: NiivueModel.model_module_version, _view_name: NiivueModel.view_name, _view_module: NiivueModel.view_module, _view_module_version: NiivueModel.view_module_version });
    }
    initialize(attributes, options) {
        super.initialize(attributes, options);
        this.on('msg:custom', (command, buffers) => {
            this.currentProcessing = this.currentProcessing.then(async () => {
                await this.onCommand(command, buffers);
            });
        });
        this.createNV();
    }
    async callNVFunctionByName(functionName, argsList) {
        const isAsync = this.nv[functionName].constructor.name === 'AsyncFunction';
        // If the function is async, use `await`
        if (isAsync) {
            await this.nv[functionName](...argsList);
        }
        else {
            this.nv[functionName](...argsList);
        }
    }
    async onCommand(command, buffers) {
        const name = command[0];
        const args = command[1];
        try {
            await this.processCommand(name, args, buffers);
        }
        catch (e) {
            if (e instanceof Error) {
                if (e.name === 'TypeError' &&
                    e.message ===
                        "Cannot read properties of null (reading 'createTexture')") {
                    console.warn('Niivue widget not attached to a canvas. Display the widget to attach it to a canvas.');
                    return;
                }
                console.error(e);
            }
        }
    }
    async processCommand(name, args, buffers) {
        if (setters.includes(name)) {
            this.callNVFunctionByName(name, args);
        }
        switch (name) {
            case 'addVolumeFromBase64':
                this.nv.addVolume(niivue.NVImage.loadFromBase64({
                    name: args[0],
                    base64: utils_1.arrayBufferToBase64(buffers[0].buffer),
                }));
                break;
            case 'runCustomCode': {
                let result, hasResult = false;
                const code = utils_1.arrayBufferToString(buffers[0].buffer);
                try {
                    result = eval(code);
                    hasResult = true;
                }
                catch (e) {
                    if (e instanceof Error) {
                        console.error(e.stack);
                    }
                }
                this.sendCustomCodeResult(args[0], hasResult, result);
                break;
            }
        }
    }
    sendCustomCodeResult(id, hasResult, result) {
        let data = new ArrayBuffer(0);
        if (hasResult) {
            const str = result === undefined ? 'undefined' : JSON.stringify(result);
            data = utils_1.stringToArrayBuffer(str);
        }
        //chunk data into 5mb chunks
        const chunkSize = 5 * 1024 * 1024;
        const numChunks = Math.ceil(data.byteLength / chunkSize);
        for (let i = 0; i < numChunks; ++i) {
            const begin = i * chunkSize;
            const end = Math.min(begin + chunkSize, data.byteLength);
            const chunk = data.slice(begin, end);
            this.send({ event: ['customCodeResult', id, numChunks - 1 - i] }, {}, [
                chunk,
            ]);
        }
        if (numChunks === 0) {
            this.send({ event: ['customCodeResult', id, 0] }, {});
        }
    }
    async createNV() {
        this.nv = new niivue.Niivue({
            isResizeCanvas: false,
            logging: true,
            textHeight: this.get('text_height'),
            colorbarHeight: this.get('colorbar_height'),
            colorbarMargin: this.get('colorbar_margin'),
            crosshairWidth: this.get('crosshair_width'),
            rulerWidth: this.get('ruler_width'),
            backColor: this.get('back_color'),
            crosshairColor: this.get('crosshair_color'),
            fontColor: this.get('font_color'),
            selectionBoxColor: this.get('selection_box_color'),
            clipPlaneColor: this.get('clip_plane_color'),
            rulerColor: this.get('ruler_color'),
            show3Dcrosshair: this.get('show_3D_crosshair'),
            trustCalMinMax: this.get('trust_cal_min_max'),
            clipPlaneHotKey: this.get('clip_plane_hot_key'),
            viewModeHotKey: this.get('view_mode_hot_key'),
            keyDebounceTime: this.get('key_debounce_time'),
            doubleTouchTimeout: this.get('double_touch_timeout'),
            longTouchTimeout: this.get('long_touch_timeout'),
            isRadiologicalConvention: this.get('is_radiological_convention'),
            loadingText: this.get('loading_text'),
            dragAndDropEnabled: this.get('drag_and_drop_enabled'),
            isNearestInterpolation: this.get('is_nearest_interpolation'),
            isAtlasOutline: this.get('is_atlas_outline'),
            isRuler: this.get('is_ruler'),
            isColorbar: this.get('is_colorbar'),
            isOrientCube: this.get('is_orient_cube'),
            multiplanarPadPixels: this.get('multiplanar_pad_pixels'),
            multiplanarForceRender: this.get('multiplanar_force_render'),
            meshThicknessOn2D: this.get('mesh_thickness_on_2D') === 1.7976931348623157e308
                ? undefined
                : this.get('mesh_thickness_on_2D'),
            dragMode: this.get('drag_mode'),
            isDepthPickMesh: this.get('is_depth_pick_mesh'),
            isCornerOrientationText: this.get('is_corner_orientation_text'),
            sagittalNoseLeft: this.get('sagittal_nose_left'),
            isSliceMM: this.get('is_slice_MM'),
            isHighResolutionCapable: this.get('is_high_resolution_capable'),
            drawingEnabled: this.get('drawing_enabled'),
            penValue: this.get('pen_value') === 1.7976931348623157e308
                ? undefined
                : this.get('pen_value'),
            isFilledPen: this.get('is_filled_pen'),
            maxDrawUndoBitmaps: this.get('max_draw_undo_bitmaps'),
            thumbnail: this.get('thumbnail') || '',
        });
        console.log(this.nv.document);
    }
}
exports.NiivueModel = NiivueModel;
NiivueModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
NiivueModel.model_name = 'NiivueModel';
NiivueModel.model_module = version_1.MODULE_NAME;
NiivueModel.model_module_version = version_1.MODULE_VERSION;
NiivueModel.view_name = 'NiivueView'; // Set to null if no view
NiivueModel.view_module = version_1.MODULE_NAME; // Set to null if no view
NiivueModel.view_module_version = version_1.MODULE_VERSION;
class NiivueView extends base_1.DOMWidgetView {
    //for changing things / listening to callbacks
    render() {
        //reason for canvas creation being in here is 2-fold
        //1) NiivueVIEW
        //2) https://ipywidgets.readthedocs.io/en/7.7.0/examples/Widget%20Low%20Level.html#Models-and-Views
        //   "Multiple WidgetViews can be linked to a single WidgetModel. This is how you can redisplay the same Widget multiple times and it still works."
        this.canvas = document.createElement('canvas');
        this.canvas.classList.add('niivue-widget');
        this.resize();
        this.updateCanvas();
        //this.value_changed();
        this.model.on_some_change(['width', 'height'], this.resize, this);
        //this.model.on('change:value', this.value_changed, this);
    }
    resize() {
        //resize div
        this.el.setAttribute('width', this.model.get('width'));
        this.el.setAttribute('height', this.model.get('height'));
        this.el.setAttribute('style', `width: ${this.model.get('width')}px; height: ${this.model.get('height')}px;`);
        //resize canvas
        this.canvas.setAttribute('width', this.model.get('width'));
        this.canvas.setAttribute('height', this.model.get('height'));
        this.canvas.setAttribute('style', `width: ${this.model.get('width')}px; height: ${this.model.get('height')};`);
        //redraw
        this.model.nv.drawScene();
    }
    updateCanvas() {
        this.el.appendChild(this.canvas);
        this.model.nv.attachToCanvas(this.canvas);
        this.el.style.backgroundColor = 'transparent';
    }
}
exports.NiivueView = NiivueView;


/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

module.exports = JSON.parse('{"name":"ipyniivue","version":"1.0.0","description":"Jupyter-Niivue bridge","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/niivue/ipyniivue","bugs":{"url":"https://github.com/niivue/ipyniivue/issues"},"license":"BSD-3-Clause","author":{"name":"Niivue","email":"aandroulakis@zoho.com"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/niivue/ipyniivue"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf ipyniivue/labextension","clean:nbextension":"rimraf ipyniivue/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2 || ^3 || ^4 || ^5 || ^6","@niivue/niivue":"^0.33.1"},"devDependencies":{"@babel/core":"^7.21.4","@babel/preset-env":"^7.21.4","@babel/preset-typescript":"^7.21.4","@jupyter-widgets/base-manager":"^1.0.2","@jupyterlab/builder":"^3.0.0","@lumino/application":"^1.6.0","@lumino/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","babel-jest":"^29.5.0","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.6.3","mkdirp":"^0.5.1","npm-run-all":"^4.1.5","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.5.6","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.61.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"ipyniivue/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js.a94960b4534765a2f282.js.map