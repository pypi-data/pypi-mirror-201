"use strict";(self.webpackChunkgrader_labextension=self.webpackChunkgrader_labextension||[]).push([[171,122,158],{22122:(e,r,t)=>{function n(){return n=Object.assign?Object.assign.bind():function(e){for(var r=1;r<arguments.length;r++){var t=arguments[r];for(var n in t)Object.prototype.hasOwnProperty.call(t,n)&&(e[n]=t[n])}return e},n.apply(this,arguments)}t.d(r,{Z:()=>n})},45042:(e,r,t)=>{t.d(r,{Z:()=>n});const n=function(e){var r=Object.create(null);return function(t){return void 0===r[t]&&(r[t]=e(t)),r[t]}}},71826:(e,r,t)=>{t.d(r,{O:()=>h});const n=function(e){for(var r,t=0,n=0,o=e.length;o>=4;++n,o-=4)r=1540483477*(65535&(r=255&e.charCodeAt(n)|(255&e.charCodeAt(++n))<<8|(255&e.charCodeAt(++n))<<16|(255&e.charCodeAt(++n))<<24))+(59797*(r>>>16)<<16),t=1540483477*(65535&(r^=r>>>24))+(59797*(r>>>16)<<16)^1540483477*(65535&t)+(59797*(t>>>16)<<16);switch(o){case 3:t^=(255&e.charCodeAt(n+2))<<16;case 2:t^=(255&e.charCodeAt(n+1))<<8;case 1:t=1540483477*(65535&(t^=255&e.charCodeAt(n)))+(59797*(t>>>16)<<16)}return(((t=1540483477*(65535&(t^=t>>>13))+(59797*(t>>>16)<<16))^t>>>15)>>>0).toString(36)},o={animationIterationCount:1,borderImageOutset:1,borderImageSlice:1,borderImageWidth:1,boxFlex:1,boxFlexGroup:1,boxOrdinalGroup:1,columnCount:1,columns:1,flex:1,flexGrow:1,flexPositive:1,flexShrink:1,flexNegative:1,flexOrder:1,gridRow:1,gridRowEnd:1,gridRowSpan:1,gridRowStart:1,gridColumn:1,gridColumnEnd:1,gridColumnSpan:1,gridColumnStart:1,msGridRow:1,msGridRowSpan:1,msGridColumn:1,msGridColumnSpan:1,fontWeight:1,lineHeight:1,opacity:1,order:1,orphans:1,tabSize:1,widows:1,zIndex:1,zoom:1,WebkitLineClamp:1,fillOpacity:1,floodOpacity:1,stopOpacity:1,strokeDasharray:1,strokeDashoffset:1,strokeMiterlimit:1,strokeOpacity:1,strokeWidth:1};var i=t(45042),a=/[A-Z]|^ms/g,s=/_EMO_([^_]+?)_([^]*?)_EMO_/g,l=function(e){return 45===e.charCodeAt(1)},u=function(e){return null!=e&&"boolean"!=typeof e},c=(0,i.Z)((function(e){return l(e)?e:e.replace(a,"-$&").toLowerCase()})),f=function(e,r){switch(e){case"animation":case"animationName":if("string"==typeof r)return r.replace(s,(function(e,r,t){return v={name:r,styles:t,next:v},r}))}return 1===o[e]||l(e)||"number"!=typeof r||0===r?r:r+"px"};function d(e,r,t){if(null==t)return"";if(void 0!==t.__emotion_styles)return t;switch(typeof t){case"boolean":return"";case"object":if(1===t.anim)return v={name:t.name,styles:t.styles,next:v},t.name;if(void 0!==t.styles){var n=t.next;if(void 0!==n)for(;void 0!==n;)v={name:n.name,styles:n.styles,next:v},n=n.next;return t.styles+";"}return function(e,r,t){var n="";if(Array.isArray(t))for(var o=0;o<t.length;o++)n+=d(e,r,t[o])+";";else for(var i in t){var a=t[i];if("object"!=typeof a)null!=r&&void 0!==r[a]?n+=i+"{"+r[a]+"}":u(a)&&(n+=c(i)+":"+f(i,a)+";");else if(!Array.isArray(a)||"string"!=typeof a[0]||null!=r&&void 0!==r[a[0]]){var s=d(e,r,a);switch(i){case"animation":case"animationName":n+=c(i)+":"+s+";";break;default:n+=i+"{"+s+"}"}}else for(var l=0;l<a.length;l++)u(a[l])&&(n+=c(i)+":"+f(i,a[l])+";")}return n}(e,r,t);case"function":if(void 0!==e){var o=v,i=t(e);return v=o,d(e,r,i)}}if(null==r)return t;var a=r[t];return void 0!==a?a:t}var v,m=/label:\s*([^\s;\n{]+)\s*(;|$)/g,h=function(e,r,t){if(1===e.length&&"object"==typeof e[0]&&null!==e[0]&&void 0!==e[0].styles)return e[0];var o=!0,i="";v=void 0;var a=e[0];null==a||void 0===a.raw?(o=!1,i+=d(t,r,a)):i+=a[0];for(var s=1;s<e.length;s++)i+=d(t,r,e[s]),o&&(i+=a[s]);m.lastIndex=0;for(var l,u="";null!==(l=m.exec(i));)u+="-"+l[1];return{name:n(i)+u,styles:i,next:v}}},27278:(e,r,t)=>{t.d(r,{L:()=>i,j:()=>a});var n=t(56271),o=!!n.useInsertionEffect&&n.useInsertionEffect,i=o||function(e){return e()},a=o||n.useLayoutEffect},70444:(e,r,t)=>{function n(e,r,t){var n="";return t.split(" ").forEach((function(t){void 0!==e[t]?r.push(e[t]+";"):n+=t+" "})),n}t.d(r,{My:()=>i,fp:()=>n,hC:()=>o});var o=function(e,r,t){var n=e.key+"-"+r.name;!1===t&&void 0===e.registered[n]&&(e.registered[n]=r.styles)},i=function(e,r,t){o(e,r,t);var n=e.key+"-"+r.name;if(void 0===e.inserted[r.name]){var i=r;do{e.insert(r===i?"."+n:"",i,e.sheet,!0),i=i.next}while(void 0!==i)}}}}]);