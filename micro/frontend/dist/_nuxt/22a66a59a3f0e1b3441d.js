(window.webpackJsonp=window.webpackJsonp||[]).push([[5],{322:function(e,r,t){var content=t(329);"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,t(76).default)("571af42b",content,!0,{sourceMap:!1})},328:function(e,r,t){"use strict";var o=t(322);t.n(o).a},329:function(e,r,t){(r=t(75)(!1)).push([e.i,".login{width:50vw}",""]),e.exports=r},338:function(e,r,t){"use strict";t.r(r);t(24);var o=t(2),n={data:function(){return{ruleForm:{username:"",password:"",email:""},rules:{username:[{required:!0,message:"Please input username",trigger:"blur"},{min:3,max:35,message:"Length should be 3 to 5",trigger:"blur"}],password:[{required:!0,message:"Please input password",trigger:"blur"},{min:3,max:35,message:"Length should be 3 to 5",trigger:"blur"}],email:[{required:!0,message:"Please input password",trigger:"blur"},{type:"email",message:"Please enter a valid email address",trigger:"blur"}]}}},mounted:function(){if(window){var e=localStorage.getItem("mt-todo-token")||null,r=JSON.parse(localStorage.getItem("mt-todo-user"))||null;e&&r&&(this.$store.commit("addToken",e),this.$store.commit("addUser",r),this.$router.push("tasks"))}},methods:{submitForm:function(e){var r=this;this.$refs[e].validate(function(){var e=Object(o.a)(regeneratorRuntime.mark((function e(t){var o,n;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(!t){e.next=7;break}return e.next=3,r.$http.$post("/users-api/users",r.ruleForm);case 3:o=e.sent,window&&(n=JSON.stringify(o.user),localStorage.setItem("mt-todo-token",o.authToken),localStorage.setItem("mt-todo-user",n),r.$store.commit("addToken",o.authToken),r.$store.commit("addUser",o.user),r.$router.push("/tasks")),e.next=9;break;case 7:return r.$notify.error({title:"Error",message:"Cannot register user"}),e.abrupt("return",!1);case 9:case"end":return e.stop()}}),e)})));return function(r){return e.apply(this,arguments)}}())},resetForm:function(e){this.$refs[e].resetFields()}}},l=(t(328),t(43)),component=Object(l.a)(n,(function(){var e=this,r=e.$createElement,t=e._self._c||r;return t("div",{staticClass:"login"},[t("h1",{staticStyle:{margin:"3rem"}},[e._v("\n    Register user\n  ")]),e._v(" "),t("el-form",{ref:"ruleForm",staticClass:"demo-ruleForm",attrs:{model:e.ruleForm,"status-icon":"",rules:e.rules,"label-width":"120px"}},[t("el-form-item",{attrs:{label:"Username",prop:"username"}},[t("el-input",{model:{value:e.ruleForm.username,callback:function(r){e.$set(e.ruleForm,"username",r)},expression:"ruleForm.username"}})],1),e._v(" "),t("el-form-item",{attrs:{label:"Email",prop:"email"}},[t("el-input",{model:{value:e.ruleForm.email,callback:function(r){e.$set(e.ruleForm,"email",r)},expression:"ruleForm.email"}})],1),e._v(" "),t("el-form-item",{attrs:{label:"Password",prop:"password"}},[t("el-input",{attrs:{type:"password",autocomplete:"off"},model:{value:e.ruleForm.password,callback:function(r){e.$set(e.ruleForm,"password",r)},expression:"ruleForm.password"}})],1),e._v(" "),t("el-form-item",[t("el-button",{attrs:{type:"primary"},on:{click:function(r){return e.submitForm("ruleForm")}}},[e._v("\n        Submit\n      ")]),e._v(" "),t("el-button",{on:{click:function(r){return e.resetForm("ruleForm")}}},[e._v("\n        Reset\n      ")])],1)],1),e._v(" "),t("span",[e._v("or "),t("nuxt-link",{attrs:{to:"/login"}},[e._v("login")]),e._v(" user!")],1)],1)}),[],!1,null,null,null);r.default=component.exports}}]);