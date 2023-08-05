"use strict";(self.webpackChunkgrader_labextension=self.webpackChunkgrader_labextension||[]).push([[423],{72643:(e,t,o)=>{o.d(t,{Z:()=>w});var r=o(19756),n=o(22122),l=o(56271),i=o(86010),s=o(94780),a=o(56796),c=o(67070),d=o(56686),u=o(97936),f=o(2734),b=o(71657),h=o(90948),m=o(18941),p=o(85893);const v=["className","slots","slotProps","direction","orientation","disabled"],S=(0,h.ZP)(u.Z,{name:"MuiTabScrollButton",slot:"Root",overridesResolver:(e,t)=>{const{ownerState:o}=e;return[t.root,o.orientation&&t[o.orientation]]}})((({ownerState:e})=>(0,n.Z)({width:40,flexShrink:0,opacity:.8,[`&.${m.Z.disabled}`]:{opacity:0}},"vertical"===e.orientation&&{width:"100%",height:40,"& svg":{transform:`rotate(${e.isRtl?-90:90}deg)`}}))),w=l.forwardRef((function(e,t){var o,l;const u=(0,b.Z)({props:e,name:"MuiTabScrollButton"}),{className:h,slots:w={},slotProps:Z={},direction:x}=u,g=(0,r.Z)(u,v),y="rtl"===(0,f.Z)().direction,E=(0,n.Z)({isRtl:y},u),B=(e=>{const{classes:t,orientation:o,disabled:r}=e,n={root:["root",o,r&&"disabled"]};return(0,s.Z)(n,m.C,t)})(E),C=null!=(o=w.StartScrollButtonIcon)?o:c.Z,M=null!=(l=w.EndScrollButtonIcon)?l:d.Z,T=(0,a.Z)({elementType:C,externalSlotProps:Z.startScrollButtonIcon,additionalProps:{fontSize:"small"},ownerState:E}),R=(0,a.Z)({elementType:M,externalSlotProps:Z.endScrollButtonIcon,additionalProps:{fontSize:"small"},ownerState:E});return(0,p.jsx)(S,(0,n.Z)({component:"div",className:(0,i.Z)(B.root,h),ref:t,role:null,ownerState:E,tabIndex:null},g,{children:"left"===x?(0,p.jsx)(C,(0,n.Z)({},T)):(0,p.jsx)(M,(0,n.Z)({},R))}))}))},18941:(e,t,o)=>{o.d(t,{C:()=>l,Z:()=>i});var r=o(1588),n=o(34867);function l(e){return(0,n.Z)("MuiTabScrollButton",e)}const i=(0,r.Z)("MuiTabScrollButton",["root","vertical","horizontal","disabled"])},48481:(e,t,o)=>{o.d(t,{Z:()=>W});var r=o(19756),n=o(22122),l=o(56271),i=(o(76607),o(86010)),s=o(94780),a=o(56796),c=o(90948),d=o(71657),u=o(2734),f=o(57144);let b;function h(){if(b)return b;const e=document.createElement("div"),t=document.createElement("div");return t.style.width="10px",t.style.height="1px",e.appendChild(t),e.dir="rtl",e.style.fontSize="14px",e.style.width="4px",e.style.height="1px",e.style.position="absolute",e.style.top="-1000px",e.style.overflow="scroll",document.body.appendChild(e),b="reverse",e.scrollLeft>0?b="default":(e.scrollLeft=1,0===e.scrollLeft&&(b="negative")),document.body.removeChild(e),b}function m(e,t){const o=e.scrollLeft;if("rtl"!==t)return o;switch(h()){case"negative":return e.scrollWidth-e.clientWidth+o;case"reverse":return e.scrollWidth-e.clientWidth-o;default:return o}}function p(e){return(1+Math.sin(Math.PI*e-Math.PI/2))/2}var v=o(5340),S=o(85893);const w=["onChange"],Z={width:99,height:99,position:"absolute",top:-9999,overflow:"scroll"};var x=o(72643),g=o(2068),y=o(90852),E=o(8038);const B=["aria-label","aria-labelledby","action","centered","children","className","component","allowScrollButtonsMobile","indicatorColor","onChange","orientation","ScrollButtonComponent","scrollButtons","selectionFollowsFocus","slots","slotProps","TabIndicatorProps","TabScrollButtonProps","textColor","value","variant","visibleScrollbar"],C=(e,t)=>e===t?e.firstChild:t&&t.nextElementSibling?t.nextElementSibling:e.firstChild,M=(e,t)=>e===t?e.lastChild:t&&t.previousElementSibling?t.previousElementSibling:e.lastChild,T=(e,t,o)=>{let r=!1,n=o(e,t);for(;n;){if(n===e.firstChild){if(r)return;r=!0}const t=n.disabled||"true"===n.getAttribute("aria-disabled");if(n.hasAttribute("tabindex")&&!t)return void n.focus();n=o(e,n)}},R=(0,c.ZP)("div",{name:"MuiTabs",slot:"Root",overridesResolver:(e,t)=>{const{ownerState:o}=e;return[{[`& .${y.Z.scrollButtons}`]:t.scrollButtons},{[`& .${y.Z.scrollButtons}`]:o.scrollButtonsHideMobile&&t.scrollButtonsHideMobile},t.root,o.vertical&&t.vertical]}})((({ownerState:e,theme:t})=>(0,n.Z)({overflow:"hidden",minHeight:48,WebkitOverflowScrolling:"touch",display:"flex"},e.vertical&&{flexDirection:"column"},e.scrollButtonsHideMobile&&{[`& .${y.Z.scrollButtons}`]:{[t.breakpoints.down("sm")]:{display:"none"}}}))),I=(0,c.ZP)("div",{name:"MuiTabs",slot:"Scroller",overridesResolver:(e,t)=>{const{ownerState:o}=e;return[t.scroller,o.fixed&&t.fixed,o.hideScrollbar&&t.hideScrollbar,o.scrollableX&&t.scrollableX,o.scrollableY&&t.scrollableY]}})((({ownerState:e})=>(0,n.Z)({position:"relative",display:"inline-block",flex:"1 1 auto",whiteSpace:"nowrap"},e.fixed&&{overflowX:"hidden",width:"100%"},e.hideScrollbar&&{scrollbarWidth:"none","&::-webkit-scrollbar":{display:"none"}},e.scrollableX&&{overflowX:"auto",overflowY:"hidden"},e.scrollableY&&{overflowY:"auto",overflowX:"hidden"}))),P=(0,c.ZP)("div",{name:"MuiTabs",slot:"FlexContainer",overridesResolver:(e,t)=>{const{ownerState:o}=e;return[t.flexContainer,o.vertical&&t.flexContainerVertical,o.centered&&t.centered]}})((({ownerState:e})=>(0,n.Z)({display:"flex"},e.vertical&&{flexDirection:"column"},e.centered&&{justifyContent:"center"}))),k=(0,c.ZP)("span",{name:"MuiTabs",slot:"Indicator",overridesResolver:(e,t)=>t.indicator})((({ownerState:e,theme:t})=>(0,n.Z)({position:"absolute",height:2,bottom:0,width:"100%",transition:t.transitions.create()},"primary"===e.indicatorColor&&{backgroundColor:(t.vars||t).palette.primary.main},"secondary"===e.indicatorColor&&{backgroundColor:(t.vars||t).palette.secondary.main},e.vertical&&{height:"100%",width:2,right:0}))),L=(0,c.ZP)((function(e){const{onChange:t}=e,o=(0,r.Z)(e,w),i=l.useRef(),s=l.useRef(null),a=()=>{i.current=s.current.offsetHeight-s.current.clientHeight};return l.useEffect((()=>{const e=(0,f.Z)((()=>{const e=i.current;a(),e!==i.current&&t(i.current)})),o=(0,v.Z)(s.current);return o.addEventListener("resize",e),()=>{e.clear(),o.removeEventListener("resize",e)}}),[t]),l.useEffect((()=>{a(),t(i.current)}),[t]),(0,S.jsx)("div",(0,n.Z)({style:Z,ref:s},o))}),{name:"MuiTabs",slot:"ScrollbarSize"})({overflowX:"auto",overflowY:"hidden",scrollbarWidth:"none","&::-webkit-scrollbar":{display:"none"}}),N={},W=l.forwardRef((function(e,t){const o=(0,d.Z)({props:e,name:"MuiTabs"}),c=(0,u.Z)(),b="rtl"===c.direction,{"aria-label":w,"aria-labelledby":Z,action:W,centered:z=!1,children:A,className:H,component:X="div",allowScrollButtonsMobile:j=!1,indicatorColor:F="primary",onChange:Y,orientation:D="horizontal",ScrollButtonComponent:$=x.Z,scrollButtons:V="auto",selectionFollowsFocus:q,slots:O={},slotProps:_={},TabIndicatorProps:K={},TabScrollButtonProps:U={},textColor:G="primary",value:J,variant:Q="standard",visibleScrollbar:ee=!1}=o,te=(0,r.Z)(o,B),oe="scrollable"===Q,re="vertical"===D,ne=re?"scrollTop":"scrollLeft",le=re?"top":"left",ie=re?"bottom":"right",se=re?"clientHeight":"clientWidth",ae=re?"height":"width",ce=(0,n.Z)({},o,{component:X,allowScrollButtonsMobile:j,indicatorColor:F,orientation:D,vertical:re,scrollButtons:V,textColor:G,variant:Q,visibleScrollbar:ee,fixed:!oe,hideScrollbar:oe&&!ee,scrollableX:oe&&!re,scrollableY:oe&&re,centered:z&&!oe,scrollButtonsHideMobile:!j}),de=(e=>{const{vertical:t,fixed:o,hideScrollbar:r,scrollableX:n,scrollableY:l,centered:i,scrollButtonsHideMobile:a,classes:c}=e,d={root:["root",t&&"vertical"],scroller:["scroller",o&&"fixed",r&&"hideScrollbar",n&&"scrollableX",l&&"scrollableY"],flexContainer:["flexContainer",t&&"flexContainerVertical",i&&"centered"],indicator:["indicator"],scrollButtons:["scrollButtons",a&&"scrollButtonsHideMobile"],scrollableX:[n&&"scrollableX"],hideScrollbar:[r&&"hideScrollbar"]};return(0,s.Z)(d,y.m,c)})(ce),ue=(0,a.Z)({elementType:O.StartScrollButtonIcon,externalSlotProps:_.startScrollButtonIcon,ownerState:ce}),fe=(0,a.Z)({elementType:O.EndScrollButtonIcon,externalSlotProps:_.endScrollButtonIcon,ownerState:ce}),[be,he]=l.useState(!1),[me,pe]=l.useState(N),[ve,Se]=l.useState({start:!1,end:!1}),[we,Ze]=l.useState({overflow:"hidden",scrollbarWidth:0}),xe=new Map,ge=l.useRef(null),ye=l.useRef(null),Ee=()=>{const e=ge.current;let t,o;if(e){const o=e.getBoundingClientRect();t={clientWidth:e.clientWidth,scrollLeft:e.scrollLeft,scrollTop:e.scrollTop,scrollLeftNormalized:m(e,c.direction),scrollWidth:e.scrollWidth,top:o.top,bottom:o.bottom,left:o.left,right:o.right}}if(e&&!1!==J){const e=ye.current.children;if(e.length>0){const t=e[xe.get(J)];o=t?t.getBoundingClientRect():null}}return{tabsMeta:t,tabMeta:o}},Be=(0,g.Z)((()=>{const{tabsMeta:e,tabMeta:t}=Ee();let o,r=0;if(re)o="top",t&&e&&(r=t.top-e.top+e.scrollTop);else if(o=b?"right":"left",t&&e){const n=b?e.scrollLeftNormalized+e.clientWidth-e.scrollWidth:e.scrollLeft;r=(b?-1:1)*(t[o]-e[o]+n)}const n={[o]:r,[ae]:t?t[ae]:0};if(isNaN(me[o])||isNaN(me[ae]))pe(n);else{const e=Math.abs(me[o]-n[o]),t=Math.abs(me[ae]-n[ae]);(e>=1||t>=1)&&pe(n)}})),Ce=(e,{animation:t=!0}={})=>{t?function(e,t,o,r={},n=(()=>{})){const{ease:l=p,duration:i=300}=r;let s=null;const a=t[e];let c=!1;const d=r=>{if(c)return void n(new Error("Animation cancelled"));null===s&&(s=r);const u=Math.min(1,(r-s)/i);t[e]=l(u)*(o-a)+a,u>=1?requestAnimationFrame((()=>{n(null)})):requestAnimationFrame(d)};a===o?n(new Error("Element already at target position")):requestAnimationFrame(d)}(ne,ge.current,e,{duration:c.transitions.duration.standard}):ge.current[ne]=e},Me=e=>{let t=ge.current[ne];re?t+=e:(t+=e*(b?-1:1),t*=b&&"reverse"===h()?-1:1),Ce(t)},Te=()=>{const e=ge.current[se];let t=0;const o=Array.from(ye.current.children);for(let r=0;r<o.length;r+=1){const n=o[r];if(t+n[se]>e){0===r&&(t=e);break}t+=n[se]}return t},Re=()=>{Me(-1*Te())},Ie=()=>{Me(Te())},Pe=l.useCallback((e=>{Ze({overflow:null,scrollbarWidth:e})}),[]),ke=(0,g.Z)((e=>{const{tabsMeta:t,tabMeta:o}=Ee();if(o&&t)if(o[le]<t[le]){const r=t[ne]+(o[le]-t[le]);Ce(r,{animation:e})}else if(o[ie]>t[ie]){const r=t[ne]+(o[ie]-t[ie]);Ce(r,{animation:e})}})),Le=(0,g.Z)((()=>{if(oe&&!1!==V){const{scrollTop:e,scrollHeight:t,clientHeight:o,scrollWidth:r,clientWidth:n}=ge.current;let l,i;if(re)l=e>1,i=e<t-o-1;else{const e=m(ge.current,c.direction);l=b?e<r-n-1:e>1,i=b?e>1:e<r-n-1}l===ve.start&&i===ve.end||Se({start:l,end:i})}}));l.useEffect((()=>{const e=(0,f.Z)((()=>{ge.current&&(Be(),Le())})),t=(0,v.Z)(ge.current);let o;return t.addEventListener("resize",e),"undefined"!=typeof ResizeObserver&&(o=new ResizeObserver(e),Array.from(ye.current.children).forEach((e=>{o.observe(e)}))),()=>{e.clear(),t.removeEventListener("resize",e),o&&o.disconnect()}}),[Be,Le]);const Ne=l.useMemo((()=>(0,f.Z)((()=>{Le()}))),[Le]);l.useEffect((()=>()=>{Ne.clear()}),[Ne]),l.useEffect((()=>{he(!0)}),[]),l.useEffect((()=>{Be(),Le()})),l.useEffect((()=>{ke(N!==me)}),[ke,me]),l.useImperativeHandle(W,(()=>({updateIndicator:Be,updateScrollButtons:Le})),[Be,Le]);const We=(0,S.jsx)(k,(0,n.Z)({},K,{className:(0,i.Z)(de.indicator,K.className),ownerState:ce,style:(0,n.Z)({},me,K.style)}));let ze=0;const Ae=l.Children.map(A,(e=>{if(!l.isValidElement(e))return null;const t=void 0===e.props.value?ze:e.props.value;xe.set(t,ze);const o=t===J;return ze+=1,l.cloneElement(e,(0,n.Z)({fullWidth:"fullWidth"===Q,indicator:o&&!be&&We,selected:o,selectionFollowsFocus:q,onChange:Y,textColor:G,value:t},1!==ze||!1!==J||e.props.tabIndex?{}:{tabIndex:0}))})),He=(()=>{const e={};e.scrollbarSizeListener=oe?(0,S.jsx)(L,{onChange:Pe,className:(0,i.Z)(de.scrollableX,de.hideScrollbar)}):null;const t=ve.start||ve.end,o=oe&&("auto"===V&&t||!0===V);return e.scrollButtonStart=o?(0,S.jsx)($,(0,n.Z)({slots:{StartScrollButtonIcon:O.StartScrollButtonIcon},slotProps:{startScrollButtonIcon:ue},orientation:D,direction:b?"right":"left",onClick:Re,disabled:!ve.start},U,{className:(0,i.Z)(de.scrollButtons,U.className)})):null,e.scrollButtonEnd=o?(0,S.jsx)($,(0,n.Z)({slots:{EndScrollButtonIcon:O.EndScrollButtonIcon},slotProps:{endScrollButtonIcon:fe},orientation:D,direction:b?"left":"right",onClick:Ie,disabled:!ve.end},U,{className:(0,i.Z)(de.scrollButtons,U.className)})):null,e})();return(0,S.jsxs)(R,(0,n.Z)({className:(0,i.Z)(de.root,H),ownerState:ce,ref:t,as:X},te,{children:[He.scrollButtonStart,He.scrollbarSizeListener,(0,S.jsxs)(I,{className:de.scroller,ownerState:ce,style:{overflow:we.overflow,[re?"margin"+(b?"Left":"Right"):"marginBottom"]:ee?void 0:-we.scrollbarWidth},ref:ge,onScroll:Ne,children:[(0,S.jsx)(P,{"aria-label":w,"aria-labelledby":Z,"aria-orientation":"vertical"===D?"vertical":null,className:de.flexContainer,ownerState:ce,onKeyDown:e=>{const t=ye.current,o=(0,E.Z)(t).activeElement;if("tab"!==o.getAttribute("role"))return;let r="horizontal"===D?"ArrowLeft":"ArrowUp",n="horizontal"===D?"ArrowRight":"ArrowDown";switch("horizontal"===D&&b&&(r="ArrowRight",n="ArrowLeft"),e.key){case r:e.preventDefault(),T(t,o,M);break;case n:e.preventDefault(),T(t,o,C);break;case"Home":e.preventDefault(),T(t,null,C);break;case"End":e.preventDefault(),T(t,null,M)}},ref:ye,role:"tablist",children:Ae}),be&&We]}),He.scrollButtonEnd]}))}))},90852:(e,t,o)=>{o.d(t,{Z:()=>i,m:()=>l});var r=o(1588),n=o(34867);function l(e){return(0,n.Z)("MuiTabs",e)}const i=(0,r.Z)("MuiTabs",["root","vertical","flexContainer","flexContainerVertical","centered","scroller","fixed","scrollableX","scrollableY","hideScrollbar","scrollButtons","scrollButtonsHideMobile","indicator"])},6585:(e,t,o)=>{o.d(t,{Z:()=>b});var r=o(22122),n=o(19756),l=o(56271),i=o(93939),s=o(2734),a=o(30577),c=o(51705),d=o(85893);const u=["addEndListener","appear","children","easing","in","onEnter","onEntered","onEntering","onExit","onExited","onExiting","style","timeout","TransitionComponent"],f={entering:{transform:"none"},entered:{transform:"none"}},b=l.forwardRef((function(e,t){const o=(0,s.Z)(),b={enter:o.transitions.duration.enteringScreen,exit:o.transitions.duration.leavingScreen},{addEndListener:h,appear:m=!0,children:p,easing:v,in:S,onEnter:w,onEntered:Z,onEntering:x,onExit:g,onExited:y,onExiting:E,style:B,timeout:C=b,TransitionComponent:M=i.Transition}=e,T=(0,n.Z)(e,u),R=l.useRef(null),I=(0,c.Z)(R,p.ref,t),P=e=>t=>{if(e){const o=R.current;void 0===t?e(o):e(o,t)}},k=P(x),L=P(((e,t)=>{(0,a.n)(e);const r=(0,a.C)({style:B,timeout:C,easing:v},{mode:"enter"});e.style.webkitTransition=o.transitions.create("transform",r),e.style.transition=o.transitions.create("transform",r),w&&w(e,t)})),N=P(Z),W=P(E),z=P((e=>{const t=(0,a.C)({style:B,timeout:C,easing:v},{mode:"exit"});e.style.webkitTransition=o.transitions.create("transform",t),e.style.transition=o.transitions.create("transform",t),g&&g(e)})),A=P(y);return(0,d.jsx)(M,(0,r.Z)({appear:m,in:S,nodeRef:R,onEnter:L,onEntered:N,onEntering:k,onExit:z,onExited:A,onExiting:W,addEndListener:e=>{h&&h(R.current,e)},timeout:C},T,{children:(e,t)=>l.cloneElement(p,(0,r.Z)({style:(0,r.Z)({transform:"scale(0)",visibility:"exited"!==e||S?void 0:"hidden"},f[e],B,p.props.style),ref:I},t))}))}))}}]);