// create the component
Vue.component("tag-compo", {
  name: "tag-compo",
  props: {
    checked: {
      type: Boolean,
      default: false,
    },
    count: {
      default: 0,
    },
    label: {
      type: String,
      default: "Test Tag",
    },
    checked: {
      type: Boolean,
      default: false,
    },
  },
  data: function () {
    // unlike app , the compo's data has to be a function
    return {};
  },
  methods: {
    check: function () {
      this.checked = !this.checked;
    },
    clicked: function () {
      console.log(
        `Clicked tag with label : ${this.label} and count ${this.count}`,
      );
    },
  },
  template: `<div class="tag" @click='clicked'>
                <input class="form-check-input" type="checkbox" v-if="checked"/>
                <input class="form-check-input" type="checkbox" v-if="!checked"/>
                <span class="tag-name">{{label}}</span>
                <span class="count">{{count}}</span>
          </div>`,
});
