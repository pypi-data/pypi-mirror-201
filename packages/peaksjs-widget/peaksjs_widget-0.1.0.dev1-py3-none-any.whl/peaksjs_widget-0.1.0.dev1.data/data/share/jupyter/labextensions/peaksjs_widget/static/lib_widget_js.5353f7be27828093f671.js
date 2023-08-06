(self["webpackChunkpeaksjs_widget"] = self["webpackChunkpeaksjs_widget"] || []).push([["lib_widget_js"],{

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

// Copyright (c) AntoineDaurat
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
//# sourceMappingURL=version.js.map

/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

// Copyright (c) AntoineDaurat
// Distributed under the terms of the Modified BSD License.
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.PeaksJSView = exports.PeaksJSModel = void 0;
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
// Import the CSS
__webpack_require__(/*! ../css/widget.css */ "./css/widget.css");
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const peaks_js_1 = __importDefault(__webpack_require__(/*! peaks.js */ "webpack/sharing/consume/default/peaks.js/peaks.js"));
const konva_1 = __importDefault(__webpack_require__(/*! konva */ "webpack/sharing/consume/default/konva/konva"));
class CustomSegmentMarker {
    constructor(options) {
        this._options = options;
    }
    init(group) {
        const handleWidth = 10;
        this.handleHeight = 20;
        const handleX = -(handleWidth / 2) + 0.5; // Place in the middle of the marker
        this._handle = new konva_1.default.Rect({
            x: handleX,
            y: 0,
            width: handleWidth,
            height: this.handleHeight,
            fill: this._options.color
        });
        this._line = new konva_1.default.Line({
            stroke: this._options.color,
            strokeWidth: 1
        });
        group.add(this._handle);
        group.add(this._line);
        this.fitToView();
    }
    fitToView() {
        const layer = this._options.layer;
        const height = layer.getHeight();
        this._handle.y(height / 2 - this.handleHeight / 2);
        this._line.points([0.5, 0, 0.5, height]);
    }
    timeUpdated() {
        // (optional, see below)
    }
    destroy() {
        // (optional, see below)
    }
}
function newSegmentMarker(options) {
    return new CustomSegmentMarker(options);
}
class PeaksJSModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: PeaksJSModel.model_name, _model_module: PeaksJSModel.model_module, _model_module_version: PeaksJSModel.model_module_version, _view_name: PeaksJSModel.view_name, _view_module: PeaksJSModel.view_module, _view_module_version: PeaksJSModel.view_module_version });
    }
}
exports.PeaksJSModel = PeaksJSModel;
PeaksJSModel.serializers = Object.assign({ zoomview: { deserialize: base_1.unpack_models }, overview: { deserialize: base_1.unpack_models }, play_button: { deserialize: base_1.unpack_models }, save_button: { deserialize: base_1.unpack_models }, audio: { deserialize: base_1.unpack_models } }, base_1.DOMWidgetModel.serializers);
PeaksJSModel.model_name = 'PeaksJSModel';
PeaksJSModel.model_module = version_1.MODULE_NAME;
PeaksJSModel.model_module_version = version_1.MODULE_VERSION;
PeaksJSModel.view_name = 'PeaksJSView'; // Set to null if no view
PeaksJSModel.view_module = version_1.MODULE_NAME; // Set to null if no view
PeaksJSModel.view_module_version = version_1.MODULE_VERSION;
class PeaksJSView extends base_1.DOMWidgetView {
    render() {
        super.render();
        this.model.on("change:zoomview", this.init_zoomview, this);
        this.model.on("change:overview", this.init_overview, this);
        this.model.on("change:play_button", this.init_play_button, this);
        this.model.on("change:save_button", this.init_save_button, this);
        this.model.on("change:audio", this.init_peaks, this);
        this.model.on("change:segments", this.segments_changed, this);
        this.model.on("change:points", this.points_changed, this);
        this.model.on("change:playing", this.toggle_playing, this);
        this.views = new base_1.ViewList(this.add_view, null, this);
        const _this = this;
        // this.listenTo(this.model, "change:zoomview", (model, value) => {
        //     _this.views.update([value,]);
        // });
        // this.listenTo(this.model, "change:overview", (model, value) => {
        //     _this.views.update([value,]);
        // });
        // this.listenTo(this.model, "change:play_button", (model, value) => {
        //     _this.views.update([value,]);
        // });
        // this.listenTo(this.model, "change:audio", (model, value) => {
        //     _this.views.update([value,]);
        // });
        this.listenTo(this.model, "change:segments", this.segments_changed);
        this.listenTo(this.model, "change:points", this.points_changed);
        this.displayed.then(() => {
            _this.init_zoomview();
            _this.init_overview();
            _this.init_play_button();
            _this.init_save_button();
            _this.init_peaks();
        });
        this.views.update([
            this.model.get("zoomview"),
            this.model.get("overview"),
            this.model.get("play_button"),
            this.model.get("save_button"),
            this.model.get("audio")
        ]).then(r => r.map(v => v.render()));
        const elementId = this.model.get("element_id");
        $(this.el).attr("id", elementId);
    }
    add_view(child_model, index) {
        return this.create_child_view(child_model, { parent: this })
            .then(view => {
            view.trigger("displayed");
            return view;
        })
            .catch(err => {
            return err;
        });
    }
    init_zoomview() {
        const that = this;
        const elementId = this.model.get("element_id");
        this.views.views[0].then(v => {
            that.zoomview = $(v.el)
                .text("\n")
                .attr("id", "zoomview-" + elementId)
                .attr("tabindex", "0")
                .css({ width: '100%', height: '200px', 'white-space': 'pre' });
            if (that.model.get("as_container"))
                $(that.el).append(that.zoomview);
        });
    }
    init_overview() {
        const that = this;
        const elementId = this.model.get("element_id");
        this.views.views[1].then(v => {
            that.overview = $(v.el)
                .text("\n")
                .attr("id", "overview-" + elementId)
                .css({ width: '100%', height: '15px', 'white-space': 'pre' });
            if (that.model.get("as_container"))
                $(that.el).append(that.overview);
        });
    }
    init_play_button() {
        const model = this.model;
        const that = this;
        this.views.views[2].then(v => {
            this.playBtn = $(v.el)
                .on("click", function () {
                const playing = model.get('playing');
                model.set('playing', !playing);
                model.save_changes();
                that.touch();
                that.send({ playing: !playing });
            });
            if (that.model.get("as_container"))
                $((this.el))
                    .append(this.playBtn);
        });
    }
    init_save_button() {
        const that = this;
        this.views.views[3].then(v => {
            $(that.el).append($(v.el).on("click", function () {
                const link = document.createElement('a');
                link.href = that.audio.src;
                link.setAttribute('download', `${that.model.get("element_id")}.mp3`); //or any other extension
                document.body.appendChild(link);
                link.click();
            }));
        });
    }
    init_peaks() {
        const that = this;
        const audioContext = new AudioContext();
        const segments = this.model.get("segments");
        const points = this.model.get("points");
        Promise.all(this.views.views).then(v => {
            const a = v[4];
            const audioElement = a.el;
            const zoomview = v[0].el;
            const overview = v[1].el;
            $(that.el).append(audioElement);
            that.audio = audioElement;
            // @ts-ignore
            const options = {
                zoomview: {
                    container: zoomview,
                    waveformColor: 'rgba(0,100,255,0.95)',
                    playheadColor: '#000000',
                    wheelMode: "scroll"
                },
                overview: {
                    container: overview,
                    waveformColor: 'rgba(0,100,255,0.95)',
                    playheadColor: '#000000',
                    showAxisLabels: false,
                    //                 highlightColor: "rgba(64,94,103,0.51)",
                    highlightOffset: 0,
                },
                zoomLevels: [16],
                mediaElement: audioElement,
                webAudio: {
                    audioContext: audioContext,
                    scale: 16,
                    multiChannel: false
                },
                // Bind keyboard controls
                keyboard: false,
                // Keyboard nudge increment in seconds (left arrow/right arrow)
                nudgeIncrement: 1.,
                segments: segments,
                points: points,
                // @ts-ignore
                createSegmentMarker: newSegmentMarker,
            };
            peaks_js_1.default.init(options, function (err, peaks) {
                if (err || peaks === undefined || peaks === null) {
                    console.error('Failed to initialize Peaks instance: ' + err.message);
                    return;
                }
                that.peaks = peaks;
                const peaksZoomView = peaks.views.getView('zoomview');
                peaksZoomView.setZoom({ seconds: Math.min(audioElement.duration, 180.) });
                /*
                * alt + click: add segment
                * alt + SHIFT + click: remove segment
                * Ctrl + alt + click: edit segment's label
                * Ctrl + click: add point
                * Ctrl + SHIFT + click: remove point
                * Ctrl + wheel: zoom
                * Ctr + dbl-click: reset zoom
                * SHIFT + wheel: scroll wvaveform
                * */
                peaks.on("zoomview.click", (event) => {
                    if (event.evt.altKey && !event.evt.shiftKey && !event.evt.ctrlKey) {
                        const newSegment = {
                            startTime: event.time,
                            endTime: event.time + .1,
                            editable: true,
                            id: that.model.get("id_count"),
                            color: "#ff640e",
                            labelText: ''
                        };
                        peaks.segments.add(newSegment);
                        that.model.set("id_count", newSegment.id + 1);
                        that.touch();
                        that.send({ newSegment: newSegment });
                    }
                    else if (event.evt.ctrlKey && !event.evt.altKey && !event.evt.shiftKey) {
                        const newPoint = {
                            time: event.time
                        };
                        peaks.points.add(newPoint);
                        that.send({ newPoint: newPoint });
                    }
                });
                peaks.on("segments.click", (event) => {
                    if (event.evt.altKey && event.evt.shiftKey) {
                        peaks.segments.removeById(event.segment.id);
                        that.send({
                            removeSegment: {
                                startTime: event.segment.startTime,
                                endTime: event.segment.endTime,
                                id: event.segment.id,
                                color: event.segment.color,
                                labelText: event.segment.labelText
                            }
                        });
                    }
                    else if (event.evt.ctrlKey && event.evt.altKey) {
                        const i = prompt("Enter cluster index", "0");
                        event.segment.update({ labelText: i });
                        that.send({
                            editSegment: {
                                startTime: event.segment.startTime,
                                endTime: event.segment.endTime,
                                id: event.segment.id,
                                color: event.segment.color,
                                labelText: i,
                                editable: true
                            }
                        });
                    }
                    else {
                        that.send({
                            clickSegment: {
                                startTime: event.segment.startTime,
                                endTime: event.segment.endTime,
                                id: event.segment.id,
                                color: event.segment.color,
                                labelText: event.segment.labelText,
                                editable: event.segment.editable
                            }
                        });
                    }
                });
                peaks.on("segments.dragend", (event) => {
                    that.send({
                        editSegment: {
                            startTime: event.segment.startTime,
                            endTime: event.segment.endTime,
                            id: event.segment.id,
                            color: event.segment.color,
                            labelText: event.segment.labelText,
                            editable: true
                        }
                    });
                });
                peaks.on("player.seeked", (event) => {
                });
                zoomview.addEventListener("keydown", (e) => {
                    if (e.code === 'Space') {
                        that.playBtn.trigger("click");
                        e.preventDefault();
                    }
                    else if (e.code.includes("Arrow")) {
                        const currentTime = peaks.player.getCurrentTime();
                        const zoomview = peaks.views.getView('zoomview');
                        // @ts-ignore
                        const scale = zoomview.getEndTime() - zoomview.getStartTime();
                        let factor = 1 / 500;
                        if (e.shiftKey) {
                            factor = 1 / 50;
                        }
                        if (e.code === "ArrowRight") {
                            peaks.player.seek(currentTime + (scale * factor));
                        }
                        else if (e.code === "ArrowLeft") {
                            peaks.player.seek(currentTime - (scale * factor));
                        }
                    }
                });
                zoomview.addEventListener("wheel", (event) => {
                    const zoomview = peaks.views.getView('zoomview');
                    if (!zoomview)
                        return;
                    if (event.ctrlKey) {
                        // @ts-ignore
                        const startTime = zoomview.getStartTime();
                        // @ts-ignore
                        const endTime = zoomview.getEndTime();
                        // @ts-ignore
                        const newDuration = (endTime - startTime) * (event.wheelDelta > 0 ? 1.1 : .9);
                        zoomview.setZoom({
                            seconds: Math.min(audioElement.duration, Math.max(newDuration, 0.356))
                        });
                        event.preventDefault();
                        that.send({
                            // @ts-ignore
                            updateZoomView: { startTime: zoomview.getStartTime(), endTime: zoomview.getEndTime() }
                        });
                    }
                });
                zoomview.addEventListener("dblclick", (event) => {
                    if (event.ctrlKey) {
                        peaks.views.getView('zoomview').setZoom({ seconds: peaks.player.getDuration() });
                    }
                    else if (!event.altKey) {
                        that.playBtn.trigger("click");
                    }
                });
            });
        });
    }
    segments_changed() {
        let segments = this.model.get("segments");
        this.peaks.segments.removeAll();
        this.peaks.segments.add(segments);
    }
    points_changed() {
        let points = this.model.get("points");
        this.peaks.points.removeAll();
        this.peaks.points.add(points);
    }
    toggle_playing() {
        const playing = this.model.get("playing");
        if (playing) {
            this.peaks.player.play();
            this.playBtn.children("i").removeClass("fa-play").addClass("fa-pause");
        }
        else {
            this.peaks.player.pause();
            this.playBtn.children("i").removeClass("fa-pause").addClass("fa-play");
        }
    }
}
exports.PeaksJSView = PeaksJSView;
//# sourceMappingURL=widget.js.map

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./css/widget.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/widget.css ***!
  \**************************************************************/
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, "\n", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/api.js":
/*!*****************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/api.js ***!
  \*****************************************************/
/***/ ((module) => {

"use strict";


/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
// css base code, injected by the css-loader
// eslint-disable-next-line func-names
module.exports = function (useSourceMap) {
  var list = []; // return the list of modules as css string

  list.toString = function toString() {
    return this.map(function (item) {
      var content = cssWithMappingToString(item, useSourceMap);

      if (item[2]) {
        return "@media ".concat(item[2], " {").concat(content, "}");
      }

      return content;
    }).join('');
  }; // import a list of modules into the list
  // eslint-disable-next-line func-names


  list.i = function (modules, mediaQuery, dedupe) {
    if (typeof modules === 'string') {
      // eslint-disable-next-line no-param-reassign
      modules = [[null, modules, '']];
    }

    var alreadyImportedModules = {};

    if (dedupe) {
      for (var i = 0; i < this.length; i++) {
        // eslint-disable-next-line prefer-destructuring
        var id = this[i][0];

        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }

    for (var _i = 0; _i < modules.length; _i++) {
      var item = [].concat(modules[_i]);

      if (dedupe && alreadyImportedModules[item[0]]) {
        // eslint-disable-next-line no-continue
        continue;
      }

      if (mediaQuery) {
        if (!item[2]) {
          item[2] = mediaQuery;
        } else {
          item[2] = "".concat(mediaQuery, " and ").concat(item[2]);
        }
      }

      list.push(item);
    }
  };

  return list;
};

function cssWithMappingToString(item, useSourceMap) {
  var content = item[1] || ''; // eslint-disable-next-line prefer-destructuring

  var cssMapping = item[3];

  if (!cssMapping) {
    return content;
  }

  if (useSourceMap && typeof btoa === 'function') {
    var sourceMapping = toComment(cssMapping);
    var sourceURLs = cssMapping.sources.map(function (source) {
      return "/*# sourceURL=".concat(cssMapping.sourceRoot || '').concat(source, " */");
    });
    return [content].concat(sourceURLs).concat([sourceMapping]).join('\n');
  }

  return [content].join('\n');
} // Adapted from convert-source-map (MIT)


function toComment(sourceMap) {
  // eslint-disable-next-line no-undef
  var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap))));
  var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
  return "/*# ".concat(data, " */");
}

/***/ }),

/***/ "./css/widget.css":
/*!************************!*\
  !*** ./css/widget.css ***!
  \************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/widget.css");

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.id, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);



module.exports = content.locals || {};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";


var isOldIE = function isOldIE() {
  var memo;
  return function memorize() {
    if (typeof memo === 'undefined') {
      // Test for IE <= 9 as proposed by Browserhacks
      // @see http://browserhacks.com/#hack-e71d8692f65334173fee715c222cb805
      // Tests for existence of standard globals is to allow style-loader
      // to operate correctly into non-standard environments
      // @see https://github.com/webpack-contrib/style-loader/issues/177
      memo = Boolean(window && document && document.all && !window.atob);
    }

    return memo;
  };
}();

var getTarget = function getTarget() {
  var memo = {};
  return function memorize(target) {
    if (typeof memo[target] === 'undefined') {
      var styleTarget = document.querySelector(target); // Special case to return head of iframe instead of iframe itself

      if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
        try {
          // This will throw an exception if access to iframe is blocked
          // due to cross-origin restrictions
          styleTarget = styleTarget.contentDocument.head;
        } catch (e) {
          // istanbul ignore next
          styleTarget = null;
        }
      }

      memo[target] = styleTarget;
    }

    return memo[target];
  };
}();

var stylesInDom = [];

function getIndexByIdentifier(identifier) {
  var result = -1;

  for (var i = 0; i < stylesInDom.length; i++) {
    if (stylesInDom[i].identifier === identifier) {
      result = i;
      break;
    }
  }

  return result;
}

function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];

  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var index = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3]
    };

    if (index !== -1) {
      stylesInDom[index].references++;
      stylesInDom[index].updater(obj);
    } else {
      stylesInDom.push({
        identifier: identifier,
        updater: addStyle(obj, options),
        references: 1
      });
    }

    identifiers.push(identifier);
  }

  return identifiers;
}

function insertStyleElement(options) {
  var style = document.createElement('style');
  var attributes = options.attributes || {};

  if (typeof attributes.nonce === 'undefined') {
    var nonce =  true ? __webpack_require__.nc : 0;

    if (nonce) {
      attributes.nonce = nonce;
    }
  }

  Object.keys(attributes).forEach(function (key) {
    style.setAttribute(key, attributes[key]);
  });

  if (typeof options.insert === 'function') {
    options.insert(style);
  } else {
    var target = getTarget(options.insert || 'head');

    if (!target) {
      throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
    }

    target.appendChild(style);
  }

  return style;
}

function removeStyleElement(style) {
  // istanbul ignore if
  if (style.parentNode === null) {
    return false;
  }

  style.parentNode.removeChild(style);
}
/* istanbul ignore next  */


var replaceText = function replaceText() {
  var textStore = [];
  return function replace(index, replacement) {
    textStore[index] = replacement;
    return textStore.filter(Boolean).join('\n');
  };
}();

function applyToSingletonTag(style, index, remove, obj) {
  var css = remove ? '' : obj.media ? "@media ".concat(obj.media, " {").concat(obj.css, "}") : obj.css; // For old IE

  /* istanbul ignore if  */

  if (style.styleSheet) {
    style.styleSheet.cssText = replaceText(index, css);
  } else {
    var cssNode = document.createTextNode(css);
    var childNodes = style.childNodes;

    if (childNodes[index]) {
      style.removeChild(childNodes[index]);
    }

    if (childNodes.length) {
      style.insertBefore(cssNode, childNodes[index]);
    } else {
      style.appendChild(cssNode);
    }
  }
}

function applyToTag(style, options, obj) {
  var css = obj.css;
  var media = obj.media;
  var sourceMap = obj.sourceMap;

  if (media) {
    style.setAttribute('media', media);
  } else {
    style.removeAttribute('media');
  }

  if (sourceMap && typeof btoa !== 'undefined') {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  } // For old IE

  /* istanbul ignore if  */


  if (style.styleSheet) {
    style.styleSheet.cssText = css;
  } else {
    while (style.firstChild) {
      style.removeChild(style.firstChild);
    }

    style.appendChild(document.createTextNode(css));
  }
}

var singleton = null;
var singletonCounter = 0;

function addStyle(obj, options) {
  var style;
  var update;
  var remove;

  if (options.singleton) {
    var styleIndex = singletonCounter++;
    style = singleton || (singleton = insertStyleElement(options));
    update = applyToSingletonTag.bind(null, style, styleIndex, false);
    remove = applyToSingletonTag.bind(null, style, styleIndex, true);
  } else {
    style = insertStyleElement(options);
    update = applyToTag.bind(null, style, options);

    remove = function remove() {
      removeStyleElement(style);
    };
  }

  update(obj);
  return function updateStyle(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap) {
        return;
      }

      update(obj = newObj);
    } else {
      remove();
    }
  };
}

module.exports = function (list, options) {
  options = options || {}; // Force single-tag solution on IE6-9, which has a hard limit on the # of <style>
  // tags it will allow on a page

  if (!options.singleton && typeof options.singleton !== 'boolean') {
    options.singleton = isOldIE();
  }

  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];

    if (Object.prototype.toString.call(newList) !== '[object Array]') {
      return;
    }

    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDom[index].references--;
    }

    var newLastIdentifiers = modulesToDom(newList, options);

    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];

      var _index = getIndexByIdentifier(_identifier);

      if (stylesInDom[_index].references === 0) {
        stylesInDom[_index].updater();

        stylesInDom.splice(_index, 1);
      }
    }

    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"peaksjs-widget","version":"0.1.0","description":"ipywidget to interact with audio waveforms through peaks.js","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/ktonal/peaksjs-widget","bugs":{"url":"https://github.com/ktonal/peaksjs-widget/issues"},"license":"BSD-3-Clause","author":{"name":"AntoineDaurat","email":"ktonalberlin@gmail.com"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/ktonal/peaksjs-widget"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf peaksjs_widget/labextension","clean:nbextension":"rimraf peaksjs_widget/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^6","@jupyter-widgets/controls":"^5","underscore":"^1.13.6","konva":"^8.3.10","peaks.js":"^2.0.2"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyter-widgets/base-manager":"^1.0.2","@jupyterlab/builder":"^3.0.0","@lumino/application":"^1.6.0","@lumino/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.61.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"peaksjs_widget/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js.5353f7be27828093f671.js.map