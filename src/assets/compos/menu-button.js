// create the component
Vue.component("side-menu-button", {
  name: "side-menu-button",
  props: {
    biclass: {
      default: "bi-check2-square",
    },
    spanText: {
        type:String,
      default: "default value",
    },
    count: {
      default: 99,
    },
  },
  data: function () {
    // unlike app , the compo's data has to be a function
    return {};
  },
  methods: {},
  template: `
  <a href="#" class="menu-link">
        <div class="menu-left">
            <i :class="'bi ' + biclass"></i>
            <span>{{spanText}}</span>
        </div>

        <span class="notif-badge" v-if="count > 0">{{count}}</span>
    </a>`,
});
