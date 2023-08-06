/*! For license information please see 61231-Qr0C5dGpxh8.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[61231],{14095:(e,t,i)=>{i(56299),i(65660);var r=i(26110),a=i(98235),o=i(9672),n=i(87156),s=i(50856);(0,o.k)({_template:s.d`
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
`,is:"iron-autogrow-textarea",behaviors:[a.x,r.a],properties:{value:{observer:"_valueChanged",type:String,notify:!0},bindValue:{observer:"_bindValueChanged",type:String,notify:!0},rows:{type:Number,value:1,observer:"_updateCached"},maxRows:{type:Number,value:0,observer:"_updateCached"},autocomplete:{type:String,value:"off"},autofocus:{type:Boolean,value:!1},autocapitalize:{type:String,value:"none"},inputmode:{type:String},placeholder:{type:String},readonly:{type:String},required:{type:Boolean},minlength:{type:Number},maxlength:{type:Number},label:{type:String}},listeners:{input:"_onInput"},get textarea(){return this.$.textarea},get selectionStart(){return this.$.textarea.selectionStart},get selectionEnd(){return this.$.textarea.selectionEnd},set selectionStart(e){this.$.textarea.selectionStart=e},set selectionEnd(e){this.$.textarea.selectionEnd=e},attached:function(){navigator.userAgent.match(/iP(?:[oa]d|hone)/)&&!navigator.userAgent.match(/OS 1[3456789]/)&&(this.$.textarea.style.marginLeft="-3px")},validate:function(){var e=this.$.textarea.validity.valid;return e&&(this.required&&""===this.value?e=!1:this.hasValidator()&&(e=a.x.validate.call(this,this.value))),this.invalid=!e,this.fire("iron-input-validate"),e},_bindValueChanged:function(e){this.value=e},_valueChanged:function(e){var t=this.textarea;t&&(t.value!==e&&(t.value=e||0===e?e:""),this.bindValue=e,this.$.mirror.innerHTML=this._valueForMirror(),this.fire("bind-value-changed",{value:this.bindValue}))},_onInput:function(e){var t=(0,n.vz)(e).path;this.value=t?t[0].value:e.target.value},_constrain:function(e){var t;for(e=e||[""],t=this.maxRows>0&&e.length>this.maxRows?e.slice(0,this.maxRows):e.slice(0);this.rows>0&&t.length<this.rows;)t.push("");return t.join("<br/>")+"&#160;"},_valueForMirror:function(){var e=this.textarea;if(e)return this.tokens=e&&e.value?e.value.replace(/&/gm,"&amp;").replace(/"/gm,"&quot;").replace(/'/gm,"&#39;").replace(/</gm,"&lt;").replace(/>/gm,"&gt;").split("\n"):[""],this._constrain(this.tokens)},_updateCached:function(){this.$.mirror.innerHTML=this._constrain(this.tokens)}});i(2178),i(98121),i(65911);var l=i(21006),d=i(66668);(0,o.k)({_template:s.d`
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
`,is:"paper-textarea",behaviors:[d.d0,l.V],properties:{_ariaLabelledBy:{observer:"_ariaLabelledByChanged",type:String},_ariaDescribedBy:{observer:"_ariaDescribedByChanged",type:String},value:{type:String},rows:{type:Number,value:1},maxRows:{type:Number,value:0}},get selectionStart(){return this.$.input.textarea.selectionStart},set selectionStart(e){this.$.input.textarea.selectionStart=e},get selectionEnd(){return this.$.input.textarea.selectionEnd},set selectionEnd(e){this.$.input.textarea.selectionEnd=e},_ariaLabelledByChanged:function(e){this._focusableElement.setAttribute("aria-labelledby",e)},_ariaDescribedByChanged:function(e){this._focusableElement.setAttribute("aria-describedby",e)},get _focusableElement(){return this.inputElement.textarea}})},54091:(e,t,i)=>{i.r(t),i.d(t,{HuiDialogReportProblemToAis:()=>v,ReportProblemToAisWs:()=>f});i(14271),i(63436),i(44577),i(53973),i(51095),i(14095);var r=i(68144),a=i(79932),o=(i(76870),i(34821)),n=i(11654);function s(){s=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var a=t.placement;if(t.kind===r&&("static"===a||"prototype"===a)){var o="static"===a?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],a={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,a)}),this),e.forEach((function(e){if(!p(e))return i.push(e);var t=this.decorateElement(e,a);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],a=e.decorators,o=a.length-1;o>=0;o--){var n=t[e.placement];n.splice(n.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,a[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var d=l.extras;if(d){for(var p=0;p<d.length;p++)this.addElementPlacement(d[p],t);i.push.apply(i,d)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var a=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(a)||a);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var n=0;n<e.length-1;n++)for(var s=n+1;s<e.length;s++)if(e[n].key===e[s].key&&e[n].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[n].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=h(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var a=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},a)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(a,"get","The property descriptor of a field descriptor"),this.disallowProperty(a,"set","The property descriptor of a field descriptor"),this.disallowProperty(a,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:u(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=u(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function l(e){var t,i=h(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function p(e){return e.decorators&&e.decorators.length}function c(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function u(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function h(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}const f=(e,t,i,r)=>e.callWS({type:"ais_cloud/report_ais_problem",problem_type:t,problem_desc:i,problem_data:r});let v=function(e,t,i,r){var a=s();if(r)for(var o=0;o<r.length;o++)a=r[o](a);var n=t((function(e){a.initializeInstanceElements(e,u.elements)}),i),u=a.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var a,o=e[r];if("method"===o.kind&&(a=t.find(i)))if(c(o.descriptor)||c(a.descriptor)){if(p(o)||p(a))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");a.descriptor=o.descriptor}else{if(p(o)){if(p(a))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");a.decorators=o.decorators}d(o,a)}else t.push(o)}return t}(n.d.map(l)),e);return a.initializeClassElements(n.F,u.elements),a.runClassFinishers(n.F,u.finishers)}([(0,a.Mo)("hui-dialog-report-problem-to-ais")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"_params",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"_loading",value:()=>!1},{kind:"field",decorators:[(0,a.Cb)()],key:"_problemDescription",value:()=>""},{kind:"field",decorators:[(0,a.Cb)()],key:"_aisAnswer",value:void 0},{kind:"field",key:"_aisMediaInfo",value:void 0},{kind:"method",key:"showDialog",value:function(e){this._params=e,this._aisMediaInfo=this.hass.states["media_player.wbudowany_glosnik"],this._aisAnswer=void 0,this._problemDescription=""}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,this._aisAnswer=void 0,this._problemDescription=""}},{kind:"method",key:"render",value:function(){var e,t,i,a,n;return this._params?r.dy` <ha-dialog open hideActions .heading="${(0,o.i)(this.hass,"Zgłoszenie problemu ze źródłem multimediów")}" @closed="${this.closeDialog}"> ${this._loading?r.dy`<ha-circular-progress active></ha-circular-progress>`:r.dy``} ${this._loading?r.dy` <p> Wysyłam zgłoszenie do AIS </p>`:r.dy`<p> Problem z odtwarzaniem ${null===(e=this._aisMediaInfo)||void 0===e?void 0:e.attributes.source}, <b></b>${null===(t=this._aisMediaInfo)||void 0===t?void 0:t.attributes.media_title} <span class="aisUrl"> <br>z adresu URL <ha-icon icon="mdi:web"></ha-icon>: <b></b>${null===(i=this._aisMediaInfo)||void 0===i?void 0:i.attributes.media_content_id} </span> </p> <div class="img404"><img src="${null===(a=this._aisMediaInfo)||void 0===a?void 0:a.attributes.media_stream_image}"></div> ${this._aisAnswer?r.dy` <div style="text-align:center"> ${this._aisAnswer.error?r.dy` <h2> Podczas przesyłania zgłoszenia wystąpił problem </h2> <p> ${null===(n=this._aisAnswer)||void 0===n?void 0:n.message} </p> <p> Sprawdz połączenie z Internetem i spróbuj ponownie później. </p> `:r.dy` <h2> Przesłano zgłoszenie do AIS, o numerze: ${this._aisAnswer.report_id} </h2> <p> ${this._aisAnswer.message} </p> `} </div> <div class="sendProblemToAisButton"> <mwc-button raised @click="${this.closeDialog}"> <ha-icon icon="hass:close-thick"></ha-icon>  OK </mwc-button> </div> `:r.dy` <p> Wyślij zgłoszenie do AI-Speaker. Postaramy się jak najszybciej naprawić ten problem. </p> <paper-textarea label="Dodatkowy opis dla AI-Speaker" placeholder="Tu możesz np. podać nowy adres zasobu, jeżeli go znasz." name="description" .value="${this._problemDescription}" @value-changed="${this._handleProblemDescriptionChange}"></paper-textarea> <div class="sendProblemToAisButton"> <mwc-button raised @click="${this._handleReportProblemToAis}"> <ha-icon icon="hass:email-send"></ha-icon>  Wyślij zgłoszenie do AI-Speaker </mwc-button> </div>`}`} </ha-dialog>`:r.dy``}},{kind:"method",key:"_reportProblemToAis",value:async function(){this._loading=!0;let e={message:"",email:"",report_id:0,error:!1};try{var t,i;e=await f(this.hass,"media_source",this._problemDescription,(null===(t=this._aisMediaInfo)||void 0===t?void 0:t.attributes.media_title)+" "+(null===(i=this._aisMediaInfo)||void 0===i?void 0:i.attributes.media_content_id))}catch(t){e.message=t.message,e.error=!0,this._loading=!1}return this._loading=!1,e}},{kind:"method",key:"_handleReportProblemToAis",value:async function(){this._aisAnswer=await this._reportProblemToAis()}},{kind:"method",key:"_handleProblemDescriptionChange",value:function(e){this._problemDescription=e.detail.value}},{kind:"get",static:!0,key:"styles",value:function(){return[n.yu,r.iv`ha-dialog{--dialog-content-padding:0 24px 20px}div.sendProblemToAisButton{text-align:center;margin:10px}div.img404{text-align:center}img{max-width:500px;max-height:300px;-webkit-filter:grayscale(100%);filter:grayscale(100%)}span.aisUrl{word-wrap:break-word}ha-circular-progress{--mdc-theme-primary:var(--primary-color);display:flex;justify-content:center;margin-top:40px;margin-bottom:20px}`]}}]}}),r.oi)}}]);
//# sourceMappingURL=61231-Qr0C5dGpxh8.js.map