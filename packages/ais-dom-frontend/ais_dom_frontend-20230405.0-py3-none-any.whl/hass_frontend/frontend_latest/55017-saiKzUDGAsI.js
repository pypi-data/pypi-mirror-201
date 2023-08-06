/*! For license information please see 55017-saiKzUDGAsI.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[55017],{18601:(e,t,n)=>{n.d(t,{Wg:()=>p,qN:()=>r.q});var o,i,s=n(87480),a=n(79932),r=n(78220);const l=null!==(i=null===(o=window.ShadyDOM)||void 0===o?void 0:o.inUse)&&void 0!==i&&i;class p extends r.H{constructor(){super(...arguments),this.disabled=!1,this.containingForm=null,this.formDataListener=e=>{this.disabled||this.setFormData(e.formData)}}findFormElement(){if(!this.shadowRoot||l)return null;const e=this.getRootNode().querySelectorAll("form");for(const t of Array.from(e))if(t.contains(this))return t;return null}connectedCallback(){var e;super.connectedCallback(),this.containingForm=this.findFormElement(),null===(e=this.containingForm)||void 0===e||e.addEventListener("formdata",this.formDataListener)}disconnectedCallback(){var e;super.disconnectedCallback(),null===(e=this.containingForm)||void 0===e||e.removeEventListener("formdata",this.formDataListener),this.containingForm=null}click(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",(e=>{this.dispatchEvent(new Event("change",e))}))}}p.shadowRootOptions={mode:"open",delegatesFocus:!0},(0,s.__decorate)([(0,a.Cb)({type:Boolean})],p.prototype,"disabled",void 0)},51644:(e,t,n)=>{n.d(t,{$:()=>s,P:()=>a});n(56299),n(26110);var o=n(8621),i=n(87156);const s={properties:{pressed:{type:Boolean,readOnly:!0,value:!1,reflectToAttribute:!0,observer:"_pressedChanged"},toggles:{type:Boolean,value:!1,reflectToAttribute:!0},active:{type:Boolean,value:!1,notify:!0,reflectToAttribute:!0},pointerDown:{type:Boolean,readOnly:!0,value:!1},receivedFocusFromKeyboard:{type:Boolean,readOnly:!0},ariaActiveAttribute:{type:String,value:"aria-pressed",observer:"_ariaActiveAttributeChanged"}},listeners:{down:"_downHandler",up:"_upHandler",tap:"_tapHandler"},observers:["_focusChanged(focused)","_activeChanged(active, ariaActiveAttribute)"],keyBindings:{"enter:keydown":"_asyncClick","space:keydown":"_spaceKeyDownHandler","space:keyup":"_spaceKeyUpHandler"},_mouseEventRe:/^mouse/,_tapHandler:function(){this.toggles?this._userActivate(!this.active):this.active=!1},_focusChanged:function(e){this._detectKeyboardFocus(e),e||this._setPressed(!1)},_detectKeyboardFocus:function(e){this._setReceivedFocusFromKeyboard(!this.pointerDown&&e)},_userActivate:function(e){this.active!==e&&(this.active=e,this.fire("change"))},_downHandler:function(e){this._setPointerDown(!0),this._setPressed(!0),this._setReceivedFocusFromKeyboard(!1)},_upHandler:function(){this._setPointerDown(!1),this._setPressed(!1)},_spaceKeyDownHandler:function(e){var t=e.detail.keyboardEvent,n=(0,i.vz)(t).localTarget;this.isLightDescendant(n)||(t.preventDefault(),t.stopImmediatePropagation(),this._setPressed(!0))},_spaceKeyUpHandler:function(e){var t=e.detail.keyboardEvent,n=(0,i.vz)(t).localTarget;this.isLightDescendant(n)||(this.pressed&&this._asyncClick(),this._setPressed(!1))},_asyncClick:function(){this.async((function(){this.click()}),1)},_pressedChanged:function(e){this._changedButtonState()},_ariaActiveAttributeChanged:function(e,t){t&&t!=e&&this.hasAttribute(t)&&this.removeAttribute(t)},_activeChanged:function(e,t){this.toggles?this.setAttribute(this.ariaActiveAttribute,e?"true":"false"):this.removeAttribute(this.ariaActiveAttribute),this._changedButtonState()},_controlStateChanged:function(){this.disabled?this._setPressed(!1):this._changedButtonState()},_changedButtonState:function(){this._buttonStateChanged&&this._buttonStateChanged()}},a=[o.G,s]},70019:(e,t,n)=>{n(56299);const o=n(50856).d`<custom-style>
  <style is="custom-style">
    html {

      /* Shared Styles */
      --paper-font-common-base: {
        font-family: 'Roboto', 'Noto', sans-serif;
        -webkit-font-smoothing: antialiased;
      };

      --paper-font-common-code: {
        font-family: 'Roboto Mono', 'Consolas', 'Menlo', monospace;
        -webkit-font-smoothing: antialiased;
      };

      --paper-font-common-expensive-kerning: {
        text-rendering: optimizeLegibility;
      };

      --paper-font-common-nowrap: {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      };

      /* Material Font Styles */

      --paper-font-display4: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 112px;
        font-weight: 300;
        letter-spacing: -.044em;
        line-height: 120px;
      };

      --paper-font-display3: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 56px;
        font-weight: 400;
        letter-spacing: -.026em;
        line-height: 60px;
      };

      --paper-font-display2: {
        @apply --paper-font-common-base;

        font-size: 45px;
        font-weight: 400;
        letter-spacing: -.018em;
        line-height: 48px;
      };

      --paper-font-display1: {
        @apply --paper-font-common-base;

        font-size: 34px;
        font-weight: 400;
        letter-spacing: -.01em;
        line-height: 40px;
      };

      --paper-font-headline: {
        @apply --paper-font-common-base;

        font-size: 24px;
        font-weight: 400;
        letter-spacing: -.012em;
        line-height: 32px;
      };

      --paper-font-title: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 20px;
        font-weight: 500;
        line-height: 28px;
      };

      --paper-font-subhead: {
        @apply --paper-font-common-base;

        font-size: 16px;
        font-weight: 400;
        line-height: 24px;
      };

      --paper-font-body2: {
        @apply --paper-font-common-base;

        font-size: 14px;
        font-weight: 500;
        line-height: 24px;
      };

      --paper-font-body1: {
        @apply --paper-font-common-base;

        font-size: 14px;
        font-weight: 400;
        line-height: 20px;
      };

      --paper-font-caption: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 12px;
        font-weight: 400;
        letter-spacing: 0.011em;
        line-height: 20px;
      };

      --paper-font-menu: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 13px;
        font-weight: 500;
        line-height: 24px;
      };

      --paper-font-button: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 14px;
        font-weight: 500;
        letter-spacing: 0.018em;
        line-height: 24px;
        text-transform: uppercase;
      };

      --paper-font-code2: {
        @apply --paper-font-common-code;

        font-size: 14px;
        font-weight: 700;
        line-height: 20px;
      };

      --paper-font-code1: {
        @apply --paper-font-common-code;

        font-size: 14px;
        font-weight: 500;
        line-height: 20px;
      };

    }

  </style>
</custom-style>`;o.setAttribute("style","display: none;"),document.head.appendChild(o.content)},79021:(e,t,n)=>{n.d(t,{Z:()=>a});var o=n(90394),i=n(34327),s=n(23682);function a(e,t){(0,s.Z)(2,arguments);var n=(0,i.Z)(e),a=(0,o.Z)(t);return isNaN(a)?new Date(NaN):a?(n.setDate(n.getDate()+a),n):n}},59699:(e,t,n)=>{n.d(t,{Z:()=>r});var o=n(90394),i=n(39244),s=n(23682),a=36e5;function r(e,t){(0,s.Z)(2,arguments);var n=(0,o.Z)(t);return(0,i.Z)(e,n*a)}},39244:(e,t,n)=>{n.d(t,{Z:()=>a});var o=n(90394),i=n(34327),s=n(23682);function a(e,t){(0,s.Z)(2,arguments);var n=(0,i.Z)(e).getTime(),a=(0,o.Z)(t);return new Date(n+a)}},32182:(e,t,n)=>{n.d(t,{Z:()=>a});var o=n(90394),i=n(34327),s=n(23682);function a(e,t){(0,s.Z)(2,arguments);var n=(0,i.Z)(e),a=(0,o.Z)(t);if(isNaN(a))return new Date(NaN);if(!a)return n;var r=n.getDate(),l=new Date(n.getTime());return l.setMonth(n.getMonth()+a+1,0),r>=l.getDate()?l:(n.setFullYear(l.getFullYear(),l.getMonth(),r),n)}},33651:(e,t,n)=>{n.d(t,{Z:()=>a});var o=n(90394),i=n(79021),s=n(23682);function a(e,t){(0,s.Z)(2,arguments);var n=7*(0,o.Z)(t);return(0,i.Z)(e,n)}},27605:(e,t,n)=>{n.d(t,{Z:()=>a});var o=n(90394),i=n(32182),s=n(23682);function a(e,t){(0,s.Z)(2,arguments);var n=(0,o.Z)(t);return(0,i.Z)(e,12*n)}},93752:(e,t,n)=>{n.d(t,{Z:()=>s});var o=n(34327),i=n(23682);function s(e){(0,i.Z)(1,arguments);var t=(0,o.Z)(e);return t.setHours(23,59,59,999),t}},1905:(e,t,n)=>{n.d(t,{Z:()=>s});var o=n(34327),i=n(23682);function s(e){(0,i.Z)(1,arguments);var t=(0,o.Z)(e),n=t.getMonth();return t.setFullYear(t.getFullYear(),n+1,0),t.setHours(23,59,59,999),t}},70390:(e,t,n)=>{n.d(t,{Z:()=>i});var o=n(93752);function i(){return(0,o.Z)(Date.now())}},59281:(e,t,n)=>{n.d(t,{Z:()=>r});var o=n(55020),i=n(34327),s=n(90394),a=n(23682);function r(e,t){var n,r,l,p,c,d,u,h;(0,a.Z)(1,arguments);var f=(0,o.j)(),v=(0,s.Z)(null!==(n=null!==(r=null!==(l=null!==(p=null==t?void 0:t.weekStartsOn)&&void 0!==p?p:null==t||null===(c=t.locale)||void 0===c||null===(d=c.options)||void 0===d?void 0:d.weekStartsOn)&&void 0!==l?l:f.weekStartsOn)&&void 0!==r?r:null===(u=f.locale)||void 0===u||null===(h=u.options)||void 0===h?void 0:h.weekStartsOn)&&void 0!==n?n:0);if(!(v>=0&&v<=6))throw new RangeError("weekStartsOn must be between 0 and 6 inclusively");var m=(0,i.Z)(e),g=m.getDay(),_=6+(g<v?-7:0)-(g-v);return m.setDate(m.getDate()+_),m.setHours(23,59,59,999),m}},70451:(e,t,n)=>{n.d(t,{Z:()=>s});var o=n(34327),i=n(23682);function s(e){(0,i.Z)(1,arguments);var t=(0,o.Z)(e),n=t.getFullYear();return t.setFullYear(n+1,0,0),t.setHours(23,59,59,999),t}},47538:(e,t,n)=>{function o(){var e=new Date,t=e.getFullYear(),n=e.getMonth(),o=e.getDate(),i=new Date(0);return i.setFullYear(t,n,o-1),i.setHours(23,59,59,999),i}n.d(t,{Z:()=>o})},82045:(e,t,n)=>{n.d(t,{Z:()=>s});var o=n(34327),i=n(23682);function s(e,t){(0,i.Z)(2,arguments);var n=(0,o.Z)(e).getTime(),s=(0,o.Z)(t.start).getTime(),a=(0,o.Z)(t.end).getTime();if(!(s<=a))throw new RangeError("Invalid interval");return n>=s&&n<=a}},13250:(e,t,n)=>{n.d(t,{Z:()=>s});var o=n(34327),i=n(23682);function s(e){(0,i.Z)(1,arguments);var t=(0,o.Z)(e);return t.setDate(1),t.setHours(0,0,0,0),t}},27088:(e,t,n)=>{n.d(t,{Z:()=>i});var o=n(59429);function i(){return(0,o.Z)(Date.now())}},69388:(e,t,n)=>{n.d(t,{Z:()=>s});var o=n(34327),i=n(23682);function s(e){(0,i.Z)(1,arguments);var t=(0,o.Z)(e),n=new Date(0);return n.setFullYear(t.getFullYear(),0,1),n.setHours(0,0,0,0),n}},83008:(e,t,n)=>{function o(){var e=new Date,t=e.getFullYear(),n=e.getMonth(),o=e.getDate(),i=new Date(0);return i.setFullYear(t,n,o-1),i.setHours(0,0,0,0),i}n.d(t,{Z:()=>o})},19596:(e,t,n)=>{n.d(t,{sR:()=>d});var o=n(81563),i=n(38941);const s=(e,t)=>{var n,o;const i=e._$AN;if(void 0===i)return!1;for(const e of i)null===(o=(n=e)._$AO)||void 0===o||o.call(n,t,!1),s(e,t);return!0},a=e=>{let t,n;do{if(void 0===(t=e._$AM))break;n=t._$AN,n.delete(e),e=t}while(0===(null==n?void 0:n.size))},r=e=>{for(let t;t=e._$AM;e=t){let n=t._$AN;if(void 0===n)t._$AN=n=new Set;else if(n.has(e))break;n.add(e),c(t)}};function l(e){void 0!==this._$AN?(a(this),this._$AM=e,r(this)):this._$AM=e}function p(e,t=!1,n=0){const o=this._$AH,i=this._$AN;if(void 0!==i&&0!==i.size)if(t)if(Array.isArray(o))for(let e=n;e<o.length;e++)s(o[e],!1),a(o[e]);else null!=o&&(s(o,!1),a(o));else s(this,e)}const c=e=>{var t,n,o,s;e.type==i.pX.CHILD&&(null!==(t=(o=e)._$AP)&&void 0!==t||(o._$AP=p),null!==(n=(s=e)._$AQ)&&void 0!==n||(s._$AQ=l))};class d extends i.Xe{constructor(){super(...arguments),this._$AN=void 0}_$AT(e,t,n){super._$AT(e,t,n),r(this),this.isConnected=e._$AU}_$AO(e,t=!0){var n,o;e!==this.isConnected&&(this.isConnected=e,e?null===(n=this.reconnected)||void 0===n||n.call(this):null===(o=this.disconnected)||void 0===o||o.call(this)),t&&(s(this,e),a(this))}setValue(e){if((0,o.OR)(this._$Ct))this._$Ct._$AI(e,this);else{const t=[...this._$Ct._$AH];t[this._$Ci]=e,this._$Ct._$AI(t,this,0)}}disconnected(){}reconnected(){}}},81563:(e,t,n)=>{n.d(t,{E_:()=>v,OR:()=>r,_Y:()=>p,fk:()=>c,hN:()=>a,hl:()=>u,i9:()=>h,pt:()=>s,ws:()=>f});var o=n(15304);const{I:i}=o.Al,s=e=>null===e||"object"!=typeof e&&"function"!=typeof e,a=(e,t)=>void 0===t?void 0!==(null==e?void 0:e._$litType$):(null==e?void 0:e._$litType$)===t,r=e=>void 0===e.strings,l=()=>document.createComment(""),p=(e,t,n)=>{var o;const s=e._$AA.parentNode,a=void 0===t?e._$AB:t._$AA;if(void 0===n){const t=s.insertBefore(l(),a),o=s.insertBefore(l(),a);n=new i(t,o,e,e.options)}else{const t=n._$AB.nextSibling,i=n._$AM,r=i!==e;if(r){let t;null===(o=n._$AQ)||void 0===o||o.call(n,e),n._$AM=e,void 0!==n._$AP&&(t=e._$AU)!==i._$AU&&n._$AP(t)}if(t!==a||r){let e=n._$AA;for(;e!==t;){const t=e.nextSibling;s.insertBefore(e,a),e=t}}}return n},c=(e,t,n=e)=>(e._$AI(t,n),e),d={},u=(e,t=d)=>e._$AH=t,h=e=>e._$AH,f=e=>{var t;null===(t=e._$AP)||void 0===t||t.call(e,!1,!0);let n=e._$AA;const o=e._$AB.nextSibling;for(;n!==o;){const e=n.nextSibling;n.remove(),n=e}},v=e=>{e._$AR()}},57835:(e,t,n)=>{n.d(t,{XM:()=>o.XM,Xe:()=>o.Xe,pX:()=>o.pX});var o=n(38941)},18848:(e,t,n)=>{n.d(t,{r:()=>r});var o=n(15304),i=n(38941),s=n(81563);const a=(e,t,n)=>{const o=new Map;for(let i=t;i<=n;i++)o.set(e[i],i);return o},r=(0,i.XM)(class extends i.Xe{constructor(e){if(super(e),e.type!==i.pX.CHILD)throw Error("repeat() can only be used in text expressions")}ht(e,t,n){let o;void 0===n?n=t:void 0!==t&&(o=t);const i=[],s=[];let a=0;for(const t of e)i[a]=o?o(t,a):a,s[a]=n(t,a),a++;return{values:s,keys:i}}render(e,t,n){return this.ht(e,t,n).values}update(e,[t,n,i]){var r;const l=(0,s.i9)(e),{values:p,keys:c}=this.ht(t,n,i);if(!Array.isArray(l))return this.ut=c,p;const d=null!==(r=this.ut)&&void 0!==r?r:this.ut=[],u=[];let h,f,v=0,m=l.length-1,g=0,_=p.length-1;for(;v<=m&&g<=_;)if(null===l[v])v++;else if(null===l[m])m--;else if(d[v]===c[g])u[g]=(0,s.fk)(l[v],p[g]),v++,g++;else if(d[m]===c[_])u[_]=(0,s.fk)(l[m],p[_]),m--,_--;else if(d[v]===c[_])u[_]=(0,s.fk)(l[v],p[_]),(0,s._Y)(e,u[_+1],l[v]),v++,_--;else if(d[m]===c[g])u[g]=(0,s.fk)(l[m],p[g]),(0,s._Y)(e,l[v],l[m]),m--,g++;else if(void 0===h&&(h=a(c,g,_),f=a(d,v,m)),h.has(d[v]))if(h.has(d[m])){const t=f.get(c[g]),n=void 0!==t?l[t]:null;if(null===n){const t=(0,s._Y)(e,l[v]);(0,s.fk)(t,p[g]),u[g]=t}else u[g]=(0,s.fk)(n,p[g]),(0,s._Y)(e,l[v],n),l[t]=null;g++}else(0,s.ws)(l[m]),m--;else(0,s.ws)(l[v]),v++;for(;g<=_;){const t=(0,s._Y)(e,u[_+1]);(0,s.fk)(t,p[g]),u[g++]=t}for(;v<=m;){const e=l[v++];null!==e&&(0,s.ws)(e)}return this.ut=c,(0,s.hl)(e,u),o.Jb}})}}]);
//# sourceMappingURL=55017-saiKzUDGAsI.js.map