/*! For license information please see 84575-qCITP6jPRbU.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[84575],{18601:(e,t,a)=>{a.d(t,{Wg:()=>p,qN:()=>l.q});var i,r,o=a(87480),n=a(79932),l=a(78220);const s=null!==(r=null===(i=window.ShadyDOM)||void 0===i?void 0:i.inUse)&&void 0!==r&&r;class p extends l.H{constructor(){super(...arguments),this.disabled=!1,this.containingForm=null,this.formDataListener=e=>{this.disabled||this.setFormData(e.formData)}}findFormElement(){if(!this.shadowRoot||s)return null;const e=this.getRootNode().querySelectorAll("form");for(const t of Array.from(e))if(t.contains(this))return t;return null}connectedCallback(){var e;super.connectedCallback(),this.containingForm=this.findFormElement(),null===(e=this.containingForm)||void 0===e||e.addEventListener("formdata",this.formDataListener)}disconnectedCallback(){var e;super.disconnectedCallback(),null===(e=this.containingForm)||void 0===e||e.removeEventListener("formdata",this.formDataListener),this.containingForm=null}click(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",(e=>{this.dispatchEvent(new Event("change",e))}))}}p.shadowRootOptions={mode:"open",delegatesFocus:!0},(0,o.__decorate)([(0,n.Cb)({type:Boolean})],p.prototype,"disabled",void 0)},13529:(e,t,a)=>{var i=a(87480),r=a(79932),o=a(49412),n=a(3762);let l=class extends o.K{};l.styles=[n.W],l=(0,i.__decorate)([(0,r.Mo)("mwc-select")],l)},14095:(e,t,a)=>{a(56299),a(65660);var i=a(26110),r=a(98235),o=a(9672),n=a(87156),l=a(50856);(0,o.k)({_template:l.d`
    <style>
      :host {
        display: inline-block;
        position: relative;
        width: 400px;
        border: 1px solid;
        padding: 2px;
        -moz-appearance: textarea;
        -webkit-appearance: textarea;
        overflow: hidden;
      }

      .mirror-text {
        visibility: hidden;
        word-wrap: break-word;
        @apply --iron-autogrow-textarea;
      }

      .fit {
        @apply --layout-fit;
      }

      textarea {
        position: relative;
        outline: none;
        border: none;
        resize: none;
        background: inherit;
        color: inherit;
        /* see comments in template */
        width: 100%;
        height: 100%;
        font-size: inherit;
        font-family: inherit;
        line-height: inherit;
        text-align: inherit;
        @apply --iron-autogrow-textarea;
      }

      textarea::-webkit-input-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea:-moz-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea::-moz-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea:-ms-input-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }
    </style>

    <!-- the mirror sizes the input/textarea so it grows with typing -->
    <!-- use &#160; instead &nbsp; of to allow this element to be used in XHTML -->
    <div id="mirror" class="mirror-text" aria-hidden="true">&nbsp;</div>

    <!-- size the input/textarea with a div, because the textarea has intrinsic size in ff -->
    <div class="textarea-container fit">
      <textarea id="textarea" name$="[[name]]" aria-label$="[[label]]" autocomplete$="[[autocomplete]]" autofocus$="[[autofocus]]" autocapitalize$="[[autocapitalize]]" inputmode$="[[inputmode]]" placeholder$="[[placeholder]]" readonly$="[[readonly]]" required$="[[required]]" disabled$="[[disabled]]" rows$="[[rows]]" minlength$="[[minlength]]" maxlength$="[[maxlength]]"></textarea>
    </div>
`,is:"iron-autogrow-textarea",behaviors:[r.x,i.a],properties:{value:{observer:"_valueChanged",type:String,notify:!0},bindValue:{observer:"_bindValueChanged",type:String,notify:!0},rows:{type:Number,value:1,observer:"_updateCached"},maxRows:{type:Number,value:0,observer:"_updateCached"},autocomplete:{type:String,value:"off"},autofocus:{type:Boolean,value:!1},autocapitalize:{type:String,value:"none"},inputmode:{type:String},placeholder:{type:String},readonly:{type:String},required:{type:Boolean},minlength:{type:Number},maxlength:{type:Number},label:{type:String}},listeners:{input:"_onInput"},get textarea(){return this.$.textarea},get selectionStart(){return this.$.textarea.selectionStart},get selectionEnd(){return this.$.textarea.selectionEnd},set selectionStart(e){this.$.textarea.selectionStart=e},set selectionEnd(e){this.$.textarea.selectionEnd=e},attached:function(){navigator.userAgent.match(/iP(?:[oa]d|hone)/)&&!navigator.userAgent.match(/OS 1[3456789]/)&&(this.$.textarea.style.marginLeft="-3px")},validate:function(){var e=this.$.textarea.validity.valid;return e&&(this.required&&""===this.value?e=!1:this.hasValidator()&&(e=r.x.validate.call(this,this.value))),this.invalid=!e,this.fire("iron-input-validate"),e},_bindValueChanged:function(e){this.value=e},_valueChanged:function(e){var t=this.textarea;t&&(t.value!==e&&(t.value=e||0===e?e:""),this.bindValue=e,this.$.mirror.innerHTML=this._valueForMirror(),this.fire("bind-value-changed",{value:this.bindValue}))},_onInput:function(e){var t=(0,n.vz)(e).path;this.value=t?t[0].value:e.target.value},_constrain:function(e){var t;for(e=e||[""],t=this.maxRows>0&&e.length>this.maxRows?e.slice(0,this.maxRows):e.slice(0);this.rows>0&&t.length<this.rows;)t.push("");return t.join("<br/>")+"&#160;"},_valueForMirror:function(){var e=this.textarea;if(e)return this.tokens=e&&e.value?e.value.replace(/&/gm,"&amp;").replace(/"/gm,"&quot;").replace(/'/gm,"&#39;").replace(/</gm,"&lt;").replace(/>/gm,"&gt;").split("\n"):[""],this._constrain(this.tokens)},_updateCached:function(){this.$.mirror.innerHTML=this._constrain(this.tokens)}});a(2178),a(98121),a(65911);var s=a(21006),p=a(66668);(0,o.k)({_template:l.d`
    <style>
      :host {
        display: block;
      }

      :host([hidden]) {
        display: none !important;
      }

      label {
        pointer-events: none;
      }
    </style>

    <paper-input-container no-label-float$="[[noLabelFloat]]" always-float-label="[[_computeAlwaysFloatLabel(alwaysFloatLabel,placeholder)]]" auto-validate$="[[autoValidate]]" disabled$="[[disabled]]" invalid="[[invalid]]">

      <label hidden$="[[!label]]" aria-hidden="true" for$="[[_inputId]]" slot="label">[[label]]</label>

      <iron-autogrow-textarea class="paper-input-input" slot="input" id$="[[_inputId]]" aria-labelledby$="[[_ariaLabelledBy]]" aria-describedby$="[[_ariaDescribedBy]]" bind-value="{{value}}" invalid="{{invalid}}" validator$="[[validator]]" disabled$="[[disabled]]" autocomplete$="[[autocomplete]]" autofocus$="[[autofocus]]" inputmode$="[[inputmode]]" name$="[[name]]" placeholder$="[[placeholder]]" readonly$="[[readonly]]" required$="[[required]]" minlength$="[[minlength]]" maxlength$="[[maxlength]]" autocapitalize$="[[autocapitalize]]" rows$="[[rows]]" max-rows$="[[maxRows]]" on-change="_onChange"></iron-autogrow-textarea>

      <template is="dom-if" if="[[errorMessage]]">
        <paper-input-error aria-live="assertive" slot="add-on">[[errorMessage]]</paper-input-error>
      </template>

      <template is="dom-if" if="[[charCounter]]">
        <paper-input-char-counter slot="add-on"></paper-input-char-counter>
      </template>

    </paper-input-container>
`,is:"paper-textarea",behaviors:[p.d0,s.V],properties:{_ariaLabelledBy:{observer:"_ariaLabelledByChanged",type:String},_ariaDescribedBy:{observer:"_ariaDescribedByChanged",type:String},value:{type:String},rows:{type:Number,value:1},maxRows:{type:Number,value:0}},get selectionStart(){return this.$.input.textarea.selectionStart},set selectionStart(e){this.$.input.textarea.selectionStart=e},get selectionEnd(){return this.$.input.textarea.selectionEnd},set selectionEnd(e){this.$.input.textarea.selectionEnd=e},_ariaLabelledByChanged:function(e){this._focusableElement.setAttribute("aria-labelledby",e)},_ariaDescribedByChanged:function(e){this._focusableElement.setAttribute("aria-describedby",e)},get _focusableElement(){return this.inputElement.textarea}})},25782:(e,t,a)=>{a(56299),a(65660),a(70019),a(97968);var i=a(9672),r=a(50856),o=a(33760);(0,i.k)({_template:r.d`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[o.U]})},33760:(e,t,a)=>{a.d(t,{U:()=>o});a(56299);var i=a(51644),r=a(26110);const o=[i.P,r.a,{hostAttributes:{role:"option",tabindex:"0"}}]},89194:(e,t,a)=>{a(56299),a(65660),a(70019);var i=a(9672),r=a(50856);(0,i.k)({_template:r.d`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"})},97968:(e,t,a)=>{a(65660),a(70019);const i=document.createElement("template");i.setAttribute("style","display: none;"),i.innerHTML="<dom-module id=\"paper-item-shared-styles\">\n  <template>\n    <style>\n      :host, .paper-item {\n        display: block;\n        position: relative;\n        min-height: var(--paper-item-min-height, 48px);\n        padding: 0px 16px;\n      }\n\n      .paper-item {\n        @apply --paper-font-subhead;\n        border:none;\n        outline: none;\n        background: white;\n        width: 100%;\n        text-align: left;\n      }\n\n      :host([hidden]), .paper-item[hidden] {\n        display: none !important;\n      }\n\n      :host(.iron-selected), .paper-item.iron-selected {\n        font-weight: var(--paper-item-selected-weight, bold);\n\n        @apply --paper-item-selected;\n      }\n\n      :host([disabled]), .paper-item[disabled] {\n        color: var(--paper-item-disabled-color, var(--disabled-text-color));\n\n        @apply --paper-item-disabled;\n      }\n\n      :host(:focus), .paper-item:focus {\n        position: relative;\n        outline: 0;\n\n        @apply --paper-item-focused;\n      }\n\n      :host(:focus):before, .paper-item:focus:before {\n        @apply --layout-fit;\n\n        background: currentColor;\n        content: '';\n        opacity: var(--dark-divider-opacity);\n        pointer-events: none;\n\n        @apply --paper-item-focused-before;\n      }\n    </style>\n  </template>\n</dom-module>",document.head.appendChild(i.content)},53973:(e,t,a)=>{a(56299),a(65660),a(97968);var i=a(9672),r=a(50856),o=a(33760);(0,i.k)({_template:r.d`
    <style include="paper-item-shared-styles">
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
      }
    </style>
    <slot></slot>
`,is:"paper-item",behaviors:[o.U]})},51095:(e,t,a)=>{a(56299);var i=a(23823),r=a(9672),o=a(50856);(0,r.k)({_template:o.d`
    <style>
      :host {
        display: block;
        padding: 8px 0;

        background: var(--paper-listbox-background-color, var(--primary-background-color));
        color: var(--paper-listbox-color, var(--primary-text-color));

        @apply --paper-listbox;
      }
    </style>

    <slot></slot>
`,is:"paper-listbox",behaviors:[i.i],hostAttributes:{role:"listbox"}})},81563:(e,t,a)=>{a.d(t,{E_:()=>y,OR:()=>l,_Y:()=>p,fk:()=>d,hN:()=>n,hl:()=>c,i9:()=>h,pt:()=>o,ws:()=>m});var i=a(15304);const{I:r}=i.Al,o=e=>null===e||"object"!=typeof e&&"function"!=typeof e,n=(e,t)=>void 0===t?void 0!==(null==e?void 0:e._$litType$):(null==e?void 0:e._$litType$)===t,l=e=>void 0===e.strings,s=()=>document.createComment(""),p=(e,t,a)=>{var i;const o=e._$AA.parentNode,n=void 0===t?e._$AB:t._$AA;if(void 0===a){const t=o.insertBefore(s(),n),i=o.insertBefore(s(),n);a=new r(t,i,e,e.options)}else{const t=a._$AB.nextSibling,r=a._$AM,l=r!==e;if(l){let t;null===(i=a._$AQ)||void 0===i||i.call(a,e),a._$AM=e,void 0!==a._$AP&&(t=e._$AU)!==r._$AU&&a._$AP(t)}if(t!==n||l){let e=a._$AA;for(;e!==t;){const t=e.nextSibling;o.insertBefore(e,n),e=t}}}return a},d=(e,t,a=e)=>(e._$AI(t,a),e),u={},c=(e,t=u)=>e._$AH=t,h=e=>e._$AH,m=e=>{var t;null===(t=e._$AP)||void 0===t||t.call(e,!1,!0);let a=e._$AA;const i=e._$AB.nextSibling;for(;a!==i;){const e=a.nextSibling;a.remove(),a=e}},y=e=>{e._$AR()}},57835:(e,t,a)=>{a.d(t,{XM:()=>i.XM,Xe:()=>i.Xe,pX:()=>i.pX});var i=a(38941)},34990:(e,t,a)=>{a.d(t,{l:()=>n});var i=a(15304),r=a(38941);const o={},n=(0,r.XM)(class extends r.Xe{constructor(){super(...arguments),this.ot=o}render(e,t){return t()}update(e,[t,a]){if(Array.isArray(t)){if(Array.isArray(this.ot)&&this.ot.length===t.length&&t.every(((e,t)=>e===this.ot[t])))return i.Jb}else if(this.ot===t)return i.Jb;return this.ot=Array.isArray(t)?Array.from(t):t,this.render(t,a)}})},18848:(e,t,a)=>{a.d(t,{r:()=>l});var i=a(15304),r=a(38941),o=a(81563);const n=(e,t,a)=>{const i=new Map;for(let r=t;r<=a;r++)i.set(e[r],r);return i},l=(0,r.XM)(class extends r.Xe{constructor(e){if(super(e),e.type!==r.pX.CHILD)throw Error("repeat() can only be used in text expressions")}ht(e,t,a){let i;void 0===a?a=t:void 0!==t&&(i=t);const r=[],o=[];let n=0;for(const t of e)r[n]=i?i(t,n):n,o[n]=a(t,n),n++;return{values:o,keys:r}}render(e,t,a){return this.ht(e,t,a).values}update(e,[t,a,r]){var l;const s=(0,o.i9)(e),{values:p,keys:d}=this.ht(t,a,r);if(!Array.isArray(s))return this.ut=d,p;const u=null!==(l=this.ut)&&void 0!==l?l:this.ut=[],c=[];let h,m,y=0,v=s.length-1,b=0,f=p.length-1;for(;y<=v&&b<=f;)if(null===s[y])y++;else if(null===s[v])v--;else if(u[y]===d[b])c[b]=(0,o.fk)(s[y],p[b]),y++,b++;else if(u[v]===d[f])c[f]=(0,o.fk)(s[v],p[f]),v--,f--;else if(u[y]===d[f])c[f]=(0,o.fk)(s[y],p[f]),(0,o._Y)(e,c[f+1],s[y]),y++,f--;else if(u[v]===d[b])c[b]=(0,o.fk)(s[v],p[b]),(0,o._Y)(e,s[y],s[v]),v--,b++;else if(void 0===h&&(h=n(d,b,f),m=n(u,y,v)),h.has(u[y]))if(h.has(u[v])){const t=m.get(d[b]),a=void 0!==t?s[t]:null;if(null===a){const t=(0,o._Y)(e,s[y]);(0,o.fk)(t,p[b]),c[b]=t}else c[b]=(0,o.fk)(a,p[b]),(0,o._Y)(e,s[y],a),s[t]=null;b++}else(0,o.ws)(s[v]),v--;else(0,o.ws)(s[y]),y++;for(;b<=f;){const t=(0,o._Y)(e,c[f+1]);(0,o.fk)(t,p[b]),c[b++]=t}for(;y<=v;){const e=s[y++];null!==e&&(0,o.ws)(e)}return this.ut=d,(0,o.hl)(e,c),i.Jb}})}}]);
//# sourceMappingURL=84575-qCITP6jPRbU.js.map