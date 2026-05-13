// create the component
Vue.component("side-menu-button", {
  name: "side-menu-button",
  props: {
    biclass: {
      default: "bi-check2-square",
    },
    spanText: {
      type: String,
      default: "default value",
    },
    count: {
      default: 0,
    },
    url: {
      type: String,
      default: "",
    },
    counterId:{
      type:String,
      default:"menu"
    }
  },
  data: function () {
    // unlike app , the compo's data has to be a function
    return {};
  },
  methods: {
    gotourl: function () {
      if (this.url) {
        window.location.href = this.url;
      }
    },
  },
  template: `<a href="#" class="menu-link" @click='gotourl()'>
        <div class="menu-left">
            <i :class="'bi ' + biclass"></i>
            <span>{{spanText}}</span>
        </div>

        <span class="notif-badge" v-if="count > 0">{{count}}</span>
    </a>`,
});
