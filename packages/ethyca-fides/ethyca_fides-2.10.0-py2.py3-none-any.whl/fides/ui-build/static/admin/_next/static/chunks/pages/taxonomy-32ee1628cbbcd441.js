(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[4202],{96356:function(e,t,n){"use strict";n.d(t,{SD:function(){return m},Sn:function(){return c},Vp:function(){return u}});var r=n(10894),i=n(81439),a=n(15031),s=n(67294);function o(){return o=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},o.apply(this,arguments)}var l=["isDisabled","children"],u=(0,i.Gp)((function(e,t){var n=(0,i.jC)("Tag",e),r=(0,i.Lr)(e),a=o({display:"inline-flex",verticalAlign:"top",alignItems:"center",maxWidth:"100%"},n.container);return s.createElement(i.Fo,{value:n},s.createElement(i.m$.span,o({ref:t},r,{__css:a})))}));a.Ts&&(u.displayName="Tag");var c=(0,i.Gp)((function(e,t){var n=(0,i.yK)();return s.createElement(i.m$.span,o({ref:t,isTruncated:!0},e,{__css:n.label}))}));a.Ts&&(c.displayName="TagLabel");var d=(0,i.Gp)((function(e,t){return s.createElement(r.JO,o({ref:t,verticalAlign:"top",marginEnd:"0.5rem"},e))}));a.Ts&&(d.displayName="TagLeftIcon");var f=(0,i.Gp)((function(e,t){return s.createElement(r.JO,o({ref:t,verticalAlign:"top",marginStart:"0.5rem"},e))}));a.Ts&&(f.displayName="TagRightIcon");var p=function(e){return s.createElement(r.JO,o({verticalAlign:"inherit",viewBox:"0 0 512 512"},e),s.createElement("path",{fill:"currentColor",d:"M289.94 256l95-95A24 24 0 00351 127l-95 95-95-95a24 24 0 00-34 34l95 95-95 95a24 24 0 1034 34l95-95 95 95a24 24 0 0034-34z"}))};a.Ts&&(p.displayName="TagCloseIcon");var m=function(e){var t=e.isDisabled,n=e.children,r=function(e,t){if(null==e)return{};var n,r,i={},a=Object.keys(e);for(r=0;r<a.length;r++)n=a[r],t.indexOf(n)>=0||(i[n]=e[n]);return i}(e,l),a=o({display:"flex",alignItems:"center",justifyContent:"center",outline:"0"},(0,i.yK)().closeButton);return s.createElement(i.m$.button,o({"aria-label":"close"},r,{type:"button",disabled:t,__css:a}),n||s.createElement(p,null))};a.Ts&&(m.displayName="TagCloseButton")},77046:function(e,t,n){"use strict";var r=n(59499),i=n(4730),a=n(96356),s=n(85893),o=["name","onClose"];function l(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function u(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?l(Object(n),!0).forEach((function(t){(0,r.Z)(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):l(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}t.Z=function(e){var t=e.name,n=e.onClose,r=(0,i.Z)(e,o),l=u({backgroundColor:"primary.400",color:"white","data-testid":"taxonomy-entity-".concat(t),width:"fit-content",size:"sm"},r);return n?(0,s.jsxs)(a.Vp,u(u({display:"flex",justifyContent:"space-between"},l),{},{children:[(0,s.jsx)(a.Sn,{children:t}),(0,s.jsx)(a.SD,{onClick:n,color:"white"})]})):(0,s.jsx)(a.Vp,u(u({},l),{},{children:t}))}},45009:function(e,t,n){"use strict";n.d(t,{C:function(){return r},P:function(){return i}});var r=function e(t,n){var r;if(null==n&&t.every((function(e){return void 0===e.parent_key})))r=t;else{var i=null!==n&&void 0!==n?n:null;r=t.filter((function(e){return e.parent_key===i}))}return r.map((function(n){var r,i=n.fides_key;return{value:n.fides_key,label:""===n.name||null==n.name?n.fides_key:n.name,description:n.description,children:e(t,i),is_default:null!==(r=n.is_default)&&void 0!==r&&r}}))},i=function(e){var t=e.split(".");return 1===t.length?"":t.slice(0,t.length-1).join(".")}},10272:function(e,t,n){"use strict";n.r(t),n.d(t,{default:function(){return Q}});var r=n(68527),i=n(48057),a=n(15193),s=n(97142),o=n(52313),l=n(50029),u=n(16835),c=n(59499),d=n(87794),f=n.n(d),p=n(67294),m=n(25646),y=n(24524),v=n(7045),x=n(64656),g=n(96016),b=n(65698),h=n(29482),_=n(44116),j=n(45009),k=n(58183),E=n(85893);function O(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function w(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?O(Object(n),!0).forEach((function(t){(0,c.Z)(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):O(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}var T=function(e,t){var n,r,i,a,s;return{fides_key:null!==(n=e.fides_key)&&void 0!==n?n:"",name:null!==(r=e.name)&&void 0!==r?r:"",description:null!==(i=e.description)&&void 0!==i?i:"",parent_key:null!==(a=e.parent_key)&&void 0!==a?a:"",is_default:null!==(s=e.is_default)&&void 0!==s&&s,customFieldValues:t}},C=function(e,t){var n=""===e.fides_key,r=w({},t);if(n){var i=(0,j.P)(t.fides_key);r.parent_key=""===i?void 0:i}else r.parent_key=""===e.parent_key?void 0:e.parent_key,r.fides_key=e.fides_key;return delete r.customFieldValues,r},D=n(96356),P=n(97375),F=n(28609),S=n(49609),Z=n(94090);function z(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function A(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?z(Object(n),!0).forEach((function(t){(0,c.Z)(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):z(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}var M=function(e){var t=e.nodes,n=e.focusedKey,i=e.renderHover,a=e.renderTag,s=(0,p.useState)(void 0),o=s[0],l=s[1],u=function e(t){var s=arguments.length>1&&void 0!==arguments[1]?arguments[1]:0,u=(null===o||void 0===o?void 0:o.value)===t.value,c=n===t.value,d={borderBottom:"1px solid",borderColor:"gray.200",display:"flex",justifyContent:"space-between",alignItems:"center",pl:3*s,_hover:{bg:"gray.50"},onMouseEnter:function(){l(t)},onMouseLeave:function(){l(void 0)}},f=u&&i?i(t):null;return 0===t.children.length?(0,E.jsxs)(r.xu,A(A({py:2},d),{},{"data-testid":"item-".concat(t.label),children:[(0,E.jsxs)(r.xu,{display:"flex",alignItems:"center",children:[(0,E.jsx)(r.xv,{pl:5,color:c?"complimentary.500":void 0,mr:2,children:t.label}),a?a(t):null]}),f]})):(0,E.jsxs)(Z.Qd,{p:0,border:"none","data-testid":"accordion-item-".concat(t.label),children:[(0,E.jsxs)(r.xu,A(A({},d),{},{children:[(0,E.jsxs)(Z.KF,{_expanded:{color:"complimentary.500"},_hover:{bg:"gray.50"},pl:0,color:c?"complimentary.500":void 0,children:[(0,E.jsx)(Z.XE,{}),(0,E.jsx)(r.xv,{mr:2,children:t.label}),a?a(t):null]}),f]})),(0,E.jsx)(Z.Hk,{p:0,children:t.children.map((function(t){return(0,E.jsx)(p.Fragment,{children:e(t,s+1)},t.value)}))})]})};return(0,E.jsx)(r.xu,{boxSizing:"border-box",children:(0,E.jsx)(Z.UQ,{allowMultiple:!0,children:t.map((function(e){return(0,E.jsx)(r.xu,{children:u(e)},e.value)}))})})},V=n(58144),K=n(10846),L=n(26595),I=function(e){var t=e.node,n=e.onEdit,r=e.onDelete,i=!t.is_default;return(0,E.jsxs)(a.hE,{size:"xs",isAttached:!0,variant:"outline","data-testid":"action-btns",mr:"2",children:[(0,E.jsx)(a.zx,{"data-testid":"edit-btn",onClick:function(){return n(t)},children:"Edit"}),i?(0,E.jsx)(a.zx,{"data-testid":"delete-btn",onClick:function(){return r(t)},children:"Delete"}):null]})},N=n(79762),G=n(4612),R=n(82175),X=n(74231),B=n(77046),U=function(e){var t=e.labels,n=e.onCancel,i=e.onSubmit,s=e.renderExtraFormFields,o=e.initialValues,u=(0,F.pm)(),c=(0,p.useState)(null),d=c[0],m=c[1],y=X.Ry().shape({fides_key:X.Z_().required().label(t.fides_key)}),v=""===o.fides_key,x=function(e){var t=(0,b.nU)(e);m(t.message)},h=function(){var e=(0,l.Z)(f().mark((function e(t){var r;return f().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return m(null),e.next=3,i(o,t);case 3:r=e.sent,(0,b.D4)(r)?x(r.error):(u((0,K.t5)("Taxonomy successfully ".concat(v?"created":"updated"))),v&&n());case 5:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}();return(0,E.jsxs)(r.Kq,{pl:6,spacing:6,"data-testid":"".concat(v?"create":"edit","-taxonomy-form"),children:[(0,E.jsxs)(r.X6,{size:"md",textTransform:"capitalize","data-testid":"form-heading",children:[v?"Create":"Modify"," ",t.fides_key]}),(0,E.jsx)(R.J9,{initialValues:o,onSubmit:h,validationSchema:y,enableReinitialize:!0,children:function(e){var i=e.dirty,l=e.values;return(0,E.jsxs)(R.l0,{children:[(0,E.jsxs)(r.Kq,{mb:6,children:[v?(0,E.jsx)(g.j0,{name:"fides_key",label:t.fides_key}):(0,E.jsxs)(r.rj,{templateColumns:"1fr 3fr",children:[(0,E.jsx)(N.lX,{children:t.fides_key}),(0,E.jsx)(r.xu,{children:(0,E.jsx)(B.Z,{name:o.fides_key})})]}),(0,E.jsx)(g.j0,{name:"name",label:t.name}),(0,E.jsx)(g.Ks,{name:"description",label:t.description}),t.parent_key&&(v?(0,E.jsxs)(r.rj,{templateColumns:"1fr 3fr",children:[(0,E.jsx)(N.lX,{children:t.parent_key}),(0,E.jsx)(r.xu,{mr:"2",children:(0,E.jsx)(G.II,{"data-testid":"input-parent_key",disabled:!0,value:(0,j.P)(l.fides_key),size:"sm"})})]}):(0,E.jsx)(g.j0,{name:"parent_key",label:t.parent_key,disabled:!v})),s?s(l):null]}),d?(0,E.jsx)(r.xv,{color:"red",mb:2,"data-testid":"taxonomy-form-error",children:d}):null,(0,E.jsxs)(a.hE,{size:"sm",children:[(0,E.jsx)(a.zx,{"data-testid":"cancel-btn",variant:"outline",onClick:n,children:"Cancel"}),(0,E.jsx)(a.zx,{"data-testid":"submit-btn",variant:"primary",type:"submit",disabled:!v&&!i,children:v?"Create entity":"Update entity"})]})]})}})]})},q=function(e){var t=e.node;return t.is_default?null:(0,E.jsx)(D.Vp,{backgroundColor:"gray.500",color:"white",size:"sm",height:"fit-content","data-testid":"custom-tag-".concat(t.label),children:"Custom"})},H={fides_key:"",parent_key:"",name:"",description:""},J=function(e){var t=e.useTaxonomy,n=(0,s.T)(),i=t(),a=i.isLoading,o=i.data,u=i.labels,c=i.entityToEdit,d=i.setEntityToEdit,m=i.handleCreate,y=i.handleEdit,v=i.handleDelete,x=i.renderExtraFormFields,g=i.transformEntityToInitialValues,h=(0,p.useMemo)((function(){return o?(0,j.C)(o):null}),[o]),_=(0,p.useState)(null),O=_[0],w=_[1],T=(0,s.C)(k.yK);(0,p.useEffect)((function(){T&&d(null)}),[T,d]);var C=function(){n((0,k.Gz)(!1))},D=(0,P.qY)(),Z=D.isOpen,z=D.onOpen,A=D.onClose,N=(0,F.pm)();if(a)return(0,E.jsx)(r.M5,{children:(0,E.jsx)(S.$,{})});if(!h)return(0,E.jsx)(r.xv,{children:"Could not find data."});var G=u.fides_key.toLocaleLowerCase(),R=function(e){var t;T&&C();var n=null!==(t=null===o||void 0===o?void 0:o.find((function(t){return t.fides_key===e.value})))&&void 0!==t?t:null;d(n)},X=function(e){w(e),z()},B=function(){var e=(0,l.Z)(f().mark((function e(){var t;return f().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(!O){e.next=7;break}return e.next=3,v(O.value);case 3:t=e.sent,(0,L.isErrorResult)(t)?N((0,K.Vo)((0,b.e$)(t.error))):N((0,K.t5)("Successfully deleted ".concat(G))),A(),d(null);case 7:case"end":return e.stop()}}),e)})));return function(){return e.apply(this,arguments)}}();return(0,E.jsxs)(E.Fragment,{children:[(0,E.jsxs)(r.MI,{columns:2,spacing:2,children:[(0,E.jsx)(M,{nodes:h,focusedKey:null===c||void 0===c?void 0:c.fides_key,renderHover:function(e){return(0,E.jsx)(I,{onDelete:X,onEdit:R,node:e})},renderTag:function(e){return(0,E.jsx)(q,{node:e})}}),c?(0,E.jsx)(U,{labels:u,onCancel:function(){return d(null)},onSubmit:y,renderExtraFormFields:x,initialValues:g(c)}):null,T?(0,E.jsx)(U,{labels:u,onCancel:C,onSubmit:m,renderExtraFormFields:x,initialValues:g(H)}):null]}),O?(0,E.jsx)(V.Z,{isOpen:Z,onClose:A,onConfirm:B,title:"Delete ".concat(G),message:(0,E.jsxs)(r.Kq,{children:[(0,E.jsxs)(r.xv,{children:["You are about to permanently delete the ",G," ",(0,E.jsx)(r.xv,{color:"complimentary.500",as:"span",fontWeight:"bold",children:O.value})," ","from your taxonomy. Are you sure you would like to continue?"]}),O.children.length?(0,E.jsxs)(r.xv,{color:"red","data-testid":"delete-children-warning",children:["Deleting"," ",(0,E.jsx)(r.xv,{as:"span",fontWeight:"bold",children:O.value})," ","will also delete all of its children."]}):null]})}):null]})},$=[{label:"Data Categories",content:(0,E.jsx)(J,{useTaxonomy:function(){var e=v.P6.DATA_CATEGORY,t=(0,p.useState)(null),n=t[0],r=t[1],i=(0,k.MO)(),a=i.data,s=i.isLoading,o=(0,k.Ti)(),c=(0,u.Z)(o,1)[0],d=(0,k.jU)(),x=(0,u.Z)(d,1)[0],g=(0,k.K9)(),b=(0,u.Z)(g,1)[0],h=(0,y.m)({resourceFidesKey:null===n||void 0===n?void 0:n.fides_key,resourceType:e}),_=function(){var e=(0,l.Z)(f().mark((function e(t,n){var r,i;return f().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return r=C(t,n),e.next=3,c(r);case 3:if(i=e.sent,!h.isEnabled){e.next=7;break}return e.next=7,h.upsertCustomFields(n);case 7:return e.abrupt("return",i);case 8:case"end":return e.stop()}}),e)})));return function(t,n){return e.apply(this,arguments)}}(),j=function(){var e=(0,l.Z)(f().mark((function e(t,n){var r,i;return f().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(r=C(t,n),i=x(r),!h.isEnabled){e.next=5;break}return e.next=5,h.upsertCustomFields(n);case 5:return e.abrupt("return",i);case 6:case"end":return e.stop()}}),e)})));return function(t,n){return e.apply(this,arguments)}}();return{data:a,isLoading:s,labels:{fides_key:"Data category",name:"Category name",description:"Category description",parent_key:"Parent category"},resourceType:e,entityToEdit:n,setEntityToEdit:r,handleCreate:_,handleEdit:j,handleDelete:b,renderExtraFormFields:function(t){return(0,E.jsx)(m.uc,{resourceFidesKey:t.fides_key,resourceType:e})},transformEntityToInitialValues:function(e){return T(e,h.customFieldValues)}}}})},{label:"Data Uses",content:(0,E.jsx)(J,{useTaxonomy:function(){var e=v.P6.DATA_USE,t=(0,p.useState)(null),n=t[0],r=t[1],i=(0,_.fd)(),a=i.data,s=i.isLoading,o={fides_key:"Data use",name:"Data use name",description:"Data use description",parent_key:"Parent data use",legal_basis:"Legal basis",special_category:"Special category",recipient:"Recipient",legitimate_interest:"Legitimate interest",legitimate_interest_impact_assessment:"Legitimate interest impact assessment"},c=(0,_.Ql)(),d=(0,u.Z)(c,1)[0],h=(0,_.LG)(),j=(0,u.Z)(h,1)[0],k=(0,_.gu)(),O=(0,u.Z)(k,1)[0],D=function(e){var t,n,r;return w(w({},e),{},{legitimate_interest_impact_assessment:""===e.legitimate_interest_impact_assessment?void 0:e.legitimate_interest_impact_assessment,legitimate_interest:!("true"!==(null===(t=e.legitimate_interest)||void 0===t?void 0:t.toString())),legal_basis:""===(null===(n=e.legal_basis)||void 0===n?void 0:n.toString())?void 0:e.legal_basis,special_category:""===(null===(r=e.special_category)||void 0===r?void 0:r.toString())?void 0:e.special_category})},P=(0,y.m)({resourceFidesKey:null===n||void 0===n?void 0:n.fides_key,resourceType:e}),F=function(){var e=(0,l.Z)(f().mark((function e(t,n){var r,i;return f().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return r=D(C(t,n)),e.next=3,d(r);case 3:if(i=e.sent,!P.isEnabled){e.next=7;break}return e.next=7,P.upsertCustomFields(n);case 7:return e.abrupt("return",i);case 8:case"end":return e.stop()}}),e)})));return function(t,n){return e.apply(this,arguments)}}(),S=function(){var e=(0,l.Z)(f().mark((function e(t,n){var r,i;return f().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(r=D(C(t,n)),i=j(r),!P.isEnabled){e.next=5;break}return e.next=5,P.upsertCustomFields(n);case 5:return e.abrupt("return",i);case 6:case"end":return e.stop()}}),e)})));return function(t,n){return e.apply(this,arguments)}}(),Z=O,z=(0,b.MM)(v.cc),A=(0,b.MM)(v.pj);return{data:a,isLoading:s,labels:o,resourceType:e,entityToEdit:n,setEntityToEdit:r,handleCreate:F,handleEdit:S,handleDelete:Z,renderExtraFormFields:function(t){var n;return(0,E.jsxs)(E.Fragment,{children:[(0,E.jsx)(g.AP,{name:"legal_basis",label:o.legal_basis,options:z,isClearable:!0}),(0,E.jsx)(g.AP,{name:"special_category",label:o.special_category,options:A,isClearable:!0}),(0,E.jsx)(g.VT,{name:"recipients",label:o.recipient,options:[],size:"sm",disableMenu:!0,isMulti:!0}),(0,E.jsx)(g.xt,{name:"legitimate_interest",label:o.legitimate_interest,options:x.H}),"true"===(null===(n=t.legitimate_interest)||void 0===n?void 0:n.toString())?(0,E.jsx)(g.j0,{name:"legitimate_interest_impact_assessment",label:o.legitimate_interest_impact_assessment}):null,(0,E.jsx)(m.uc,{resourceFidesKey:t.fides_key,resourceType:e})]})},transformEntityToInitialValues:function(e){var t,n;return w(w({},T(e,P.customFieldValues)),{},{legal_basis:e.legal_basis,special_category:e.special_category,recipients:null!==(t=e.recipients)&&void 0!==t?t:[],legitimate_interest:null==e.legitimate_interest?"false":e.legitimate_interest.toString(),legitimate_interest_impact_assessment:null!==(n=e.legitimate_interest_impact_assessment)&&void 0!==n?n:""})}}}})},{label:"Data Subjects",content:(0,E.jsx)(J,{useTaxonomy:function(){var e=v.P6.DATA_SUBJECT,t=(0,p.useState)(null),n=t[0],r=t[1],i=(0,h.te)(),a=i.data,s=i.isLoading,o={fides_key:"Data subject",name:"Data subject name",description:"Data subject description",rights:"Rights",strategy:"Strategy",automatic_decisions:"Automatic decisions or profiling"},c=(0,h.wG)(),d=(0,u.Z)(c,1)[0],_=(0,h.h8)(),j=(0,u.Z)(_,1)[0],k=(0,h.Kv)(),O=(0,u.Z)(k,1)[0],D=function(e){var t,n=w(w({},e),{},{rights:e.rights.length?{values:e.rights,strategy:e.strategy}:void 0,automatic_decisions_or_profiling:!("true"!==(null===(t=e.automated_decisions_or_profiling)||void 0===t?void 0:t.toString()))});return delete n.strategy,n},P=(0,y.m)({resourceFidesKey:null===n||void 0===n?void 0:n.fides_key,resourceType:e}),F=function(){var e=(0,l.Z)(f().mark((function e(t,n){var r,i;return f().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return r=D(C(t,n)),e.next=3,d(r);case 3:if(i=e.sent,!P.isEnabled){e.next=7;break}return e.next=7,P.upsertCustomFields(n);case 7:return e.abrupt("return",i);case 8:case"end":return e.stop()}}),e)})));return function(t,n){return e.apply(this,arguments)}}(),S=function(){var e=(0,l.Z)(f().mark((function e(t,n){var r,i;return f().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(r=D(C(t,n)),i=j(r),!P.isEnabled){e.next=5;break}return e.next=5,P.upsertCustomFields(n);case 5:return e.abrupt("return",i);case 6:case"end":return e.stop()}}),e)})));return function(t,n){return e.apply(this,arguments)}}();return{data:a,isLoading:s,labels:o,resourceType:e,entityToEdit:n,setEntityToEdit:r,handleCreate:F,handleEdit:S,handleDelete:O,renderExtraFormFields:function(t){return(0,E.jsxs)(E.Fragment,{children:[(0,E.jsx)(g.AP,{name:"rights",label:o.rights,options:(0,b.MM)(v.ts),isMulti:!0}),t.rights&&t.rights.length?(0,E.jsx)(g.AP,{name:"strategy",label:o.strategy,options:(0,b.MM)(v.jX)}):null,(0,E.jsx)(g.xt,{name:"automatic_decisions_or_profiling",label:o.automatic_decisions,options:x.H}),(0,E.jsx)(m.uc,{resourceFidesKey:t.fides_key,resourceType:e})]})},transformEntityToInitialValues:function(e){var t,n,r;return w(w({},T(e,P.customFieldValues)),{},{rights:null!==(t=null===(n=e.rights)||void 0===n?void 0:n.values)&&void 0!==t?t:[],strategy:null===(r=e.rights)||void 0===r?void 0:r.strategy,automatic_decisions_or_profiling:null==e.automated_decisions_or_profiling?"false":e.automated_decisions_or_profiling.toString()})}}}})}],W=function(){var e=(0,s.T)();return(0,E.jsxs)(r.xu,{"data-testid":"taxonomy-tabs",display:"flex",children:[(0,E.jsx)(o.Z,{border:"full-width",data:$,flexGrow:1,isLazy:!0}),(0,E.jsx)(r.xu,{borderBottom:"2px solid",borderColor:"gray.200",height:"fit-content",pr:"2",pb:"2",children:(0,E.jsx)(a.zx,{size:"sm",variant:"outline",onClick:function(){e((0,k.Gz)(!0))},"data-testid":"add-taxonomy-btn",children:"Add Taxonomy Entity +"})})]})},Q=function(){return(0,E.jsxs)(i.Z,{title:"Datasets",children:[(0,E.jsx)(r.X6,{mb:2,fontSize:"2xl",fontWeight:"semibold",children:"Taxonomy Management"}),(0,E.jsx)(W,{})]})}},26595:function(e,t,n){"use strict";n.d(t,{isAPIError:function(){return r.Bw},isErrorResult:function(){return r.D4}});var r=n(27396)},66199:function(e,t,n){(window.__NEXT_P=window.__NEXT_P||[]).push(["/taxonomy",function(){return n(10272)}])}},function(e){e.O(0,[5630,3206,4231,6114,1012,8057,7080,4197,9774,2888,179],(function(){return t=66199,e(e.s=t);var t}));var t=e.O();_N_E=t}]);