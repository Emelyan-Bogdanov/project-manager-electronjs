// create the component
Vue.component("sidebar-section-header", {
  name: "sidebar-section-header",
  props: {
    title: {
      default: "Default value",
    },
  },
  data: function () {
    // unlike app , the compo's data has to be a function
    return {};
  },
  methods: {},
  template: `
  <div class="section-header">
        <div class="sidebar-title mb-0">{{title}}</div>
        <div class="plus-btn">
            <i class="bi bi-plus"></i>
        </div>
    </div>`,
});
