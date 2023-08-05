"use strict";(self.webpackChunkgrader_labextension=self.webpackChunkgrader_labextension||[]).push([[978],{80230:(r,t,n)=>{n.d(t,{y:()=>l});var e=n(30137),o=n(70204),i=n(46766),u=n(92749),c=n(53912),a=n(58474),s=n(68846),l=function(){function r(r){r&&(this._subscribe=r)}return r.prototype.lift=function(t){var n=new r;return n.source=this,n.operator=t,n},r.prototype.subscribe=function(r,t,n){var i,u=this,c=(i=r)&&i instanceof e.Lv||function(r){return r&&(0,a.m)(r.next)&&(0,a.m)(r.error)&&(0,a.m)(r.complete)}(i)&&(0,o.Nn)(i)?r:new e.Hp(r,t,n);return(0,s.x)((function(){var r=u,t=r.operator,n=r.source;c.add(t?t.call(c,n):n?u._subscribe(c):u._trySubscribe(c))})),c},r.prototype._trySubscribe=function(r){try{return this._subscribe(r)}catch(t){r.error(t)}},r.prototype.forEach=function(r,t){var n=this;return new(t=f(t))((function(t,o){var i=new e.Hp({next:function(t){try{r(t)}catch(r){o(r),i.unsubscribe()}},error:o,complete:t});n.subscribe(i)}))},r.prototype._subscribe=function(r){var t;return null===(t=this.source)||void 0===t?void 0:t.subscribe(r)},r.prototype[i.L]=function(){return this},r.prototype.pipe=function(){for(var r=[],t=0;t<arguments.length;t++)r[t]=arguments[t];return(0,u.U)(r)(this)},r.prototype.toPromise=function(r){var t=this;return new(r=f(r))((function(r,n){var e;t.subscribe((function(r){return e=r}),(function(r){return n(r)}),(function(){return r(e)}))}))},r.create=function(t){return new r(t)},r}();function f(r){var t;return null!==(t=null!=r?r:c.v.Promise)&&void 0!==t?t:Promise}},30137:(r,t,n)=>{n.d(t,{Hp:()=>b,Lv:()=>h});var e=n(35987),o=n(58474),i=n(70204),u=n(53912),c=n(40005),a=n(22967),s=l("C",void 0,void 0);function l(r,t,n){return{kind:r,value:t,error:n}}var f=n(68380),p=n(68846),h=function(r){function t(t){var n=r.call(this)||this;return n.isStopped=!1,t?(n.destination=t,(0,i.Nn)(t)&&t.add(n)):n.destination=x,n}return(0,e.ZT)(t,r),t.create=function(r,t,n){return new b(r,t,n)},t.prototype.next=function(r){this.isStopped?w(function(r){return l("N",r,void 0)}(r),this):this._next(r)},t.prototype.error=function(r){this.isStopped?w(l("E",void 0,r),this):(this.isStopped=!0,this._error(r))},t.prototype.complete=function(){this.isStopped?w(s,this):(this.isStopped=!0,this._complete())},t.prototype.unsubscribe=function(){this.closed||(this.isStopped=!0,r.prototype.unsubscribe.call(this),this.destination=null)},t.prototype._next=function(r){this.destination.next(r)},t.prototype._error=function(r){try{this.destination.error(r)}finally{this.unsubscribe()}},t.prototype._complete=function(){try{this.destination.complete()}finally{this.unsubscribe()}},t}(i.w0),v=Function.prototype.bind;function y(r,t){return v.call(r,t)}var d=function(){function r(r){this.partialObserver=r}return r.prototype.next=function(r){var t=this.partialObserver;if(t.next)try{t.next(r)}catch(r){m(r)}},r.prototype.error=function(r){var t=this.partialObserver;if(t.error)try{t.error(r)}catch(r){m(r)}else m(r)},r.prototype.complete=function(){var r=this.partialObserver;if(r.complete)try{r.complete()}catch(r){m(r)}},r}(),b=function(r){function t(t,n,e){var i,c,a=r.call(this)||this;return(0,o.m)(t)||!t?i={next:null!=t?t:void 0,error:null!=n?n:void 0,complete:null!=e?e:void 0}:a&&u.v.useDeprecatedNextContext?((c=Object.create(t)).unsubscribe=function(){return a.unsubscribe()},i={next:t.next&&y(t.next,c),error:t.error&&y(t.error,c),complete:t.complete&&y(t.complete,c)}):i=t,a.destination=new d(i),a}return(0,e.ZT)(t,r),t}(h);function m(r){u.v.useDeprecatedSynchronousErrorHandling?(0,p.O)(r):(0,c.h)(r)}function w(r,t){var n=u.v.onStoppedNotification;n&&f.z.setTimeout((function(){return n(r,t)}))}var x={closed:!0,next:a.Z,error:function(r){throw r},complete:a.Z}},70204:(r,t,n)=>{n.d(t,{Lc:()=>a,Nn:()=>s,w0:()=>c});var e=n(35987),o=n(58474),i=n(25948),u=n(3699),c=function(){function r(r){this.initialTeardown=r,this.closed=!1,this._parentage=null,this._finalizers=null}var t;return r.prototype.unsubscribe=function(){var r,t,n,u,c;if(!this.closed){this.closed=!0;var a=this._parentage;if(a)if(this._parentage=null,Array.isArray(a))try{for(var s=(0,e.XA)(a),f=s.next();!f.done;f=s.next())f.value.remove(this)}catch(t){r={error:t}}finally{try{f&&!f.done&&(t=s.return)&&t.call(s)}finally{if(r)throw r.error}}else a.remove(this);var p=this.initialTeardown;if((0,o.m)(p))try{p()}catch(r){c=r instanceof i.B?r.errors:[r]}var h=this._finalizers;if(h){this._finalizers=null;try{for(var v=(0,e.XA)(h),y=v.next();!y.done;y=v.next()){var d=y.value;try{l(d)}catch(r){c=null!=c?c:[],r instanceof i.B?c=(0,e.ev)((0,e.ev)([],(0,e.CR)(c)),(0,e.CR)(r.errors)):c.push(r)}}}catch(r){n={error:r}}finally{try{y&&!y.done&&(u=v.return)&&u.call(v)}finally{if(n)throw n.error}}}if(c)throw new i.B(c)}},r.prototype.add=function(t){var n;if(t&&t!==this)if(this.closed)l(t);else{if(t instanceof r){if(t.closed||t._hasParent(this))return;t._addParent(this)}(this._finalizers=null!==(n=this._finalizers)&&void 0!==n?n:[]).push(t)}},r.prototype._hasParent=function(r){var t=this._parentage;return t===r||Array.isArray(t)&&t.includes(r)},r.prototype._addParent=function(r){var t=this._parentage;this._parentage=Array.isArray(t)?(t.push(r),t):t?[t,r]:r},r.prototype._removeParent=function(r){var t=this._parentage;t===r?this._parentage=null:Array.isArray(t)&&(0,u.P)(t,r)},r.prototype.remove=function(t){var n=this._finalizers;n&&(0,u.P)(n,t),t instanceof r&&t._removeParent(this)},r.EMPTY=((t=new r).closed=!0,t),r}(),a=c.EMPTY;function s(r){return r instanceof c||r&&"closed"in r&&(0,o.m)(r.remove)&&(0,o.m)(r.add)&&(0,o.m)(r.unsubscribe)}function l(r){(0,o.m)(r)?r():r.unsubscribe()}},53912:(r,t,n)=>{n.d(t,{v:()=>e});var e={onUnhandledError:null,onStoppedNotification:null,Promise:void 0,useDeprecatedSynchronousErrorHandling:!1,useDeprecatedNextContext:!1}},87878:(r,t,n)=>{n.d(t,{Xf:()=>y});var e=n(35987),o=n(45685),i=n(53841),u=n(80230),c=n(71764),a=n(58430),s=n(88729),l=n(1837),f=n(48671),p=n(58474),h=n(40005),v=n(46766);function y(r){if(r instanceof u.y)return r;if(null!=r){if((0,c.c)(r))return m=r,new u.y((function(r){var t=m[v.L]();if((0,p.m)(t.subscribe))return t.subscribe(r);throw new TypeError("Provided object does not correctly implement Symbol.observable")}));if((0,o.z)(r))return b=r,new u.y((function(r){for(var t=0;t<b.length&&!r.closed;t++)r.next(b[t]);r.complete()}));if((0,i.t)(r))return y=r,new u.y((function(r){y.then((function(t){r.closed||(r.next(t),r.complete())}),(function(t){return r.error(t)})).then(null,h.h)}));if((0,a.D)(r))return d(r);if((0,l.T)(r))return n=r,new u.y((function(r){var t,o;try{for(var i=(0,e.XA)(n),u=i.next();!u.done;u=i.next()){var c=u.value;if(r.next(c),r.closed)return}}catch(r){t={error:r}}finally{try{u&&!u.done&&(o=i.return)&&o.call(i)}finally{if(t)throw t.error}}r.complete()}));if((0,f.L)(r))return t=r,d((0,f.Q)(t))}var t,n,y,b,m;throw(0,s.z)(r)}function d(r){return new u.y((function(t){(function(r,t){var n,o,i,u;return(0,e.mG)(this,void 0,void 0,(function(){var c,a;return(0,e.Jh)(this,(function(s){switch(s.label){case 0:s.trys.push([0,5,6,11]),n=(0,e.KL)(r),s.label=1;case 1:return[4,n.next()];case 2:if((o=s.sent()).done)return[3,4];if(c=o.value,t.next(c),t.closed)return[2];s.label=3;case 3:return[3,1];case 4:return[3,11];case 5:return a=s.sent(),i={error:a},[3,11];case 6:return s.trys.push([6,,9,10]),o&&!o.done&&(u=n.return)?[4,u.call(n)]:[3,8];case 7:s.sent(),s.label=8;case 8:return[3,10];case 9:if(i)throw i.error;return[7];case 10:return[7];case 11:return t.complete(),[2]}}))}))})(r,t).catch((function(r){return t.error(r)}))}))}},2566:(r,t,n)=>{n.d(t,{Q:()=>i,x:()=>o});var e=n(35987);function o(r,t,n,e,o){return new i(r,t,n,e,o)}var i=function(r){function t(t,n,e,o,i,u){var c=r.call(this,t)||this;return c.onFinalize=i,c.shouldUnsubscribe=u,c._next=n?function(r){try{n(r)}catch(r){t.error(r)}}:r.prototype._next,c._error=o?function(r){try{o(r)}catch(r){t.error(r)}finally{this.unsubscribe()}}:r.prototype._error,c._complete=e?function(){try{e()}catch(r){t.error(r)}finally{this.unsubscribe()}}:r.prototype._complete,c}return(0,e.ZT)(t,r),t.prototype.unsubscribe=function(){var t;if(!this.shouldUnsubscribe||this.shouldUnsubscribe()){var n=this.closed;r.prototype.unsubscribe.call(this),!n&&(null===(t=this.onFinalize)||void 0===t||t.call(this))}},t}(n(30137).Lv)},34978:(r,t,n)=>{n.d(t,{w:()=>u});var e=n(87878),o=n(96798),i=n(2566);function u(r,t){return(0,o.e)((function(n,o){var u=null,c=0,a=!1,s=function(){return a&&!u&&o.complete()};n.subscribe((0,i.x)(o,(function(n){null==u||u.unsubscribe();var a=0,l=c++;(0,e.Xf)(r(n,l)).subscribe(u=(0,i.x)(o,(function(r){return o.next(t?t(n,r,l,a++):r)}),(function(){u=null,s()})))}),(function(){a=!0,s()})))}))}},68380:(r,t,n)=>{n.d(t,{z:()=>o});var e=n(35987),o={setTimeout:function(r,t){for(var n=[],i=2;i<arguments.length;i++)n[i-2]=arguments[i];var u=o.delegate;return(null==u?void 0:u.setTimeout)?u.setTimeout.apply(u,(0,e.ev)([r,t],(0,e.CR)(n))):setTimeout.apply(void 0,(0,e.ev)([r,t],(0,e.CR)(n)))},clearTimeout:function(r){var t=o.delegate;return((null==t?void 0:t.clearTimeout)||clearTimeout)(r)},delegate:void 0}},39768:(r,t,n)=>{n.d(t,{h:()=>e});var e="function"==typeof Symbol&&Symbol.iterator?Symbol.iterator:"@@iterator"},46766:(r,t,n)=>{n.d(t,{L:()=>e});var e="function"==typeof Symbol&&Symbol.observable||"@@observable"},25948:(r,t,n)=>{n.d(t,{B:()=>e});var e=(0,n(1819).d)((function(r){return function(t){r(this),this.message=t?t.length+" errors occurred during unsubscription:\n"+t.map((function(r,t){return t+1+") "+r.toString()})).join("\n  "):"",this.name="UnsubscriptionError",this.errors=t}}))},3699:(r,t,n)=>{function e(r,t){if(r){var n=r.indexOf(t);0<=n&&r.splice(n,1)}}n.d(t,{P:()=>e})},1819:(r,t,n)=>{function e(r){var t=r((function(r){Error.call(r),r.stack=(new Error).stack}));return t.prototype=Object.create(Error.prototype),t.prototype.constructor=t,t}n.d(t,{d:()=>e})},68846:(r,t,n)=>{n.d(t,{O:()=>u,x:()=>i});var e=n(53912),o=null;function i(r){if(e.v.useDeprecatedSynchronousErrorHandling){var t=!o;if(t&&(o={errorThrown:!1,error:null}),r(),t){var n=o,i=n.errorThrown,u=n.error;if(o=null,i)throw u}}else r()}function u(r){e.v.useDeprecatedSynchronousErrorHandling&&o&&(o.errorThrown=!0,o.error=r)}},90278:(r,t,n)=>{function e(r){return r}n.d(t,{y:()=>e})},45685:(r,t,n)=>{n.d(t,{z:()=>e});var e=function(r){return r&&"number"==typeof r.length&&"function"!=typeof r}},58430:(r,t,n)=>{n.d(t,{D:()=>o});var e=n(58474);function o(r){return Symbol.asyncIterator&&(0,e.m)(null==r?void 0:r[Symbol.asyncIterator])}},58474:(r,t,n)=>{function e(r){return"function"==typeof r}n.d(t,{m:()=>e})},71764:(r,t,n)=>{n.d(t,{c:()=>i});var e=n(46766),o=n(58474);function i(r){return(0,o.m)(r[e.L])}},1837:(r,t,n)=>{n.d(t,{T:()=>i});var e=n(39768),o=n(58474);function i(r){return(0,o.m)(null==r?void 0:r[e.h])}},53841:(r,t,n)=>{n.d(t,{t:()=>o});var e=n(58474);function o(r){return(0,e.m)(null==r?void 0:r.then)}},48671:(r,t,n)=>{n.d(t,{L:()=>u,Q:()=>i});var e=n(35987),o=n(58474);function i(r){return(0,e.FC)(this,arguments,(function(){var t,n,o;return(0,e.Jh)(this,(function(i){switch(i.label){case 0:t=r.getReader(),i.label=1;case 1:i.trys.push([1,,9,10]),i.label=2;case 2:return[4,(0,e.qq)(t.read())];case 3:return n=i.sent(),o=n.value,n.done?[4,(0,e.qq)(void 0)]:[3,5];case 4:return[2,i.sent()];case 5:return[4,(0,e.qq)(o)];case 6:return[4,i.sent()];case 7:return i.sent(),[3,2];case 8:return[3,10];case 9:return t.releaseLock(),[7];case 10:return[2]}}))}))}function u(r){return(0,o.m)(null==r?void 0:r.getReader)}},96798:(r,t,n)=>{n.d(t,{A:()=>o,e:()=>i});var e=n(58474);function o(r){return(0,e.m)(null==r?void 0:r.lift)}function i(r){return function(t){if(o(t))return t.lift((function(t){try{return r(t,this)}catch(r){this.error(r)}}));throw new TypeError("Unable to lift unknown Observable type")}}},22967:(r,t,n)=>{function e(){}n.d(t,{Z:()=>e})},92749:(r,t,n)=>{n.d(t,{U:()=>i,z:()=>o});var e=n(90278);function o(){for(var r=[],t=0;t<arguments.length;t++)r[t]=arguments[t];return i(r)}function i(r){return 0===r.length?e.y:1===r.length?r[0]:function(t){return r.reduce((function(r,t){return t(r)}),t)}}},40005:(r,t,n)=>{n.d(t,{h:()=>i});var e=n(53912),o=n(68380);function i(r){o.z.setTimeout((function(){var t=e.v.onUnhandledError;if(!t)throw r;t(r)}))}},88729:(r,t,n)=>{function e(r){return new TypeError("You provided "+(null!==r&&"object"==typeof r?"an invalid object":"'"+r+"'")+" where a stream was expected. You can provide an Observable, Promise, ReadableStream, Array, AsyncIterable, or Iterable.")}n.d(t,{z:()=>e})},35987:(r,t,n)=>{n.d(t,{CR:()=>a,FC:()=>f,Jh:()=>u,KL:()=>p,XA:()=>c,ZT:()=>o,ev:()=>s,mG:()=>i,qq:()=>l});var e=function(r,t){return e=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(r,t){r.__proto__=t}||function(r,t){for(var n in t)Object.prototype.hasOwnProperty.call(t,n)&&(r[n]=t[n])},e(r,t)};function o(r,t){if("function"!=typeof t&&null!==t)throw new TypeError("Class extends value "+String(t)+" is not a constructor or null");function n(){this.constructor=r}e(r,t),r.prototype=null===t?Object.create(t):(n.prototype=t.prototype,new n)}function i(r,t,n,e){return new(n||(n=Promise))((function(o,i){function u(r){try{a(e.next(r))}catch(r){i(r)}}function c(r){try{a(e.throw(r))}catch(r){i(r)}}function a(r){var t;r.done?o(r.value):(t=r.value,t instanceof n?t:new n((function(r){r(t)}))).then(u,c)}a((e=e.apply(r,t||[])).next())}))}function u(r,t){var n,e,o,i,u={label:0,sent:function(){if(1&o[0])throw o[1];return o[1]},trys:[],ops:[]};return i={next:c(0),throw:c(1),return:c(2)},"function"==typeof Symbol&&(i[Symbol.iterator]=function(){return this}),i;function c(c){return function(a){return function(c){if(n)throw new TypeError("Generator is already executing.");for(;i&&(i=0,c[0]&&(u=0)),u;)try{if(n=1,e&&(o=2&c[0]?e.return:c[0]?e.throw||((o=e.return)&&o.call(e),0):e.next)&&!(o=o.call(e,c[1])).done)return o;switch(e=0,o&&(c=[2&c[0],o.value]),c[0]){case 0:case 1:o=c;break;case 4:return u.label++,{value:c[1],done:!1};case 5:u.label++,e=c[1],c=[0];continue;case 7:c=u.ops.pop(),u.trys.pop();continue;default:if(!((o=(o=u.trys).length>0&&o[o.length-1])||6!==c[0]&&2!==c[0])){u=0;continue}if(3===c[0]&&(!o||c[1]>o[0]&&c[1]<o[3])){u.label=c[1];break}if(6===c[0]&&u.label<o[1]){u.label=o[1],o=c;break}if(o&&u.label<o[2]){u.label=o[2],u.ops.push(c);break}o[2]&&u.ops.pop(),u.trys.pop();continue}c=t.call(r,u)}catch(r){c=[6,r],e=0}finally{n=o=0}if(5&c[0])throw c[1];return{value:c[0]?c[1]:void 0,done:!0}}([c,a])}}}function c(r){var t="function"==typeof Symbol&&Symbol.iterator,n=t&&r[t],e=0;if(n)return n.call(r);if(r&&"number"==typeof r.length)return{next:function(){return r&&e>=r.length&&(r=void 0),{value:r&&r[e++],done:!r}}};throw new TypeError(t?"Object is not iterable.":"Symbol.iterator is not defined.")}function a(r,t){var n="function"==typeof Symbol&&r[Symbol.iterator];if(!n)return r;var e,o,i=n.call(r),u=[];try{for(;(void 0===t||t-- >0)&&!(e=i.next()).done;)u.push(e.value)}catch(r){o={error:r}}finally{try{e&&!e.done&&(n=i.return)&&n.call(i)}finally{if(o)throw o.error}}return u}function s(r,t,n){if(n||2===arguments.length)for(var e,o=0,i=t.length;o<i;o++)!e&&o in t||(e||(e=Array.prototype.slice.call(t,0,o)),e[o]=t[o]);return r.concat(e||Array.prototype.slice.call(t))}function l(r){return this instanceof l?(this.v=r,this):new l(r)}function f(r,t,n){if(!Symbol.asyncIterator)throw new TypeError("Symbol.asyncIterator is not defined.");var e,o=n.apply(r,t||[]),i=[];return e={},u("next"),u("throw"),u("return"),e[Symbol.asyncIterator]=function(){return this},e;function u(r){o[r]&&(e[r]=function(t){return new Promise((function(n,e){i.push([r,t,n,e])>1||c(r,t)}))})}function c(r,t){try{(n=o[r](t)).value instanceof l?Promise.resolve(n.value.v).then(a,s):f(i[0][2],n)}catch(r){f(i[0][3],r)}var n}function a(r){c("next",r)}function s(r){c("throw",r)}function f(r,t){r(t),i.shift(),i.length&&c(i[0][0],i[0][1])}}function p(r){if(!Symbol.asyncIterator)throw new TypeError("Symbol.asyncIterator is not defined.");var t,n=r[Symbol.asyncIterator];return n?n.call(r):(r=c(r),t={},e("next"),e("throw"),e("return"),t[Symbol.asyncIterator]=function(){return this},t);function e(n){t[n]=r[n]&&function(t){return new Promise((function(e,o){!function(r,t,n,e){Promise.resolve(e).then((function(t){r({value:t,done:n})}),t)}(e,o,(t=r[n](t)).done,t.value)}))}}}Object.create,Object.create}}]);