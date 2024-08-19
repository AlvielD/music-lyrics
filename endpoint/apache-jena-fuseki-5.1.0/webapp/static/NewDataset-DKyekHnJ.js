import{M as h}from"./Menu-BwrQSYMS.js";import{_ as p,bI as f,bQ as v,bN as b,r as l,a as o,b as e,d as r,w as d,v as y,F as w,e as k,o as i,bs as N,t as g}from"./index-9t_Zu7tB.js";import{a as D,d as F}from"./index-C-z09IKS.js";f.add(v);const M={name:"NewDataset",components:{Menu:h,FontAwesomeIcon:b},data(){return{form:{datasetName:null,datasetType:null},datasetTypes:[{item:"mem",name:"In-memory – dataset will be recreated when Fuseki restarts, but contents will be lost"},{item:"tdb2",name:"Persistent (TDB2) – dataset will persist across Fuseki restarts"}]}},methods:{async onSubmit(n){n.preventDefault();try{await this.$fusekiService.createDataset(this.form.datasetName,this.form.datasetType),await this.$router.push("/manage"),D(this,`Dataset "${this.form.datasetName}" created`)}catch(s){F(this,s)}}}},S={class:"container-fluid"},x={class:"row mt-4"},I={class:"col-12"},V=e("h2",null,"New dataset",-1),B={class:"card"},$={class:"card-header"},A={class:"card-body"},P={class:"container-fluid"},T={class:"row"},U={class:"col-12"},q={class:"row input-group has-validation align-items-center"},C=e("label",{for:"dataset-name",class:"col-4 col-lg-2 form-label col-form-label-sm"},"Dataset name",-1),E={class:"col g-0"},L=e("div",{class:"invalid-feedback"}," Please choose a dataset name. ",-1),Q={class:"row input-group has-validation align-items-center"},R=e("label",{class:"col-4 col-lg-2 form-label col-form-label-sm"},"Dataset type",-1),j={class:"col"},z={class:"row"},G=["id","value","onUpdate:modelValue"],H=["for"],J=e("div",{class:"invalid-feedback"}," Please choose a dataset type. ",-1),K={type:"submit",class:"btn btn-primary"},O=e("span",{class:"ms-1"},"create dataset",-1);function W(n,s,X,Y,a,c){const m=l("Menu"),_=l("FontAwesomeIcon");return i(),o("div",S,[e("div",x,[e("div",I,[V,e("div",B,[e("nav",$,[r(m)]),e("div",A,[e("div",P,[e("div",T,[e("div",U,[e("form",{onSubmit:s[1]||(s[1]=(...t)=>c.onSubmit&&c.onSubmit(...t)),ref:"form"},[e("div",q,[C,e("div",E,[d(e("input",{"onUpdate:modelValue":s[0]||(s[0]=t=>a.form.datasetName=t),type:"text",id:"dataset-name",ref:"dataset-name",class:"form-control",placeholder:"dataset name",required:""},null,512),[[y,a.form.datasetName]])]),L]),e("div",Q,[R,e("div",j,[e("div",z,[(i(!0),o(w,null,k(a.datasetTypes,t=>(i(),o("div",{key:t.item,class:"form-check"},[d(e("input",{id:`data-set-type-${t.item}`,value:t.item,"onUpdate:modelValue":u=>a.form.datasetType=u,class:"form-check-input",type:"radio",name:"dataset-type",required:""},null,8,G),[[N,a.form.datasetType]]),(i(),o("label",{for:`data-set-type-${t.item}`,key:`data-set-type-${t.item}`,class:"form-check-label"},g(t.name),9,H))]))),128)),J])])]),e("button",K,[r(_,{icon:"check"}),O])],544)])])])])])])])])}const se=p(M,[["render",W]]);export{se as default};
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiTmV3RGF0YXNldC1ES3lla0huSi5qcyIsInNvdXJjZXMiOlsiLi4vLi4vLi4vc3JjL3ZpZXdzL21hbmFnZS9OZXdEYXRhc2V0LnZ1ZSJdLCJzb3VyY2VzQ29udGVudCI6WyI8IS0tXG4gICBMaWNlbnNlZCB0byB0aGUgQXBhY2hlIFNvZnR3YXJlIEZvdW5kYXRpb24gKEFTRikgdW5kZXIgb25lIG9yIG1vcmVcbiAgIGNvbnRyaWJ1dG9yIGxpY2Vuc2UgYWdyZWVtZW50cy4gIFNlZSB0aGUgTk9USUNFIGZpbGUgZGlzdHJpYnV0ZWQgd2l0aFxuICAgdGhpcyB3b3JrIGZvciBhZGRpdGlvbmFsIGluZm9ybWF0aW9uIHJlZ2FyZGluZyBjb3B5cmlnaHQgb3duZXJzaGlwLlxuICAgVGhlIEFTRiBsaWNlbnNlcyB0aGlzIGZpbGUgdG8gWW91IHVuZGVyIHRoZSBBcGFjaGUgTGljZW5zZSwgVmVyc2lvbiAyLjBcbiAgICh0aGUgXCJMaWNlbnNlXCIpOyB5b3UgbWF5IG5vdCB1c2UgdGhpcyBmaWxlIGV4Y2VwdCBpbiBjb21wbGlhbmNlIHdpdGhcbiAgIHRoZSBMaWNlbnNlLiAgWW91IG1heSBvYnRhaW4gYSBjb3B5IG9mIHRoZSBMaWNlbnNlIGF0XG5cbiAgICAgICBodHRwOi8vd3d3LmFwYWNoZS5vcmcvbGljZW5zZXMvTElDRU5TRS0yLjBcblxuICAgVW5sZXNzIHJlcXVpcmVkIGJ5IGFwcGxpY2FibGUgbGF3IG9yIGFncmVlZCB0byBpbiB3cml0aW5nLCBzb2Z0d2FyZVxuICAgZGlzdHJpYnV0ZWQgdW5kZXIgdGhlIExpY2Vuc2UgaXMgZGlzdHJpYnV0ZWQgb24gYW4gXCJBUyBJU1wiIEJBU0lTLFxuICAgV0lUSE9VVCBXQVJSQU5USUVTIE9SIENPTkRJVElPTlMgT0YgQU5ZIEtJTkQsIGVpdGhlciBleHByZXNzIG9yIGltcGxpZWQuXG4gICBTZWUgdGhlIExpY2Vuc2UgZm9yIHRoZSBzcGVjaWZpYyBsYW5ndWFnZSBnb3Zlcm5pbmcgcGVybWlzc2lvbnMgYW5kXG4gICBsaW1pdGF0aW9ucyB1bmRlciB0aGUgTGljZW5zZS5cbi0tPlxuXG48dGVtcGxhdGU+XG4gIDxkaXYgY2xhc3M9XCJjb250YWluZXItZmx1aWRcIj5cbiAgICA8ZGl2IGNsYXNzPVwicm93IG10LTRcIj5cbiAgICAgIDxkaXYgY2xhc3M9XCJjb2wtMTJcIj5cbiAgICAgICAgPGgyPk5ldyBkYXRhc2V0PC9oMj5cbiAgICAgICAgPGRpdiBjbGFzcz1cImNhcmRcIj5cbiAgICAgICAgICA8bmF2IGNsYXNzPVwiY2FyZC1oZWFkZXJcIj5cbiAgICAgICAgICAgIDxNZW51IC8+XG4gICAgICAgICAgPC9uYXY+XG4gICAgICAgICAgPGRpdiBjbGFzcz1cImNhcmQtYm9keVwiPlxuICAgICAgICAgICAgPGRpdiBjbGFzcz1cImNvbnRhaW5lci1mbHVpZFwiPlxuICAgICAgICAgICAgICA8ZGl2IGNsYXNzPVwicm93XCI+XG4gICAgICAgICAgICAgICAgPGRpdiBjbGFzcz1cImNvbC0xMlwiPlxuICAgICAgICAgICAgICAgICAgPGZvcm1cbiAgICAgICAgICAgICAgICAgICAgQHN1Ym1pdD1cIm9uU3VibWl0XCJcbiAgICAgICAgICAgICAgICAgICAgcmVmPVwiZm9ybVwiXG4gICAgICAgICAgICAgICAgICA+XG4gICAgICAgICAgICAgICAgICAgIDxkaXYgY2xhc3M9XCJyb3cgaW5wdXQtZ3JvdXAgaGFzLXZhbGlkYXRpb24gYWxpZ24taXRlbXMtY2VudGVyXCI+XG4gICAgICAgICAgICAgICAgICAgICAgPGxhYmVsIGZvcj1cImRhdGFzZXQtbmFtZVwiIGNsYXNzPVwiY29sLTQgY29sLWxnLTIgZm9ybS1sYWJlbCBjb2wtZm9ybS1sYWJlbC1zbVwiPkRhdGFzZXQgbmFtZTwvbGFiZWw+XG4gICAgICAgICAgICAgICAgICAgICAgPGRpdiBjbGFzcz1cImNvbCBnLTBcIj5cbiAgICAgICAgICAgICAgICAgICAgICAgIDxpbnB1dFxuICAgICAgICAgICAgICAgICAgICAgICAgICB2LW1vZGVsPVwiZm9ybS5kYXRhc2V0TmFtZVwiXG4gICAgICAgICAgICAgICAgICAgICAgICAgIHR5cGU9XCJ0ZXh0XCJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgaWQ9XCJkYXRhc2V0LW5hbWVcIlxuICAgICAgICAgICAgICAgICAgICAgICAgICByZWY9XCJkYXRhc2V0LW5hbWVcIlxuICAgICAgICAgICAgICAgICAgICAgICAgICBjbGFzcz1cImZvcm0tY29udHJvbFwiXG4gICAgICAgICAgICAgICAgICAgICAgICAgIHBsYWNlaG9sZGVyPVwiZGF0YXNldCBuYW1lXCJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgcmVxdWlyZWRcbiAgICAgICAgICAgICAgICAgICAgICAgIC8+XG4gICAgICAgICAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICAgICAgICAgICAgPGRpdiBjbGFzcz1cImludmFsaWQtZmVlZGJhY2tcIj5cbiAgICAgICAgICAgICAgICAgICAgICAgIFBsZWFzZSBjaG9vc2UgYSBkYXRhc2V0IG5hbWUuXG4gICAgICAgICAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPVwicm93IGlucHV0LWdyb3VwIGhhcy12YWxpZGF0aW9uIGFsaWduLWl0ZW1zLWNlbnRlclwiPlxuICAgICAgICAgICAgICAgICAgICAgIDxsYWJlbCBjbGFzcz1cImNvbC00IGNvbC1sZy0yIGZvcm0tbGFiZWwgY29sLWZvcm0tbGFiZWwtc21cIj5EYXRhc2V0IHR5cGU8L2xhYmVsPlxuICAgICAgICAgICAgICAgICAgICAgIDxkaXYgY2xhc3M9XCJjb2xcIj5cbiAgICAgICAgICAgICAgICAgICAgICAgIDxkaXYgY2xhc3M9XCJyb3dcIj5cbiAgICAgICAgICAgICAgICAgICAgICAgICAgPGRpdlxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHYtZm9yPVwiZGF0YXNldFR5cGUgb2YgZGF0YXNldFR5cGVzXCJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICA6a2V5PVwiZGF0YXNldFR5cGUuaXRlbVwiXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgY2xhc3M9XCJmb3JtLWNoZWNrXCJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgPlxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxpbnB1dFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgOmlkPVwiYGRhdGEtc2V0LXR5cGUtJHtkYXRhc2V0VHlwZS5pdGVtfWBcIlxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgOnZhbHVlPVwiZGF0YXNldFR5cGUuaXRlbVwiXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICB2LW1vZGVsPVwiZm9ybS5kYXRhc2V0VHlwZVwiXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICBjbGFzcz1cImZvcm0tY2hlY2staW5wdXRcIlxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdHlwZT1cInJhZGlvXCJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIG5hbWU9XCJkYXRhc2V0LXR5cGVcIlxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgcmVxdWlyZWRcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICA+XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgPGxhYmVsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICA6Zm9yPVwiYGRhdGEtc2V0LXR5cGUtJHtkYXRhc2V0VHlwZS5pdGVtfWBcIlxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgOmtleT1cImBkYXRhLXNldC10eXBlLSR7ZGF0YXNldFR5cGUuaXRlbX1gXCJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGNsYXNzPVwiZm9ybS1jaGVjay1sYWJlbFwiXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgPlxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAge3sgZGF0YXNldFR5cGUubmFtZSB9fVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvbGFiZWw+XG4gICAgICAgICAgICAgICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPVwiaW52YWxpZC1mZWVkYmFja1wiPlxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIFBsZWFzZSBjaG9vc2UgYSBkYXRhc2V0IHR5cGUuXG4gICAgICAgICAgICAgICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgICAgICAgICA8YnV0dG9uXG4gICAgICAgICAgICAgICAgICAgICAgdHlwZT1cInN1Ym1pdFwiXG4gICAgICAgICAgICAgICAgICAgICAgY2xhc3M9XCJidG4gYnRuLXByaW1hcnlcIlxuICAgICAgICAgICAgICAgICAgICA+XG4gICAgICAgICAgICAgICAgICAgICAgPEZvbnRBd2Vzb21lSWNvbiBpY29uPVwiY2hlY2tcIiAvPlxuICAgICAgICAgICAgICAgICAgICAgIDxzcGFuIGNsYXNzPVwibXMtMVwiPmNyZWF0ZSBkYXRhc2V0PC9zcGFuPlxuICAgICAgICAgICAgICAgICAgICA8L2J1dHRvbj5cbiAgICAgICAgICAgICAgICAgIDwvZm9ybT5cbiAgICAgICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0PlxuaW1wb3J0IE1lbnUgZnJvbSAnQC9jb21wb25lbnRzL21hbmFnZS9NZW51LnZ1ZSdcbmltcG9ydCB7IGxpYnJhcnkgfSBmcm9tICdAZm9ydGF3ZXNvbWUvZm9udGF3ZXNvbWUtc3ZnLWNvcmUnXG5pbXBvcnQgeyBmYUNoZWNrIH0gZnJvbSAnQGZvcnRhd2Vzb21lL2ZyZWUtc29saWQtc3ZnLWljb25zJ1xuaW1wb3J0IHsgRm9udEF3ZXNvbWVJY29uIH0gZnJvbSAnQGZvcnRhd2Vzb21lL3Z1ZS1mb250YXdlc29tZSdcbmltcG9ydCB7IGRpc3BsYXlFcnJvciwgZGlzcGxheU5vdGlmaWNhdGlvbiB9IGZyb20gJ0AvdXRpbHMnXG5cbmxpYnJhcnkuYWRkKGZhQ2hlY2spXG5cbmV4cG9ydCBkZWZhdWx0IHtcbiAgbmFtZTogJ05ld0RhdGFzZXQnLFxuXG4gIGNvbXBvbmVudHM6IHtcbiAgICBNZW51LFxuICAgIEZvbnRBd2Vzb21lSWNvblxuICB9LFxuXG4gIGRhdGEgKCkge1xuICAgIHJldHVybiB7XG4gICAgICBmb3JtOiB7XG4gICAgICAgIGRhdGFzZXROYW1lOiBudWxsLFxuICAgICAgICBkYXRhc2V0VHlwZTogbnVsbFxuICAgICAgfSxcbiAgICAgIGRhdGFzZXRUeXBlczogW1xuICAgICAgICB7XG4gICAgICAgICAgaXRlbTogJ21lbScsXG4gICAgICAgICAgbmFtZTogJ0luLW1lbW9yeSDigJMgZGF0YXNldCB3aWxsIGJlIHJlY3JlYXRlZCB3aGVuIEZ1c2VraSByZXN0YXJ0cywgYnV0IGNvbnRlbnRzIHdpbGwgYmUgbG9zdCdcbiAgICAgICAgfSxcbiAgICAgICAgLy8ge1xuICAgICAgICAvLyAgIGl0ZW06ICd0ZGInLFxuICAgICAgICAvLyAgIG5hbWU6ICdQZXJzaXN0ZW50IOKAkyBkYXRhc2V0IHdpbGwgcGVyc2lzdCBhY3Jvc3MgRnVzZWtpIHJlc3RhcnQnXG4gICAgICAgIC8vIH0sXG4gICAgICAgIHtcbiAgICAgICAgICBpdGVtOiAndGRiMicsXG4gICAgICAgICAgbmFtZTogJ1BlcnNpc3RlbnQgKFREQjIpIOKAkyBkYXRhc2V0IHdpbGwgcGVyc2lzdCBhY3Jvc3MgRnVzZWtpIHJlc3RhcnRzJ1xuICAgICAgICB9XG4gICAgICBdXG4gICAgfVxuICB9LFxuXG4gIG1ldGhvZHM6IHtcbiAgICBhc3luYyBvblN1Ym1pdCAoZXZ0KSB7XG4gICAgICBldnQucHJldmVudERlZmF1bHQoKVxuICAgICAgdHJ5IHtcbiAgICAgICAgYXdhaXQgdGhpcy4kZnVzZWtpU2VydmljZS5jcmVhdGVEYXRhc2V0KHRoaXMuZm9ybS5kYXRhc2V0TmFtZSwgdGhpcy5mb3JtLmRhdGFzZXRUeXBlKVxuICAgICAgICBhd2FpdCB0aGlzLiRyb3V0ZXIucHVzaCgnL21hbmFnZScpXG4gICAgICAgIGRpc3BsYXlOb3RpZmljYXRpb24odGhpcywgYERhdGFzZXQgXCIke3RoaXMuZm9ybS5kYXRhc2V0TmFtZX1cIiBjcmVhdGVkYClcbiAgICAgIH0gY2F0Y2ggKGVycm9yKSB7XG4gICAgICAgIGRpc3BsYXlFcnJvcih0aGlzLCBlcnJvcilcbiAgICAgIH1cbiAgICB9XG4gIH1cbn1cbjwvc2NyaXB0PlxuIl0sIm5hbWVzIjpbImxpYnJhcnkiLCJmYUNoZWNrIiwiX3NmY19tYWluIiwiTWVudSIsIkZvbnRBd2Vzb21lSWNvbiIsImV2dCIsImRpc3BsYXlOb3RpZmljYXRpb24iLCJlcnJvciIsImRpc3BsYXlFcnJvciIsIl9ob2lzdGVkXzEiLCJfaG9pc3RlZF8yIiwiX2hvaXN0ZWRfMyIsIl9ob2lzdGVkXzQiLCJfY3JlYXRlRWxlbWVudFZOb2RlIiwiX2hvaXN0ZWRfNSIsIl9ob2lzdGVkXzYiLCJfaG9pc3RlZF83IiwiX2hvaXN0ZWRfOCIsIl9ob2lzdGVkXzkiLCJfaG9pc3RlZF8xMCIsIl9ob2lzdGVkXzExIiwiX2hvaXN0ZWRfMTMiLCJfaG9pc3RlZF8xNCIsIl9ob2lzdGVkXzE1IiwiX2hvaXN0ZWRfMTYiLCJfaG9pc3RlZF8xNyIsIl9ob2lzdGVkXzE4IiwiX2hvaXN0ZWRfMTkiLCJfaG9pc3RlZF8yMCIsIl9ob2lzdGVkXzIxIiwiX2hvaXN0ZWRfMjMiLCJfb3BlbkJsb2NrIiwiX2NyZWF0ZUVsZW1lbnRCbG9jayIsIl9jcmVhdGVWTm9kZSIsIl9jb21wb25lbnRfTWVudSIsIiRvcHRpb25zIiwiYXJncyIsIl9ob2lzdGVkXzEyIiwiX2NhY2hlIiwiJGV2ZW50IiwiJGRhdGEiLCJfdk1vZGVsVGV4dCIsIl9GcmFnbWVudCIsIl9yZW5kZXJMaXN0IiwiZGF0YXNldFR5cGUiLCJfdk1vZGVsUmFkaW8iLCJfaG9pc3RlZF8yMiIsIl9jb21wb25lbnRfRm9udEF3ZXNvbWVJY29uIl0sIm1hcHBpbmdzIjoib09BNEdBQSxFQUFRLElBQUlDLENBQU8sRUFFbkIsTUFBS0MsRUFBVSxDQUNiLEtBQU0sYUFFTixXQUFZLENBQ1YsS0FBQUMsRUFDQSxnQkFBQUMsQ0FDRCxFQUVELE1BQVEsQ0FDTixNQUFPLENBQ0wsS0FBTSxDQUNKLFlBQWEsS0FDYixZQUFhLElBQ2QsRUFDRCxhQUFjLENBQ1osQ0FDRSxLQUFNLE1BQ04sS0FBTSx1RkFDUCxFQUtELENBQ0UsS0FBTSxPQUNOLEtBQU0saUVBQ1IsQ0FDRixDQUNGLENBQ0QsRUFFRCxRQUFTLENBQ1AsTUFBTSxTQUFVQyxFQUFLLENBQ25CQSxFQUFJLGVBQWUsRUFDbkIsR0FBSSxDQUNGLE1BQU0sS0FBSyxlQUFlLGNBQWMsS0FBSyxLQUFLLFlBQWEsS0FBSyxLQUFLLFdBQVcsRUFDcEYsTUFBTSxLQUFLLFFBQVEsS0FBSyxTQUFTLEVBQ2pDQyxFQUFvQixLQUFNLFlBQVksS0FBSyxLQUFLLFdBQVcsV0FBVyxDQUN0RSxPQUFPQyxFQUFPLENBQ2RDLEVBQWEsS0FBTUQsQ0FBSyxDQUMxQixDQUNGLENBQ0YsQ0FDRixFQXZJT0UsRUFBQSxDQUFBLE1BQU0saUJBQWlCLEVBQ3JCQyxFQUFBLENBQUEsTUFBTSxVQUFVLEVBQ2RDLEVBQUEsQ0FBQSxNQUFNLFFBQVEsRUFDakJDLEVBQUFDLEVBQW9CLFVBQWhCLGNBQVcsRUFBQSxFQUNWQyxFQUFBLENBQUEsTUFBTSxNQUFNLEVBQ1ZDLEVBQUEsQ0FBQSxNQUFNLGFBQWEsRUFHbkJDLEVBQUEsQ0FBQSxNQUFNLFdBQVcsRUFDZkMsRUFBQSxDQUFBLE1BQU0saUJBQWlCLEVBQ3JCQyxFQUFBLENBQUEsTUFBTSxLQUFLLEVBQ1RDLEVBQUEsQ0FBQSxNQUFNLFFBQVEsRUFLVkMsRUFBQSxDQUFBLE1BQU0sbURBQW1ELElBQzVEUCxFQUFrRyxRQUFBLENBQTNGLElBQUksZUFBZSxNQUFNLCtDQUE4QyxlQUFZLEVBQUEsRUFDckZRLEVBQUEsQ0FBQSxNQUFNLFNBQVMsRUFXcEJDLEVBQUFULEVBRU0sTUFGRCxDQUFBLE1BQU0sb0JBQW1CLGtDQUU5QixFQUFBLEVBRUdVLEVBQUEsQ0FBQSxNQUFNLG1EQUFtRCxFQUM1REMsRUFBQVgsRUFBK0UsUUFBeEUsQ0FBQSxNQUFNLCtDQUE4QyxlQUFZLEVBQUEsRUFDbEVZLEVBQUEsQ0FBQSxNQUFNLEtBQUssRUFDVEMsRUFBQSxDQUFBLE1BQU0sS0FBSyxFQXREeENDLEVBQUEsQ0FBQSxLQUFBLFFBQUEscUJBQUEsRUFBQUMsRUFBQSxDQUFBLEtBQUEsRUE2RTBCQyxFQUFBaEIsRUFFTSxNQUZELENBQUEsTUFBTSxvQkFBbUIsa0NBRTlCLEVBQUEsS0FLSixLQUFLLFNBQ0wsTUFBTSxtQkFHTmlCLEVBQUFqQixFQUF3QyxPQUFsQyxDQUFBLE1BQU0sUUFBTyxpQkFBYyxFQUFBLG1FQXRFckQsT0FBQWtCLEVBQUEsRUFBQUMsRUFnRk0sTUFoRk52QixFQWdGTSxDQS9FSkksRUE4RU0sTUE5RU5ILEVBOEVNLENBN0VKRyxFQTRFTSxNQTVFTkYsRUE0RU0sQ0EzRUpDLEVBQ0FDLEVBeUVNLE1BekVOQyxFQXlFTSxDQXhFSkQsRUFFTSxNQUZORSxFQUVNLENBREprQixFQUFRQyxDQUFBLElBRVZyQixFQW9FTSxNQXBFTkcsRUFvRU0sQ0FuRUpILEVBa0VNLE1BbEVOSSxFQWtFTSxDQWpFSkosRUFnRU0sTUFoRU5LLEVBZ0VNLENBL0RKTCxFQThETSxNQTlETk0sRUE4RE0sQ0E3REpOLEVBNERPLE9BQUEsQ0EzREosNkJBQVFzQixFQUFRLFVBQUFBLEVBQUEsU0FBQSxHQUFBQyxDQUFBLEdBQ2pCLElBQUksU0FFSnZCLEVBZ0JNLE1BaEJOTyxFQWdCTSxDQWZKaUIsRUFDQXhCLEVBVU0sTUFWTlEsRUFVTSxHQVRKUixFQVFFLFFBQUEsQ0E3QzFCLHNCQXNDbUN5QixFQUFBLENBQUEsSUFBQUEsRUFBQSxDQUFBLEVBQUFDLEdBQUFDLEVBQUEsS0FBSyxZQUFXRCxHQUN6QixLQUFLLE9BQ0wsR0FBRyxlQUNILElBQUksZUFDSixNQUFNLGVBQ04sWUFBWSxlQUNaLFNBQUEsZUFOUyxDQUFBRSxFQUFBRCxFQUFBLEtBQUssV0FBVyxNQVM3QmxCLElBSUZULEVBK0JNLE1BL0JOVSxFQStCTSxDQTlCSkMsRUFDQVgsRUE0Qk0sTUE1Qk5ZLEVBNEJNLENBM0JKWixFQTBCTSxNQTFCTmEsRUEwQk0sRUF6QkpLLEVBQUEsRUFBQSxFQUFBQyxFQXFCTVUsRUE1RWhDLEtBQUFDLEVBd0RrREgsRUFBWSxhQUEzQkksUUFEVFosRUFxQk0sTUFBQSxDQW5CSCxJQUFLWSxFQUFZLEtBQ2xCLE1BQU0saUJBRU4vQixFQVFDLFFBQUEsQ0FQRSxHQUFFLGlCQUFtQitCLEVBQVksSUFBSSxHQUNyQyxNQUFPQSxFQUFZLEtBOURsRCxzQkErRHVDTCxHQUFBQyxFQUFBLEtBQUssWUFBV0QsRUFDekIsTUFBTSxtQkFDTixLQUFLLFFBQ0wsS0FBSyxlQUNMLFNBQUEsRUFuRTlCLEVBQUEsS0FBQSxFQUFBWixDQUFBLEVBQUEsQ0ErRHVDLENBQUFrQixFQUFBTCxFQUFBLEtBQUssV0FBVyxTQU0zQlIsRUFNUSxRQUFBLENBTEwsSUFBRyxpQkFBbUJZLEVBQVksSUFBSSxHQUN0QyxJQUFHLGlCQUFtQkEsRUFBWSxJQUFJLEdBQ3ZDLE1BQU0sc0JBRUhBLEVBQVksSUFBSSxFQTFFakQsRUFBQWhCLENBQUEsYUE2RTBCQyxRQU1OaEIsRUFNUyxTQU5UaUMsRUFNUyxDQUZQYixFQUFnQ2MsRUFBQSxDQUFmLEtBQUssT0FBTyxDQUFBLEVBQzdCakIifQ==
