// create the component
Vue.component("company-logo", {
  name: "company-logo",
  props: {
    compName: {
        type:String,
        default:"Vecteurs"
    }
  },
  data: function () {
    return {};
  },
  methods: {
  },
  template: `
    <div class="logo">
        <div class="logo-circle"></div>
        <h5 class="mb-0">{{compName}}</h5>
    </div>`,
});
