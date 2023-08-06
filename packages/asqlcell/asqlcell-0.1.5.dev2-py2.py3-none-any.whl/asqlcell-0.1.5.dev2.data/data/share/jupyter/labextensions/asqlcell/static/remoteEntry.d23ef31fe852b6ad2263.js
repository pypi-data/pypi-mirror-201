var _JUPYTERLAB;
/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "webpack/container/entry/asqlcell":
/*!***********************!*\
  !*** container entry ***!
  \***********************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

var moduleMap = {
	"./index": () => {
		return Promise.all([__webpack_require__.e("vendors-node_modules_css-loader_dist_runtime_api_js-node_modules_react-icons_fa_index_esm_js--88e3a8"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_react-dom"), __webpack_require__.e("lib_WidgetModel_js"), __webpack_require__.e("lib_index_js")]).then(() => (() => ((__webpack_require__(/*! ./lib/index.js */ "./lib/index.js")))));
	},
	"./extension": () => {
		return Promise.all([__webpack_require__.e("vendors-node_modules_css-loader_dist_runtime_api_js-node_modules_react-icons_fa_index_esm_js--88e3a8"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_react-dom"), __webpack_require__.e("lib_WidgetModel_js"), __webpack_require__.e("lib_plugin_js")]).then(() => (() => ((__webpack_require__(/*! ./lib/plugin */ "./lib/plugin.js")))));
	}
};
var get = (module, getScope) => {
	__webpack_require__.R = getScope;
	getScope = (
		__webpack_require__.o(moduleMap, module)
			? moduleMap[module]()
			: Promise.resolve().then(() => {
				throw new Error('Module "' + module + '" does not exist in container.');
			})
	);
	__webpack_require__.R = undefined;
	return getScope;
};
var init = (shareScope, initScope) => {
	if (!__webpack_require__.S) return;
	var name = "default"
	var oldScope = __webpack_require__.S[name];
	if(oldScope && oldScope !== shareScope) throw new Error("Container initialization failed as it has already been initialized with a different share scope");
	__webpack_require__.S[name] = shareScope;
	return __webpack_require__.I(name, initScope);
};

// This exports getters to disallow modifications
__webpack_require__.d(exports, {
	get: () => (get),
	init: () => (init)
});

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			id: moduleId,
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = __webpack_modules__;
/******/ 	
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = __webpack_module_cache__;
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	(() => {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = (module) => {
/******/ 			var getter = module && module.__esModule ?
/******/ 				() => (module['default']) :
/******/ 				() => (module);
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/ensure chunk */
/******/ 	(() => {
/******/ 		__webpack_require__.f = {};
/******/ 		// This file contains only the entry chunk.
/******/ 		// The chunk loading function for additional chunks
/******/ 		__webpack_require__.e = (chunkId) => {
/******/ 			return Promise.all(Object.keys(__webpack_require__.f).reduce((promises, key) => {
/******/ 				__webpack_require__.f[key](chunkId, promises);
/******/ 				return promises;
/******/ 			}, []));
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/get javascript chunk filename */
/******/ 	(() => {
/******/ 		// This function allow to reference async chunks
/******/ 		__webpack_require__.u = (chunkId) => {
/******/ 			// return url for filenames based on template
/******/ 			return "" + chunkId + "." + {"vendors-node_modules_css-loader_dist_runtime_api_js-node_modules_react-icons_fa_index_esm_js--88e3a8":"45f9fc5252980bfee5f1","webpack_sharing_consume_default_react":"5388768cc31e7d8be853","webpack_sharing_consume_default_react-dom":"881bb802596f79983f2e","lib_WidgetModel_js":"8d6f7768295488a648ba","lib_index_js":"cebaae03136818c0dd72","lib_plugin_js":"032d7c4fb06be9325ce9","vendors-node_modules_babel_runtime_helpers_esm_extends_js-node_modules_emotion_cache_dist_emo-075c3f":"8e4924b6b0e41a6b0b36","vendors-node_modules_emotion_react_dist_emotion-react_browser_esm_js":"a53488aa862aa97d3720","webpack_sharing_consume_default_emotion_serialize_emotion_serialize-webpack_sharing_consume_d-2bf41c":"b0c7ed5de7d3d0d7774b","vendors-node_modules_emotion_serialize_dist_emotion-serialize_browser_esm_js":"3c9d262ebe6c83de52ef","node_modules_emotion_memoize_dist_emotion-memoize_esm_js":"530def463350cb5f9a75","node_modules_emotion_utils_dist_emotion-utils_browser_esm_js":"1bc2f34572107dad5842","vendors-node_modules_mantine_core_esm_index_js":"eb3620999cc769e20e07","webpack_sharing_consume_default_emotion_react_emotion_react-webpack_sharing_consume_default_e-cc324f":"1a59f38d4c6f4706e5f8","vendors-node_modules_mantine_hooks_esm_index_js":"68b966eb8abfdfe4b44d","vendors-node_modules_prop-types_index_js":"89668eb60d7266a83f8a","vendors-node_modules_tabler_icons-react_dist_esm_tabler-icons-react_js":"c20def303a73fbe08185","vendors-node_modules_vega-util_build_vega-util_module_js":"d39adb152bc54e0419c1","vendors-node_modules_react-vega_esm_index_js":"a64ce3df4f0632f84f07","webpack_sharing_consume_default_vega-lite_vega-lite-webpack_sharing_consume_default_vega_vega":"bc0cc6e76635963a8380","vendors-node_modules_vega-event-selector_build_vega-event-selector_module_js-node_modules_veg-b76955":"0dd8a3518a841c430ecd","vendors-node_modules_vega-lite_build_src_index_js":"f8de247f932a22dacd12","webpack_sharing_consume_default_vega_vega":"16c2d919e78ecc437af6","node_modules_fast-deep-equal_index_js":"ee6a910718a1ec2a0460","vendors-node_modules_vega_build_vega_module_js":"ef93fdd1f9313cf04cb5"}[chunkId] + ".js";
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/global */
/******/ 	(() => {
/******/ 		__webpack_require__.g = (function() {
/******/ 			if (typeof globalThis === 'object') return globalThis;
/******/ 			try {
/******/ 				return this || new Function('return this')();
/******/ 			} catch (e) {
/******/ 				if (typeof window === 'object') return window;
/******/ 			}
/******/ 		})();
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/load script */
/******/ 	(() => {
/******/ 		var inProgress = {};
/******/ 		var dataWebpackPrefix = "asqlcell:";
/******/ 		// loadScript function to load a script via script tag
/******/ 		__webpack_require__.l = (url, done, key, chunkId) => {
/******/ 			if(inProgress[url]) { inProgress[url].push(done); return; }
/******/ 			var script, needAttach;
/******/ 			if(key !== undefined) {
/******/ 				var scripts = document.getElementsByTagName("script");
/******/ 				for(var i = 0; i < scripts.length; i++) {
/******/ 					var s = scripts[i];
/******/ 					if(s.getAttribute("src") == url || s.getAttribute("data-webpack") == dataWebpackPrefix + key) { script = s; break; }
/******/ 				}
/******/ 			}
/******/ 			if(!script) {
/******/ 				needAttach = true;
/******/ 				script = document.createElement('script');
/******/ 		
/******/ 				script.charset = 'utf-8';
/******/ 				script.timeout = 120;
/******/ 				if (__webpack_require__.nc) {
/******/ 					script.setAttribute("nonce", __webpack_require__.nc);
/******/ 				}
/******/ 				script.setAttribute("data-webpack", dataWebpackPrefix + key);
/******/ 				script.src = url;
/******/ 			}
/******/ 			inProgress[url] = [done];
/******/ 			var onScriptComplete = (prev, event) => {
/******/ 				// avoid mem leaks in IE.
/******/ 				script.onerror = script.onload = null;
/******/ 				clearTimeout(timeout);
/******/ 				var doneFns = inProgress[url];
/******/ 				delete inProgress[url];
/******/ 				script.parentNode && script.parentNode.removeChild(script);
/******/ 				doneFns && doneFns.forEach((fn) => (fn(event)));
/******/ 				if(prev) return prev(event);
/******/ 			};
/******/ 			var timeout = setTimeout(onScriptComplete.bind(null, undefined, { type: 'timeout', target: script }), 120000);
/******/ 			script.onerror = onScriptComplete.bind(null, script.onerror);
/******/ 			script.onload = onScriptComplete.bind(null, script.onload);
/******/ 			needAttach && document.head.appendChild(script);
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/sharing */
/******/ 	(() => {
/******/ 		__webpack_require__.S = {};
/******/ 		var initPromises = {};
/******/ 		var initTokens = {};
/******/ 		__webpack_require__.I = (name, initScope) => {
/******/ 			if(!initScope) initScope = [];
/******/ 			// handling circular init calls
/******/ 			var initToken = initTokens[name];
/******/ 			if(!initToken) initToken = initTokens[name] = {};
/******/ 			if(initScope.indexOf(initToken) >= 0) return;
/******/ 			initScope.push(initToken);
/******/ 			// only runs once
/******/ 			if(initPromises[name]) return initPromises[name];
/******/ 			// creates a new share scope if needed
/******/ 			if(!__webpack_require__.o(__webpack_require__.S, name)) __webpack_require__.S[name] = {};
/******/ 			// runs all init snippets from all modules reachable
/******/ 			var scope = __webpack_require__.S[name];
/******/ 			var warn = (msg) => (typeof console !== "undefined" && console.warn && console.warn(msg));
/******/ 			var uniqueName = "asqlcell";
/******/ 			var register = (name, version, factory, eager) => {
/******/ 				var versions = scope[name] = scope[name] || {};
/******/ 				var activeVersion = versions[version];
/******/ 				if(!activeVersion || (!activeVersion.loaded && (!eager != !activeVersion.eager ? eager : uniqueName > activeVersion.from))) versions[version] = { get: factory, from: uniqueName, eager: !!eager };
/******/ 			};
/******/ 			var initExternal = (id) => {
/******/ 				var handleError = (err) => (warn("Initialization of sharing external failed: " + err));
/******/ 				try {
/******/ 					var module = __webpack_require__(id);
/******/ 					if(!module) return;
/******/ 					var initFn = (module) => (module && module.init && module.init(__webpack_require__.S[name], initScope))
/******/ 					if(module.then) return promises.push(module.then(initFn, handleError));
/******/ 					var initResult = initFn(module);
/******/ 					if(initResult && initResult.then) return promises.push(initResult['catch'](handleError));
/******/ 				} catch(err) { handleError(err); }
/******/ 			}
/******/ 			var promises = [];
/******/ 			switch(name) {
/******/ 				case "default": {
/******/ 					register("@emotion/react", "11.10.5", () => (Promise.all([__webpack_require__.e("vendors-node_modules_babel_runtime_helpers_esm_extends_js-node_modules_emotion_cache_dist_emo-075c3f"), __webpack_require__.e("vendors-node_modules_emotion_react_dist_emotion-react_browser_esm_js"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_emotion_serialize_emotion_serialize-webpack_sharing_consume_d-2bf41c")]).then(() => (() => (__webpack_require__(/*! ./node_modules/@emotion/react/dist/emotion-react.browser.esm.js */ "./node_modules/@emotion/react/dist/emotion-react.browser.esm.js"))))));
/******/ 					register("@emotion/serialize", "1.1.1", () => (Promise.all([__webpack_require__.e("vendors-node_modules_emotion_serialize_dist_emotion-serialize_browser_esm_js"), __webpack_require__.e("node_modules_emotion_memoize_dist_emotion-memoize_esm_js")]).then(() => (() => (__webpack_require__(/*! ./node_modules/@emotion/serialize/dist/emotion-serialize.browser.esm.js */ "./node_modules/@emotion/serialize/dist/emotion-serialize.browser.esm.js"))))));
/******/ 					register("@emotion/utils", "1.2.0", () => (__webpack_require__.e("node_modules_emotion_utils_dist_emotion-utils_browser_esm_js").then(() => (() => (__webpack_require__(/*! ./node_modules/@emotion/utils/dist/emotion-utils.browser.esm.js */ "./node_modules/@emotion/utils/dist/emotion-utils.browser.esm.js"))))));
/******/ 					register("@mantine/core", "5.10.0", () => (Promise.all([__webpack_require__.e("vendors-node_modules_babel_runtime_helpers_esm_extends_js-node_modules_emotion_cache_dist_emo-075c3f"), __webpack_require__.e("vendors-node_modules_mantine_core_esm_index_js"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_react-dom"), __webpack_require__.e("webpack_sharing_consume_default_emotion_react_emotion_react-webpack_sharing_consume_default_e-cc324f")]).then(() => (() => (__webpack_require__(/*! ./node_modules/@mantine/core/esm/index.js */ "./node_modules/@mantine/core/esm/index.js"))))));
/******/ 					register("@mantine/hooks", "5.10.0", () => (Promise.all([__webpack_require__.e("vendors-node_modules_mantine_hooks_esm_index_js"), __webpack_require__.e("webpack_sharing_consume_default_react")]).then(() => (() => (__webpack_require__(/*! ./node_modules/@mantine/hooks/esm/index.js */ "./node_modules/@mantine/hooks/esm/index.js"))))));
/******/ 					register("@tabler/icons-react", "2.14.0", () => (Promise.all([__webpack_require__.e("vendors-node_modules_prop-types_index_js"), __webpack_require__.e("vendors-node_modules_tabler_icons-react_dist_esm_tabler-icons-react_js"), __webpack_require__.e("webpack_sharing_consume_default_react")]).then(() => (() => (__webpack_require__(/*! ./node_modules/@tabler/icons-react/dist/esm/tabler-icons-react.js */ "./node_modules/@tabler/icons-react/dist/esm/tabler-icons-react.js"))))));
/******/ 					register("asqlcell", "0.1.0", () => (Promise.all([__webpack_require__.e("vendors-node_modules_css-loader_dist_runtime_api_js-node_modules_react-icons_fa_index_esm_js--88e3a8"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_react-dom"), __webpack_require__.e("lib_WidgetModel_js"), __webpack_require__.e("lib_index_js")]).then(() => (() => (__webpack_require__(/*! ./lib/index.js */ "./lib/index.js"))))));
/******/ 					register("react-vega", "7.6.0", () => (Promise.all([__webpack_require__.e("vendors-node_modules_prop-types_index_js"), __webpack_require__.e("vendors-node_modules_vega-util_build_vega-util_module_js"), __webpack_require__.e("vendors-node_modules_react-vega_esm_index_js"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_vega-lite_vega-lite-webpack_sharing_consume_default_vega_vega")]).then(() => (() => (__webpack_require__(/*! ./node_modules/react-vega/esm/index.js */ "./node_modules/react-vega/esm/index.js"))))));
/******/ 					register("vega-lite", "5.5.0", () => (Promise.all([__webpack_require__.e("vendors-node_modules_vega-event-selector_build_vega-event-selector_module_js-node_modules_veg-b76955"), __webpack_require__.e("vendors-node_modules_vega-util_build_vega-util_module_js"), __webpack_require__.e("vendors-node_modules_vega-lite_build_src_index_js"), __webpack_require__.e("webpack_sharing_consume_default_vega_vega"), __webpack_require__.e("node_modules_fast-deep-equal_index_js")]).then(() => (() => (__webpack_require__(/*! ./node_modules/vega-lite/build/src/index.js */ "./node_modules/vega-lite/build/src/index.js"))))));
/******/ 					register("vega", "5.22.1", () => (Promise.all([__webpack_require__.e("vendors-node_modules_vega-event-selector_build_vega-event-selector_module_js-node_modules_veg-b76955"), __webpack_require__.e("vendors-node_modules_vega-util_build_vega-util_module_js"), __webpack_require__.e("vendors-node_modules_vega_build_vega_module_js")]).then(() => (() => (__webpack_require__(/*! ./node_modules/vega/build/vega.module.js */ "./node_modules/vega/build/vega.module.js"))))));
/******/ 				}
/******/ 				break;
/******/ 			}
/******/ 			if(!promises.length) return initPromises[name] = 1;
/******/ 			return initPromises[name] = Promise.all(promises).then(() => (initPromises[name] = 1));
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/publicPath */
/******/ 	(() => {
/******/ 		var scriptUrl;
/******/ 		if (__webpack_require__.g.importScripts) scriptUrl = __webpack_require__.g.location + "";
/******/ 		var document = __webpack_require__.g.document;
/******/ 		if (!scriptUrl && document) {
/******/ 			if (document.currentScript)
/******/ 				scriptUrl = document.currentScript.src
/******/ 			if (!scriptUrl) {
/******/ 				var scripts = document.getElementsByTagName("script");
/******/ 				if(scripts.length) scriptUrl = scripts[scripts.length - 1].src
/******/ 			}
/******/ 		}
/******/ 		// When supporting browsers where an automatic publicPath is not supported you must specify an output.publicPath manually via configuration
/******/ 		// or pass an empty string ("") and set the __webpack_public_path__ variable from your code to use your own logic.
/******/ 		if (!scriptUrl) throw new Error("Automatic publicPath is not supported in this browser");
/******/ 		scriptUrl = scriptUrl.replace(/#.*$/, "").replace(/\?.*$/, "").replace(/\/[^\/]+$/, "/");
/******/ 		__webpack_require__.p = scriptUrl;
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/consumes */
/******/ 	(() => {
/******/ 		var parseVersion = (str) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			var p=p=>{return p.split(".").map((p=>{return+p==p?+p:p}))},n=/^([^-+]+)?(?:-([^+]+))?(?:\+(.+))?$/.exec(str),r=n[1]?p(n[1]):[];return n[2]&&(r.length++,r.push.apply(r,p(n[2]))),n[3]&&(r.push([]),r.push.apply(r,p(n[3]))),r;
/******/ 		}
/******/ 		var versionLt = (a, b) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			a=parseVersion(a),b=parseVersion(b);for(var r=0;;){if(r>=a.length)return r<b.length&&"u"!=(typeof b[r])[0];var e=a[r],n=(typeof e)[0];if(r>=b.length)return"u"==n;var t=b[r],f=(typeof t)[0];if(n!=f)return"o"==n&&"n"==f||("s"==f||"u"==n);if("o"!=n&&"u"!=n&&e!=t)return e<t;r++}
/******/ 		}
/******/ 		var rangeToString = (range) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			var r=range[0],n="";if(1===range.length)return"*";if(r+.5){n+=0==r?">=":-1==r?"<":1==r?"^":2==r?"~":r>0?"=":"!=";for(var e=1,a=1;a<range.length;a++){e--,n+="u"==(typeof(t=range[a]))[0]?"-":(e>0?".":"")+(e=2,t)}return n}var g=[];for(a=1;a<range.length;a++){var t=range[a];g.push(0===t?"not("+o()+")":1===t?"("+o()+" || "+o()+")":2===t?g.pop()+" "+g.pop():rangeToString(t))}return o();function o(){return g.pop().replace(/^\((.+)\)$/,"$1")}
/******/ 		}
/******/ 		var satisfy = (range, version) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			if(0 in range){version=parseVersion(version);var e=range[0],r=e<0;r&&(e=-e-1);for(var n=0,i=1,a=!0;;i++,n++){var f,s,g=i<range.length?(typeof range[i])[0]:"";if(n>=version.length||"o"==(s=(typeof(f=version[n]))[0]))return!a||("u"==g?i>e&&!r:""==g!=r);if("u"==s){if(!a||"u"!=g)return!1}else if(a)if(g==s)if(i<=e){if(f!=range[i])return!1}else{if(r?f>range[i]:f<range[i])return!1;f!=range[i]&&(a=!1)}else if("s"!=g&&"n"!=g){if(r||i<=e)return!1;a=!1,i--}else{if(i<=e||s<g!=r)return!1;a=!1}else"s"!=g&&"n"!=g&&(a=!1,i--)}}var t=[],o=t.pop.bind(t);for(n=1;n<range.length;n++){var u=range[n];t.push(1==u?o()|o():2==u?o()&o():u?satisfy(u,version):!o())}return!!o();
/******/ 		}
/******/ 		var ensureExistence = (scopeName, key) => {
/******/ 			var scope = __webpack_require__.S[scopeName];
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) throw new Error("Shared module " + key + " doesn't exist in shared scope " + scopeName);
/******/ 			return scope;
/******/ 		};
/******/ 		var findVersion = (scope, key) => {
/******/ 			var versions = scope[key];
/******/ 			var key = Object.keys(versions).reduce((a, b) => {
/******/ 				return !a || versionLt(a, b) ? b : a;
/******/ 			}, 0);
/******/ 			return key && versions[key]
/******/ 		};
/******/ 		var findSingletonVersionKey = (scope, key) => {
/******/ 			var versions = scope[key];
/******/ 			return Object.keys(versions).reduce((a, b) => {
/******/ 				return !a || (!versions[a].loaded && versionLt(a, b)) ? b : a;
/******/ 			}, 0);
/******/ 		};
/******/ 		var getInvalidSingletonVersionMessage = (scope, key, version, requiredVersion) => {
/******/ 			return "Unsatisfied version " + version + " from " + (version && scope[key][version].from) + " of shared singleton module " + key + " (required " + rangeToString(requiredVersion) + ")"
/******/ 		};
/******/ 		var getSingleton = (scope, scopeName, key, requiredVersion) => {
/******/ 			var version = findSingletonVersionKey(scope, key);
/******/ 			return get(scope[key][version]);
/******/ 		};
/******/ 		var getSingletonVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			var version = findSingletonVersionKey(scope, key);
/******/ 			if (!satisfy(requiredVersion, version)) typeof console !== "undefined" && console.warn && console.warn(getInvalidSingletonVersionMessage(scope, key, version, requiredVersion));
/******/ 			return get(scope[key][version]);
/******/ 		};
/******/ 		var getStrictSingletonVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			var version = findSingletonVersionKey(scope, key);
/******/ 			if (!satisfy(requiredVersion, version)) throw new Error(getInvalidSingletonVersionMessage(scope, key, version, requiredVersion));
/******/ 			return get(scope[key][version]);
/******/ 		};
/******/ 		var findValidVersion = (scope, key, requiredVersion) => {
/******/ 			var versions = scope[key];
/******/ 			var key = Object.keys(versions).reduce((a, b) => {
/******/ 				if (!satisfy(requiredVersion, b)) return a;
/******/ 				return !a || versionLt(a, b) ? b : a;
/******/ 			}, 0);
/******/ 			return key && versions[key]
/******/ 		};
/******/ 		var getInvalidVersionMessage = (scope, scopeName, key, requiredVersion) => {
/******/ 			var versions = scope[key];
/******/ 			return "No satisfying version (" + rangeToString(requiredVersion) + ") of shared module " + key + " found in shared scope " + scopeName + ".\n" +
/******/ 				"Available versions: " + Object.keys(versions).map((key) => {
/******/ 				return key + " from " + versions[key].from;
/******/ 			}).join(", ");
/******/ 		};
/******/ 		var getValidVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			var entry = findValidVersion(scope, key, requiredVersion);
/******/ 			if(entry) return get(entry);
/******/ 			throw new Error(getInvalidVersionMessage(scope, scopeName, key, requiredVersion));
/******/ 		};
/******/ 		var warnInvalidVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			typeof console !== "undefined" && console.warn && console.warn(getInvalidVersionMessage(scope, scopeName, key, requiredVersion));
/******/ 		};
/******/ 		var get = (entry) => {
/******/ 			entry.loaded = 1;
/******/ 			return entry.get()
/******/ 		};
/******/ 		var init = (fn) => (function(scopeName, a, b, c) {
/******/ 			var promise = __webpack_require__.I(scopeName);
/******/ 			if (promise && promise.then) return promise.then(fn.bind(fn, scopeName, __webpack_require__.S[scopeName], a, b, c));
/******/ 			return fn(scopeName, __webpack_require__.S[scopeName], a, b, c);
/******/ 		});
/******/ 		
/******/ 		var load = /*#__PURE__*/ init((scopeName, scope, key) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return get(findVersion(scope, key));
/******/ 		});
/******/ 		var loadFallback = /*#__PURE__*/ init((scopeName, scope, key, fallback) => {
/******/ 			return scope && __webpack_require__.o(scope, key) ? get(findVersion(scope, key)) : fallback();
/******/ 		});
/******/ 		var loadVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return get(findValidVersion(scope, key, version) || warnInvalidVersion(scope, scopeName, key, version) || findVersion(scope, key));
/******/ 		});
/******/ 		var loadSingleton = /*#__PURE__*/ init((scopeName, scope, key) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getSingleton(scope, scopeName, key);
/******/ 		});
/******/ 		var loadSingletonVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadStrictVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getValidVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadStrictSingletonVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getStrictSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return get(findValidVersion(scope, key, version) || warnInvalidVersion(scope, scopeName, key, version) || findVersion(scope, key));
/******/ 		});
/******/ 		var loadSingletonFallback = /*#__PURE__*/ init((scopeName, scope, key, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return getSingleton(scope, scopeName, key);
/******/ 		});
/******/ 		var loadSingletonVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return getSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadStrictVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			var entry = scope && __webpack_require__.o(scope, key) && findValidVersion(scope, key, version);
/******/ 			return entry ? get(entry) : fallback();
/******/ 		});
/******/ 		var loadStrictSingletonVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return getStrictSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var installedModules = {};
/******/ 		var moduleToHandlerMapping = {
/******/ 			"webpack/sharing/consume/default/react": () => (loadSingletonVersionCheck("default", "react", [1,17,0,1])),
/******/ 			"webpack/sharing/consume/default/react-dom": () => (loadSingletonVersionCheck("default", "react-dom", [1,17,0,1])),
/******/ 			"webpack/sharing/consume/default/@jupyter-widgets/base": () => (loadSingletonVersionCheck("default", "@jupyter-widgets/base", [,[1,4,0,0],[1,3,0,0],[1,2,0,0],[1,1,1,10],1,1,1])),
/******/ 			"webpack/sharing/consume/default/@mantine/core/@mantine/core": () => (loadStrictVersionCheckFallback("default", "@mantine/core", [1,5,10,0], () => (Promise.all([__webpack_require__.e("vendors-node_modules_babel_runtime_helpers_esm_extends_js-node_modules_emotion_cache_dist_emo-075c3f"), __webpack_require__.e("vendors-node_modules_mantine_core_esm_index_js"), __webpack_require__.e("webpack_sharing_consume_default_emotion_react_emotion_react-webpack_sharing_consume_default_e-cc324f")]).then(() => (() => (__webpack_require__(/*! @mantine/core */ "./node_modules/@mantine/core/esm/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@mantine/hooks/@mantine/hooks?07de": () => (loadStrictVersionCheckFallback("default", "@mantine/hooks", [1,5,10,0], () => (__webpack_require__.e("vendors-node_modules_mantine_hooks_esm_index_js").then(() => (() => (__webpack_require__(/*! @mantine/hooks */ "./node_modules/@mantine/hooks/esm/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@tabler/icons-react/@tabler/icons-react": () => (loadStrictVersionCheckFallback("default", "@tabler/icons-react", [1,2,14,0], () => (Promise.all([__webpack_require__.e("vendors-node_modules_prop-types_index_js"), __webpack_require__.e("vendors-node_modules_tabler_icons-react_dist_esm_tabler-icons-react_js")]).then(() => (() => (__webpack_require__(/*! @tabler/icons-react */ "./node_modules/@tabler/icons-react/dist/esm/tabler-icons-react.js"))))))),
/******/ 			"webpack/sharing/consume/default/react-vega/react-vega": () => (loadStrictVersionCheckFallback("default", "react-vega", [1,7,6,0], () => (Promise.all([__webpack_require__.e("vendors-node_modules_prop-types_index_js"), __webpack_require__.e("vendors-node_modules_vega-util_build_vega-util_module_js"), __webpack_require__.e("vendors-node_modules_react-vega_esm_index_js"), __webpack_require__.e("webpack_sharing_consume_default_vega-lite_vega-lite-webpack_sharing_consume_default_vega_vega")]).then(() => (() => (__webpack_require__(/*! react-vega */ "./node_modules/react-vega/esm/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@emotion/utils/@emotion/utils?b902": () => (loadStrictVersionCheckFallback("default", "@emotion/utils", [1,1,2,0], () => (__webpack_require__.e("node_modules_emotion_utils_dist_emotion-utils_browser_esm_js").then(() => (() => (__webpack_require__(/*! @emotion/utils */ "./node_modules/@emotion/utils/dist/emotion-utils.browser.esm.js"))))))),
/******/ 			"webpack/sharing/consume/default/@emotion/serialize/@emotion/serialize?d98d": () => (loadStrictVersionCheckFallback("default", "@emotion/serialize", [1,1,1,1], () => (__webpack_require__.e("vendors-node_modules_emotion_serialize_dist_emotion-serialize_browser_esm_js").then(() => (() => (__webpack_require__(/*! @emotion/serialize */ "./node_modules/@emotion/serialize/dist/emotion-serialize.browser.esm.js"))))))),
/******/ 			"webpack/sharing/consume/default/@emotion/react/@emotion/react": () => (loadStrictVersionCheckFallback("default", "@emotion/react", [0,11,9,0], () => (Promise.all([__webpack_require__.e("vendors-node_modules_emotion_react_dist_emotion-react_browser_esm_js"), __webpack_require__.e("webpack_sharing_consume_default_emotion_serialize_emotion_serialize-webpack_sharing_consume_d-2bf41c")]).then(() => (() => (__webpack_require__(/*! @emotion/react */ "./node_modules/@emotion/react/dist/emotion-react.browser.esm.js"))))))),
/******/ 			"webpack/sharing/consume/default/@emotion/serialize/@emotion/serialize?bf19": () => (loadFallback("default", "@emotion/serialize", () => (__webpack_require__.e("vendors-node_modules_emotion_serialize_dist_emotion-serialize_browser_esm_js").then(() => (() => (__webpack_require__(/*! @emotion/serialize */ "./node_modules/@emotion/serialize/dist/emotion-serialize.browser.esm.js"))))))),
/******/ 			"webpack/sharing/consume/default/@emotion/utils/@emotion/utils?0e78": () => (loadFallback("default", "@emotion/utils", () => (__webpack_require__.e("node_modules_emotion_utils_dist_emotion-utils_browser_esm_js").then(() => (() => (__webpack_require__(/*! @emotion/utils */ "./node_modules/@emotion/utils/dist/emotion-utils.browser.esm.js"))))))),
/******/ 			"webpack/sharing/consume/default/@mantine/hooks/@mantine/hooks?89f7": () => (loadStrictVersionCheckFallback("default", "@mantine/hooks", [4,5,10,0], () => (__webpack_require__.e("vendors-node_modules_mantine_hooks_esm_index_js").then(() => (() => (__webpack_require__(/*! @mantine/hooks */ "./node_modules/@mantine/hooks/esm/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/vega/vega?aaa9": () => (loadStrictVersionCheckFallback("default", "vega", [1,5,21,0], () => (Promise.all([__webpack_require__.e("vendors-node_modules_vega-event-selector_build_vega-event-selector_module_js-node_modules_veg-b76955"), __webpack_require__.e("vendors-node_modules_vega_build_vega_module_js")]).then(() => (() => (__webpack_require__(/*! vega */ "./node_modules/vega/build/vega.module.js"))))))),
/******/ 			"webpack/sharing/consume/default/vega-lite/vega-lite": () => (loadStrictVersionCheckFallback("default", "vega-lite", [0], () => (Promise.all([__webpack_require__.e("vendors-node_modules_vega-event-selector_build_vega-event-selector_module_js-node_modules_veg-b76955"), __webpack_require__.e("vendors-node_modules_vega-lite_build_src_index_js"), __webpack_require__.e("webpack_sharing_consume_default_vega_vega")]).then(() => (() => (__webpack_require__(/*! vega-lite */ "./node_modules/vega-lite/build/src/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/vega/vega?c4e2": () => (loadStrictVersionCheckFallback("default", "vega", [1,5,22,0], () => (__webpack_require__.e("vendors-node_modules_vega_build_vega_module_js").then(() => (() => (__webpack_require__(/*! vega */ "./node_modules/vega/build/vega.module.js")))))))
/******/ 		};
/******/ 		// no consumes in initial chunks
/******/ 		var chunkMapping = {
/******/ 			"webpack_sharing_consume_default_react": [
/******/ 				"webpack/sharing/consume/default/react"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_react-dom": [
/******/ 				"webpack/sharing/consume/default/react-dom"
/******/ 			],
/******/ 			"lib_WidgetModel_js": [
/******/ 				"webpack/sharing/consume/default/@jupyter-widgets/base",
/******/ 				"webpack/sharing/consume/default/@mantine/core/@mantine/core",
/******/ 				"webpack/sharing/consume/default/@mantine/hooks/@mantine/hooks?07de",
/******/ 				"webpack/sharing/consume/default/@tabler/icons-react/@tabler/icons-react",
/******/ 				"webpack/sharing/consume/default/react-vega/react-vega"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_emotion_serialize_emotion_serialize-webpack_sharing_consume_d-2bf41c": [
/******/ 				"webpack/sharing/consume/default/@emotion/utils/@emotion/utils?b902",
/******/ 				"webpack/sharing/consume/default/@emotion/serialize/@emotion/serialize?d98d"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_emotion_react_emotion_react-webpack_sharing_consume_default_e-cc324f": [
/******/ 				"webpack/sharing/consume/default/@emotion/react/@emotion/react",
/******/ 				"webpack/sharing/consume/default/@emotion/serialize/@emotion/serialize?bf19",
/******/ 				"webpack/sharing/consume/default/@emotion/utils/@emotion/utils?0e78",
/******/ 				"webpack/sharing/consume/default/@mantine/hooks/@mantine/hooks?89f7"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_vega-lite_vega-lite-webpack_sharing_consume_default_vega_vega": [
/******/ 				"webpack/sharing/consume/default/vega/vega?aaa9",
/******/ 				"webpack/sharing/consume/default/vega-lite/vega-lite"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_vega_vega": [
/******/ 				"webpack/sharing/consume/default/vega/vega?c4e2"
/******/ 			]
/******/ 		};
/******/ 		__webpack_require__.f.consumes = (chunkId, promises) => {
/******/ 			if(__webpack_require__.o(chunkMapping, chunkId)) {
/******/ 				chunkMapping[chunkId].forEach((id) => {
/******/ 					if(__webpack_require__.o(installedModules, id)) return promises.push(installedModules[id]);
/******/ 					var onFactory = (factory) => {
/******/ 						installedModules[id] = 0;
/******/ 						__webpack_require__.m[id] = (module) => {
/******/ 							delete __webpack_require__.c[id];
/******/ 							module.exports = factory();
/******/ 						}
/******/ 					};
/******/ 					var onError = (error) => {
/******/ 						delete installedModules[id];
/******/ 						__webpack_require__.m[id] = (module) => {
/******/ 							delete __webpack_require__.c[id];
/******/ 							throw error;
/******/ 						}
/******/ 					};
/******/ 					try {
/******/ 						var promise = moduleToHandlerMapping[id]();
/******/ 						if(promise.then) {
/******/ 							promises.push(installedModules[id] = promise.then(onFactory)['catch'](onError));
/******/ 						} else onFactory(promise);
/******/ 					} catch(e) { onError(e); }
/******/ 				});
/******/ 			}
/******/ 		}
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/jsonp chunk loading */
/******/ 	(() => {
/******/ 		// no baseURI
/******/ 		
/******/ 		// object to store loaded and loading chunks
/******/ 		// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 		// [resolve, reject, Promise] = chunk loading, 0 = chunk loaded
/******/ 		var installedChunks = {
/******/ 			"asqlcell": 0
/******/ 		};
/******/ 		
/******/ 		__webpack_require__.f.j = (chunkId, promises) => {
/******/ 				// JSONP chunk loading for javascript
/******/ 				var installedChunkData = __webpack_require__.o(installedChunks, chunkId) ? installedChunks[chunkId] : undefined;
/******/ 				if(installedChunkData !== 0) { // 0 means "already installed".
/******/ 		
/******/ 					// a Promise means "currently loading".
/******/ 					if(installedChunkData) {
/******/ 						promises.push(installedChunkData[2]);
/******/ 					} else {
/******/ 						if(!/^webpack_sharing_consume_default_(emotion_(react_emotion_react\-webpack_sharing_consume_default_e\-cc324f|serialize_emotion_serialize\-webpack_sharing_consume_d\-2bf41c)|react(|\-dom)|vega(|\-lite_vega\-lite\-webpack_sharing_consume_default_vega)_vega)$/.test(chunkId)) {
/******/ 							// setup Promise in chunk cache
/******/ 							var promise = new Promise((resolve, reject) => (installedChunkData = installedChunks[chunkId] = [resolve, reject]));
/******/ 							promises.push(installedChunkData[2] = promise);
/******/ 		
/******/ 							// start chunk loading
/******/ 							var url = __webpack_require__.p + __webpack_require__.u(chunkId);
/******/ 							// create error before stack unwound to get useful stacktrace later
/******/ 							var error = new Error();
/******/ 							var loadingEnded = (event) => {
/******/ 								if(__webpack_require__.o(installedChunks, chunkId)) {
/******/ 									installedChunkData = installedChunks[chunkId];
/******/ 									if(installedChunkData !== 0) installedChunks[chunkId] = undefined;
/******/ 									if(installedChunkData) {
/******/ 										var errorType = event && (event.type === 'load' ? 'missing' : event.type);
/******/ 										var realSrc = event && event.target && event.target.src;
/******/ 										error.message = 'Loading chunk ' + chunkId + ' failed.\n(' + errorType + ': ' + realSrc + ')';
/******/ 										error.name = 'ChunkLoadError';
/******/ 										error.type = errorType;
/******/ 										error.request = realSrc;
/******/ 										installedChunkData[1](error);
/******/ 									}
/******/ 								}
/******/ 							};
/******/ 							__webpack_require__.l(url, loadingEnded, "chunk-" + chunkId, chunkId);
/******/ 						} else installedChunks[chunkId] = 0;
/******/ 					}
/******/ 				}
/******/ 		};
/******/ 		
/******/ 		// no prefetching
/******/ 		
/******/ 		// no preloaded
/******/ 		
/******/ 		// no HMR
/******/ 		
/******/ 		// no HMR manifest
/******/ 		
/******/ 		// no on chunks loaded
/******/ 		
/******/ 		// install a JSONP callback for chunk loading
/******/ 		var webpackJsonpCallback = (parentChunkLoadingFunction, data) => {
/******/ 			var [chunkIds, moreModules, runtime] = data;
/******/ 			// add "moreModules" to the modules object,
/******/ 			// then flag all "chunkIds" as loaded and fire callback
/******/ 			var moduleId, chunkId, i = 0;
/******/ 			if(chunkIds.some((id) => (installedChunks[id] !== 0))) {
/******/ 				for(moduleId in moreModules) {
/******/ 					if(__webpack_require__.o(moreModules, moduleId)) {
/******/ 						__webpack_require__.m[moduleId] = moreModules[moduleId];
/******/ 					}
/******/ 				}
/******/ 				if(runtime) var result = runtime(__webpack_require__);
/******/ 			}
/******/ 			if(parentChunkLoadingFunction) parentChunkLoadingFunction(data);
/******/ 			for(;i < chunkIds.length; i++) {
/******/ 				chunkId = chunkIds[i];
/******/ 				if(__webpack_require__.o(installedChunks, chunkId) && installedChunks[chunkId]) {
/******/ 					installedChunks[chunkId][0]();
/******/ 				}
/******/ 				installedChunks[chunkId] = 0;
/******/ 			}
/******/ 		
/******/ 		}
/******/ 		
/******/ 		var chunkLoadingGlobal = self["webpackChunkasqlcell"] = self["webpackChunkasqlcell"] || [];
/******/ 		chunkLoadingGlobal.forEach(webpackJsonpCallback.bind(null, 0));
/******/ 		chunkLoadingGlobal.push = webpackJsonpCallback.bind(null, chunkLoadingGlobal.push.bind(chunkLoadingGlobal));
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/nonce */
/******/ 	(() => {
/******/ 		__webpack_require__.nc = undefined;
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// module cache are used so entry inlining is disabled
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	var __webpack_exports__ = __webpack_require__("webpack/container/entry/asqlcell");
/******/ 	(_JUPYTERLAB = typeof _JUPYTERLAB === "undefined" ? {} : _JUPYTERLAB).asqlcell = __webpack_exports__;
/******/ 	
/******/ })()
;
//# sourceMappingURL=remoteEntry.d23ef31fe852b6ad2263.js.map